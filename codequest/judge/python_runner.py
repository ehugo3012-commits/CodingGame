"""Run Python submissions, in a subprocess when possible, else in-process."""

import json
import os
import subprocess
import tempfile
import threading
from pathlib import Path

from .. import config
from . import py_harness

HARNESS = Path(py_harness.__file__).resolve()
# Generous: the first ``import sympy`` on a phone can take several seconds.
STARTUP_SLACK = 15.0
MEMORY_MB = 2048
MAX_RESTARTS = 3

_inprocess_lock = threading.Lock()


def run(code, inputs, time_limit=2.0):
    """Return one result dict per input (see :func:`py_harness.run_tests`)."""
    if not inputs:
        return []
    exe = config.python_executable()
    if exe:
        return _run_subprocess(exe, code, inputs, time_limit)
    return _run_inprocess(code, inputs, time_limit)


def _run_inprocess(code, inputs, time_limit):
    # Serialise: recursion limit and the stdio proxies are process-global.
    with _inprocess_lock:
        return list(py_harness.run_tests(code, inputs, time_limit))


def _run_subprocess(exe, code, inputs, time_limit):
    results = []
    restarts = 0
    with tempfile.TemporaryDirectory(prefix="cq-py-") as tmp:
        tmp = Path(tmp)
        while len(results) < len(inputs):
            pending = inputs[len(results):]
            job = tmp / "job.json"
            out = tmp / f"out{restarts}.jsonl"
            job.write_text(json.dumps({
                "code": code, "inputs": pending,
                "time_limit": time_limit, "memory_mb": MEMORY_MB,
            }), encoding="utf-8")
            wall = STARTUP_SLACK + (time_limit + 1.5) * len(pending)
            env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
            try:
                proc = subprocess.run(
                    [exe, "-I", str(HARNESS), str(job), str(out)],
                    stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                    stderr=subprocess.PIPE, timeout=wall, cwd=tmp, env=env,
                )
                crashed = proc.returncode not in (0, 3)
                crash_msg = proc.stderr.decode("utf-8", "replace")[-4000:]
                if proc.returncode < 0:
                    crash_msg = f"Interpreter killed by signal {-proc.returncode}. {crash_msg}"
            except subprocess.TimeoutExpired:
                crashed, crash_msg = True, "timeout"

            batch = []
            if out.exists():
                for line in out.read_text(encoding="utf-8").splitlines():
                    if line.strip():
                        batch.append(json.loads(line))
            # A "hung" harness reports the stuck test as timeout and the rest as
            # skipped: keep the timeout, drop the skips and restart after it.
            batch = [r for r in batch if r["status"] != "skipped"]
            results.extend(batch)

            if crashed and len(results) < len(inputs):
                if crash_msg == "timeout":
                    results.append(_result("timeout", time=time_limit))
                else:
                    results.append(_result("error", error=crash_msg or "Python crashed"))
                restarts += 1
            elif len(results) < len(inputs) and not batch:
                results.append(_result("error", error="No result from harness"))
                restarts += 1
            elif len(results) < len(inputs):
                restarts += 1

            if restarts > MAX_RESTARTS:
                break
    while len(results) < len(inputs):
        results.append(_result("skipped"))
    return results[: len(inputs)]


def _result(status, stdout="", stderr="", error="", time=0.0):
    return {"status": status, "stdout": stdout, "stderr": stderr, "error": error, "time": time}
