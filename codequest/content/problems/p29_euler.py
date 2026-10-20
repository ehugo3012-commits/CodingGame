"""Number Theory, Project-Euler flavoured: palindromic products, amicable pairs, digit factorials."""


def _pal_gen(rng):
    qs = [rng.randint(101102, 999999) for _ in range(40)]
    return [f"{len(qs)}\n" + "\n".join(map(str, qs))]


def _amic_gen(rng):
    return [str(rng.randint(1, 3000)), str(rng.randint(10**4, 10**5)), str(rng.randint(5 * 10**4, 10**5))]


def _digfac_gen(rng):
    return [str(rng.randint(10, 1000)), str(rng.randint(10**4, 10**5)), str(rng.randint(10, 10**5))]


PROBLEMS = [
    dict(
        id="palindrome-from-two-3-digits",
        title="Palindrome from Two 3-Digit Factors",
        difficulty="medium",
        category="Number Theory",
        tags=["palindromes", "brute-force", "precomputation", "binary-search"],
        inspired_by="Project Euler #4 Largest Palindrome Product (HackerRank ProjectEuler+ variant)",
        statement="""
A **palindromic number** reads the same both ways, like `9009 = 91 × 99`.

For each query `N`, find the **largest** palindrome that is **strictly less
than `N`** and can be written as the product of **two 3-digit numbers**
(each between 100 and 999).

The smallest such 6-digit palindrome is `101101 = 143 × 707`, and every query
has `N > 101101`, so an answer always exists. Only 6-digit palindromes count
here (all queries are below 10⁶).
""",
        input_format="First line: `t` (1 ≤ t ≤ 100). Next `t` lines: `N` (101101 < N < 10⁶).",
        output_format="For each query, the largest valid palindrome below `N`.",
        hints=[
            "There are only 900 six-digit palindromes (`abccba`). It's cheaper to start from palindromes than from "
            "all ~400 000 products.",
            "A palindrome `p` qualifies if some `i` in `[100, 999]` divides it with `100 <= p // i <= 999`. You only need "
            "to try `i` up to `√p`.",
            "Precompute the sorted list of qualifying palindromes once, then answer each query with a binary search: "
            "`bisect.bisect_left(lst, N) - 1` in Python, `lower_bound` in C++.",
        ],
        samples=["2\n101110\n800000"],
        tests=["1\n101102", "1\n999999", "3\n906609\n906610\n580086"],
        gen=_pal_gen,
        starter_python="""import bisect

t = int(input())
queries = [int(input()) for _ in range(t)]
good = []   # sorted palindromes that are products of two 3-digit numbers
# TODO: fill `good`
for N in queries:
    print(0)
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    vector<int> good;  // sorted palindromes that are products of two 3-digit numbers
    // TODO: fill `good`
    int t;
    cin >> t;
    while (t--) {
        int N;
        cin >> N;
        // TODO: largest element of good that is < N
        cout << 0 << "\\n";
    }
    return 0;
}
""",
        solution_python=r"""import bisect
from math import isqrt

good = []
for a in range(1, 10):
    for b in range(10):
        for c in range(10):
            p = 100001 * a + 10010 * b + 1100 * c
            lo = max(100, -(-p // 999))
            for i in range(lo, isqrt(p) + 1):
                if p % i == 0:
                    good.append(p)
                    break
good.sort()
t = int(input())
out = []
for _ in range(t):
    N = int(input())
    out.append(good[bisect.bisect_left(good, N) - 1])
print("\n".join(map(str, out)))
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
using namespace std;

bool isPal(int x) {
    string s = to_string(x);
    return equal(s.begin(), s.end(), s.rbegin());
}

int main() {
    vector<int> good;
    for (int i = 100; i <= 999; i++)
        for (int j = i; j <= 999; j++) {
            int p = i * j;
            if (p >= 100000 && isPal(p)) good.push_back(p);
        }
    sort(good.begin(), good.end());
    good.erase(unique(good.begin(), good.end()), good.end());
    int t;
    cin >> t;
    while (t--) {
        int N;
        cin >> N;
        auto it = lower_bound(good.begin(), good.end(), N);
        cout << *(it - 1) << "\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="amicable-pairs-up-to-n",
        title="Amicable Pairs up to N",
        difficulty="medium",
        category="Number Theory",
        tags=["divisors", "sieve", "amicable-numbers"],
        inspired_by="Project Euler #21 Amicable Numbers",
        statement="""
Let `d(x)` be the sum of the **proper divisors** of `x` (divisors smaller than
`x`). For example the proper divisors of 220 are 1, 2, 4, 5, 10, 11, 20, 22,
44, 55 and 110, so `d(220) = 284`; and `d(284) = 1 + 2 + 4 + 71 + 142 = 220`.

Two **different** numbers `a < b` with `d(a) = b` and `d(b) = a` form an
**amicable pair** — `(220, 284)` is the smallest one, known since Pythagoras.
(A number with `d(x) = x`, like 6, is *perfect*, not amicable.)

List every amicable pair whose **both** members are `≤ N`.
""",
        input_format="One integer `N` (1 ≤ N ≤ 10⁵).",
        output_format="""First line: the number `k` of pairs. Then `k` lines `a b` (with `a < b`), sorted by `a`.""",
        hints=[
            "Computing `d(x)` by trial division for every `x` is O(N·√N) — too slow in Python. Use a **divisor-sum "
            "sieve** instead.",
            "Sieve idea: for every `i` from 1 to `N // 2`, add `i` to `d[2i], d[3i], d[4i], …` (all multiples of `i` "
            "except `i` itself). Total work ≈ N·ln N. Python: a faster variant pairs each divisor `i ≤ √j` with `j // i`.",
            "Then for each `a`: let `b = d[a]`; it's a pair if `a < b <= N` and `d[b] == a`. Checking only `a < b` lists "
            "each pair once.",
        ],
        samples=["300", "5000"],
        tests=["1", "219", "283", "284", "100000", "6"],
        gen=_amic_gen,
        starter_python="""N = int(input())
d = [0] * (N + 1)   # d[x] = sum of proper divisors of x
# TODO: fill d with a divisor-sum sieve
pairs = []
# TODO: find the pairs (a, b) with a < b <= N
print(len(pairs))
for a, b in pairs:
    print(a, b)
""",
        starter_cpp="""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int N;
    cin >> N;
    vector<long long> d(N + 1, 0);  // d[x] = sum of proper divisors of x
    // TODO: divisor-sum sieve
    vector<pair<int, int>> pairs;
    // TODO: find the pairs (a, b) with a < b <= N
    cout << pairs.size() << "\\n";
    for (auto &p : pairs) cout << p.first << " " << p.second << "\\n";
    return 0;
}
""",
        solution_python=r"""N = int(input())
d = [1] * (N + 1)
d[0] = 0
if N >= 1:
    d[1] = 0
i = 2
while i * i <= N:
    d[i * i] += i
    for j in range(i * (i + 1), N + 1, i):
        d[j] += i + j // i
    i += 1
pairs = []
for a in range(2, N + 1):
    b = d[a]
    if a < b <= N and d[b] == a:
        pairs.append((a, b))
out = [str(len(pairs))] + [f"{a} {b}" for a, b in pairs]
print("\n".join(out))
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int N;
    cin >> N;
    vector<long long> d(N + 1, 0);
    for (int i = 1; i <= N / 2; i++)
        for (int j = 2 * i; j <= N; j += i) d[j] += i;
    vector<pair<int, int>> pairs;
    for (int a = 2; a <= N; a++) {
        long long b = d[a];
        if (a < b && b <= N && d[b] == a) pairs.push_back({a, (int)b});
    }
    cout << pairs.size() << "\n";
    for (auto &p : pairs) cout << p.first << " " << p.second << "\n";
    return 0;
}
""",
    ),
    dict(
        id="digit-factorial-divisors",
        title="Digit Factorial Divisors",
        difficulty="medium",
        category="Number Theory",
        tags=["factorials", "digits", "precomputation"],
        inspired_by="Project Euler #34 Digit Factorials (HackerRank ProjectEuler+ variant)",
        statement="""
`145` is a curious number: `1! + 4! + 5! = 1 + 24 + 120 = 145`. Only one other
such number exists, `40585`.

Let's relax the condition. Call `x` **curious** if `x` **divides** the sum of
the factorials of its digits. For example `19` is curious, since
`1! + 9! = 362881 = 19 × 19099`.

Find the **sum** of all curious numbers `x` with `10 ≤ x < N`.
""",
        input_format="One integer `N` (10 ≤ N ≤ 10⁵).",
        output_format="One integer: the sum of all curious `x` with `10 ≤ x < N` (0 if there are none).",
        hints=[
            "Precompute `fact[0..9]` once. For each `x`, the digit-factorial sum is `fact` of every digit added up "
            "(peel digits with `x % 10` and `x // 10`).",
            "Faster: build a table `f[x] = f[x // 10] + fact[x % 10]` for all `x < N` in one increasing loop — "
            "each entry reuses the previous one, O(1) per number. (Careful: `f[0]` should be 0 here; `x ≥ 10` never "
            "needs `0!` for a leading digit.)",
            "Then add up every `x` in `[10, N)` with `f[x] % x == 0`. The digit sums stay below 6·9! ≈ 2.2·10⁶, so "
            "`int` is enough in C++, but the total sum needs `long long`.",
        ],
        samples=["20", "200"],
        tests=["10", "11", "146", "40586", "100000"],
        gen=_digfac_gen,
        starter_python="""from math import factorial

N = int(input())
fact = [factorial(d) for d in range(10)]
total = 0
for x in range(10, N):
    # TODO: compute the digit-factorial sum of x and test divisibility
    pass
print(total)
""",
        starter_cpp="""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int N;
    cin >> N;
    long long fact[10];
    fact[0] = 1;
    for (int d = 1; d < 10; d++) fact[d] = fact[d - 1] * d;
    long long total = 0;
    for (int x = 10; x < N; x++) {
        // TODO: compute the digit-factorial sum of x and test divisibility
    }
    cout << total << "\\n";
    return 0;
}
""",
        solution_python=r"""from math import factorial

N = int(input())
fact = [factorial(d) for d in range(10)]
f = [0] * N
total = 0
for x in range(1, N):
    f[x] = f[x // 10] + fact[x % 10]
    if x >= 10 and f[x] % x == 0:
        total += x
print(total)
""",
        solution_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int N;
    cin >> N;
    long long fact[10];
    fact[0] = 1;
    for (int d = 1; d < 10; d++) fact[d] = fact[d - 1] * d;
    long long total = 0;
    for (int x = 10; x < N; x++) {
        long long s = 0;
        for (int y = x; y > 0; y /= 10) s += fact[y % 10];
        if (s % x == 0) total += x;
    }
    cout << total << "\n";
    return 0;
}
""",
    ),
]
