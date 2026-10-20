"""Basics: loops and text patterns."""


def _lines(t, make):
    return f"{t}\n" + "\n".join(make() for _ in range(t))


def _triangle_case(rng):
    kind = rng.randrange(5)
    if kind == 0:
        a = rng.randint(1, 10**9)
        return f"{a} {a} {a}"
    if kind == 1:
        a, b = rng.randint(1, 10**9), rng.randint(1, 10**9)
        s = [a, a, b]
        rng.shuffle(s)
        return " ".join(map(str, s))
    if kind == 2:  # degenerate: c == a + b
        a, b = rng.randint(1, 5 * 10**8), rng.randint(1, 5 * 10**8)
        s = [a, b, a + b]
        rng.shuffle(s)
        return " ".join(map(str, s))
    hi = 10**9 if kind == 3 else 20
    return " ".join(str(rng.randint(1, hi)) for _ in range(3))


PROBLEMS = [
    dict(
        id="multiplication-table",
        title="Multiplication Table",
        difficulty="beginner",
        category="Basics",
        tags=["loops", "formatting"],
        inspired_by="Classic beginner exercise (HackerRank '30 Days of Code: Loops')",
        statement="""
Print the multiplication table of `n` from 1 to 10.

For `n = 3` the first lines are:

```
3 x 1 = 3
3 x 2 = 6
3 x 3 = 9
```
""",
        input_format="A single integer `n` (1 ≤ n ≤ 1000).",
        output_format="Exactly 10 lines. Line `i` is `n x i = r` where `r = n · i`, with single spaces "
                      "exactly as in the example (the `x` is a lowercase letter x).",
        hints=[
            "A loop that runs i = 1, 2, …, 10: Python `for i in range(1, 11):`; C++ `for (int i = 1; i <= 10; i++)`.",
            "Python: an f-string builds the line easily: `f\"{n} x {i} = {n * i}\"`.",
            "C++: chain the pieces: `cout << n << \" x \" << i << \" = \" << n * i << \"\\n\";`.",
        ],
        samples=["3"],
        tests=["1", "1000", "7", "10"],
        gen=lambda rng: [str(rng.randint(1, 1000)) for _ in range(3)],
        checker="exact",
        starter_python=r"""n = int(input())
# TODO: print the 10 lines of the table
""",
        starter_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    // TODO: print the 10 lines of the table
    return 0;
}
""",
        solution_python=r"""n = int(input())
for i in range(1, 11):
    print(f"{n} x {i} = {n * i}")
""",
        solution_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    for (int i = 1; i <= 10; i++) {
        cout << n << " x " << i << " = " << n * i << "\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="star-staircase",
        title="Star Staircase",
        difficulty="beginner",
        category="Basics",
        tags=["loops", "patterns", "nested-loops"],
        inspired_by="HackerRank 'Staircase' (left-aligned variant)",
        statement="""
Draw a staircase of stars `*` with `n` steps. Step `i` (counting from 1 at
the top) consists of `i` stars. For `n = 4`:

```
*
**
***
****
```
""",
        input_format="A single integer `n` (1 ≤ n ≤ 50).",
        output_format="`n` lines; line `i` contains exactly `i` characters `*` and nothing else.",
        hints=[
            "You need one line per step, so start with a loop over i = 1..n.",
            "Python can repeat a string: `\"*\" * 3` is `\"***\"`.",
            "C++: either an inner loop printing `*` i times, or `string(i, '*')` which builds a string of i stars "
            "(`#include <string>`). End each line with `\"\\n\"`.",
        ],
        samples=["4"],
        tests=["1", "2", "50", "10"],
        gen=lambda rng: [str(rng.randint(3, 50)) for _ in range(3)],
        checker="exact",
        starter_python=r"""n = int(input())
# TODO: print the staircase
""",
        starter_cpp=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    int n;
    cin >> n;
    // TODO: print the staircase
    return 0;
}
""",
        solution_python=r"""n = int(input())
for i in range(1, n + 1):
    print("*" * i)
""",
        solution_cpp=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) cout << string(i, '*') << "\n";
    return 0;
}
""",
    ),
    dict(
        id="star-pyramid",
        title="Star Pyramid",
        difficulty="easy",
        category="Basics",
        tags=["loops", "patterns", "nested-loops"],
        inspired_by="Classic pattern-printing exercise",
        statement="""
Draw a centred pyramid of stars with `n` rows. Row `i` (counting from 1 at the
top) has `n − i` spaces followed by `2·i − 1` stars. For `n = 3`:

```
  *
 ***
*****
```
""",
        input_format="A single integer `n` (1 ≤ n ≤ 40).",
        output_format="`n` lines forming the pyramid. Leading spaces matter; trailing spaces are ignored.",
        hints=[
            "Work out each row separately: how many spaces, then how many stars? Check your formula on row 1 and row n.",
            "Python: `\" \" * k + \"*\" * m` glues k spaces and m stars together.",
            "C++: `string(k, ' ') + string(m, '*')` builds the same row.",
        ],
        samples=["3"],
        tests=["1", "2", "40", "5"],
        gen=lambda rng: [str(rng.randint(3, 40)) for _ in range(3)],
        checker="exact",
        starter_python=r"""n = int(input())
for i in range(1, n + 1):
    # TODO: print row i (spaces, then stars)
    pass
""",
        starter_cpp=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        // TODO: print row i (spaces, then stars)
    }
    return 0;
}
""",
        solution_python=r"""n = int(input())
for i in range(1, n + 1):
    print(" " * (n - i) + "*" * (2 * i - 1))
""",
        solution_cpp=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        cout << string(n - i, ' ') << string(2 * i - 1, '*') << "\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="sum-of-odds-in-range",
        title="Sum of Odd Numbers in a Range",
        difficulty="easy",
        category="Basics",
        tags=["loops", "modulo", "accumulator"],
        inspired_by="Classic loop exercise",
        statement="""
Given two integers `l` and `r`, compute the sum of all **odd** integers `x`
with `l ≤ x ≤ r`. Both ends are included and may be negative.

For `l = 1, r = 6` the odd numbers are 1, 3, 5 and their sum is 9.
If there are no odd numbers in the range, the sum is 0.
""",
        input_format="First line: `t` (1 ≤ t ≤ 100). Then `t` lines, each with two integers `l r` "
                     "(−10⁴ ≤ l ≤ r ≤ 10⁴).",
        output_format="For each test case print the sum on its own line.",
        hints=[
            "Keep a running total that starts at 0, loop x from l to r, and add x whenever it is odd.",
            "Python: `range(l, r + 1)` includes r. C++: `for (int x = l; x <= r; x++)`.",
            "C++: `-3 % 2 == -1`, so test oddness with `x % 2 != 0`, not `x % 2 == 1`.",
            "Bonus: odd numbers form an arithmetic sequence, so a formula can skip the loop entirely.",
        ],
        samples=["3\n1 6\n-3 3\n4 4"],
        tests=["1\n-10000 10000", "1\n1 10000", "1\n-10000 -1", "2\n0 0\n-7 -7", "1\n-9999 9998"],
        gen=lambda rng: [_lines(30, lambda: " ".join(map(str, sorted((rng.randint(-10**4, 10**4),
                                                                        rng.randint(-10**4, 10**4))))))
                         for _ in range(2)],
        starter_python=r"""t = int(input())
for _ in range(t):
    l, r = map(int, input().split())
    total = 0
    # TODO: add every odd number between l and r to total
    print(total)
""",
        starter_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int l, r;
        cin >> l >> r;
        long long total = 0;
        // TODO: add every odd number between l and r to total
        cout << total << "\n";
    }
    return 0;
}
""",
        solution_python=r"""t = int(input())
for _ in range(t):
    l, r = map(int, input().split())
    print(sum(x for x in range(l, r + 1) if x % 2 != 0))
""",
        solution_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int l, r;
        cin >> l >> r;
        long long total = 0;
        for (int x = l; x <= r; x++)
            if (x % 2 != 0) total += x;
        cout << total << "\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="triangle-classifier",
        title="Triangle Classifier",
        difficulty="easy",
        category="Basics",
        tags=["conditionals", "sorting", "overflow"],
        inspired_by="Classic exercise (Kattis 'Triangle'-style classification)",
        statement="""
Three sticks have lengths `a`, `b` and `c`. They form a (non-degenerate)
triangle only if the longest stick is **strictly shorter** than the other two
together.

Classify each set of sticks:

* `INVALID` – they cannot form a triangle,
* `EQUILATERAL` – all three lengths are equal,
* `ISOSCELES` – exactly two lengths are equal,
* `SCALENE` – all lengths differ.
""",
        input_format="First line: `t` (1 ≤ t ≤ 100). Then `t` lines, each with three integers `a b c` "
                     "(1 ≤ a, b, c ≤ 10⁹).",
        output_format="For each test case print one of the four words on its own line.",
        hints=[
            "Check validity first: the order of a, b, c is arbitrary, so find the largest (sorting the three is easiest).",
            "After sorting so that x ≤ y ≤ z, the sticks form a triangle exactly when `x + y > z`.",
            "C++: `x + y` can reach 2·10⁹, which overflows `int`. Read the lengths into `long long`.",
        ],
        samples=["4\n3 4 5\n2 2 2\n5 3 5\n1 2 3"],
        tests=["1\n1 1 1", "1\n1000000000 1000000000 1000000000", "1\n1000000000 1000000000 1",
               "1\n1 1 1000000000", "3\n2 3 4\n4 3 2\n10 1 1"],
        gen=lambda rng: [_lines(40, lambda: _triangle_case(rng)) for _ in range(2)],
        starter_python=r"""t = int(input())
for _ in range(t):
    a, b, c = map(int, input().split())
    # TODO: print INVALID, EQUILATERAL, ISOSCELES or SCALENE
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
        // TODO: print INVALID, EQUILATERAL, ISOSCELES or SCALENE
    }
    return 0;
}
""",
        solution_python=r"""t = int(input())
for _ in range(t):
    x, y, z = sorted(map(int, input().split()))
    if x + y <= z:
        print("INVALID")
    elif x == z:
        print("EQUILATERAL")
    elif x == y or y == z:
        print("ISOSCELES")
    else:
        print("SCALENE")
""",
        solution_cpp=r"""#include <iostream>
#include <algorithm>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long s[3];
        cin >> s[0] >> s[1] >> s[2];
        sort(s, s + 3);
        if (s[0] + s[1] <= s[2]) cout << "INVALID\n";
        else if (s[0] == s[2]) cout << "EQUILATERAL\n";
        else if (s[0] == s[1] || s[1] == s[2]) cout << "ISOSCELES\n";
        else cout << "SCALENE\n";
    }
    return 0;
}
""",
    ),
]
