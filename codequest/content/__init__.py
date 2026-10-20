'''Source of truth for the lesson & problem library.

Content is authored as plain Python so tests can be *generated* and every
reference solution is executed at build time. Run::

    python tools/build_content.py

to validate everything and regenerate ``codequest/data/*.json`` (which is what
the app actually loads; the JSON is committed so no build step is needed to
run the app).

Problems  (``content/problems/*.py`` each define ``PROBLEMS = [dict, ...]``)
---------------------------------------------------------------------------
Every problem is stdin -> stdout, so one problem serves both language tracks.

Required keys
    id              unique kebab-case slug, e.g. "two-sum"
    title           "Two Sum"
    difficulty      beginner | easy | medium | hard | expert
    category        e.g. "Basics", "Strings", "Arrays", "Hashing", "Math",
                    "Sorting & Searching", "Two Pointers", "Recursion",
                    "Dynamic Programming", "Graphs", "Greedy",
                    "Bit Manipulation", "Number Theory", "Math & Data"
    statement       Markdown. Original wording (inspired by, never copied from,
                    other platforms).
    input_format    Markdown
    output_format   Markdown
    hints           list[str], ordered from gentle nudge to strong nudge. Hints
                    teach the syntax/idea needed but never give the full answer.
    samples         list[str] of stdin strings shown to the learner (1-3)
    solution_python reference solution (reads stdin, writes stdout)

Optional keys
    tests           list[str] hidden stdin strings
    gen             callable(rng: random.Random) -> list[str]  more hidden tests
                    (rng is seeded from the id, so builds are reproducible)
    solution_cpp    C++17 reference. If present the problem appears in the C++
                    track and must agree with the Python reference on every test.
    starter_python  starter code (defaults to a generic template)
    starter_cpp     starter code (defaults to a generic template)
    checker         tokens (default) | exact | tokens_ci | float | unordered | sympy
    time_limit      seconds per test (default 2.0). Size tests so the Python
                    reference runs well under a quarter of this on a desktop.
    tags            list[str]
    inspired_by     e.g. "LeetCode #1 Two Sum", "Project Euler #1"
    languages       override, e.g. ["python"] for SymPy/NumPy problems

Lessons  (``content/lessons/*.py`` each define ``LESSONS = [dict, ...]``)
------------------------------------------------------------------------
    id, track ("python" | "cpp"), unit, title, summary (one line),
    body        Markdown: short paragraphs, ```lang fenced snippets, lists
    examples    list of {"title", "code", "stdin"?, "explain"?} - runnable;
                each must run without error (output is captured at build)
    challenge   optional {"prompt", "starter", "solution", "samples",
                "tests"?, "checker"?} - a tiny judged exercise

Files are processed in filename order, so prefix them (``python_01_basics.py``).
'''

PY_STARTER = """import sys

def main():
    data = sys.stdin.read().split()
    # TODO: solve the problem and print the answer
    print()

main()
"""

CPP_STARTER = """#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    // TODO: read input, solve, print the answer
    return 0;
}
"""
