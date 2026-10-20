# CodeQuest 🧩

A mobile coding-education and puzzle app for Android. It has Python and C++
tracks, short lessons, LeetCode-style judged problems with hidden tests, a
**Math & Data** category built on SymPy and NumPy, and gamification: XP,
levels, streaks, badges and a coding-minutes tracker.

It runs in **Termux** today (`python -m codequest`) and packages into an
**APK** with Buildozer.

| | |
|---|---|
| **Lessons** | 62 bite-sized lessons (29 Python + 33 C++). Each has runnable examples and most end in a judged mini-challenge |
| **Problems** | 150 problems from *beginner* (24) to *expert* (15), 121 of them solvable in both Python and C++,, inspired by LeetCode, Project Euler, Codeforces, CSES, HackerRank, AtCoder and Rosalind |
| **Math & Data** | 29 SymPy/NumPy problems with symbolic and floating-point answer checking |
| **Tracking** | Daily coding minutes, attempts (passed and failed), solves, streaks, XP and levels, and 31 badges |

---

## 1. Why this stack? (the framework decision)

Your phone already has Python, Clang, SymPy and NumPy in Termux. The hard
requirement is that the app has to **compile and run the learner's code**.
That rules out most "pretty UI" options. The candidates:

| Option | Editing code on a phone | Runs C++ | Ships as an APK | Verdict |
|---|---|---|---|---|
| **Kivy (native widgets)** | Weak. `CodeInput` handles soft keyboards, selection and scrolling badly | No compiler inside an APK | Yes, via Buildozer | Fine for games, poor for an editor |
| **Tasker-only web UI (Scenes / WebView)** | OK | Yes, through Termux | Needs Tasker App Factory (fragile) | Great for automation, not as the main app |
| **BeeWare / Briefcase** | Native widgets, immature on Android | No | Yes | Too young for this |
| ✅ **Python stdlib server + HTML/JS UI** | Best. The real browser text engine, with a custom symbol bar and syntax highlighting | Yes, through Termux's `clang++` | Yes. Buildozer's **`webview` bootstrap** runs the same server inside the APK | **Chosen** |

**The result is one codebase that runs in two places:**

```
┌──────────── Android WebView / Chrome ────────────┐
│  SPA (vanilla JS, offline, no CDN)               │
│  Learn · Practice · Playground · Profile         │
└───────────────▲──────────────────────────────────┘
                │ JSON over http://127.0.0.1
┌───────────────┴──────────────────────────────────┐
│ codequest.server (http.server, stdlib only)      │
│  ├─ catalog   lessons/problems (data/*.json)     │
│  ├─ progress  SQLite: time, attempts, XP, badges │
│  └─ judge     python_runner ─ subprocess harness │
│               cpp_runner   ─ clang++/g++ -O2     │
│               checkers     ─ tokens/float/sympy… │
└──────────────────────────────────────────────────┘
```

* **Termux mode** (full power). Python runs in an isolated subprocess and C++
  is compiled with Termux's `clang++`.
* **APK mode.** The p4a webview bootstrap starts `main.py` and shows it in a
  WebView. Python (with NumPy and SymPy) runs **in-process**, since an APK
  has no standalone interpreter. C++ can't be compiled inside an APK, so it
  is **forwarded to a CodeQuest instance running in Termux** (the "Termux
  judge"). You can start that judge from Tasker.
* **No dependencies** beyond the Python standard library. NumPy and SymPy are
  only needed for the Math & Data problems.

---

## 2. Run it in Termux (step by step)

```bash
# 1. Get the code onto the phone
pkg install git
git clone https://github.com/ehugo3012-commits/CodingGame.git
cd CodingGame

# 2. One-time setup: python, clang, numpy (pkg), sympy (pip), launchers, Tasker scripts
bash termux/setup.sh

# 3. Start: runs the server in the background and opens the app in your browser
codequest-start
```

Manual alternative: `python -m codequest --open`, then browse to
<http://127.0.0.1:8765>. Stop it with `codequest-stop`.

* **Home-screen icon.** Install **Termux:Widget** and add the *CodeQuest*
  shortcut. `setup.sh` already put it in `~/.shortcuts/`.
* **Where your progress lives.** `~/.codequest/progress.db` (SQLite). You can
  also export it as JSON from **Profile → Export**.
* **Note.** `pip install numpy` usually fails in Termux. Use
  `pkg install python-numpy`, which `setup.sh` does for you.

---

## 3. Build the APK

Buildozer needs a desktop Linux toolchain (Android SDK/NDK). **It does not
run inside Termux.** There are two easy routes.

### Route A: GitHub Actions (no PC needed)

The repo includes `.github/workflows/build.yml`. Every push:

1. runs the unit tests,
2. runs **every reference solution against every test** (`tools/build_content.py`),
3. builds `bin/codequest-*.apk` with Buildozer and uploads it as the
   **`codequest-apk`** artifact.

On your phone, open the repo on GitHub → **Actions** → the latest run →
download `codequest-apk`. Unzip it and install the APK (allow "install
unknown apps" for your browser or file manager). The first build takes
around 30–40 minutes because NumPy is compiled for ARM. Later builds are
cached.

### Route B: a Linux PC / WSL2

```bash
pip install buildozer==1.5.0 "cython<3.1"
sudo apt install -y openjdk-17-jdk zip unzip autoconf automake libtool pkg-config \
     zlib1g-dev libncurses5-dev libncursesw5-dev cmake libffi-dev libssl-dev
buildozer -v android debug          # → bin/codequest-1.0.0-arm64-v8a-debug.apk
adb install bin/*.apk               # or copy the file to the phone
```

Key `buildozer.spec` choices:

* `p4a.bootstrap = webview` and `p4a.port = 5000`: the APK shows our web UI.
* `requirements = python3,numpy,sympy,mpmath`
* `android.archs = arm64-v8a`. Add `armeabi-v7a` for very old phones; this
  doubles build time.

### C++ inside the APK → the Termux judge

1. In Termux, run `codequest-start --no-open`. This starts a CodeQuest
   server on port 8765 with `clang++`.
2. In the APK, open **Profile → Settings → Termux judge URL** and set
   `http://127.0.0.1:8765`.

From then on the APK judges Python itself and sends C++ to Termux. Your
progress stays in the APK. Make step 1 automatic with the Tasker recipe below.

---

## 4. Tasker automation

`setup.sh` installs three scripts into `~/.termux/tasker/`. You need the
**Termux:Tasker** plugin, plus **Termux:API** for notifications.

| Script | Suggested Tasker profile |
|---|---|
| `codequest-start.sh` | *Event → Device Boot*: keeps the C++ judge and server always available |
| `codequest-streak-reminder.sh` | *Time → 20:00 daily*: if you haven't earned XP today, it posts a "🔥 your N-day streak ends at midnight" notification that opens Practice. It prints a status line that Tasker receives as `%stdout` |
| `codequest-stop.sh` | *State → Battery Low* or *Event → Display Off* (+ wait), to save battery |

**Example: streak reminder**

Tasker → **Profiles** → **+** → **Time** 20:00 → **New Task** →
**+** → **Plugin → Termux:Tasker** → Configuration: *Executable* =
`codequest-streak-reminder.sh`. Leave *Execute in a terminal session* unticked.

Your stats are all available as JSON at `http://127.0.0.1:8765/api/home` and
`/api/profile`. You can use Tasker's **HTTP Request** action with them to
build your own widgets or KWGT/KLWP overlays (e.g. today's minutes or the
streak counter).

---

## 5. How the app works

### Learning module

Each track (Python 🐍 / C++ ⚡) is a series of units of short lessons. A
lesson has:

* a short explanation, with common pitfalls called out,
* runnable examples (**▶ Run**, or **✎ Edit in playground**),
* a judged **"Your turn"** challenge with hidden tests. Passing it completes
  the lesson.

### Problem-solving module

* **stdin → stdout.** Every problem reads input and prints output, so one
  problem works in both languages. Starter code already parses the input.
* **▶ Run** checks the visible samples and shows a diff of your output vs the
  expected output. **⌨ Input** runs your code on custom input. **🚀 Submit**
  runs samples plus **hidden tests**. Hidden tests show only pass/fail, never
  their data.
* **💡 Hints** unlock one at a time, from a gentle nudge to the key
  syntax/idea, and never the full answer. Each hint costs 15% of the
  problem's XP, but you always keep at least 40%.
* **Verdicts:** Accepted, Wrong Answer, Runtime Error (with a traceback
  limited to your code), Time Limit Exceeded, Output Limit Exceeded,
  Compilation Error (compiler output).
* **Answer checkers** (per problem): exact tokens; exact lines (for ASCII
  art); case-insensitive; **float** (1e-6 tolerance); **unordered** lines;
  **sympy**, which compares expressions symbolically so `1 + 2*x` equals
  `2*x + 1`.
* After you solve a problem, its **reference solution** unlocks so you can
  compare approaches.
* `#include <bits/stdc++.h>` works even with Termux's clang/libc++, thanks to
  a bundled shim header.

### Gamification and tracking

| Thing | Rule |
|---|---|
| **XP** | Beginner 10 · Easy 20 · Medium 40 · Hard 70 · Expert 120. Solving in your 2nd language gives 50%. Lessons give 5, or 15 with a challenge |
| **Levels** | Each level needs 50 XP more than the last (100, 150, 200 …). Titles run *Novice → Apprentice → Coder → … → Grandmaster* |
| **Streak** | Consecutive days on which you earned XP. Today's streak stays alive until midnight |
| **Coding minutes** | Counted only while the app is visible, you're in a lesson, problem or the playground, and you touched or typed within the last 2 minutes. Shown as a 14-day chart against your daily goal |
| **Attempts** | Every submission is logged with its verdict and passed/total, so you get an acceptance rate and per-problem history |
| **Badges** | 31 badges, e.g. *Sharpshooter* (first try, no hints), *Never Give Up* (solve after 5+ fails), *Polyglot*, *Number Cruncher*, *Night Owl*, *Week Warrior*, *Marathon* |
| **Problem of the day** | A deterministic daily pick from your unsolved problems, shown on Home |

---

## 6. Adding your own lessons and problems

Content is plain Python in `codequest/content/`, so tests can be
**generated**. The full schema is in `codequest/content/__init__.py`.
Minimal problem:

```python
# codequest/content/problems/p50_mine.py
PROBLEMS = [dict(
    id="double-it", title="Double It", difficulty="beginner", category="Basics",
    statement="Print twice the number.", input_format="An integer n.",
    output_format="2·n", hints=["Multiply by 2 with `*`."],
    samples=["21"], tests=["0", "-5"],
    gen=lambda rng: [str(rng.randint(-10**9, 10**9)) for _ in range(5)],
    solution_python="print(2 * int(input()))",
    solution_cpp="#include <iostream>\nint main(){long long n;std::cin>>n;std::cout<<2*n;}",
)]
```

```bash
python tools/build_content.py --only p50 --no-write   # validate just your file
python tools/build_content.py                         # rebuild codequest/data/*.json
```

The builder runs the Python reference to produce the expected outputs. It
checks that the C++ reference **agrees on every test**, that the starter code
compiles, and warns about slow or oversized tests.

---

## 7. Development

```bash
python -m unittest discover -s tests -v   # judge, progress, API, content sanity
python -m codequest --verbose             # log every request
```

```
codequest/
  server.py        HTTP server + JSON API (stdlib only)
  judge/           py_harness.py (sandboxed runner), python_runner, cpp_runner, checkers
  progress.py      SQLite store: activity, attempts, solves, hints, XP, badges, drafts
  gamify.py        XP rules, levels, badge definitions, streak maths
  catalog.py       loads data/*.json, strips hidden tests/solutions for the client
  content/         lesson & problem sources (Python)  →  data/*.json
  static/          index.html, css/app.css, js/{app,editor,md,api}.js
main.py            APK entry point (python-for-android webview bootstrap)
buildozer.spec     APK build config
termux/            setup.sh, start/stop launchers, Tasker scripts
tools/             build_content.py
tests/             unittest suite
```

### Security notes

The judge runs code you type, on your own phone. It protects against
accidents (infinite loops, runaway output, deep recursion, crashes), not
against deliberately malicious code. The server listens only on `127.0.0.1`.
It rejects requests whose `Host`/`Origin` isn't local and only accepts JSON
POSTs, so a web page open in your browser can't make Termux execute code.
Don't use `--host 0.0.0.0` on untrusted networks.
