"""Read-only access to the built lesson & problem library (``data/*.json``).

The JSON is produced by ``tools/build_content.py`` from the Python sources in
``codequest/content``. Hidden tests and reference solutions never leave the
server unless the learner has earned them (solutions unlock after a solve).
"""

import json

from . import config, gamify

DIFF_ORDER = {d: i for i, d in enumerate(gamify.DIFFICULTIES)}


class Catalog:
    def __init__(self, data_dir=config.DATA_DIR):
        self.problems = self._load(data_dir / "problems.json")
        self.lessons = self._load(data_dir / "lessons.json")
        self.problems.sort(key=lambda p: (DIFF_ORDER.get(p["difficulty"], 9), p.get("order", 0)))
        self._pindex = {p["id"]: p for p in self.problems}
        self._lindex = {l["id"]: l for l in self.lessons}

    @staticmethod
    def _load(path):
        if not path.exists():
            return []
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)

    # --- used by ProgressStore for badge stats
    def problem_meta(self, pid):
        return self._pindex.get(pid)

    def problem_count(self):
        return len(self.problems)

    def lesson_count(self, track):
        return sum(1 for l in self.lessons if l["track"] == track)

    # --- problems
    def problem(self, pid):
        return self._pindex.get(pid)

    def categories(self):
        seen = []
        for p in self.problems:
            if p["category"] not in seen:
                seen.append(p["category"])
        return sorted(seen, key=lambda c: (c == "Math & Data", c))

    @staticmethod
    def problem_summary(p):
        return {k: p[k] for k in ("id", "title", "difficulty", "category", "languages",
                                  "tags", "inspired_by")} | {
            "xp": gamify.BASE_XP.get(p["difficulty"], 10), "hint_count": len(p["hints"])}

    @staticmethod
    def problem_public(p):
        out = {k: p[k] for k in ("id", "title", "difficulty", "category", "languages", "tags",
                                 "inspired_by", "statement", "input_format", "output_format",
                                 "starter", "samples", "checker", "time_limit")}
        out["hint_count"] = len(p["hints"])
        out["hidden_test_count"] = len(p["tests"])
        out["xp"] = gamify.BASE_XP.get(p["difficulty"], 10)
        return out

    # --- lessons
    def lesson(self, lid):
        return self._lindex.get(lid)

    def lesson_list(self, track):
        return [l for l in self.lessons if l["track"] == track]

    @staticmethod
    def lesson_summary(l):
        return {k: l[k] for k in ("id", "track", "unit", "title", "summary")} | {
            "has_challenge": bool(l.get("challenge"))}

    @staticmethod
    def lesson_public(l):
        out = {k: l[k] for k in ("id", "track", "unit", "title", "summary", "body", "examples")}
        ch = l.get("challenge")
        if ch:
            out["challenge"] = {k: ch[k] for k in ("prompt", "starter", "samples", "checker")}
            out["challenge"]["hidden_test_count"] = len(ch["tests"])
        else:
            out["challenge"] = None
        return out
