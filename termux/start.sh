#!/data/data/com.termux/files/usr/bin/bash
# Start the CodeQuest server in the background (if needed) and open the UI.
DIR="__CODEQUEST_DIR__"
PORT="${CODEQUEST_PORT:-8765}"
URL="http://127.0.0.1:$PORT/"
LOG="$HOME/.codequest/server.log"
mkdir -p "$HOME/.codequest"

if ! curl -fsS "${URL}api/health" >/dev/null 2>&1; then
  # Keep the CPU awake while the server runs so judging isn't throttled.
  command -v termux-wake-lock >/dev/null && termux-wake-lock
  (cd "$DIR" && nohup python -m codequest --port "$PORT" >"$LOG" 2>&1 &)
  for _ in $(seq 1 40); do
    curl -fsS "${URL}api/health" >/dev/null 2>&1 && break
    sleep 0.25
  done
fi

if [ "${1:-}" != "--no-open" ]; then
  termux-open-url "$URL" 2>/dev/null || echo "Open $URL in your browser"
fi
