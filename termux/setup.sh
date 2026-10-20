#!/data/data/com.termux/files/usr/bin/bash
# One-time CodeQuest setup for Termux.
#   bash termux/setup.sh
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"

echo "==> Installing packages (python, clang, numpy)…"
pkg update -y
pkg install -y python clang python-numpy curl
# SymPy is pure Python; pip works fine for it in Termux.
pip install --upgrade sympy mpmath

echo "==> Optional: termux-api for notifications (also install the Termux:API app)"
pkg install -y termux-api || true

echo "==> Installing launcher scripts"
mkdir -p "$HOME/.shortcuts" "$HOME/.termux/tasker" "$PREFIX/bin"
for f in start stop; do
  sed "s#__CODEQUEST_DIR__#$HERE#g" "$HERE/termux/$f.sh" > "$PREFIX/bin/codequest-$f"
  chmod +x "$PREFIX/bin/codequest-$f"
done
# Termux:Widget home-screen shortcut
cp "$PREFIX/bin/codequest-start" "$HOME/.shortcuts/CodeQuest"
# Termux:Tasker scripts (Tasker -> Plugin -> Termux:Tasker -> pick the script)
for f in "$HERE"/termux/tasker/*.sh; do
  name="$(basename "$f")"
  sed "s#__CODEQUEST_DIR__#$HERE#g" "$f" > "$HOME/.termux/tasker/$name"
  chmod +x "$HOME/.termux/tasker/$name"
done

echo "==> Self-test"
(cd "$HERE" && python -m unittest discover -s tests 2>&1 | tail -3)

cat <<MSG

All set!  Start CodeQuest with:   codequest-start
Stop it with:                     codequest-stop
Home-screen widget:  install Termux:Widget and add the "CodeQuest" shortcut.
Tasker:              see README.md -> "Tasker automation".
MSG
