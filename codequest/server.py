"""CodeQuest HTTP server: JSON API + the single-page web UI.

Stdlib only (http.server) so it runs unchanged in Termux and inside the
python-for-android "webview" bootstrap used for the APK.

Run:  python -m codequest            (http://127.0.0.1:8765)
"""

import argparse
import datetime as dt
import json
import mimetypes
import re
import threading
import time
import traceback
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from . import __version__, config, gamify, judge
from .catalog import Catalog
from .progress import ProgressStore

MAX_BODY = 1024 * 1024
LOCAL_HOSTS = {"127.0.0.1", "localhost", "[::1]", "::1"}


class ApiError(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status
        self.message = message


class App:
    """All request handling logic, independent of the HTTP plumbing (testable)."""

    def __init__(self, store, catalog, allow_remote_hosts=False):
        self.store = store
        self.catalog = catalog
        self.allow_remote_hosts = allow_remote_hosts
        self.routes = []
        r = self._route
        r("GET", r"/api/health", self.health)
        r("GET", r"/api/home", self.home)
        r("GET", r"/api/lessons", self.lessons)
        r("GET", r"/api/lessons/(?P<lid>[\w-]+)", self.lesson)
        r("POST", r"/api/lessons/(?P<lid>[\w-]+)/complete", self.lesson_complete)
        r("POST", r"/api/lessons/(?P<lid>[\w-]+)/challenge", self.lesson_challenge)
        r("GET", r"/api/problems", self.problems)
        r("GET", r"/api/problems/(?P<pid>[\w-]+)", self.problem)
        r("POST", r"/api/problems/(?P<pid>[\w-]+)/hint", self.problem_hint)
        r("POST", r"/api/problems/(?P<pid>[\w-]+)/run", self.problem_run)
        r("POST", r"/api/problems/(?P<pid>[\w-]+)/submit", self.problem_submit)
        r("POST", r"/api/run", self.playground_run)
        r("POST", r"/api/raw-run", self.raw_run)
        r("POST", r"/api/heartbeat", self.heartbeat)
        r("GET", r"/api/profile", self.profile)
        r("GET", r"/api/settings", self.get_settings)
        r("POST", r"/api/settings", self.set_settings)
        r("POST", r"/api/drafts", self.save_draft)
        r("GET", r"/api/drafts", self.get_draft)
        r("GET", r"/api/export", self.export)

    def _route(self, method, pattern, fn):
        self.routes.append((method, re.compile(pattern + r"$"), fn))

    def dispatch(self, method, path, query, body, headers):
        tz = headers.get("X-TZ-Offset")
        if tz is not None:
            try:
                tz = max(-900, min(900, int(tz)))
                if tz != self.store.get_setting("tz_offset"):
                    self.store.set_setting("tz_offset", tz)
            except ValueError:
                pass
        for m, rx, fn in self.routes:
            match = rx.match(path)
            if match and m == method:
                return fn(query=query, body=body or {}, **match.groupdict())
        raise ApiError(HTTPStatus.NOT_FOUND, f"No route for {method} {path}")

    # ------------------------------------------------------------- helpers
    def _remote(self):
        return self.store.get_setting("remote_judge") or None

    def _execute(self, lang, code, inputs, time_limit):
        if lang not in judge.LANGS:
            raise ApiError(HTTPStatus.BAD_REQUEST, f"Unknown language {lang!r}")
        if not isinstance(code, str) or len(code) > 100_000:
            raise ApiError(HTTPStatus.BAD_REQUEST, "Code missing or too long")
        try:
            return judge.execute(lang, code, inputs, time_limit, remote_url=self._remote())
        except judge.JudgeUnavailable as exc:
            raise ApiError(HTTPStatus.SERVICE_UNAVAILABLE, str(exc)) from exc

    def _get_problem(self, pid):
        p = self.catalog.problem(pid)
        if not p:
            raise ApiError(HTTPStatus.NOT_FOUND, f"Unknown problem {pid}")
        return p

    def _get_lesson(self, lid):
        l = self.catalog.lesson(lid)
        if not l:
            raise ApiError(HTTPStatus.NOT_FOUND, f"Unknown lesson {lid}")
        return l

    @staticmethod
    def _lang(body, allowed):
        lang = body.get("lang", "python")
        if lang not in allowed:
            raise ApiError(HTTPStatus.BAD_REQUEST, f"This problem is not available in {lang}")
        return lang

    def _judge_tests(self, lang, code, samples, hidden, checker, time_limit):
        """Run samples + hidden tests; build a learner-safe report."""
        tests = samples + hidden
        raw = self._execute(lang, code, [t["input"] for t in tests], time_limit)
        overall, graded = judge.grade(raw, [t["output"] for t in tests], checker)
        report = []
        for i, (t, g) in enumerate(zip(tests, graded)):
            is_sample = i < len(samples)
            item = {"index": i + 1, "kind": "sample" if is_sample else "hidden",
                    "verdict": g["verdict"], "time": g["time"]}
            if is_sample:
                item.update(input=t["input"], expected=t["output"], output=g["stdout"][:20000])
            if g["verdict"] in ("error", "compile_error", "output_limit"):
                item["error"] = g["error"][-4000:]
            if g["stderr"] and is_sample:
                item["stderr"] = g["stderr"][-2000:]
            report.append(item)
        passed = sum(1 for g in graded if g["verdict"] == "ok")
        compile_error = graded[0]["error"] if graded and graded[0]["verdict"] == "compile_error" else None
        return {"verdict": overall, "verdict_text": judge.VERDICTS[overall], "passed": passed,
                "total": len(graded), "tests": report, "compile_error": compile_error}

    def _reward_payload(self, reward):
        reward = dict(reward)
        reward["level"] = gamify.level_for(self.store.total_xp())
        reward["streak"] = self.store.streaks()[0]
        return reward

    # ---------------------------------------------------------- endpoints
    def health(self, **_):
        return {
            "version": __version__,
            "android_app": config.IS_ANDROID_APP,
            "termux": config.IS_TERMUX,
            "python": {"mode": "subprocess" if config.python_executable() else "in-process"},
            "cpp": {"local": config.cxx_compiler() is not None,
                    "compiler": config.cxx_compiler(), "remote": self._remote()},
            "libraries": {m: config.has_module(m) for m in ("numpy", "sympy")},
            "counts": {"problems": self.catalog.problem_count(),
                       "lessons_python": self.catalog.lesson_count("python"),
                       "lessons_cpp": self.catalog.lesson_count("cpp")},
        }

    def home(self, **_):
        done = self.store.lessons_done()
        solved = self.store.solved_map()
        cont = {}
        for track in judge.LANGS:
            nxt = next((l for l in self.catalog.lesson_list(track) if l["id"] not in done), None)
            total = self.catalog.lesson_count(track)
            cont[track] = {"next": self.catalog.lesson_summary(nxt) if nxt else None,
                           "done": sum(1 for l in self.catalog.lesson_list(track) if l["id"] in done),
                           "total": total}
        unsolved = [p for p in self.catalog.problems if p["id"] not in solved]
        daily = None
        if unsolved:
            # Deterministic "problem of the day", easiest-first bias.
            day = self.store.today()
            pool = unsolved[: max(8, len(unsolved) // 3)]
            daily = self.catalog.problem_summary(pool[(day * 7919) % len(pool)])
        prof = self.store.profile(self.catalog)
        return {"level": prof["level"], "streak": prof["streak"], "time": prof["time"],
                "solved": prof["problems"]["solved"], "total_problems": prof["problems"]["total"],
                "continue": cont, "daily": daily,
                "badges_earned": sum(1 for b in prof["badges"] if b["earned_at"])}

    def lessons(self, query, **_):
        track = (query.get("track") or ["python"])[0]
        done = self.store.lessons_done()
        units = []
        for l in self.catalog.lesson_list(track):
            if not units or units[-1]["name"] != l["unit"]:
                units.append({"name": l["unit"], "lessons": []})
            units[-1]["lessons"].append(dict(self.catalog.lesson_summary(l), done=l["id"] in done))
        return {"track": track, "units": units}

    def lesson(self, lid, **_):
        l = self._get_lesson(lid)
        siblings = self.catalog.lesson_list(l["track"])
        idx = next(i for i, s in enumerate(siblings) if s["id"] == lid)
        out = self.catalog.lesson_public(l)
        out["done"] = lid in self.store.lessons_done()
        out["xp"] = l["xp"]
        out["prev"] = siblings[idx - 1]["id"] if idx > 0 else None
        out["next"] = siblings[idx + 1]["id"] if idx + 1 < len(siblings) else None
        out["position"] = [idx + 1, len(siblings)]
        if out["challenge"]:
            out["challenge"]["draft"] = self.store.get_draft(f"lesson:{lid}")
            if out["done"]:
                out["challenge"]["solution"] = l["challenge"]["solution"]
        return out

    def lesson_complete(self, lid, **_):
        l = self._get_lesson(lid)
        if l.get("challenge"):
            raise ApiError(HTTPStatus.BAD_REQUEST, "Pass the challenge to complete this lesson")
        return self._reward_payload(self.store.complete_lesson(lid, l["track"], l["xp"], self.catalog))

    def lesson_challenge(self, lid, body, **_):
        l = self._get_lesson(lid)
        ch = l.get("challenge")
        if not ch:
            raise ApiError(HTTPStatus.BAD_REQUEST, "This lesson has no challenge")
        code = body.get("code", "")
        self.store.save_draft(f"lesson:{lid}", code)
        submit = body.get("mode") == "submit"
        hidden = ch["tests"] if submit else []
        result = self._judge_tests(l["track"], code, ch["samples"], hidden,
                                   ch["checker"], ch["time_limit"])
        if submit and result["verdict"] == "ok":
            reward = self.store.complete_lesson(lid, l["track"], l["xp"], self.catalog)
            result["reward"] = self._reward_payload(reward)
            result["solution"] = ch["solution"]
        return result

    def problems(self, **_):
        solved = self.store.solved_map()
        attempted = self.store.attempted_ids()
        items = []
        for p in self.catalog.problems:
            s = self.catalog.problem_summary(p)
            s["solved"] = sorted(solved.get(p["id"], ()))
            s["attempted"] = p["id"] in attempted
            items.append(s)
        return {"problems": items, "categories": self.catalog.categories(),
                "difficulties": gamify.DIFFICULTIES}

    def problem(self, pid, query, **_):
        p = self._get_problem(pid)
        out = self.catalog.problem_public(p)
        revealed = self.store.revealed_hints(pid)
        out["hints"] = [p["hints"][i] for i in revealed if i < len(p["hints"])]
        solved = sorted(self.store.solved_map().get(pid, ()))
        out["solved"] = solved
        out["history"] = self.store.problem_history(pid)
        out["drafts"] = {lang: self.store.get_draft(f"problem:{pid}:{lang}") for lang in p["languages"]}
        hints = len(revealed)
        out["xp_now"] = gamify.problem_xp(p["difficulty"], hints, second_language=bool(solved))
        if solved:
            out["solution"] = p["solution"]
        return out

    def problem_hint(self, pid, **_):
        p = self._get_problem(pid)
        revealed = self.store.revealed_hints(pid)
        nxt = len(revealed)
        if nxt >= len(p["hints"]):
            raise ApiError(HTTPStatus.BAD_REQUEST, "No more hints - you've got this!")
        used = self.store.reveal_hint(pid, nxt)
        solved = bool(self.store.solved_map().get(pid))
        return {"index": nxt, "hint": p["hints"][nxt], "hints_used": used,
                "remaining": len(p["hints"]) - used,
                "xp_now": gamify.problem_xp(p["difficulty"], used, second_language=solved)}

    def problem_run(self, pid, body, **_):
        """Run on the visible samples, or on custom stdin. Never recorded."""
        p = self._get_problem(pid)
        lang = self._lang(body, p["languages"])
        code = body.get("code", "")
        self.store.save_draft(f"problem:{pid}:{lang}", code)
        if "stdin" in body and body["stdin"] is not None:
            res = self._execute(lang, code, [str(body["stdin"])], p["time_limit"])[0]
            return {"custom": True, **res}
        return self._judge_tests(lang, code, p["samples"], [], p["checker"], p["time_limit"])

    def problem_submit(self, pid, body, **_):
        p = self._get_problem(pid)
        lang = self._lang(body, p["languages"])
        code = body.get("code", "")
        self.store.save_draft(f"problem:{pid}:{lang}", code)
        result = self._judge_tests(lang, code, p["samples"], p["tests"], p["checker"], p["time_limit"])
        reward = self.store.record_attempt(p, lang, result["verdict"], result["passed"],
                                           result["total"], self.catalog)
        result["reward"] = self._reward_payload(reward)
        if result["verdict"] == "ok":
            result["solution"] = p["solution"]
        return result

    def playground_run(self, body, **_):
        lang = body.get("lang", "python")
        res = self._execute(lang, body.get("code", ""), [str(body.get("stdin", ""))], 10.0)[0]
        self.store.save_draft(f"playground:{lang}", body.get("code", ""))
        return res

    def raw_run(self, body, **_):
        """Used by the APK to delegate C++ to a Termux CodeQuest instance."""
        inputs = body.get("inputs")
        if not isinstance(inputs, list) or len(inputs) > 200:
            raise ApiError(HTTPStatus.BAD_REQUEST, "inputs must be a list (max 200)")
        tl = min(float(body.get("time_limit", 2.0)), 20.0)
        lang = body.get("lang")
        if lang == "cpp" and not config.cxx_compiler():
            raise ApiError(HTTPStatus.SERVICE_UNAVAILABLE, "No C++ compiler on this judge")
        if lang not in judge.LANGS:
            raise ApiError(HTTPStatus.BAD_REQUEST, "bad lang")
        code = body.get("code", "")
        if lang == "python":
            from .judge import python_runner
            return {"results": python_runner.run(code, [str(i) for i in inputs], tl)}
        from .judge import cpp_runner
        return {"results": cpp_runner.run(code, [str(i) for i in inputs], tl)}

    def heartbeat(self, body, **_):
        self.store.add_activity(body.get("seconds", 0))
        return {"ok": True, "today_minutes": self.store.minutes_by_day(1)[0]["minutes"]}

    def profile(self, **_):
        prof = self.store.profile(self.catalog)
        for r in prof["recent"]:
            r["when"] = dt.datetime.fromtimestamp(
                r["ts"] - self.store.get_setting("tz_offset") * 60, dt.timezone.utc
            ).strftime("%b %d %H:%M")
        return prof

    def get_settings(self, **_):
        return self.store.settings()

    def set_settings(self, body, **_):
        for key, value in body.items():
            if key == "daily_goal":
                value = max(1, min(600, int(value)))
            elif key == "font_size":
                value = max(10, min(24, int(value)))
            elif key == "remote_judge":
                value = str(value).strip()
                if value and not re.match(r"^https?://[\w.\-\[\]:]+/?$", value):
                    raise ApiError(HTTPStatus.BAD_REQUEST, "Judge URL looks like http://127.0.0.1:8765")
            elif key == "preferred_lang" and value not in judge.LANGS:
                raise ApiError(HTTPStatus.BAD_REQUEST, "bad language")
            try:
                self.store.set_setting(key, value)
            except KeyError:
                raise ApiError(HTTPStatus.BAD_REQUEST, f"Unknown setting {key}") from None
        if "daily_goal" in body:
            self.store.update_badges(self.catalog)
        return self.store.settings()

    def save_draft(self, body, **_):
        key, code = body.get("key"), body.get("code")
        if not isinstance(key, str) or not re.match(r"^(problem|lesson|playground):[\w:-]+$", key):
            raise ApiError(HTTPStatus.BAD_REQUEST, "bad draft key")
        if not isinstance(code, str) or len(code) > 100_000:
            raise ApiError(HTTPStatus.BAD_REQUEST, "bad code")
        self.store.save_draft(key, code)
        return {"ok": True}

    def get_draft(self, query, **_):
        key = (query.get("key") or [""])[0]
        return {"key": key, "code": self.store.get_draft(key)}

    def export(self, **_):
        return {"exported_at": time.time(), "version": __version__, **self.store.export()}


class Handler(BaseHTTPRequestHandler):
    server_version = f"CodeQuest/{__version__}"
    app: App = None  # set by make_server
    quiet = True

    def log_message(self, fmt, *args):
        if not self.quiet:
            super().log_message(fmt, *args)

    # -------------------------------------------------- request protection
    def _host_ok(self):
        """Block DNS-rebinding & cross-site requests from web pages.

        A malicious page opened in the phone's browser could otherwise POST
        code to 127.0.0.1 and have Termux execute it.
        """
        if self.app.allow_remote_hosts:
            return True
        host = urlparse("//" + (self.headers.get("Host") or "")).hostname or ""
        if host not in LOCAL_HOSTS:
            return False
        origin = self.headers.get("Origin")
        if origin and origin != "null":
            if (urlparse(origin).hostname or "") not in LOCAL_HOSTS:
                return False
        return True

    def _send(self, status, payload, content_type="application/json; charset=utf-8", extra=None):
        data = payload if isinstance(payload, bytes) else json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Content-Type-Options", "nosniff")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(data)

    def _api(self, method):
        if not self._host_ok():
            return self._send(HTTPStatus.FORBIDDEN, {"error": "Forbidden host/origin"})
        url = urlparse(self.path)
        body = None
        if method == "POST":
            ctype = self.headers.get("Content-Type", "")
            if not ctype.startswith("application/json"):
                return self._send(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, {"error": "JSON only"})
            length = int(self.headers.get("Content-Length") or 0)
            if length > MAX_BODY:
                return self._send(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "Body too large"})
            try:
                body = json.loads(self.rfile.read(length) or b"{}")
            except ValueError:
                return self._send(HTTPStatus.BAD_REQUEST, {"error": "Invalid JSON"})
            if not isinstance(body, dict):
                return self._send(HTTPStatus.BAD_REQUEST, {"error": "Expected a JSON object"})
        try:
            result = self.app.dispatch(method, url.path, parse_qs(url.query), body, self.headers)
            extra = {"Cache-Control": "no-store"}
            if url.path == "/api/export":
                extra["Content-Disposition"] = 'attachment; filename="codequest-progress.json"'
            self._send(HTTPStatus.OK, result, extra=extra)
        except ApiError as exc:
            self._send(exc.status, {"error": exc.message})
        except Exception as exc:  # noqa: BLE001
            traceback.print_exc()
            self._send(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": f"{type(exc).__name__}: {exc}"})

    def _static(self):
        if not self._host_ok():
            return self._send(HTTPStatus.FORBIDDEN, b"Forbidden", "text/plain")
        path = urlparse(self.path).path
        if path in ("", "/"):
            path = "/index.html"
        target = (config.STATIC_DIR / path.lstrip("/")).resolve()
        if config.STATIC_DIR.resolve() not in target.parents or not target.is_file():
            return self._send(HTTPStatus.NOT_FOUND, b"Not found", "text/plain")
        ctype = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        if ctype.startswith("text/") or ctype in ("application/javascript",):
            ctype += "; charset=utf-8"
        if target.suffix == ".js":
            ctype = "text/javascript; charset=utf-8"
        self._send(HTTPStatus.OK, target.read_bytes(), ctype, {"Cache-Control": "no-cache"})

    def do_GET(self):
        if self.path.startswith("/api/"):
            self._api("GET")
        else:
            self._static()

    do_HEAD = do_GET

    def do_POST(self):
        if self.path.startswith("/api/"):
            self._api("POST")
        else:
            self._send(HTTPStatus.METHOD_NOT_ALLOWED, {"error": "POST to /api only"})


def make_server(host="127.0.0.1", port=config.DEFAULT_PORT, db_path=None, verbose=False):
    store = ProgressStore(db_path or (config.user_data_dir() / "progress.db"))
    app = App(store, Catalog(), allow_remote_hosts=host not in ("127.0.0.1", "localhost", "::1"))
    handler = type("BoundHandler", (Handler,), {"app": app, "quiet": not verbose})
    httpd = ThreadingHTTPServer((host, port), handler)
    httpd.daemon_threads = True
    return httpd, app


def serve(host="127.0.0.1", port=config.DEFAULT_PORT, open_browser=False, verbose=False):
    httpd, app = make_server(host, port, verbose=verbose)
    url = f"http://{'127.0.0.1' if host in ('0.0.0.0', '::') else host}:{port}/"
    cat = app.catalog
    print(f"CodeQuest {__version__} running at {url}")
    print(f"  problems: {cat.problem_count()}  lessons: "
          f"{cat.lesson_count('python')} Python / {cat.lesson_count('cpp')} C++")
    print(f"  python runner: {'subprocess' if config.python_executable() else 'in-process'}   "
          f"C++ compiler: {config.cxx_compiler() or 'none'}")
    print(f"  data: {config.user_data_dir()}")
    # Importing SymPy takes seconds on a phone: warm it up without delaying the UI.
    threading.Thread(target=lambda: [config.has_module(m) for m in ("numpy", "sympy")],
                     daemon=True).start()
    if open_browser:
        threading.Thread(target=_open, args=(url,), daemon=True).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nbye!")
    finally:
        httpd.server_close()


def _open(url):
    time.sleep(0.5)
    import shutil
    import subprocess

    if shutil.which("termux-open-url"):
        subprocess.run(["termux-open-url", url], check=False)
    else:
        import webbrowser
        webbrowser.open(url)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="codequest", description="CodeQuest coding app server")
    ap.add_argument("--host", default="127.0.0.1",
                    help="bind address (default 127.0.0.1; 0.0.0.0 exposes code execution to your network!)")
    ap.add_argument("--port", type=int, default=config.DEFAULT_PORT)
    ap.add_argument("--open", action="store_true", help="open the UI in the browser")
    ap.add_argument("--verbose", action="store_true", help="log every request")
    args = ap.parse_args(argv)
    serve(args.host, args.port, args.open, args.verbose)


if __name__ == "__main__":
    main()
