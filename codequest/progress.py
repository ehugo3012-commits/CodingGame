"""Persistent learner progress: time tracking, attempts, XP, streaks, badges.

Everything lives in one SQLite file so it is trivial to back up
(``~/.codequest/progress.db`` in Termux, app-private storage in the APK).
"""

import datetime as dt
import json
import sqlite3
import threading
import time

from . import gamify

SCHEMA = """
CREATE TABLE IF NOT EXISTS activity (
    day INTEGER PRIMARY KEY,          -- local day number (days since epoch)
    seconds INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    problem_id TEXT NOT NULL,
    lang TEXT NOT NULL,
    ts REAL NOT NULL,
    day INTEGER NOT NULL,
    verdict TEXT NOT NULL,
    passed INTEGER NOT NULL,
    total INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS attempts_problem ON attempts(problem_id, lang);
CREATE TABLE IF NOT EXISTS solved (
    problem_id TEXT NOT NULL,
    lang TEXT NOT NULL,
    ts REAL NOT NULL,
    day INTEGER NOT NULL,
    hour INTEGER NOT NULL,
    xp INTEGER NOT NULL,
    hints_used INTEGER NOT NULL,
    failed_before INTEGER NOT NULL,
    PRIMARY KEY (problem_id, lang)
);
CREATE TABLE IF NOT EXISTS hints (
    problem_id TEXT NOT NULL,
    idx INTEGER NOT NULL,
    ts REAL NOT NULL,
    PRIMARY KEY (problem_id, idx)
);
CREATE TABLE IF NOT EXISTS lessons_done (
    lesson_id TEXT PRIMARY KEY,
    track TEXT NOT NULL,
    ts REAL NOT NULL,
    day INTEGER NOT NULL,
    xp INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS xp_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts REAL NOT NULL,
    day INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    reason TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS badges (
    badge_id TEXT PRIMARY KEY,
    ts REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS drafts (
    key TEXT PRIMARY KEY,
    code TEXT NOT NULL,
    ts REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""

DEFAULT_SETTINGS = {
    "tz_offset": 0,          # minutes, as reported by JS Date.getTimezoneOffset()
    "daily_goal": 20,        # minutes of coding per day
    "remote_judge": "",      # Termux judge URL used by the APK for C++
    "preferred_lang": "python",
    "font_size": 14,
}

MAX_HEARTBEAT = 120  # seconds credited per heartbeat at most


class ProgressStore:
    def __init__(self, path):
        self.path = str(path)
        self._lock = threading.RLock()
        self.db = sqlite3.connect(self.path, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        with self._lock:
            self.db.executescript(SCHEMA)
            self.db.commit()

    # ------------------------------------------------------------------ utils
    def _q(self, sql, args=()):
        with self._lock:
            return self.db.execute(sql, args).fetchall()

    def _one(self, sql, args=()):
        rows = self._q(sql, args)
        return rows[0] if rows else None

    def _scalar(self, sql, args=(), default=0):
        row = self._one(sql, args)
        return default if row is None or row[0] is None else row[0]

    def _local(self, ts=None):
        """Return (day_number, hour) in the learner's local time zone."""
        ts = time.time() if ts is None else ts
        local = ts - int(self.get_setting("tz_offset")) * 60
        return int(local // 86400), int((local % 86400) // 3600)

    def today(self):
        return self._local()[0]

    @staticmethod
    def day_to_date(day):
        return (dt.date(1970, 1, 1) + dt.timedelta(days=day)).isoformat()

    # --------------------------------------------------------------- settings
    def get_setting(self, key):
        row = self._one("SELECT value FROM settings WHERE key=?", (key,))
        if row is None:
            return DEFAULT_SETTINGS.get(key)
        return json.loads(row["value"])

    def settings(self):
        out = dict(DEFAULT_SETTINGS)
        for row in self._q("SELECT key, value FROM settings"):
            out[row["key"]] = json.loads(row["value"])
        return out

    def set_setting(self, key, value):
        if key not in DEFAULT_SETTINGS:
            raise KeyError(key)
        with self._lock:
            self.db.execute("INSERT OR REPLACE INTO settings(key, value) VALUES (?, ?)",
                            (key, json.dumps(value)))
            self.db.commit()

    # ----------------------------------------------------------- time tracking
    def add_activity(self, seconds, ts=None):
        seconds = max(0, min(int(seconds), MAX_HEARTBEAT))
        if not seconds:
            return
        day, _ = self._local(ts)
        with self._lock:
            self.db.execute(
                "INSERT INTO activity(day, seconds) VALUES (?, ?) "
                "ON CONFLICT(day) DO UPDATE SET seconds = seconds + excluded.seconds",
                (day, seconds))
            self.db.commit()

    def minutes_by_day(self, n_days=14):
        today = self.today()
        rows = {r["day"]: r["seconds"] for r in self._q(
            "SELECT day, seconds FROM activity WHERE day > ?", (today - n_days,))}
        return [{"date": self.day_to_date(d), "minutes": round(rows.get(d, 0) / 60, 1)}
                for d in range(today - n_days + 1, today + 1)]

    # ------------------------------------------------------------------ hints
    def hints_used(self, problem_id):
        return self._scalar("SELECT COUNT(*) FROM hints WHERE problem_id=?", (problem_id,))

    def reveal_hint(self, problem_id, idx):
        with self._lock:
            self.db.execute("INSERT OR IGNORE INTO hints(problem_id, idx, ts) VALUES (?, ?, ?)",
                            (problem_id, idx, time.time()))
            self.db.commit()
        return self.hints_used(problem_id)

    def revealed_hints(self, problem_id):
        return [r["idx"] for r in self._q(
            "SELECT idx FROM hints WHERE problem_id=? ORDER BY idx", (problem_id,))]

    # --------------------------------------------------------------- attempts
    def record_attempt(self, problem, lang, verdict, passed, total, catalog):
        """Log a submission; award XP + badges on a first solve.

        ``problem`` needs ``id``, ``difficulty``. Returns a dict describing
        what happened, for the UI's celebration screen.
        """
        now = time.time()
        day, hour = self._local(now)
        pid = problem["id"]
        with self._lock:
            self.db.execute(
                "INSERT INTO attempts(problem_id, lang, ts, day, verdict, passed, total) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)", (pid, lang, now, day, verdict, passed, total))
            self.db.commit()
            result = {"first_solve": False, "xp": 0, "new_badges": []}
            if verdict != "ok":
                return result
            if self._one("SELECT 1 FROM solved WHERE problem_id=? AND lang=?", (pid, lang)):
                return result
            other_lang = self._one("SELECT 1 FROM solved WHERE problem_id=?", (pid,)) is not None
            hints = self.hints_used(pid)
            failed = self._scalar(
                "SELECT COUNT(*) FROM attempts WHERE problem_id=? AND lang=? AND verdict!='ok'",
                (pid, lang))
            xp = gamify.problem_xp(problem["difficulty"], hints, second_language=other_lang)
            self.db.execute(
                "INSERT INTO solved(problem_id, lang, ts, day, hour, xp, hints_used, failed_before) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (pid, lang, now, day, hour, xp, hints, failed))
            self._log_xp(xp, f"solve:{pid}:{lang}", now, day)
            self.db.commit()
        result.update(first_solve=True, xp=xp)
        result["new_badges"] = self.update_badges(catalog)
        return result

    def _log_xp(self, amount, reason, ts, day):
        self.db.execute("INSERT INTO xp_log(ts, day, amount, reason) VALUES (?, ?, ?, ?)",
                        (ts, day, amount, reason))

    def complete_lesson(self, lesson_id, track, xp, catalog):
        now = time.time()
        day, _ = self._local(now)
        with self._lock:
            if self._one("SELECT 1 FROM lessons_done WHERE lesson_id=?", (lesson_id,)):
                return {"first_time": False, "xp": 0, "new_badges": []}
            self.db.execute(
                "INSERT INTO lessons_done(lesson_id, track, ts, day, xp) VALUES (?, ?, ?, ?, ?)",
                (lesson_id, track, now, day, xp))
            self._log_xp(xp, f"lesson:{lesson_id}", now, day)
            self.db.commit()
        return {"first_time": True, "xp": xp, "new_badges": self.update_badges(catalog)}

    def lessons_done(self):
        return {r["lesson_id"] for r in self._q("SELECT lesson_id FROM lessons_done")}

    def solved_map(self):
        """{problem_id: set(langs)}"""
        out = {}
        for r in self._q("SELECT problem_id, lang FROM solved"):
            out.setdefault(r["problem_id"], set()).add(r["lang"])
        return out

    def attempted_ids(self):
        return {r["problem_id"] for r in self._q("SELECT DISTINCT problem_id FROM attempts")}

    def problem_history(self, problem_id, limit=10):
        return [dict(r) for r in self._q(
            "SELECT lang, ts, verdict, passed, total FROM attempts WHERE problem_id=? "
            "ORDER BY id DESC LIMIT ?", (problem_id, limit))]

    # ------------------------------------------------------------------ drafts
    def get_draft(self, key):
        row = self._one("SELECT code FROM drafts WHERE key=?", (key,))
        return row["code"] if row else None

    def save_draft(self, key, code):
        with self._lock:
            self.db.execute("INSERT OR REPLACE INTO drafts(key, code, ts) VALUES (?, ?, ?)",
                            (key, code, time.time()))
            self.db.commit()

    # ------------------------------------------------------------ aggregates
    def total_xp(self):
        return self._scalar("SELECT SUM(amount) FROM xp_log")

    def streaks(self):
        days = {r["day"] for r in self._q("SELECT DISTINCT day FROM xp_log")}
        return gamify.compute_streaks(days, self.today())

    def badge_stats(self, catalog):
        solved_rows = self._q("SELECT problem_id, lang, hour, hints_used, failed_before FROM solved")
        solved_ids = {r["problem_id"] for r in solved_rows}
        by_lang, by_diff, by_cat = {}, {}, {}
        langs_per = {}
        for r in solved_rows:
            by_lang[r["lang"]] = by_lang.get(r["lang"], 0) + 1
            langs_per.setdefault(r["problem_id"], set()).add(r["lang"])
        for pid in solved_ids:
            meta = catalog.problem_meta(pid)
            if meta:
                by_diff[meta["difficulty"]] = by_diff.get(meta["difficulty"], 0) + 1
                by_cat[meta["category"]] = by_cat.get(meta["category"], 0) + 1
        lesson_rows = self._q("SELECT track, COUNT(*) AS n FROM lessons_done GROUP BY track")
        lessons_by_track = {r["track"]: r["n"] for r in lesson_rows}
        goal = int(self.get_setting("daily_goal")) * 60
        current, best = self.streaks()
        return {
            "solved": len(solved_ids),
            "clean_solves": sum(1 for r in solved_rows
                                if r["hints_used"] == 0 and r["failed_before"] == 0),
            "max_fails_before_solve": max([r["failed_before"] for r in solved_rows] or [0]),
            "by_lang": by_lang, "by_diff": by_diff, "by_cat": by_cat,
            "both_langs": sum(1 for v in langs_per.values() if len(v) > 1),
            "night_solves": sum(1 for r in solved_rows if 0 <= r["hour"] < 5),
            "lessons": sum(lessons_by_track.values()),
            "lessons_python": lessons_by_track.get("python", 0),
            "lessons_cpp": lessons_by_track.get("cpp", 0),
            "lessons_total_python": catalog.lesson_count("python"),
            "lessons_total_cpp": catalog.lesson_count("cpp"),
            "current_streak": current, "best_streak": best,
            "goal_days": self._scalar("SELECT COUNT(*) FROM activity WHERE seconds >= ?", (goal,)),
            "max_day_minutes": self._scalar("SELECT MAX(seconds) FROM activity") / 60,
            "total_minutes": self._scalar("SELECT SUM(seconds) FROM activity") / 60,
            "level": gamify.level_for(self.total_xp())["level"],
        }

    def update_badges(self, catalog):
        """Award any newly earned badges; return their info dicts."""
        stats = self.badge_stats(catalog)
        have = {r["badge_id"] for r in self._q("SELECT badge_id FROM badges")}
        new = [b for b in gamify.earned_badges(stats) if b not in have]
        if new:
            now = time.time()
            with self._lock:
                self.db.executemany("INSERT OR IGNORE INTO badges(badge_id, ts) VALUES (?, ?)",
                                    [(b, now) for b in new])
                self.db.commit()
        return [gamify.badge_info(b) for b in new]

    def profile(self, catalog):
        stats = self.badge_stats(catalog)
        xp = self.total_xp()
        earned = {r["badge_id"]: r["ts"] for r in self._q("SELECT badge_id, ts FROM badges")}
        attempts = self._scalar("SELECT COUNT(*) FROM attempts")
        failed = self._scalar("SELECT COUNT(*) FROM attempts WHERE verdict != 'ok'")
        today = self.today()
        today_seconds = self._scalar("SELECT seconds FROM activity WHERE day=?", (today,))
        recent = [dict(r) for r in self._q(
            "SELECT problem_id, lang, ts, verdict, passed, total FROM attempts "
            "ORDER BY id DESC LIMIT 15")]
        for r in recent:
            meta = catalog.problem_meta(r["problem_id"])
            r["title"] = meta["title"] if meta else r["problem_id"]
        return {
            "level": gamify.level_for(xp),
            "streak": {"current": stats["current_streak"], "best": stats["best_streak"],
                       "active_today": self._one("SELECT 1 FROM xp_log WHERE day=?", (today,)) is not None},
            "time": {"today_minutes": round(today_seconds / 60, 1),
                     "goal_minutes": int(self.get_setting("daily_goal")),
                     "total_minutes": round(stats["total_minutes"], 1),
                     "days": self.minutes_by_day(14)},
            "problems": {"solved": stats["solved"], "attempts": attempts, "failed_attempts": failed,
                         "by_difficulty": stats["by_diff"], "by_language": stats["by_lang"],
                         "by_category": stats["by_cat"], "total": catalog.problem_count()},
            "lessons": {"done": stats["lessons"],
                        "python": [stats["lessons_python"], stats["lessons_total_python"]],
                        "cpp": [stats["lessons_cpp"], stats["lessons_total_cpp"]]},
            "badges": [dict(gamify.badge_info(b[0]), earned_at=earned.get(b[0]))
                       for b in gamify.BADGES],
            "recent": recent,
        }

    def export(self):
        tables = ["activity", "attempts", "solved", "hints", "lessons_done",
                  "xp_log", "badges", "settings"]
        return {t: [dict(r) for r in self._q(f"SELECT * FROM {t}")] for t in tables}
