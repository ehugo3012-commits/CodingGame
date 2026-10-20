"""Runtime configuration and environment detection.

CodeQuest runs in two environments:

* **Termux** (or any Linux/macOS desktop): a real ``python`` binary and a C++
  compiler (``clang++`` / ``g++``) are on PATH, so user code is executed in
  isolated subprocesses.
* **Android APK** built with Buildozer / python-for-android (webview
  bootstrap): Python is embedded in the app, there is no standalone
  interpreter binary and no C++ compiler.  Python code runs in-process and C++
  submissions are forwarded to a Termux "judge" server, if one is reachable.
"""

import os
import shutil
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
STATIC_DIR = PACKAGE_DIR / "static"
DATA_DIR = PACKAGE_DIR / "data"
CXX_INCLUDE_DIR = PACKAGE_DIR / "judge" / "include"

IS_ANDROID_APP = "ANDROID_ARGUMENT" in os.environ or "ANDROID_PRIVATE" in os.environ
IS_TERMUX = "TERMUX_VERSION" in os.environ or os.environ.get("PREFIX", "").startswith(
    "/data/data/com.termux"
)

DEFAULT_PORT = 5000 if IS_ANDROID_APP else 8765
DEFAULT_REMOTE_JUDGE = "http://127.0.0.1:8765"


def user_data_dir() -> Path:
    """Where the progress database and compile cache live."""
    override = os.environ.get("CODEQUEST_HOME")
    if override:
        path = Path(override)
    elif IS_ANDROID_APP:
        path = Path(os.environ.get("ANDROID_PRIVATE", os.getcwd())) / "codequest"
    else:
        path = Path.home() / ".codequest"
    path.mkdir(parents=True, exist_ok=True)
    return path


@lru_cache(maxsize=1)
def python_executable():
    """Return a usable standalone Python interpreter, or None.

    Inside an APK ``sys.executable`` points at the app launcher (or is empty),
    so we probe it before trusting it.
    """
    override = os.environ.get("CODEQUEST_PYTHON")
    candidates = [override] if override else []
    if not IS_ANDROID_APP:
        candidates += [sys.executable, shutil.which("python3"), shutil.which("python")]
    for exe in candidates:
        if not exe:
            continue
        try:
            proc = subprocess.run(
                [exe, "-c", "import sys; print(sys.version_info[0])"],
                capture_output=True, text=True, timeout=10,
            )
        except (OSError, subprocess.SubprocessError):
            continue
        if proc.returncode == 0 and proc.stdout.strip() == "3":
            return exe
    return None


@lru_cache(maxsize=1)
def cxx_compiler():
    """Return the C++ compiler to use, or None. Termux ships clang++."""
    override = os.environ.get("CODEQUEST_CXX")
    if override:
        return override if shutil.which(override) else None
    for name in ("clang++", "g++", "c++"):
        path = shutil.which(name)
        if path:
            return path
    return None


@lru_cache(maxsize=None)
def has_module(name: str) -> bool:
    try:
        __import__(name)
        return True
    except Exception:
        return False
