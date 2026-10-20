"""Math basics: calendars, digits, sequences and number bases."""


def _lines(t, make):
    return f"{t}\n" + "\n".join(make() for _ in range(t))


def _year(rng):
    k = rng.randrange(4)
    if k == 0:
        return str(rng.randint(1, 10**4) * 4)
    if k == 1:
        return str(rng.randint(1, 10**6) * 100)
    if k == 2:
        return str(rng.randint(1, 10**5) * 400)
    return str(rng.randint(1, 10**9))


def _big(rng):
    return str(rng.randint(0, 10 ** rng.randint(1, 18)))


PROBLEMS = [
    dict(
        id="leap-year",
        title="Leap Year?",
        difficulty="beginner",
        category="Math",
        tags=["conditionals", "modulo", "calendar"],
        inspired_by="HackerRank 'Write a function' (leap years)",
        statement="""
In the Gregorian calendar a year is a **leap year** if

* it is divisible by 4,
* **except** years divisible by 100, which are not leap years,
* **except** years divisible by 400, which are leap years after all.

So 2024 and 2000 are leap years, while 1900 and 2023 are not.
""",
        input_format="First line: `t` (1 ≤ t ≤ 100). Then `t` lines, each with a year `y` (1 ≤ y ≤ 10⁹).",
        output_format="For each year print `YES` if it is a leap year and `NO` otherwise.",
        hints=[
            "`y % 4 == 0` tests divisibility by 4; you'll need the same idea for 100 and 400.",
            "Combine conditions with `and` / `or` in Python, `&&` / `||` in C++.",
            "One compact form: leap ⇔ (divisible by 4 **and not** by 100) **or** divisible by 400.",
        ],
        samples=["4\n2024\n2000\n1900\n2023"],
        tests=["1\n1", "1\n4", "1\n400", "1\n100", "3\n1000000000\n999999996\n999999900"],
        gen=lambda rng: [_lines(30, lambda: _year(rng)) for _ in range(2)],
        starter_python=r"""t = int(input())
for _ in range(t):
    y = int(input())
    # TODO: print YES if y is a leap year, otherwise NO
""",
        starter_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long y;
        cin >> y;
        // TODO: print YES if y is a leap year, otherwise NO
    }
    return 0;
}
""",
        solution_python=r"""t = int(input())
for _ in range(t):
    y = int(input())
    leap = (y % 4 == 0 and y % 100 != 0) or y % 400 == 0
    print("YES" if leap else "NO")
""",
        solution_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long y;
        cin >> y;
        bool leap = (y % 4 == 0 && y % 100 != 0) || y % 400 == 0;
        cout << (leap ? "YES" : "NO") << "\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="digit-sum",
        title="Sum of Digits",
        difficulty="beginner",
        category="Math",
        tags=["digits", "loops", "modulo"],
        inspired_by="Classic digit-manipulation exercise",
        statement="""
Compute the sum of the decimal digits of `n`. For `n = 1234` the answer is
`1 + 2 + 3 + 4 = 10`.
""",
        input_format="First line: `t` (1 ≤ t ≤ 100). Then `t` lines, each with an integer `n` (0 ≤ n ≤ 10¹⁸).",
        output_format="For each `n` print the sum of its digits on its own line.",
        hints=[
            "`n % 10` is the last digit and `n // 10` (C++: `n / 10`) removes it. Repeat while `n > 0`.",
            "C++: 10¹⁸ needs `long long`.",
            "Alternative: treat the number as text and add up the characters: Python `int(ch)`, C++ `ch - '0'`.",
        ],
        samples=["3\n1234\n0\n999"],
        tests=["1\n1000000000000000000", "1\n999999999999999999", "2\n7\n10", "1\n123456789012345678"],
        gen=lambda rng: [_lines(30, lambda: _big(rng)) for _ in range(2)],
        starter_python=r"""t = int(input())
for _ in range(t):
    n = int(input())
    total = 0
    # TODO: add up the digits of n
    print(total)
""",
        starter_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long n;
        cin >> n;
        int total = 0;
        // TODO: add up the digits of n
        cout << total << "\n";
    }
    return 0;
}
""",
        solution_python=r"""t = int(input())
for _ in range(t):
    n = int(input())
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    print(total)
""",
        solution_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long n;
        cin >> n;
        int total = 0;
        while (n > 0) {
            total += (int)(n % 10);
            n /= 10;
        }
        cout << total << "\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="fibonacci-number",
        title="Fibonacci Numbers",
        difficulty="beginner",
        category="Math",
        tags=["loops", "sequences", "overflow"],
        inspired_by="LeetCode #509 Fibonacci Number",
        statement="""
The Fibonacci sequence starts with `F(0) = 0` and `F(1) = 1`; every later
term is the sum of the previous two:

`0, 1, 1, 2, 3, 5, 8, 13, 21, …`

Print `F(n)` for each query.
""",
        input_format="First line: `t` (1 ≤ t ≤ 100). Then `t` lines, each with an integer `n` (0 ≤ n ≤ 90).",
        output_format="For each query print `F(n)` on its own line.",
        hints=[
            "Keep just the last two terms `a, b` (starting at 0 and 1) and step forward n times: the new pair is `(b, a + b)`.",
            "Python: `a, b = b, a + b` updates both at once.",
            "C++: F(90) ≈ 2.9·10¹⁸ — far beyond `int`, but it fits in `long long`.",
            "A naive recursive function would take forever for n = 90 — use a loop.",
        ],
        samples=["4\n0\n1\n2\n10"],
        tests=["1\n90", "1\n89", "3\n3\n4\n5", "1\n50"],
        gen=lambda rng: [_lines(25, lambda: str(rng.randint(0, 90))) for _ in range(2)],
        starter_python=r"""t = int(input())
for _ in range(t):
    n = int(input())
    # TODO: compute and print F(n)
""",
        starter_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        // TODO: compute and print F(n)
    }
    return 0;
}
""",
        solution_python=r"""t = int(input())
for _ in range(t):
    n = int(input())
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    print(a)
""",
        solution_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        long long a = 0, b = 1;
        for (int i = 0; i < n; i++) {
            long long c = a + b;
            a = b;
            b = c;
        }
        cout << a << "\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="base-conversion",
        title="Base Converter",
        difficulty="easy",
        category="Math",
        tags=["number-bases", "division", "strings"],
        inspired_by="Classic number-base conversion (Kattis / HackerRank 'Binary Numbers' theme)",
        statement="""
Write the decimal number `n` in base `b`.

Digits above 9 are written with **uppercase** letters: `A` = 10, `B` = 11, …,
`F` = 15. For example `255` in base 16 is `FF`, and `10` in base 2 is `1010`.
Zero is written as `0` in every base.
""",
        input_format="First line: `t` (1 ≤ t ≤ 100). Then `t` lines, each with two integers `n b` "
                     "(0 ≤ n ≤ 10¹⁸, 2 ≤ b ≤ 16).",
        output_format="For each query print `n` written in base `b` (no leading zeros) on its own line.",
        hints=[
            "Repeatedly divide by b: the remainder `n % b` is the **last** digit, then continue with `n // b`.",
            "The digits come out in reverse order — collect them and reverse at the end.",
            "Map a digit value to a character with a lookup string: `\"0123456789ABCDEF\"[d]`.",
            "Don't forget the special case n = 0 (the loop would produce nothing). C++: use `long long`.",
        ],
        samples=["3\n10 2\n255 16\n0 7"],
        tests=["1\n1000000000000000000 2", "1\n1000000000000000000 16", "3\n1 2\n15 16\n16 16",
               "2\n35 3\n999999999999999999 15"],
        gen=lambda rng: [_lines(25, lambda: f"{_big(rng)} {rng.randint(2, 16)}") for _ in range(2)],
        starter_python=r"""DIGITS = "0123456789ABCDEF"
t = int(input())
for _ in range(t):
    n, b = map(int, input().split())
    # TODO: print n written in base b
""",
        starter_cpp=r"""#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    const string DIGITS = "0123456789ABCDEF";
    int t;
    cin >> t;
    while (t--) {
        long long n;
        int b;
        cin >> n >> b;
        // TODO: print n written in base b
    }
    return 0;
}
""",
        solution_python=r"""DIGITS = "0123456789ABCDEF"
t = int(input())
for _ in range(t):
    n, b = map(int, input().split())
    if n == 0:
        print(0)
        continue
    out = []
    while n > 0:
        out.append(DIGITS[n % b])
        n //= b
    print("".join(reversed(out)))
""",
        solution_cpp=r"""#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    const string DIGITS = "0123456789ABCDEF";
    int t;
    cin >> t;
    while (t--) {
        long long n;
        int b;
        cin >> n >> b;
        string s;
        if (n == 0) s = "0";
        while (n > 0) {
            s += DIGITS[n % b];
            n /= b;
        }
        reverse(s.begin(), s.end());
        cout << s << "\n";
    }
    return 0;
}
""",
    ),
]
