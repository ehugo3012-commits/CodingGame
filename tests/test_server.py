"""End-to-end API tests against a real server on a random port."""

import http.client
import json
import tempfile
import threading
import unittest
from pathlib import Path

from codequest import config
from codequest.catalog import Catalog
from codequest.server import make_server


class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.httpd, cls.app = make_server("127.0.0.1", 0, db_path=Path(cls.tmp.name) / "t.db")
        cls.port = cls.httpd.server_address[1]
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()
        cls.catalog = Catalog()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.app.store.db.close()
        cls.tmp.cleanup()

    def req(self, method, path, body=None, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=60)
        hdrs = {"X-TZ-Offset": "0"}
        if body is not None:
            hdrs["Content-Type"] = "application/json"
        hdrs.update(headers or {})
        conn.request(method, path, json.dumps(body) if body is not None else None, hdrs)
        resp = conn.getresponse()
        raw = resp.read()
        conn.close()
        try:
            return resp.status, json.loads(raw)
        except ValueError:
            return resp.status, raw

    def test_static_index(self):
        status, body = self.req("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn(b"CodeQuest", body)
        status, _ = self.req("GET", "/../config.py")
        self.assertEqual(status, 404)

    def test_health_and_home(self):
        status, h = self.req("GET", "/api/health")
        self.assertEqual(status, 200)
        self.assertGreater(h["counts"]["problems"], 0)
        status, home = self.req("GET", "/api/home")
        self.assertEqual(status, 200)
        self.assertIn("level", home)

    def test_hidden_data_never_leaks(self):
        _, lst = self.req("GET", "/api/problems")
        pid = lst["problems"][0]["id"]
        _, p = self.req("GET", f"/api/problems/{pid}")
        self.assertNotIn("tests", p)
        self.assertNotIn("solution", p)  # unsolved
        self.assertEqual(p["hints"], [])

    def test_hints_are_progressive(self):
        p = next(p for p in self.catalog.problems if len(p["hints"]) >= 2)
        _, h1 = self.req("POST", f"/api/problems/{p['id']}/hint", {})
        _, h2 = self.req("POST", f"/api/problems/{p['id']}/hint", {})
        self.assertEqual((h1["index"], h2["index"]), (0, 1))
        self.assertEqual(h1["hint"], p["hints"][0])
        self.assertLess(h2["xp_now"], h1["xp_now"] + 1)

    def test_submit_reference_solution_is_accepted(self):
        p = self.catalog.problem("sum-of-two")
        status, res = self.req("POST", "/api/problems/sum-of-two/submit",
                               {"lang": "python", "code": p["solution"]["python"]})
        self.assertEqual(status, 200)
        self.assertEqual(res["verdict"], "ok")
        self.assertEqual(res["passed"], res["total"])
        hidden = [t for t in res["tests"] if t["kind"] == "hidden"]
        self.assertTrue(hidden)
        self.assertTrue(all("input" not in t and "expected" not in t for t in hidden))
        self.assertIn("solution", res)
        _, again = self.req("POST", "/api/problems/sum-of-two/submit",
                            {"lang": "python", "code": p["solution"]["python"]})
        self.assertFalse(again["reward"]["first_solve"])

    def test_wrong_answer(self):
        _, res = self.req("POST", "/api/problems/fizzbuzz/submit", {"lang": "python", "code": "print(1)"})
        self.assertEqual(res["verdict"], "wrong")
        self.assertFalse(res["reward"]["first_solve"])

    @unittest.skipUnless(config.cxx_compiler(), "no C++ compiler")
    def test_cpp_submit(self):
        p = self.catalog.problem("fizzbuzz")
        _, res = self.req("POST", "/api/problems/fizzbuzz/submit", {"lang": "cpp", "code": p["solution"]["cpp"]})
        self.assertEqual(res["verdict"], "ok")

    def test_run_samples_and_custom(self):
        _, res = self.req("POST", "/api/problems/sum-of-two/run", {"lang": "python", "code": "print(5)"})
        self.assertEqual(res["tests"][0]["verdict"], "ok")
        _, res = self.req("POST", "/api/problems/sum-of-two/run",
                          {"lang": "python", "code": "print(input()[::-1])", "stdin": "abc"})
        self.assertEqual(res["stdout"], "cba\n")

    def test_playground_and_drafts(self):
        _, res = self.req("POST", "/api/run", {"lang": "python", "code": "print(6*7)", "stdin": ""})
        self.assertEqual(res["stdout"], "42\n")
        _, d = self.req("GET", "/api/drafts?key=playground:python")
        self.assertEqual(d["code"], "print(6*7)")

    def test_lesson_flow(self):
        _, lessons = self.req("GET", "/api/lessons?track=python")
        lid = lessons["units"][0]["lessons"][0]["id"]
        _, l = self.req("GET", f"/api/lessons/{lid}")
        self.assertIn("body", l)
        if l["challenge"]:
            self.assertNotIn("tests", l["challenge"])
            sol = self.catalog.lesson(lid)["challenge"]["solution"]
            _, res = self.req("POST", f"/api/lessons/{lid}/challenge", {"code": sol, "mode": "submit"})
            self.assertEqual(res["verdict"], "ok")
            self.assertTrue(res["reward"]["first_time"])

    def test_heartbeat_and_profile(self):
        self.req("POST", "/api/heartbeat", {"seconds": 30})
        _, prof = self.req("GET", "/api/profile")
        self.assertGreaterEqual(prof["time"]["today_minutes"], 0.5)

    def test_settings(self):
        status, _ = self.req("POST", "/api/settings", {"remote_judge": "javascript:alert(1)"})
        self.assertEqual(status, 400)
        status, s = self.req("POST", "/api/settings", {"daily_goal": 45})
        self.assertEqual((status, s["daily_goal"]), (200, 45))

    def test_cross_site_protection(self):
        status, _ = self.req("GET", "/api/health", headers={"Host": "evil.example"})
        self.assertEqual(status, 403)
        status, _ = self.req("POST", "/api/run", {"lang": "python", "code": "print(1)"},
                             headers={"Origin": "https://evil.example"})
        self.assertEqual(status, 403)
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        conn.request("POST", "/api/run", '{"lang":"python","code":"print(1)"}', {"Content-Type": "text/plain"})
        self.assertEqual(conn.getresponse().status, 415)
        conn.close()

    def test_raw_run(self):
        _, res = self.req("POST", "/api/raw-run",
                          {"lang": "python", "code": "print(input())", "inputs": ["a", "b"]})
        self.assertEqual([r["stdout"] for r in res["results"]], ["a\n", "b\n"])


if __name__ == "__main__":
    unittest.main()
