"""Compile and run C++ submissions with clang++ (Termux) or g++."""

import hashlib
import os
import re
import shutil
import subprocess
import tempfile
import threading
import time
from pathlib import Path

from .. import config

COMPILE_TIMEOUT = 90.0  # first compile on an older phone can be slow
MEMORY_MB = 512
OUTPUT_LIMIT = 4 * 1024 * 1024
RETURN_LIMIT = 64 * 1024
CACHE_ENTRIES = 40
FLAGS = ["-std=c++17", "-O2", "-pipe", "-w"]

SIGNAL_NAMES = {
    4: "SIGILL (illegal instruction)",
    6: "SIGABRT (abort - failed assert or uncaught exception?)",
    8: "SIGFPE (arithmetic error - division by zero?)",
    9: "SIGKILL (killed - memory limit?)",
    11: "SIGSEGV (segmentation fault - out-of-bounds access or null pointer?)",
    25: "SIGXFSZ (output limit exceeded)",
}

_cache_lock = threading.Lock()


def available():
    return config.cxx_compiler() is not None


def _cache_dir():
    path = config.user_data_dir() / "cpp-cache"
    path.mkdir(parents=True, exist_ok=True)
    return path


def compile_source(code):
    """Return ``(exe_path, None)`` or ``(None, error_message)``."""
    cxx = config.cxx_compiler()
    if not cxx:
        return None, "No C++ compiler found. In Termux run: pkg install clang"
    digest = hashlib.sha256((cxx + " ".join(FLAGS) + "\0" + code).encode()).hexdigest()[:24]
    cache = _cache_dir()
    exe = cache / f"sol-{digest}"
    with _cache_lock:
        if exe.exists():
            os.utime(exe)
            return exe, None
    with tempfile.TemporaryDirectory(prefix="cq-cpp-") as tmp:
        src = Path(tmp) / "solution.cpp"
        src.write_text(code, encoding="utf-8")
        tmp_exe = Path(tmp) / "solution"
        cmd = [cxx, *FLAGS, "-I", str(config.CXX_INCLUDE_DIR), "-o", str(tmp_exe), str(src)]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=COMPILE_TIMEOUT)
        except subprocess.TimeoutExpired:
            return None, "Compilation timed out."
        if proc.returncode != 0:
            msg = (proc.stderr or proc.stdout).replace(str(src), "solution.cpp")
            msg = re.sub(r"\x1b\[[0-9;]*m", "", msg)
            return None, msg[-8000:] or "Compilation failed."
        with _cache_lock:
            shutil.move(str(tmp_exe), exe)
            _prune_cache(cache)
    return exe, None


def _prune_cache(cache):
    entries = sorted(cache.glob("sol-*"), key=lambda p: p.stat().st_mtime, reverse=True)
    for old in entries[CACHE_ENTRIES:]:
        try:
            old.unlink()
        except OSError:
            pass


def _limits():
    try:
        import resource

        mem = MEMORY_MB * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (mem, mem))
        resource.setrlimit(resource.RLIMIT_FSIZE, (OUTPUT_LIMIT, OUTPUT_LIMIT))
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    except Exception:
        pass


def run(code, inputs, time_limit=2.0):
    """Compile once, run once per input; same result shape as the Python runner."""
    if not inputs:
        return []
    exe, err = compile_source(code)
    if err:
        return [_result("compile_error", error=err) for _ in inputs]
    results = []
    with tempfile.TemporaryDirectory(prefix="cq-run-") as tmp:
        for stdin_text in inputs:
            results.append(_run_once(exe, stdin_text, time_limit, Path(tmp)))
    return results


def _run_once(exe, stdin_text, time_limit, tmp):
    inp, outp, errp = tmp / "in.txt", tmp / "out.txt", tmp / "err.txt"
    inp.write_text(stdin_text, encoding="utf-8")
    with open(inp, "rb") as fin, open(outp, "wb") as fout, open(errp, "wb") as ferr:
        start = time.perf_counter()
        proc = subprocess.Popen([str(exe)], stdin=fin, stdout=fout, stderr=ferr,
                                cwd=tmp, preexec_fn=_limits if os.name == "posix" else None)
        try:
            code = proc.wait(timeout=time_limit)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
            code = None
        elapsed = time.perf_counter() - start
    out = outp.read_bytes()[:OUTPUT_LIMIT].decode("utf-8", "replace")
    err = errp.read_bytes()[:RETURN_LIMIT].decode("utf-8", "replace")
    if code is None:
        return _result("timeout", out[:RETURN_LIMIT], err, "", time_limit)
    if code < 0:
        sig = -code
        if sig == 25:
            return _result("output_limit", out[:RETURN_LIMIT], err, "Output limit exceeded", elapsed)
        name = SIGNAL_NAMES.get(sig, f"signal {sig}")
        return _result("error", out[:RETURN_LIMIT], err, f"Runtime error: {name}", elapsed)
    if code != 0:
        return _result("error", out[:RETURN_LIMIT], err,
                       f"Program exited with code {code} (main should return 0)", elapsed)
    return _result("ok", out, err, "", elapsed)


def _result(status, stdout="", stderr="", error="", time=0.0):
    return {"status": status, "stdout": stdout, "stderr": stderr,
            "error": error, "time": round(time, 4)}
