"""XP rules, levels and badge definitions (pure functions, no I/O)."""

DIFFICULTIES = ["beginner", "easy", "medium", "hard", "expert"]
BASE_XP = {"beginner": 10, "easy": 20, "medium": 40, "hard": 70, "expert": 120}
LESSON_XP = 5
CHALLENGE_XP = 10
HINT_PENALTY = 0.15  # each revealed hint removes 15% of the problem's XP...
MIN_XP_FACTOR = 0.4  # ...but you always keep at least 40%
SECOND_LANGUAGE_FACTOR = 0.5  # re-solving in the other language

LEVEL_TITLES = [
    "Novice", "Apprentice", "Coder", "Problem Solver", "Hacker", "Engineer",
    "Algorithmist", "Architect", "Wizard", "Grandmaster",
]


def problem_xp(difficulty, hints_used=0, second_language=False):
    factor = max(MIN_XP_FACTOR, 1.0 - HINT_PENALTY * hints_used)
    if second_language:
        factor *= SECOND_LANGUAGE_FACTOR
    return max(1, round(BASE_XP.get(difficulty, 10) * factor))


def level_threshold(level):
    """Total XP needed to *reach* ``level`` (level 1 = 0 XP).

    Increments grow by 50: 100, 150, 200, 250 ...
    """
    return 25 * (level - 1) * (level + 2)


def level_for(xp):
    level = 1
    while level_threshold(level + 1) <= xp:
        level += 1
    lo, hi = level_threshold(level), level_threshold(level + 1)
    title = LEVEL_TITLES[min(level - 1, len(LEVEL_TITLES) - 1)]
    return {"level": level, "title": title, "xp": xp, "level_start": lo,
            "level_end": hi, "progress": (xp - lo) / (hi - lo)}


# Each badge: id, name, description, icon (emoji), predicate over a stats dict.
# Stats are produced by ProgressStore.badge_stats().
BADGES = [
    ("first-solve", "Hello, World", "Solve your first problem", "🎉",
     lambda s: s["solved"] >= 1),
    ("solve-10", "Getting Warm", "Solve 10 problems", "🔥", lambda s: s["solved"] >= 10),
    ("solve-25", "Quarter Century", "Solve 25 problems", "🏅", lambda s: s["solved"] >= 25),
    ("solve-50", "Half Way There", "Solve 50 problems", "🥈", lambda s: s["solved"] >= 50),
    ("solve-100", "Centurion", "Solve 100 problems", "🏆", lambda s: s["solved"] >= 100),
    ("first-try", "Sharpshooter", "Solve a problem on the first attempt with no hints", "🎯",
     lambda s: s["clean_solves"] >= 1),
    ("clean-10", "Laser Focus", "10 first-attempt, hint-free solves", "🔭",
     lambda s: s["clean_solves"] >= 10),
    ("persistent", "Never Give Up", "Solve a problem after 5+ failed attempts", "🧗",
     lambda s: s["max_fails_before_solve"] >= 5),
    ("medium", "Level Up", "Solve a medium problem", "⚙️", lambda s: s["by_diff"].get("medium", 0) >= 1),
    ("hard", "Heavy Lifter", "Solve a hard problem", "💪", lambda s: s["by_diff"].get("hard", 0) >= 1),
    ("expert", "Grandmaster Move", "Solve an expert problem", "👑",
     lambda s: s["by_diff"].get("expert", 0) >= 1),
    ("polyglot", "Polyglot", "Solve the same problem in Python and C++", "🌐",
     lambda s: s["both_langs"] >= 1),
    ("polyglot-10", "Bilingual", "Solve 10 problems in both languages", "🗣️",
     lambda s: s["both_langs"] >= 10),
    ("cpp-10", "Pointer Wrangler", "Solve 10 problems in C++", "⚡",
     lambda s: s["by_lang"].get("cpp", 0) >= 10),
    ("py-10", "Snake Charmer", "Solve 10 problems in Python", "🐍",
     lambda s: s["by_lang"].get("python", 0) >= 10),
    ("math-5", "Number Cruncher", "Solve 5 Math & Data problems", "🧮",
     lambda s: s["by_cat"].get("Math & Data", 0) >= 5),
    ("math-15", "Data Scientist", "Solve 15 Math & Data problems", "📊",
     lambda s: s["by_cat"].get("Math & Data", 0) >= 15),
    ("dp-5", "Memo Master", "Solve 5 Dynamic Programming problems", "🧠",
     lambda s: s["by_cat"].get("Dynamic Programming", 0) >= 5),
    ("graph-5", "Pathfinder", "Solve 5 Graph problems", "🗺️",
     lambda s: s["by_cat"].get("Graphs", 0) >= 5),
    ("lesson-1", "Student", "Complete your first lesson", "📘", lambda s: s["lessons"] >= 1),
    ("lessons-py", "Pythonista", "Complete every Python lesson", "📗",
     lambda s: s["lessons_total_python"] > 0 and s["lessons_python"] >= s["lessons_total_python"]),
    ("lessons-cpp", "C++ Scholar", "Complete every C++ lesson", "📕",
     lambda s: s["lessons_total_cpp"] > 0 and s["lessons_cpp"] >= s["lessons_total_cpp"]),
    ("streak-3", "On a Roll", "3-day streak", "📅", lambda s: s["best_streak"] >= 3),
    ("streak-7", "Week Warrior", "7-day streak", "🗓️", lambda s: s["best_streak"] >= 7),
    ("streak-30", "Unstoppable", "30-day streak", "🚀", lambda s: s["best_streak"] >= 30),
    ("goal", "Goal Getter", "Hit your daily coding-minutes goal", "⏱️", lambda s: s["goal_days"] >= 1),
    ("marathon", "Marathon", "Code for 60 minutes in one day", "🏃",
     lambda s: s["max_day_minutes"] >= 60),
    ("hours-10", "Ten Hours In", "10 hours of total coding time", "⌛",
     lambda s: s["total_minutes"] >= 600),
    ("night-owl", "Night Owl", "Solve a problem between midnight and 5am", "🦉",
     lambda s: s["night_solves"] >= 1),
    ("level-5", "Rising Star", "Reach level 5", "⭐", lambda s: s["level"] >= 5),
    ("level-10", "Legend", "Reach level 10", "🌟", lambda s: s["level"] >= 10),
]

BADGE_INDEX = {b[0]: b for b in BADGES}


def badge_info(badge_id):
    b = BADGE_INDEX[badge_id]
    return {"id": b[0], "name": b[1], "description": b[2], "icon": b[3]}


def earned_badges(stats):
    return [b[0] for b in BADGES if b[4](stats)]


def compute_streaks(days, today):
    """``days``: set of ordinal day numbers with activity. Returns (current, best).

    The current streak survives until the end of today: if you were active
    yesterday but not yet today, it is still alive.
    """
    if not days:
        return 0, 0
    ordered = sorted(days)
    best = run = 1
    for prev, cur in zip(ordered, ordered[1:]):
        run = run + 1 if cur == prev + 1 else 1
        best = max(best, run)
    current = 0
    start = today if today in days else today - 1
    while start in days:
        current += 1
        start -= 1
    return current, best
