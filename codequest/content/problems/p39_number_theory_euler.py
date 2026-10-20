"""Hard / expert number theory in the Project Euler spirit: totients, Collatz, Pythagorean triples."""


def _gen_totient(rng):
    tests = []
    qs = [rng.randint(1, 300000) for _ in range(1500)] + [300000, 1, 2]
    tests.append(f"{len(qs)}\n" + "\n".join(map(str, qs)))
    qs = [rng.randint(1, 1000) for _ in range(300)]
    tests.append(f"{len(qs)}\n" + "\n".join(map(str, qs)))
    return tests


def _gen_collatz(rng):
    tests = []
    qs = [rng.randint(1, 300000) for _ in range(1500)] + [300000]
    tests.append(f"{len(qs)}\n" + "\n".join(map(str, qs)))
    qs = list(range(1, 201))
    tests.append(f"{len(qs)}\n" + "\n".join(map(str, qs)))
    return tests


def _gen_perimeter(rng):
    tests = []
    qs = [rng.randint(1, 10**6) for _ in range(1000)] + [10**6]
    tests.append(f"{len(qs)}\n" + "\n".join(map(str, qs)))
    qs = [rng.randint(1, 500) for _ in range(300)]
    tests.append(f"{len(qs)}\n" + "\n".join(map(str, qs)))
    return tests


PROBLEMS = [
    dict(
        id="totient-reduced-fractions",
        title="Counting Reduced Fractions",
        difficulty="hard",
        category="Number Theory",
        tags=["euler-totient", "sieve", "prefix-sums", "farey-sequence"],
        inspired_by="Project Euler #72 Counting fractions",
        statement="""
A **reduced proper fraction** is a fraction `a/b` with `0 < a < b` and `gcd(a, b) = 1`.
For `b ≤ 8` there are 21 of them:

`1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8`

Answer `q` questions: how many reduced proper fractions have a denominator `b ≤ N`?
""",
        input_format="""
First line: `q` (1 ≤ q ≤ 2000).
Next `q` lines: one integer `N` (1 ≤ N ≤ 3·10⁵).
""",
        output_format="For each question, one line with the count.",
        hints=[
            "For a fixed denominator `b`, the valid numerators are the `a < b` coprime to `b`: there are exactly "
            "**Euler's totient** `φ(b)` of them. So the answer is `φ(2) + φ(3) + … + φ(N)`.",
            "Compute every `φ` up to the largest `N` with a **sieve**: start with `phi[i] = i`; for each prime `p` "
            "(a number whose `phi` is still untouched, `phi[p] == p`), do `phi[k] -= phi[k] // p` for all multiples `k` of `p`.",
            "Then build prefix sums once, so each question is a single lookup.",
            "The sum for N = 3·10⁵ is about 2.7·10¹⁰ — `long long` in C++. Python speed-up: update all multiples at once with a slice, "
            "`phi[p::p] = [v - v // p for v in phi[p::p]]`.",
        ],
        samples=["2\n8\n1"],
        tests=["3\n2\n3\n4", "1\n10", "1\n300000"],
        gen=_gen_totient,
        starter_python="""import sys

def main():
    data = list(map(int, sys.stdin.read().split()))
    q = data[0]
    queries = data[1:1 + q]
    top = max(queries)
    # TODO: totient sieve up to top, prefix sums, answer the queries
    print("\\n".join("0" for _ in queries))

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    vector<int> queries(q);
    for (auto &x : queries) cin >> x;
    int top = *max_element(queries.begin(), queries.end());
    // TODO: totient sieve up to top, prefix sums, answer the queries
    for (int i = 0; i < q; i++) cout << 0 << "\\n";
    return 0;
}
""",
        solution_python="""import sys
from itertools import accumulate

def main():
    data = list(map(int, sys.stdin.read().split()))
    q = data[0]
    queries = data[1:1 + q]
    top = max(queries)
    phi = list(range(top + 1))
    for p in range(2, top + 1):
        if phi[p] == p:   # p is prime
            phi[p::p] = [v - v // p for v in phi[p::p]]
    phi[0] = phi[1] = 0
    pref = list(accumulate(phi))
    print("\\n".join(str(pref[n]) for n in queries))

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    vector<int> queries(q);
    for (auto &x : queries) cin >> x;
    int top = *max_element(queries.begin(), queries.end());
    vector<long long> phi(top + 1);
    for (int i = 0; i <= top; i++) phi[i] = i;
    for (int p = 2; p <= top; p++)
        if (phi[p] == p)
            for (int k = p; k <= top; k += p) phi[k] -= phi[k] / p;
    vector<long long> pref(top + 1, 0);
    for (int i = 2; i <= top; i++) pref[i] = pref[i - 1] + phi[i];
    for (int n : queries) cout << pref[n] << "\\n";
    return 0;
}
""",
    ),
    dict(
        id="longest-collatz-queries",
        title="Longest Collatz Chains",
        difficulty="hard",
        category="Number Theory",
        tags=["memoization", "collatz", "precomputation"],
        inspired_by="Project Euler #14 Longest Collatz sequence",
        statement="""
The Collatz rule turns `x` into `x / 2` if `x` is even and into `3x + 1` if `x` is odd.
Starting from 13 you get the chain

`13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1`

which has **10 terms** (count the start and the final 1; the chain of 1 has one term).

Answer `q` questions: among the starting numbers `1 … N`, which one produces the longest chain?
If several tie, take the **smallest** starting number. Print it together with its chain length.
""",
        input_format="""
First line: `q` (1 ≤ q ≤ 2000).
Next `q` lines: one integer `N` (1 ≤ N ≤ 3·10⁵).
""",
        output_format="For each question, one line `start length`.",
        hints=[
            "Chains merge quickly: once a chain from `s` drops below `s`, the rest of it is a chain you have already measured. "
            "**Memoise** `length[x]` for all `x ≤ top`.",
            "For `s = 2, 3, …`: follow the rule from `s`, counting steps, until the value drops below `s`; then "
            "`length[s] = steps + length[value]`.",
            "Intermediate values can exceed 2³¹ (they reach about 10¹⁰ here): use `long long` in C++.",
            "Answer all questions from one table: `best[N]` = best start in `1..N`, built with one left-to-right pass "
            "(update only on a **strictly** longer chain so ties keep the smaller start).",
        ],
        samples=["3\n10\n13\n1"],
        tests=["2\n2\n3", "1\n100", "1\n300000"],
        gen=_gen_collatz,
        starter_python="""import sys

def main():
    data = list(map(int, sys.stdin.read().split()))
    q = data[0]
    queries = data[1:1 + q]
    top = max(queries)
    length = [0] * (top + 1)
    length[1] = 1
    # TODO: memoised chain lengths, best start for every prefix
    print("\\n".join("1 1" for _ in queries))

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    vector<int> queries(q);
    for (auto &x : queries) cin >> x;
    int top = *max_element(queries.begin(), queries.end());
    vector<int> length(top + 1, 0);
    length[1] = 1;
    // TODO: memoised chain lengths, best start for every prefix
    for (int i = 0; i < q; i++) cout << "1 1\\n";
    return 0;
}
""",
        solution_python="""import sys

def main():
    data = list(map(int, sys.stdin.read().split()))
    q = data[0]
    queries = data[1:1 + q]
    top = max(queries)
    length = [0] * (top + 1)
    length[1] = 1
    for s in range(2, top + 1):
        x, steps = s, 0
        while x >= s:
            x = x >> 1 if x % 2 == 0 else 3 * x + 1
            steps += 1
        length[s] = steps + length[x]
    best_start = [1] * (top + 1)
    b = 1
    for s in range(2, top + 1):
        if length[s] > length[b]:
            b = s
        best_start[s] = b
    print("\\n".join(f"{best_start[n]} {length[best_start[n]]}" for n in queries))

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    vector<int> queries(q);
    for (auto &x : queries) cin >> x;
    int top = *max_element(queries.begin(), queries.end());
    vector<int> length(top + 1, 0), bestStart(top + 1, 1);
    length[1] = 1;
    for (int s = 2; s <= top; s++) {
        long long x = s;
        int steps = 0;
        while (x >= s) {
            x = (x % 2 == 0) ? x / 2 : 3 * x + 1;
            steps++;
        }
        length[s] = steps + length[x];
    }
    int b = 1;
    for (int s = 2; s <= top; s++) {
        if (length[s] > length[b]) b = s;
        bestStart[s] = b;
    }
    for (int n : queries) cout << bestStart[n] << " " << length[bestStart[n]] << "\\n";
    return 0;
}
""",
    ),
    dict(
        id="unique-perimeter-right-triangles",
        title="Singular Right Triangles",
        difficulty="expert",
        category="Number Theory",
        tags=["pythagorean-triples", "euclid-formula", "gcd", "sieve"],
        inspired_by="Project Euler #75 Singular integer right triangles",
        statement="""
A length of wire `L` can be bent into an integer-sided right triangle when
`a + b + c = L` and `a² + b² = c²` for positive integers `a < b < c`.
Some lengths work in exactly one way (12 → 3, 4, 5), some in several ways
(120 → (30, 40, 50), (20, 48, 52) and (24, 45, 51)), and some in none (20).

Answer `q` questions: how many lengths `L ≤ N` can be bent into an integer right
triangle in **exactly one** way?
""",
        input_format="""
First line: `q` (1 ≤ q ≤ 1100).
Next `q` lines: one integer `N` (1 ≤ N ≤ 10⁶).
""",
        output_format="For each question, one line with the count.",
        hints=[
            "Enumerating `a` and `b` is far too slow. Use **Euclid's formula**: every *primitive* triple (gcd 1) is "
            "`a = m² − n², b = 2mn, c = m² + n²` for exactly one pair `m > n > 0` with `gcd(m, n) = 1` and `m − n` odd.",
            "Its perimeter is `2m(m + n)`. Every triple is a multiple `k·(primitive)`, so its perimeter is a multiple of a primitive perimeter.",
            "Keep an array `ways[0..top]`: for each primitive perimeter `p ≤ top`, add 1 to `ways[p], ways[2p], ways[3p], …`. "
            "`m` only goes up to about `√(top / 2)`.",
            "Finally build a prefix count of the lengths with `ways[L] == 1` and answer each question by lookup.",
        ],
        samples=["3\n12\n50\n120"],
        tests=["2\n1\n11", "1\n1000000", "3\n24\n30\n60"],
        gen=_gen_perimeter,
        starter_python="""import sys
from math import gcd

def main():
    data = list(map(int, sys.stdin.read().split()))
    q = data[0]
    queries = data[1:1 + q]
    top = max(queries)
    ways = [0] * (top + 1)
    # TODO: Euclid's formula for primitive triples, mark multiples, prefix counts
    print("\\n".join("0" for _ in queries))

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    vector<int> queries(q);
    for (auto &x : queries) cin >> x;
    int top = *max_element(queries.begin(), queries.end());
    vector<int> ways(top + 1, 0);
    // TODO: Euclid's formula for primitive triples (std::gcd), mark multiples, prefix counts
    for (int i = 0; i < q; i++) cout << 0 << "\\n";
    return 0;
}
""",
        solution_python="""import sys
from math import gcd
from itertools import accumulate

def main():
    data = list(map(int, sys.stdin.read().split()))
    q = data[0]
    queries = data[1:1 + q]
    top = max(queries)
    ways = [0] * (top + 1)
    m = 2
    while 2 * m * (m + 1) <= top:
        for n in range(1 + (m & 1), m, 2):        # m - n odd
            p = 2 * m * (m + n)
            if p > top:
                break
            if gcd(m, n) == 1:
                for L in range(p, top + 1, p):
                    ways[L] += 1
        m += 1
    pref = list(accumulate(1 if w == 1 else 0 for w in ways))
    print("\\n".join(str(pref[n]) for n in queries))

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    vector<int> queries(q);
    for (auto &x : queries) cin >> x;
    int top = *max_element(queries.begin(), queries.end());
    vector<int> ways(top + 1, 0);
    for (long long m = 2; 2 * m * (m + 1) <= top; m++)
        for (long long n = 1 + (m & 1); n < m; n += 2) {
            long long p = 2 * m * (m + n);
            if (p > top) break;
            if (std::gcd(m, n) != 1) continue;
            for (long long L = p; L <= top; L += p) ways[L]++;
        }
    vector<int> pref(top + 1, 0);
    for (int L = 1; L <= top; L++) pref[L] = pref[L - 1] + (ways[L] == 1);
    for (int n : queries) cout << pref[n] << "\\n";
    return 0;
}
""",
    ),
]
