"""Judge facade: run code locally or via a Termux judge, then score it."""

import json
import urllib.error
import urllib.request

from . import checkers, cpp_runner, python_runner

LANGS = ("python", "cpp")

VERDICTS = {
    "ok": "Accepted",
    "wrong": "Wrong Answer",
    "error": "Runtime Error",
    "timeout": "Time Limit Exceeded",
    "output_limit": "Output Limit Exceeded",
    "compile_error": "Compilation Error",
    "skipped": "Skipped",
}


class JudgeUnavailable(Exception):
    pass


def execute(lang, code, inputs, time_limit=2.0, remote_url=None):
    """Run ``code`` once per stdin string; returns raw result dicts.

    C++ falls back to ``remote_url`` (a CodeQuest server running in Termux)
    when no compiler is installed locally, which is the case inside the APK.
    """
    if lang not in LANGS:
        raise ValueError(f"unknown language {lang!r}")
    if lang == "python":
        return python_runner.run(code, inputs, time_limit)
    if cpp_runner.available():
        return cpp_runner.run(code, inputs, time_limit)
    if remote_url:
        return remote_execute(remote_url, lang, code, inputs, time_limit)
    raise JudgeUnavailable(
        "No C++ compiler here. Install clang in Termux (pkg install clang) and "
        "run CodeQuest there, or start the Termux judge and set its URL in Settings."
    )


def remote_execute(url, lang, code, inputs, time_limit):
    body = json.dumps({"lang": lang, "code": code, "inputs": inputs,
                       "time_limit": time_limit}).encode()
    req = urllib.request.Request(
        url.rstrip("/") + "/api/raw-run", data=body,
        headers={"Content-Type": "application/json"}, method="POST",
    )
    timeout = 120 + (time_limit + 1) * len(inputs)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode())
    except (urllib.error.URLError, OSError, ValueError) as exc:
        raise JudgeUnavailable(f"Termux judge at {url} is not reachable ({exc}). "
                               "Start it with: cq-judge (see README).") from exc
    if "results" not in payload:
        raise JudgeUnavailable(payload.get("error", "Bad response from Termux judge"))
    return payload["results"]


def grade(raw_results, expected_outputs, checker="tokens"):
    """Attach a verdict to each raw result. Returns ``(overall, per_test)``."""
    graded = []
    for res, expected in zip(raw_results, expected_outputs):
        status = res["status"]
        if status == "ok":
            status = "ok" if checkers.check(checker, expected, res["stdout"]) else "wrong"
        graded.append(dict(res, verdict=status))
    overall = "ok"
    for g in graded:
        if g["verdict"] != "ok":
            overall = g["verdict"]
            break
    return overall, graded
