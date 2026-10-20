"""APK / desktop entry point.

python-for-android's "webview" bootstrap runs this file, waits until
something listens on ``p4a.port`` (5000, see buildozer.spec) and then points
its WebView at http://127.0.0.1:5000/. In Termux you can also simply run
``python main.py`` (port 8765).
"""

from codequest import config
from codequest.server import serve

if __name__ == "__main__":
    serve(port=config.DEFAULT_PORT)
