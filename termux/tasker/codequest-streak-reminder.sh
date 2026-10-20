#!/data/data/com.termux/files/usr/bin/bash
# Tasker: run every evening. If you haven't earned XP today, post a reminder
# notification so your streak survives. Needs the Termux:API app + package.
# Prints a one-line status, which Termux:Tasker can hand back to Tasker as %stdout.
PORT="${CODEQUEST_PORT:-8765}"
URL="http://127.0.0.1:$PORT"
"$PREFIX/bin/codequest-start" --no-open
JSON="$(curl -fsS "$URL/api/home")" || { echo "server not reachable"; exit 1; }
read -r ACTIVE STREAK MINUTES GOAL < <(python - "$JSON" <<'PY'
import json, sys
d = json.loads(sys.argv[1])
print(int(d["streak"]["active_today"]), d["streak"]["current"],
      int(d["time"]["today_minutes"]), d["time"]["goal_minutes"])
PY
)
if [ "$ACTIVE" = "1" ]; then
  echo "streak safe: $STREAK days, ${MINUTES}/${GOAL} min today"
else
  MSG="Your ${STREAK}-day streak ends at midnight! One quick problem keeps it alive."
  [ "$STREAK" = "0" ] && MSG="Start a streak today: solve one problem or finish a lesson."
  termux-notification --id codequest-streak --title "🔥 CodeQuest" --content "$MSG" \
    --action "termux-open-url $URL/#/practice" 2>/dev/null || true
  echo "reminder sent: $MSG"
fi
