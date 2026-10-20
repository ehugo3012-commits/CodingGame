"""Sanity checks on the built library (codequest/data/*.json)."""

import unittest

from codequest import gamify
from codequest.catalog import Catalog
from codequest.judge import checkers


class ContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cat = Catalog()

    def test_problems_well_formed(self):
        ids = set()
        for p in self.cat.problems:
            with self.subTest(p=p["id"]):
                self.assertNotIn(p["id"], ids)
                ids.add(p["id"])
                self.assertIn(p["difficulty"], gamify.DIFFICULTIES)
                self.assertIn(p["checker"], checkers.CHECKERS)
                self.assertTrue(p["hints"])
                self.assertTrue(p["samples"])
                self.assertTrue(set(p["languages"]) <= {"python", "cpp"})
                for lang in p["languages"]:
                    self.assertIn(lang, p["starter"])
                    self.assertIn(lang, p["solution"])
                for t in p["samples"] + p["tests"]:
                    self.assertTrue(t["output"].strip(), "every test needs an expected output")

    def test_math_and_data_is_python(self):
        for p in self.cat.problems:
            if p["category"] == "Math & Data":
                self.assertEqual(p["languages"], ["python"], p["id"])

    def test_lessons_well_formed(self):
        ids = set()
        for l in self.cat.lessons:
            with self.subTest(l=l["id"]):
                self.assertNotIn(l["id"], ids)
                ids.add(l["id"])
                self.assertIn(l["track"], ("python", "cpp"))
                self.assertTrue(l["body"])


if __name__ == "__main__":
    unittest.main()
