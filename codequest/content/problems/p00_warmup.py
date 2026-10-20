"""Warm-up problems: the very first steps. Also the style reference for authors."""

PROBLEMS = [
    dict(
        id="sum-of-two",
        title="Sum of Two Numbers",
        difficulty="beginner",
        category="Basics",
        tags=["input", "arithmetic"],
        inspired_by="Classic A+B (Codeforces / Kattis warm-up)",
        statement="""
Your very first judged program! Read two integers and print their sum.

Every problem in CodeQuest works the same way: your program **reads from
standard input** and **prints to standard output**. The judge runs it against
hidden test cases and compares what you print with the expected answer.
""",
        input_format="One line with two integers `a` and `b` (−10⁹ ≤ a, b ≤ 10⁹).",
        output_format="A single integer: `a + b`.",
        hints=[
            "Python: `input()` gives you the whole line as a string. `.split()` cuts it into pieces.",
            "Convert text to numbers with `int(...)`. `a, b = map(int, input().split())` reads both at once.",
            "C++: `long long a, b; cin >> a >> b;` — use `long long` because the sum can exceed 2³¹.",
        ],
        samples=["2 3", "-5 12"],
        tests=["0 0", "1000000000 1000000000", "-1000000000 -1000000000", "7 -7"],
        gen=lambda rng: [f"{rng.randint(-10**9, 10**9)} {rng.randint(-10**9, 10**9)}" for _ in range(5)],
        starter_python="""# Read two integers from one line, print their sum.
a, b = map(int, input().split())
# your code here
""",
        starter_cpp="""#include <iostream>
using namespace std;

int main() {
    long long a, b;
    cin >> a >> b;
    // print the sum here
    return 0;
}
""",
        solution_python="""a, b = map(int, input().split())
print(a + b)
""",
        solution_cpp="""#include <iostream>
using namespace std;

int main() {
    long long a, b;
    cin >> a >> b;
    cout << a + b << "\\n";
    return 0;
}
""",
    ),
    dict(
        id="fizzbuzz",
        title="FizzBuzz",
        difficulty="beginner",
        category="Basics",
        tags=["loops", "conditionals", "modulo"],
        inspired_by="The classic interview warm-up (LeetCode #412)",
        statement="""
Print the numbers from 1 to `n`, one per line, but:

* for multiples of 3 print `Fizz` instead of the number,
* for multiples of 5 print `Buzz`,
* for multiples of both 3 and 5 print `FizzBuzz`.
""",
        input_format="A single integer `n` (1 ≤ n ≤ 1000).",
        output_format="`n` lines as described.",
        hints=[
            "The remainder operator `%` tells you divisibility: `x % 3 == 0` means x is a multiple of 3.",
            "Order matters! Check the 'both 3 and 5' case (i.e. `x % 15 == 0`) *before* the single cases.",
            "Python: `for i in range(1, n + 1):` loops 1..n. C++: `for (int i = 1; i <= n; i++)`.",
        ],
        samples=["5", "15"],
        tests=["1", "3", "30", "100"],
        gen=lambda rng: [str(rng.randint(1, 1000)) for _ in range(3)],
        checker="exact",
        starter_python="""n = int(input())
for i in range(1, n + 1):
    # decide what to print for i
    pass
""",
        starter_cpp="""#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        // decide what to print for i
    }
    return 0;
}
""",
        solution_python="""n = int(input())
out = []
for i in range(1, n + 1):
    if i % 15 == 0:
        out.append("FizzBuzz")
    elif i % 3 == 0:
        out.append("Fizz")
    elif i % 5 == 0:
        out.append("Buzz")
    else:
        out.append(str(i))
print("\\n".join(out))
""",
        solution_cpp="""#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    for (int i = 1; i <= n; i++) {
        if (i % 15 == 0) cout << "FizzBuzz\\n";
        else if (i % 3 == 0) cout << "Fizz\\n";
        else if (i % 5 == 0) cout << "Buzz\\n";
        else cout << i << "\\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="multiples-of-3-or-5",
        title="Multiples of 3 or 5",
        difficulty="easy",
        category="Number Theory",
        tags=["math", "inclusion-exclusion"],
        inspired_by="Project Euler #1",
        statement="""
Find the sum of all natural numbers **below** `n` that are multiples of 3 or 5.

For `n = 10` these are 3, 5, 6 and 9, whose sum is 23.

There are several test cases. `n` can be as large as 10¹² — a simple loop
will be far too slow, so look for a formula.
""",
        input_format="First line: `t` (1 ≤ t ≤ 1000). Then `t` lines, each with one integer `n` (1 ≤ n ≤ 10¹²).",
        output_format="For each test case print the sum on its own line.",
        hints=[
            "Sum of multiples of k below n: there are m = (n − 1) // k of them, and k + 2k + … + mk = k·m·(m+1)/2.",
            "Multiples of 15 are counted twice (once for 3, once for 5). Inclusion–exclusion: S(3) + S(5) − S(15).",
            "C++: for n = 10¹² the answer is about 2.3·10²³, far beyond `long long` (≈ 9.2·10¹⁸). "
            "Do the arithmetic in `__int128` and print it with the provided `to_str` helper.",
        ],
        samples=["2\n10\n100"],
        tests=["1\n1", "3\n2\n3\n4", "1\n1000", "1\n1000000000000"],
        gen=lambda rng: ["50\n" + "\n".join(str(rng.randint(1, 10**12)) for _ in range(50))],
        starter_python="""t = int(input())
for _ in range(t):
    n = int(input())
    # print the sum of multiples of 3 or 5 below n
""",
        starter_cpp="""#include <iostream>
#include <string>
using namespace std;

// Helper: print a 128-bit integer (cout can't do it directly).
string to_str(__int128 x) {
    if (x == 0) return "0";
    string s;
    while (x > 0) { s += char('0' + int(x % 10)); x /= 10; }
    return string(s.rbegin(), s.rend());
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long n;
        cin >> n;
        // compute and print the answer
    }
    return 0;
}
""",
        solution_python="""def s(k, n):
    m = (n - 1) // k
    return k * m * (m + 1) // 2

t = int(input())
for _ in range(t):
    n = int(input())
    print(s(3, n) + s(5, n) - s(15, n))
""",
        solution_cpp="""#include <iostream>
#include <string>
using namespace std;

string to_str(__int128 x) {
    if (x == 0) return "0";
    string s;
    while (x > 0) { s += char('0' + int(x % 10)); x /= 10; }
    return string(s.rbegin(), s.rend());
}

__int128 s(long long k, long long n) {
    __int128 m = (n - 1) / k;
    return (__int128)k * m * (m + 1) / 2;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long n;
        cin >> n;
        cout << to_str(s(3, n) + s(5, n) - s(15, n)) << "\\n";
    }
    return 0;
}
""",
    ),
]
