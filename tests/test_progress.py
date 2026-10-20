import tempfile
import unittest
from pathlib import Path
from unittest import mock

from codequest import gamify
from codequest.progress import ProgressStore


class FakeCatalog:
    def __init__(self):
        self.meta = {
            "p1": {"id": "p1", "title": "P1", "difficulty": "easy", "category": "Basics"},
            "p2": {"id": "p2", "title": "P2", "difficulty": "hard", "category": "Math & Data"},
        }

    def problem_meta(self, pid):
        return self.meta.get(pid)

    def problem_count(self):
        return len(self.meta)

    def lesson_count(self, track):
        return 2


DAY = 86400


class ProgressTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = ProgressStore(Path(self.tmp.name) / "p.db")
        self.cat = FakeCatalog()

    def tearDown(self):
        self.store.db.close()
        self.tmp.cleanup()

    def test_first_solve_awards_xp_once(self):
        p = self.cat.meta["p1"]
        r = self.store.record_attempt(p, "python", "wrong", 1, 5, self.cat)
        self.assertFalse(r["first_solve"])
        r = self.store.record_attempt(p, "python", "ok", 5, 5, self.cat)
        self.assertTrue(r["first_solve"])
        self.assertEqual(r["xp"], gamify.BASE_XP["easy"])
        self.assertIn("first-solve", [b["id"] for b in r["new_badges"]])
        r = self.store.record_attempt(p, "python", "ok", 5, 5, self.cat)
        self.assertFalse(r["first_solve"])
        self.assertEqual(self.store.total_xp(), gamify.BASE_XP["easy"])

    def test_hints_reduce_xp_and_second_language_is_half(self):
        p = self.cat.meta["p2"]
        self.store.reveal_hint("p2", 0)
        self.store.reveal_hint("p2", 1)
        self.store.reveal_hint("p2", 1)  # idempotent
        self.assertEqual(self.store.hints_used("p2"), 2)
        r = self.store.record_attempt(p, "cpp", "ok", 3, 3, self.cat)
        self.assertEqual(r["xp"], gamify.problem_xp("hard", 2))
        r = self.store.record_attempt(p, "python", "ok", 3, 3, self.cat)
        self.assertEqual(r["xp"], gamify.problem_xp("hard", 2, second_language=True))
        self.assertIn("polyglot", [b["id"] for b in r["new_badges"]])

    def test_hint_floor(self):
        self.assertEqual(gamify.problem_xp("medium", 10), round(40 * gamify.MIN_XP_FACTOR))

    def test_lesson_completion(self):
        r = self.store.complete_lesson("py-hello", "python", 15, self.cat)
        self.assertTrue(r["first_time"])
        self.assertEqual(self.store.complete_lesson("py-hello", "python", 15, self.cat)["xp"], 0)
        self.assertEqual(self.store.total_xp(), 15)

    def test_activity_and_timezone(self):
        base = 1_700_000_000 - (1_700_000_000 % DAY)  # UTC midnight
        self.store.set_setting("tz_offset", -120)  # UTC+2
        # 23:00 UTC is already the next day at UTC+2
        self.store.add_activity(60, ts=base + 23 * 3600)
        day = self.store._local(base + 23 * 3600)[0]
        self.assertEqual(day, base // DAY + 1)
        self.store.add_activity(9999, ts=base + 23 * 3600)  # capped
        rows = self.store._q("SELECT seconds FROM activity WHERE day=?", (day,))
        self.assertEqual(rows[0]["seconds"], 60 + 120)

    def test_streaks(self):
        self.assertEqual(gamify.compute_streaks(set(), 10), (0, 0))
        self.assertEqual(gamify.compute_streaks({8, 9, 10}, 10), (3, 3))
        self.assertEqual(gamify.compute_streaks({8, 9}, 10), (2, 2))  # alive until today ends
        self.assertEqual(gamify.compute_streaks({1, 2, 3, 4, 8}, 10), (0, 4))

    def test_streak_from_xp_days(self):
        p = self.cat.meta["p1"]
        with mock.patch("time.time", return_value=1_700_000_000):
            self.store.record_attempt(p, "python", "ok", 1, 1, self.cat)
        with mock.patch("time.time", return_value=1_700_000_000 + DAY):
            self.store.complete_lesson("x", "python", 5, self.cat)
            self.assertEqual(self.store.streaks(), (2, 2))

    def test_levels(self):
        self.assertEqual(gamify.level_for(0)["level"], 1)
        self.assertEqual(gamify.level_for(99)["level"], 1)
        self.assertEqual(gamify.level_for(100)["level"], 2)
        self.assertEqual(gamify.level_for(250)["level"], 3)
        info = gamify.level_for(175)
        self.assertAlmostEqual(info["progress"], 0.5)

    def test_profile_shape(self):
        self.store.record_attempt(self.cat.meta["p1"], "python", "ok", 1, 1, self.cat)
        prof = self.store.profile(self.cat)
        self.assertEqual(prof["problems"]["solved"], 1)
        self.assertEqual(len(prof["time"]["days"]), 14)
        self.assertEqual(len(prof["badges"]), len(gamify.BADGES))
        self.assertEqual(prof["recent"][0]["title"], "P1")

    def test_settings_validation(self):
        with self.assertRaises(KeyError):
            self.store.set_setting("nope", 1)
        self.store.set_setting("daily_goal", 30)
        self.assertEqual(self.store.settings()["daily_goal"], 30)


if __name__ == "__main__":
    unittest.main()
