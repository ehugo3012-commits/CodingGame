#!/data/data/com.termux/files/usr/bin/bash
# Stop the CodeQuest server.
pkill -f "python -m codequest" && echo "CodeQuest stopped." || echo "CodeQuest was not running."
command -v termux-wake-unlock >/dev/null && termux-wake-unlock
exit 0
