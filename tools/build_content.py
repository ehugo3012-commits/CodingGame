#!/usr/bin/env python3
"""Validate the content library and compile it to codequest/data/*.json.

For every problem this:
  * generates the hidden tests (fixed + seeded random),
  * runs the Python reference to produce expected outputs,
  * runs the C++ reference (if any) and checks it agrees,
  * checks starter code compiles / parses and does NOT already pass.
For every lesson it runs each example and the challenge reference.

Usage:
    python tools/build_content.py                 # build everything
    python tools/build_content.py --only arrays   # just files matching *arrays*
    python tools/build_content.py --only arrays --no-write   # validate only
"""

import argparse
import concurrent.futures as cf
import importlib.util
import json
import random
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from codequest import config, gamify, judge  # noqa: E402
from codequest.content import CPP_STARTER, PY_STARTER  # noqa: E402
from codequest.judge import checkers  # noqa: E402

CONTENT = ROOT / "codequest" / "content"
ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REQUIRED = ["id", "title", "difficulty", "category", "statement", "input_format",
            "output_format", "hints", "samples", "solution_python"]
LESSON_REQUIRED = ["id", "track", "unit", "title", "summary", "body"]
MAX_IO_BYTES = 200_000  # inputs + expected outputs per problem
WARN_IO_BYTES = 60_000


class BuildError(Exception):
    pass


def load_modules(subdir, attr, only):
    items = []
    for path in sorted((CONTENT / subdir).glob("*.py")):
        if path.name.startswith("_"):
            continue
        if only and not any(o in path.stem for o in only):
            continue
        spec = importlib.util.spec_from_file_location(f"cq_content_{subdir}_{path.stem}", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for i, item in enumerate(getattr(mod, attr)):
            items.append((path.name, i, item))
    return items


def norm_input(s):
    s = str(s)
    return s if s.endswith("\n") else s + "\n"


def run_ok(lang, code, inputs, tl, what):
    results = judge.execute(lang, code, inputs, tl)
    for i, r in enumerate(results):
        if r["status"] != "ok":
            detail = (r["error"] or r["stderr"] or r["status"])[-1500:]
            raise BuildError(f"{what}: {lang} reference failed on input #{i} "
                             f"({r['status']}):\n{detail}\n--- input ---\n{inputs[i][:300]}")
    return results


def build_problem(src, order, p, warnings):
    pid = p.get("id", f"<{src}#{order}>")
    missing = [k for k in REQUIRED if k not in p]
    if missing:
        raise BuildError(f"{pid}: missing keys {missing}")
    if not ID_RE.match(pid):
        raise BuildError(f"{pid}: id must be kebab-case")
    if p["difficulty"] not in gamify.DIFFICULTIES:
        raise BuildError(f"{pid}: bad difficulty {p['difficulty']!r}")
    checker = p.get("checker", "tokens")
    if checker not in checkers.CHECKERS:
        raise BuildError(f"{pid}: unknown checker {checker!r}")
    if not p["hints"]:
        raise BuildError(f"{pid}: needs at least one hint")
    tl = float(p.get("time_limit", 2.0))

    samples = [norm_input(s) for s in p["samples"]]
    hidden = [norm_input(s) for s in p.get("tests", [])]
    if "gen" in p:
        rng = random.Random(f"codequest:{pid}")
        hidden += [norm_input(s) for s in p["gen"](rng)]
    if not samples:
        raise BuildError(f"{pid}: needs at least one sample")
    if len(hidden) < 3:
        warnings.append(f"{pid}: only {len(hidden)} hidden tests")
    # de-duplicate hidden tests (and drop ones equal to samples)
    seen = set(samples)
    hidden = [h for h in hidden if not (h in seen or seen.add(h))]
    inputs = samples + hidden

    t0 = time.perf_counter()
    py = run_ok("python", p["solution_python"], inputs, tl * 4, pid)
    slowest = max(r["time"] for r in py)
    if slowest > tl / 4:
        warnings.append(f"{pid}: python reference took {slowest:.2f}s on one test "
                        f"(limit {tl}s) - phones are slower, consider smaller tests")
    outputs = [r["stdout"] for r in py]
    size = sum(len(s) for s in inputs) + sum(len(o) for o in outputs)
    if size > MAX_IO_BYTES:
        raise BuildError(f"{pid}: test I/O totals {size} bytes; keep under {MAX_IO_BYTES}")
    if size > WARN_IO_BYTES:
        warnings.append(f"{pid}: test I/O is {size // 1000} KB - the app ships all of it, keep it lean")
    if any(not o.strip() for o in outputs):
        warnings.append(f"{pid}: a test produces empty output")

    languages = p.get("languages") or (["python", "cpp"] if p.get("solution_cpp") else ["python"])
    if "cpp" in languages:
        if not p.get("solution_cpp"):
            raise BuildError(f"{pid}: languages include cpp but there is no solution_cpp")
        cpp = run_ok("cpp", p["solution_cpp"], inputs, tl * 4, pid)
        for i, (r, exp) in enumerate(zip(cpp, outputs)):
            if not checkers.check(checker, exp, r["stdout"]):
                raise BuildError(f"{pid}: C++ and Python references disagree on input #{i}\n"
                                 f"input: {inputs[i][:200]!r}\npython: {exp[:200]!r}\n"
                                 f"c++: {r['stdout'][:200]!r}")

    starter = {"python": p.get("starter_python", PY_STARTER)}
    if "cpp" in languages:
        starter["cpp"] = p.get("starter_cpp", CPP_STARTER)
    for lang, code in starter.items():
        res = judge.execute(lang, code, inputs[:1], tl * 4)[0]
        if res["status"] == "compile_error":
            raise BuildError(f"{pid}: {lang} starter does not compile:\n{res['error'][:800]}")

    return {
        "id": pid, "title": p["title"], "difficulty": p["difficulty"],
        "category": p["category"], "languages": languages,
        "tags": p.get("tags", []), "inspired_by": p.get("inspired_by", ""),
        "statement": p["statement"].strip(), "input_format": p["input_format"].strip(),
        "output_format": p["output_format"].strip(), "hints": p["hints"],
        "checker": checker, "time_limit": tl, "starter": starter,
        "solution": {"python": p["solution_python"],
                     **({"cpp": p["solution_cpp"]} if "cpp" in languages else {})},
        "samples": [{"input": i, "output": o} for i, o in zip(samples, outputs)],
        "tests": [{"input": i, "output": o} for i, o in zip(hidden, outputs[len(samples):])],
        "order": order, "source": src,
        "_build_seconds": round(time.perf_counter() - t0, 2),
    }


def build_lesson(src, order, l, warnings):
    lid = l.get("id", f"<{src}#{order}>")
    missing = [k for k in LESSON_REQUIRED if k not in l]
    if missing:
        raise BuildError(f"{lid}: missing keys {missing}")
    if not ID_RE.match(lid):
        raise BuildError(f"{lid}: id must be kebab-case")
    track = l["track"]
    if track not in judge.LANGS:
        raise BuildError(f"{lid}: bad track {track!r}")
    examples = []
    for i, ex in enumerate(l.get("examples", [])):
        stdin = ex.get("stdin", "")
        res = run_ok(track, ex["code"], [stdin], 10, f"{lid} example #{i}")[0]
        examples.append({"title": ex.get("title", f"Example {i + 1}"), "code": ex["code"],
                         "stdin": stdin, "explain": ex.get("explain", ""),
                         "output": res["stdout"]})
    challenge = None
    ch = l.get("challenge")
    if ch:
        checker = ch.get("checker", "tokens")
        samples = [norm_input(s) for s in ch["samples"]]
        hidden = [norm_input(s) for s in ch.get("tests", [])]
        inputs = samples + hidden
        outs = [r["stdout"] for r in run_ok(track, ch["solution"], inputs, 10, f"{lid} challenge")]
        res = judge.execute(track, ch["starter"], inputs[:1], 10)[0]
        if res["status"] == "compile_error":
            raise BuildError(f"{lid}: challenge starter does not compile:\n{res['error'][:800]}")
        challenge = {
            "prompt": ch["prompt"].strip(), "starter": ch["starter"], "solution": ch["solution"],
            "checker": checker, "time_limit": 2.0,
            "samples": [{"input": i, "output": o} for i, o in zip(samples, outs)],
            "tests": [{"input": i, "output": o} for i, o in zip(hidden, outs[len(samples):])],
        }
    return {"id": lid, "track": track, "unit": l["unit"], "title": l["title"],
            "summary": l["summary"], "body": l["body"].strip(), "examples": examples,
            "challenge": challenge, "order": order, "source": src,
            "xp": gamify.LESSON_XP + (gamify.CHALLENGE_XP if challenge else 0)}


def parallel_build(items, fn, jobs):
    warnings, errors, out = [], [], [None] * len(items)
    with cf.ThreadPoolExecutor(max_workers=jobs) as pool:
        futs = {pool.submit(fn, src, order, item, warnings): k
                for k, (src, order, item) in enumerate(items)}
        for fut in cf.as_completed(futs):
            k = futs[fut]
            try:
                out[k] = fut.result()
                print(".", end="", flush=True)
            except BuildError as exc:
                errors.append(str(exc))
                print("E", end="", flush=True)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{items[k][0]}#{items[k][1]}: {type(exc).__name__}: {exc}")
                print("E", end="", flush=True)
    print()
    return [o for o in out if o], warnings, errors


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--only", nargs="*", help="only content files whose name contains this")
    ap.add_argument("--no-write", action="store_true", help="validate without writing JSON")
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()
    if not config.cxx_compiler():
        print("warning: no C++ compiler - C++ references are NOT being verified")

    all_errors = []
    built = {}
    for kind, subdir, attr, fn in (("problems", "problems", "PROBLEMS", build_problem),
                                   ("lessons", "lessons", "LESSONS", build_lesson)):
        items = load_modules(subdir, attr, args.only)
        if not items:
            continue
        print(f"Building {len(items)} {kind}")
        result, warnings, errors = parallel_build(items, fn, args.jobs)
        ids = [r["id"] for r in result]
        dupes = {i for i in ids if ids.count(i) > 1}
        if dupes:
            errors.append(f"duplicate {kind} ids: {sorted(dupes)}")
        for w in sorted(warnings):
            print("  warn:", w)
        all_errors += errors
        built[kind] = result
        if kind == "problems":
            by = {}
            for r in result:
                by.setdefault(r["difficulty"], 0)
                by[r["difficulty"]] += 1
            print("  by difficulty:", by)
            slow = sorted(result, key=lambda r: -r["_build_seconds"])[:3]
            print("  slowest:", [(r["id"], r["_build_seconds"]) for r in slow])

    for e in all_errors:
        print("\nERROR:", e)
    if all_errors:
        print(f"\n{len(all_errors)} error(s); nothing written.")
        return 1
    if args.no_write or args.only:
        print("Validation passed (not written: partial build or --no-write).")
        return 0
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    for kind, result in built.items():
        for r in result:
            r.pop("_build_seconds", None)
        (config.DATA_DIR / f"{kind}.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"Wrote {len(result)} {kind} -> codequest/data/{kind}.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
