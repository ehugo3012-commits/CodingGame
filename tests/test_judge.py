import unittest

from codequest import config, judge
from codequest.judge import checkers, python_runner

ADD = "a, b = map(int, input().split())\nprint(a + b)\n"
CPP_ADD = "#include <iostream>\nint main(){long long a,b;std::cin>>a>>b;std::cout<<a+b<<'\\n';}\n"


class PythonRunnerTests(unittest.TestCase):
    def run_py(self, code, inputs, tl=2.0):
        return judge.execute("python", code, inputs, tl)

    def test_basic_io(self):
        res = self.run_py(ADD, ["1 2\n", "10 -3\n"])
        self.assertEqual([r["stdout"] for r in res], ["3\n", "7\n"])
        self.assertTrue(all(r["status"] == "ok" for r in res))

    def test_stdin_idioms(self):
        code = "import sys\nprint(sum(map(int, sys.stdin.read().split())))\n"
        self.assertEqual(self.run_py(code, ["1 2\n3\n"])[0]["stdout"], "6\n")
        code = "print(sum(map(int, open(0).read().split())))\n"
        self.assertEqual(self.run_py(code, ["4 5\n"])[0]["stdout"], "9\n")
        code = "import sys\nfor line in sys.stdin:\n    print(line.strip()[::-1])\n"
        self.assertEqual(self.run_py(code, ["ab\ncd\n"])[0]["stdout"], "ba\ndc\n")

    def test_fresh_globals_per_test(self):
        code = "try:\n    seen\nexcept NameError:\n    seen = 0\nseen += 1\nprint(seen)\n"
        self.assertEqual([r["stdout"] for r in self.run_py(code, ["", ""])], ["1\n", "1\n"])

    def test_syntax_error(self):
        res = self.run_py("print(1\n", ["", ""])
        self.assertEqual({r["status"] for r in res}, {"compile_error"})
        self.assertIn("SyntaxError", res[0]["error"])

    def test_runtime_error_traceback_is_user_only(self):
        res = self.run_py("def f():\n    return 1 // 0\nf()\n", [""])[0]
        self.assertEqual(res["status"], "error")
        self.assertIn("ZeroDivisionError", res["error"])
        self.assertIn("solution.py, line 2", res["error"])
        self.assertNotIn("py_harness", res["error"])

    def test_timeout_then_continues(self):
        code = "x = input()\nif x == 'loop':\n    while True: pass\nprint(x)\n"
        res = self.run_py(code, ["loop\n", "ok\n"], tl=0.5)
        self.assertEqual(res[0]["status"], "timeout")
        self.assertEqual((res[1]["status"], res[1]["stdout"]), ("ok", "ok\n"))

    def test_timeout_in_c_code(self):
        res = self.run_py("import time\ntime.sleep(30)\n", ["", ""], tl=0.5)
        self.assertEqual([r["status"] for r in res], ["timeout", "timeout"])

    def test_bare_except_cannot_swallow_timeout(self):
        code = "while True:\n    try:\n        pass\n    except Exception:\n        pass\n"
        self.assertEqual(self.run_py(code, [""], tl=0.5)[0]["status"], "timeout")

    def test_output_limit(self):
        res = self.run_py("while True:\n    print('x' * 1000)\n", [""])[0]
        self.assertEqual(res["status"], "output_limit")

    def test_deep_recursion(self):
        code = "import sys\ndef f(n): return 0 if n == 0 else 1 + f(n - 1)\nprint(f(20000))\n"
        self.assertEqual(self.run_py(code, [""])[0]["stdout"], "20000\n")

    def test_system_exit_zero_is_fine(self):
        res = self.run_py("print('a')\nexit()\nprint('b')\n", [""])[0]
        self.assertEqual((res["status"], res["stdout"]), ("ok", "a\n"))

    def test_inprocess_mode(self):
        res = python_runner._run_inprocess(ADD, ["2 2\n"], 2.0)
        self.assertEqual(res[0]["stdout"], "4\n")
        res = python_runner._run_inprocess("while True: pass\n", [""], 0.3)
        self.assertEqual(res[0]["status"], "timeout")


@unittest.skipUnless(config.cxx_compiler(), "no C++ compiler")
class CppRunnerTests(unittest.TestCase):
    def test_compile_and_run(self):
        res = judge.execute("cpp", CPP_ADD, ["1 2\n", "5 5\n"])
        self.assertEqual([r["stdout"] for r in res], ["3\n", "10\n"])

    def test_bits_stdcpp_shim(self):
        code = "#include <bits/stdc++.h>\nusing namespace std;\nint main(){vector<int> v{3,1,2};sort(v.begin(),v.end());cout<<v[0];}\n"
        self.assertEqual(judge.execute("cpp", code, [""])[0]["stdout"], "1")

    def test_compile_error(self):
        res = judge.execute("cpp", "int main() { return x; }", ["", ""])
        self.assertEqual({r["status"] for r in res}, {"compile_error"})
        self.assertIn("solution.cpp", res[0]["error"])

    def test_timeout(self):
        code = "#include <iostream>\nint main(){volatile long long i=0; while(true) i++;}\n"
        self.assertEqual(judge.execute("cpp", code, [""], 0.5)[0]["status"], "timeout")

    def test_segfault(self):
        code = ("#include <vector>\n#include <iostream>\nint main(){std::vector<int>*p=nullptr;"
                "volatile int k=0; std::cout<<(*p)[k];}\n")
        res = judge.execute("cpp", code, [""])[0]
        self.assertEqual(res["status"], "error")

    def test_nonzero_exit(self):
        self.assertEqual(judge.execute("cpp", "int main(){return 3;}", [""])[0]["status"], "error")


class CheckerTests(unittest.TestCase):
    def test_tokens(self):
        self.assertTrue(checkers.check("tokens", "1 2\n3\n", "1\n2 3"))
        self.assertFalse(checkers.check("tokens", "1 2", "1 3"))

    def test_exact(self):
        self.assertTrue(checkers.check("exact", "a\n b\n", "a  \n b\n\n"))
        self.assertFalse(checkers.check("exact", "a\n b\n", "a\nb\n"))

    def test_float(self):
        self.assertTrue(checkers.check("float", "0.3333333", "0.33333331"))
        self.assertTrue(checkers.check("float", "x 1.5", "x 1.5000000001"))
        self.assertFalse(checkers.check("float", "1.5", "1.6"))
        self.assertTrue(checkers.check("float", "0.0", "-0.0"))

    def test_unordered(self):
        self.assertTrue(checkers.check("unordered", "a\nb\n", "b\na\n"))
        self.assertFalse(checkers.check("unordered", "a\nb\n", "a\na\n"))

    def test_tokens_ci(self):
        self.assertTrue(checkers.check("tokens_ci", "YES", "yes"))

    @unittest.skipUnless(config.has_module("sympy"), "no sympy")
    def test_sympy(self):
        self.assertTrue(checkers.check("sympy", "2*x + 1", "1 + 2*x"))
        self.assertTrue(checkers.check("sympy", "(x+1)**2", "x**2 + 2*x + 1"))
        self.assertTrue(checkers.check("sympy", "x^2", "x**2"))
        self.assertFalse(checkers.check("sympy", "x**2", "x**3"))
        self.assertFalse(checkers.check("sympy", "x", "this is not ) valid"))

    def test_grade(self):
        raw = [{"status": "ok", "stdout": "3\n", "stderr": "", "error": "", "time": 0},
               {"status": "ok", "stdout": "4\n", "stderr": "", "error": "", "time": 0}]
        overall, graded = judge.grade(raw, ["3", "5"])
        self.assertEqual(overall, "wrong")
        self.assertEqual([g["verdict"] for g in graded], ["ok", "wrong"])


if __name__ == "__main__":
    unittest.main()
