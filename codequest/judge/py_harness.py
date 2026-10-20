"""Execute a user's Python program against a list of stdin inputs.

This module is deliberately self-contained (stdlib only, no package imports)
because it is used in two ways:

1. As a script in a fresh interpreter (Termux / desktop)::

       python -I py_harness.py job.json results.jsonl

   ``job.json`` holds ``{"code": str, "inputs": [str], "time_limit": float}``.
   One JSON result per input is appended to ``results.jsonl`` as soon as the
   test finishes, so the parent can recover partial results if we get killed.

2. In-process via :func:`run_tests` (Android APK, where there is no
   standalone interpreter binary).

Running every test inside one interpreter matters on a phone: importing
SymPy can take a couple of seconds, and we only want to pay that once.

This is a *learning* sandbox, not a security boundary. It protects against
accidents (infinite loops, runaway output, deep recursion), not malice.
"""

import builtins
import io
import json
import linecache
import os
import sys
import threading
import time
import traceback

FILENAME = "<solution>"
OUTPUT_LIMIT = 4 * 1024 * 1024  # bytes of stdout per test before we give up
RETURN_LIMIT = 64 * 1024  # characters of stdout/stderr echoed back per test
STACK_SIZE = 128 * 1024 * 1024
RECURSION_LIMIT = 50_000


class OutputLimitExceeded(Exception):
    pass


class TimeLimitExceeded(BaseException):
    """Raised asynchronously inside the worker thread when time runs out.

    Derives from BaseException so a bare ``except Exception`` in user code
    does not swallow it.
    """


class _LimitedBytesIO(io.BytesIO):
    def write(self, b):
        if self.tell() + len(b) > OUTPUT_LIMIT:
            raise OutputLimitExceeded("output limit exceeded")
        return super().write(b)


def _text_stream(initial: bytes = b"", limited=False):
    raw = _LimitedBytesIO(initial) if limited else io.BytesIO(initial)
    return io.TextIOWrapper(raw, encoding="utf-8", newline=None, write_through=True)


class _ThreadLocalStream:
    """Proxy for sys.stdin/stdout/stderr that routes per thread.

    Threads that are running user code get their own buffers; every other
    thread (e.g. the HTTP server in APK mode) keeps the real stream.
    """

    def __init__(self, fallback, slot):
        self._fallback = fallback
        self._slot = slot
        self._local = threading.local()

    def _target(self):
        return getattr(self._local, self._slot, None) or self._fallback

    def bind(self, stream):
        setattr(self._local, self._slot, stream)

    def __getattr__(self, name):
        return getattr(self._target(), name)

    def __iter__(self):
        return iter(self._target())

    def __next__(self):
        return next(self._target())

    def write(self, s):
        return self._target().write(s)


_install_lock = threading.Lock()
_proxies = None


def _install_proxies():
    global _proxies
    with _install_lock:
        if _proxies is None or sys.stdout is not _proxies[1]:
            _proxies = (
                _ThreadLocalStream(sys.stdin, "s"),
                _ThreadLocalStream(sys.stdout, "s"),
                _ThreadLocalStream(sys.stderr, "s"),
            )
            sys.stdin, sys.stdout, sys.stderr = _proxies
    return _proxies


def _format_exception(exc):
    """Traceback limited to the user's own frames."""
    tb = exc.__traceback__
    while tb is not None and tb.tb_frame.f_code.co_filename != FILENAME:
        tb = tb.tb_next
    lines = traceback.format_exception(type(exc), exc, tb)
    return "".join(lines).replace('File "<solution>"', "File solution.py")


def _async_raise(thread, exc_type):
    """Inject an exception into another thread (best effort, CPython only)."""
    try:
        import ctypes

        ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_ulong(thread.ident), ctypes.py_object(exc_type)
        )
        return True
    except Exception:
        return False


def _preimport(code):
    """Import the modules the program imports *before* the clock starts.

    ``import sympy`` can take seconds on a phone; that shouldn't count against
    the learner's time limit.
    """
    import ast
    import importlib

    try:
        tree = ast.parse(code)
    except SyntaxError:
        return
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and not node.level:
            names.add(node.module.split(".")[0])
    for name in names:
        try:
            importlib.import_module(name)
        except BaseException:  # noqa: BLE001 - the real import will report it
            pass


def _run_one(compiled, stdin_text, real_fd0):
    """Run compiled code once with the given stdin. Executed in a worker thread."""
    stdin_proxy, stdout_proxy, stderr_proxy = _install_proxies()
    data = stdin_text.encode("utf-8")
    fin = _text_stream(data)
    fout = _text_stream(limited=True)
    ferr = _text_stream(limited=True)
    stdin_proxy.bind(fin)
    stdout_proxy.bind(fout)
    stderr_proxy.bind(ferr)
    if real_fd0:
        # Support the competitive-programming idiom ``open(0).read()``.
        import tempfile

        with tempfile.TemporaryFile() as tmp:
            tmp.write(data)
            tmp.flush()
            tmp.seek(0)
            os.dup2(tmp.fileno(), 0)
    status, error = "ok", ""
    glb = {"__name__": "__main__", "__builtins__": builtins, "__file__": "solution.py"}
    try:
        exec(compiled, glb)
    except SystemExit as exc:
        if exc.code not in (None, 0):
            status, error = "error", f"SystemExit: {exc.code}"
    except TimeLimitExceeded:
        status = "timeout"
    except OutputLimitExceeded:
        status, error = "output_limit", "Output limit exceeded"
    except MemoryError:
        status, error = "error", "MemoryError: your program used too much memory"
    except RecursionError as exc:
        status, error = "error", _format_exception(exc)
    except BaseException as exc:  # noqa: BLE001 - we report everything to the learner
        status, error = "error", _format_exception(exc)
    finally:
        stdin_proxy.bind(None)
        stdout_proxy.bind(None)
        stderr_proxy.bind(None)
    out = fout.buffer.getvalue().decode("utf-8", "replace")
    err = ferr.buffer.getvalue().decode("utf-8", "replace")
    return status, out, err, error


def run_tests(code, inputs, time_limit=2.0, on_result=None, real_fd0=False):
    """Run ``code`` once per input; return a list of result dicts.

    Each result: ``{"status", "stdout", "stderr", "error", "time"}`` where
    status is one of ``ok``, ``error``, ``timeout``, ``output_limit`` or
    ``compile_error``. If a test cannot be stopped after timing out, the
    remaining tests are reported as ``skipped`` and ``hung`` is set on the
    returned list so the caller can discard this interpreter.
    """
    results = []

    def emit(res):
        results.append(res)
        if on_result:
            on_result(res)

    try:
        compiled = compile(code, FILENAME, "exec")
    except SyntaxError as exc:
        msg = "".join(traceback.format_exception_only(type(exc), exc))
        msg = msg.replace('File "<solution>"', "File solution.py")
        for _ in inputs:
            emit({"status": "compile_error", "stdout": "", "stderr": "", "error": msg, "time": 0.0})
        return results

    linecache.cache[FILENAME] = (len(code), None, code.splitlines(True), FILENAME)
    _preimport(code)
    old_limit = sys.getrecursionlimit()

    for idx, stdin_text in enumerate(inputs):
        box = {}

        def target():
            sys.setrecursionlimit(RECURSION_LIMIT)
            start = time.perf_counter()
            box["res"] = _run_one(compiled, stdin_text, real_fd0)
            box["time"] = time.perf_counter() - start

        try:
            threading.stack_size(STACK_SIZE)
        except (ValueError, RuntimeError):
            pass
        worker = threading.Thread(target=target, daemon=True, name=f"cq-test-{idx}")
        worker.start()
        try:
            threading.stack_size(0)
        except (ValueError, RuntimeError):
            pass
        worker.join(time_limit)
        if worker.is_alive():
            _async_raise(worker, TimeLimitExceeded)
            worker.join(1.0)
        if worker.is_alive():
            # Stuck inside C code (e.g. time.sleep, a giant NumPy op). We can't
            # stop it, so report and bail out; the caller decides what's next.
            emit({"status": "timeout", "stdout": "", "stderr": "", "error": "", "time": time_limit})
            for _ in inputs[idx + 1:]:
                emit({"status": "skipped", "stdout": "", "stderr": "", "error": "", "time": 0.0})
            sys.setrecursionlimit(old_limit)
            results_hung = _HungList(results)
            return results_hung
        status, out, err, error = box["res"]
        elapsed = box["time"]
        if status == "ok" and elapsed > time_limit:
            status = "timeout"
        emit({
            "status": status,
            "stdout": out[:RETURN_LIMIT] if status != "ok" else out[:OUTPUT_LIMIT],
            "stderr": err[:RETURN_LIMIT],
            "error": error[:RETURN_LIMIT],
            "time": round(elapsed, 4),
        })

    sys.setrecursionlimit(old_limit)
    return results


class _HungList(list):
    hung = True


def _main(argv):
    job_path, out_path = argv[1], argv[2]
    with open(job_path, encoding="utf-8") as fh:
        job = json.load(fh)
    # Keep a private handle to the results file so user code printing to the
    # real stdout can't corrupt the protocol.
    out = open(out_path, "a", encoding="utf-8")

    def on_result(res):
        out.write(json.dumps(res) + "\n")
        out.flush()

    try:
        import resource

        limit = int(job.get("memory_mb", 0)) * 1024 * 1024
        if limit:
            resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
    except Exception:
        pass

    res = run_tests(job["code"], job["inputs"], float(job.get("time_limit", 2.0)),
                    on_result=on_result, real_fd0=True)
    out.close()
    # os._exit: don't wait for a hung daemon thread or run user atexit hooks.
    os._exit(3 if getattr(res, "hung", False) else 0)


if __name__ == "__main__":
    _main(sys.argv)
