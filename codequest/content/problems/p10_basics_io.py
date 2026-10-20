"""Beginner basics: input/output, arithmetic and simple conditionals."""


def _lines(t, make):
    return f"{t}\n" + "\n".join(make() for _ in range(t))


PROBLEMS = [
    dict(
        id="rectangle-area-perimeter",
        title="Rectangle Area & Perimeter",
        difficulty="beginner",
        category="Basics",
        tags=["arithmetic", "input"],
        inspired_by="Classic beginner exercise (HackerRank / Kattis style)",
        statement="""
A farmer wants to fence a rectangular field that is `w` metres wide and `h`
metres long. She needs to know two things:

* the **area** of the field (`w · h`), to order seeds, and
* the **perimeter** (`2 · (w + h)`), to order fence.

Print both.
""",
        input_format="One line with two integers `w` and `h` (1 ≤ w, h ≤ 10⁹).",
        output_format="One line with two integers separated by a space: the area, then the perimeter.",
        hints=[
            "Read both numbers from one line: Python `w, h = map(int, input().split())`; C++ `cin >> w >> h;`.",
            "Print two values on one line: Python `print(a, b)` puts a space between them; C++ `cout << a << \" \" << b;`.",
            "C++: the area can be as big as 10¹⁸, which does not fit in `int` (max ≈ 2.1·10⁹). Use `long long`.",
        ],
        samples=["3 4", "10 1"],
        tests=["1 1", "1000000000 1000000000", "1 1000000000", "999999937 2"],
        gen=lambda rng: [f"{rng.randint(1, 10**9)} {rng.randint(1, 10**9)}" for _ in range(5)],
        starter_python=r"""w, h = map(int, input().split())
# TODO: compute the area and the perimeter, then print them on one line
""",
        starter_cpp=r"""#include <iostream>
using namespace std;

int main() {
    long long w, h;
    cin >> w >> h;
    // TODO: compute the area and the perimeter, then print them on one line
    return 0;
}
""",
        solution_python=r"""w, h = map(int, input().split())
print(w * h, 2 * (w + h))
""",
        solution_cpp=r"""#include <iostream>
using namespace std;

int main() {
    long long w, h;
    cin >> w >> h;
    cout << w * h << " " << 2 * (w + h) << "\n";
    return 0;
}
""",
    ),
    dict(
        id="even-or-odd",
        title="Even or Odd?",
        difficulty="beginner",
        category="Basics",
        tags=["conditionals", "modulo"],
        inspired_by="Classic beginner exercise (HackerRank 'Python If-Else')",
        statement="""
For each given integer decide whether it is **even** or **odd**.

Careful: the numbers can be negative, and zero is even.
""",
        input_format="First line: `t` (1 ≤ t ≤ 100). Then `t` lines, each with one integer `x` (−10⁹ ≤ x ≤ 10⁹).",
        output_format="For each `x` print `EVEN` or `ODD` on its own line.",
        hints=[
            "A number is even exactly when the remainder after dividing by 2 is zero: `x % 2 == 0`.",
            "Use `if ... else ...` to choose between the two words.",
            "C++ gotcha: `-3 % 2` is `-1` in C++ (but `1` in Python). Testing `x % 2 == 0` works in both languages; testing `x % 2 == 1` does not!",
        ],
        samples=["3\n4\n7\n0"],
        tests=["1\n-3", "1\n-8", "4\n1000000000\n-1000000000\n999999999\n-999999999", "2\n1\n2"],
        gen=lambda rng: [_lines(30, lambda: str(rng.randint(-10**9, 10**9))) for _ in range(3)],
        starter_python=r"""t = int(input())
for _ in range(t):
    x = int(input())
    # TODO: print EVEN or ODD
""",
        starter_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long x;
        cin >> x;
        // TODO: print EVEN or ODD
    }
    return 0;
}
""",
        solution_python=r"""t = int(input())
for _ in range(t):
    x = int(input())
    print("EVEN" if x % 2 == 0 else "ODD")
""",
        solution_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long x;
        cin >> x;
        cout << (x % 2 == 0 ? "EVEN" : "ODD") << "\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="max-of-three",
        title="Largest of Three",
        difficulty="beginner",
        category="Basics",
        tags=["conditionals", "comparison"],
        inspired_by="Classic beginner exercise",
        statement="""
Three friends compare their scores from a game. Given the three scores, print
the highest one. Scores can be negative (it is a strange game).
""",
        input_format="First line: `t` (1 ≤ t ≤ 100). Then `t` lines, each with three integers `a b c` (−10⁹ ≤ a, b, c ≤ 10⁹).",
        output_format="For each test case print the largest of the three numbers on its own line.",
        hints=[
            "Start with `best = a`, then compare: if `b > best` replace `best` with `b`; do the same with `c`.",
            "Python has a built-in: `max(a, b, c)`.",
            "C++: `max(a, max(b, c))` works with `#include <algorithm>`; so does `max({a, b, c})`.",
        ],
        samples=["2\n1 5 3\n-4 -2 -9"],
        tests=["1\n7 7 7", "3\n0 0 -1\n-1000000000 -1000000000 -1000000000\n1000000000 -1000000000 0",
               "3\n3 2 1\n1 2 3\n2 3 1"],
        gen=lambda rng: [_lines(25, lambda: " ".join(str(rng.randint(-10**9, 10**9)) for _ in range(3))),
                         _lines(25, lambda: " ".join(str(rng.randint(-3, 3)) for _ in range(3)))],
        starter_python=r"""t = int(input())
for _ in range(t):
    a, b, c = map(int, input().split())
    # TODO: print the largest of a, b, c
""",
        starter_cpp=r"""#include <iostream>
#include <algorithm>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long a, b, c;
        cin >> a >> b >> c;
        // TODO: print the largest of a, b, c
    }
    return 0;
}
""",
        solution_python=r"""t = int(input())
for _ in range(t):
    a, b, c = map(int, input().split())
    print(max(a, b, c))
""",
        solution_cpp=r"""#include <iostream>
#include <algorithm>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long a, b, c;
        cin >> a >> b >> c;
        cout << max(a, max(b, c)) << "\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="letter-grade",
        title="Letter Grade",
        difficulty="beginner",
        category="Basics",
        tags=["conditionals", "if-elif"],
        inspired_by="Classic beginner exercise (HackerRank 'Grading Students' theme)",
        statement="""
A teacher converts exam scores to letter grades using this table:

| Score    | Grade |
|----------|-------|
| 90 – 100 | `A`   |
| 80 – 89  | `B`   |
| 70 – 79  | `C`   |
| 60 – 69  | `D`   |
| 0 – 59   | `F`   |

Convert every score.
""",
        input_format="First line: `t` (1 ≤ t ≤ 101). Then `t` lines, each with one integer score `s` (0 ≤ s ≤ 100).",
        output_format="For each score print its letter grade on its own line.",
        hints=[
            "Use a chain of conditions: Python `if / elif / else`, C++ `if / else if / else`.",
            "Check from the top down: if `s >= 90` it's an A; otherwise, if `s >= 80` it's a B; and so on. "
            "Because earlier branches already caught the higher scores, you only need one comparison per branch.",
        ],
        samples=["4\n95\n80\n59\n72"],
        tests=["101\n" + "\n".join(str(i) for i in range(101)), "1\n0", "1\n100", "5\n90\n89\n70\n69\n60"],
        gen=lambda rng: [_lines(20, lambda: str(rng.randint(0, 100))) for _ in range(2)],
        starter_python=r"""t = int(input())
for _ in range(t):
    s = int(input())
    # TODO: print the letter grade for s
""",
        starter_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int s;
        cin >> s;
        // TODO: print the letter grade for s
    }
    return 0;
}
""",
        solution_python=r"""t = int(input())
for _ in range(t):
    s = int(input())
    if s >= 90:
        print("A")
    elif s >= 80:
        print("B")
    elif s >= 70:
        print("C")
    elif s >= 60:
        print("D")
    else:
        print("F")
""",
        solution_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int s;
        cin >> s;
        char g;
        if (s >= 90) g = 'A';
        else if (s >= 80) g = 'B';
        else if (s >= 70) g = 'C';
        else if (s >= 60) g = 'D';
        else g = 'F';
        cout << g << "\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="celsius-to-fahrenheit",
        title="Celsius to Fahrenheit",
        difficulty="beginner",
        category="Basics",
        tags=["arithmetic", "floating-point", "formatting"],
        inspired_by="Classic beginner exercise",
        statement="""
A weather station reports temperatures in degrees Celsius, but the app needs
them in Fahrenheit. The conversion formula is

`F = C · 9 / 5 + 32`

Convert every reading.
""",
        input_format="First line: `t` (1 ≤ t ≤ 100). Then `t` lines, each with a real number `C` "
                     "(−273.1 ≤ C ≤ 10000) having at most one digit after the decimal point.",
        output_format="For each reading print the temperature in Fahrenheit with exactly two digits after "
                      "the decimal point (answers within 10⁻⁶ are accepted).",
        hints=[
            "Read real numbers with `float(...)` in Python, or a `double` in C++.",
            "Be careful with integer division: in C++ `9 / 5` is `1`! Write `9.0 / 5.0` (or multiply by `1.8`).",
            "Python: `print(f\"{f:.2f}\")` prints two decimals. C++: `#include <iomanip>` and "
            "`cout << fixed << setprecision(2) << f;`.",
        ],
        samples=["3\n0\n100\n-40"],
        tests=["1\n-273.1", "1\n10000", "4\n36.6\n-0.5\n12.3\n1"],
        gen=lambda rng: [_lines(20, lambda: f"{rng.randint(-2731, 100000) / 10:.1f}"),
                         _lines(10, lambda: str(rng.randint(-50, 50)))],
        checker="float",
        starter_python=r"""t = int(input())
for _ in range(t):
    c = float(input())
    # TODO: convert c to Fahrenheit and print it with 2 decimals
""",
        starter_cpp=r"""#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        double c;
        cin >> c;
        // TODO: convert c to Fahrenheit and print it with 2 decimals
    }
    return 0;
}
""",
        solution_python=r"""t = int(input())
for _ in range(t):
    c = float(input())
    print(f"{c * 9 / 5 + 32:.2f}")
""",
        solution_cpp=r"""#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    int t;
    cin >> t;
    cout << fixed << setprecision(2);
    while (t--) {
        double c;
        cin >> c;
        cout << c * 9.0 / 5.0 + 32.0 << "\n";
    }
    return 0;
}
""",
    ),
]
