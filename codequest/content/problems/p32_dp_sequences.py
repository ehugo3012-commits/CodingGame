"""Hard dynamic programming on sequences: edit distance, LIS, interval DP, value-indexed knapsack."""


def _rand_word(rng, n, alpha):
    return "".join(rng.choice(alpha) for _ in range(n))


def _gen_edit(rng):
    tests = []
    for la, lb, alpha, costs in [(800, 800, "ab", (1, 1, 1)), (800, 760, "acgt", (3, 2, 4)),
                                 (700, 800, "abcdefghijklmnopqrstuvwxyz", (5, 5, 100)),
                                 (300, 20, "xyz", (7, 1, 3)), (1, 800, "ab", (2, 9, 4))]:
        a = _rand_word(rng, la, alpha)
        if rng.random() < 0.5:
            # b is a mutated copy of a: makes the alignment interesting
            b = list(a[:lb]) + [rng.choice(alpha) for _ in range(max(0, lb - la))]
            for _ in range(lb // 10):
                b[rng.randrange(len(b))] = rng.choice(alpha)
            b = "".join(b)
        else:
            b = _rand_word(rng, lb, alpha)
        tests.append(f"{costs[0]} {costs[1]} {costs[2]}\n{a}\n{b}")
    return tests


def _gen_lis(rng):
    tests = []
    for n, m in [(200000, 1000000007), (200000, 999999937), (150000, 1000), (200000, 2147483), (5, 7)]:
        a = rng.randint(2, m - 1)
        c = rng.randint(0, m - 1)
        s = rng.randint(0, m - 1)
        tests.append(f"{n} {s} {a} {c} {m}")
    tests.append("200000 0 1 1 1000000000")      # strictly increasing
    tests.append("200000 0 1 7919 1000000000")   # increasing runs with one wrap-around
    tests.append("200000 5 1 999999999 1000000000")  # strictly decreasing
    return tests


def _gen_chain(rng):
    tests = []
    for n, hi in [(120, 1000), (120, 10), (100, 1000), (60, 500)]:
        tests.append(f"{n}\n" + " ".join(str(rng.randint(1, hi)) for _ in range(n + 1)))
    return tests


def _gen_knapsack(rng):
    tests = []
    for n, wmax, vmax, wcap in [(100, 10**9, 200, 10**9), (100, 10**9, 200, 3 * 10**10 // 1000),
                                (100, 10**6, 200, 5 * 10**6), (80, 10**9, 50, 10**9),
                                (100, 10**9, 200, 10**3)]:
        wcap = min(wcap, 10**9)
        items = [(rng.randint(1, wmax), rng.randint(1, vmax)) for _ in range(n)]
        tests.append(f"{n} {wcap}\n" + "\n".join(f"{w} {v}" for w, v in items))
    return tests


PROBLEMS = [
    dict(
        id="weighted-edit-distance",
        title="Weighted Edit Distance",
        difficulty="hard",
        category="Dynamic Programming",
        tags=["dp", "strings", "levenshtein"],
        inspired_by="LeetCode #72 Edit Distance / CSES 1639 Edit Distance",
        statement="""
A spelling corrector turns a word `a` into a word `b` with three operations,
each with its own price:

* **insert** one character anywhere — costs `I`,
* **delete** one character — costs `D`,
* **replace** one character by a different one — costs `S`.

Find the minimum total price to transform `a` into `b`. (Replacing can be more
expensive than deleting and inserting — the cheapest plan must account for that.)
""",
        input_format="""
First line: `I D S` (1 ≤ I, D, S ≤ 100).
Second line: the word `a`; third line: the word `b`.
Both consist of lowercase letters, 1 ≤ |a|, |b| ≤ 800.
""",
        output_format="One integer: the minimum total cost.",
        hints=[
            "Classic 2-D DP: let `dp[i][j]` = cheapest way to turn the first `i` letters of `a` into the first `j` letters of `b`.",
            "Borders: `dp[0][j] = j·I` (insert everything), `dp[i][0] = i·D` (delete everything).",
            "Transition: `dp[i][j] = min(dp[i−1][j] + D, dp[i][j−1] + I, dp[i−1][j−1] + (0 if a[i−1] == b[j−1] else S))`.",
            "Each row only needs the previous row, so two 1-D arrays of length |b|+1 are enough.",
        ],
        samples=[
            "1 1 1\nhorse\nros",
            "1 1 5\nkitten\nsitting",
        ],
        tests=[
            "1 1 1\na\na",
            "3 4 5\na\nb",
            "10 1 1\nabcdef\nabc",
            "1 10 1\nabc\nabcdef",
            "2 3 100\nzzzz\nyyyy",
        ],
        gen=_gen_edit,
        starter_python="""import sys

def main():
    data = sys.stdin.read().split()
    I, D, S = int(data[0]), int(data[1]), int(data[2])
    a, b = data[3], data[4]
    # TODO: dp over prefixes of a and b
    print(0)

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    long long I, D, S;
    string a, b;
    cin >> I >> D >> S >> a >> b;
    // TODO: dp over prefixes of a and b
    cout << 0 << "\\n";
    return 0;
}
""",
        solution_python="""import sys

def main():
    data = sys.stdin.read().split()
    I, D, S = int(data[0]), int(data[1]), int(data[2])
    a, b = data[3], data[4]
    m = len(b)
    prev = [j * I for j in range(m + 1)]
    for i in range(1, len(a) + 1):
        ai = a[i - 1]
        cur = [i * D] + [0] * m
        for j in range(1, m + 1):
            best = prev[j - 1] + (0 if ai == b[j - 1] else S)
            t = prev[j] + D
            if t < best:
                best = t
            t = cur[j - 1] + I
            if t < best:
                best = t
            cur[j] = best
        prev = cur
    print(prev[m])

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    long long I, D, S;
    string a, b;
    cin >> I >> D >> S >> a >> b;
    int n = a.size(), m = b.size();
    vector<long long> prev(m + 1), cur(m + 1);
    for (int j = 0; j <= m; j++) prev[j] = j * I;
    for (int i = 1; i <= n; i++) {
        cur[0] = i * D;
        for (int j = 1; j <= m; j++) {
            long long best = prev[j - 1] + (a[i - 1] == b[j - 1] ? 0 : S);
            best = min(best, prev[j] + D);
            best = min(best, cur[j - 1] + I);
            cur[j] = best;
        }
        swap(prev, cur);
    }
    cout << prev[m] << "\\n";
    return 0;
}
""",
    ),
    dict(
        id="lis-generated-sequence",
        title="Longest Rising Signal",
        difficulty="hard",
        category="Dynamic Programming",
        tags=["lis", "binary-search", "patience-sorting"],
        inspired_by="LeetCode #300 Longest Increasing Subsequence / CSES 1145 Increasing Subsequence",
        statement="""
A sensor produces a very long stream of readings, too long to list in the
input, so it is described by a pseudo-random generator:

```
x₀ = s
xᵢ = (a · xᵢ₋₁ + c) mod m     for i = 1, 2, …, n
```

The readings are `x₁, x₂, …, xₙ` (note: `x₀` itself is **not** a reading).

Find the length of the **longest strictly increasing subsequence** of the
readings (pick readings in their original order, each larger than the previous).

With n up to 2·10⁵ the classic O(n²) DP is far too slow.
""",
        input_format="""
One line: `n s a c m` (1 ≤ n ≤ 2·10⁵, 1 ≤ m ≤ 2·10⁹, 0 ≤ s, a, c < m).
""",
        output_format="One integer: the length of the longest strictly increasing subsequence.",
        hints=[
            "Generate the readings with a loop; in C++ use `long long` for `a * x` (up to 4·10¹⁸, still below the 9.2·10¹⁸ limit).",
            "The O(n log n) method keeps `tails[L]` = the **smallest** possible last value of an increasing "
            "subsequence of length `L + 1` seen so far. This array is always sorted.",
            "For each new value `x`, find the first position in `tails` holding a value **≥ x** "
            "(binary search). Replace it with `x`, or append `x` if there is none. The answer is `len(tails)`.",
            "Python: `bisect.bisect_left(tails, x)`. C++: `lower_bound(tails.begin(), tails.end(), x)`. "
            "(`lower_bound`, not `upper_bound`, because the subsequence must be *strictly* increasing.)",
        ],
        samples=[
            "8 1 3 1 10",
            "6 0 1 2 100",
        ],
        tests=[
            "1 0 0 0 1",
            "100 0 0 0 1",
            "10 3 0 7 10",
            "20 1 2 0 1000000000",
        ],
        gen=_gen_lis,
        starter_python="""import sys
from bisect import bisect_left

def main():
    n, s, a, c, m = map(int, sys.stdin.read().split())
    x = s
    for _ in range(n):
        x = (a * x + c) % m
        # TODO: process reading x
    print(0)

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    long long n, s, a, c, m;
    cin >> n >> s >> a >> c >> m;
    long long x = s;
    for (long long i = 0; i < n; i++) {
        x = (a * x + c) % m;
        // TODO: process reading x
    }
    cout << 0 << "\\n";
    return 0;
}
""",
        solution_python="""import sys
from bisect import bisect_left

def main():
    n, s, a, c, m = map(int, sys.stdin.read().split())
    x = s
    tails = []
    for _ in range(n):
        x = (a * x + c) % m
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    print(len(tails))

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    long long n, s, a, c, m;
    cin >> n >> s >> a >> c >> m;
    long long x = s;
    vector<long long> tails;
    for (long long i = 0; i < n; i++) {
        x = (a * x + c) % m;
        auto it = lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) tails.push_back(x);
        else *it = x;
    }
    cout << tails.size() << "\\n";
    return 0;
}
""",
    ),
    dict(
        id="matrix-chain-order",
        title="Cheapest Matrix Chain",
        difficulty="hard",
        category="Dynamic Programming",
        tags=["interval-dp", "matrix-chain"],
        inspired_by="CLRS Matrix-Chain Multiplication / AtCoder DP Contest N (Slimes)",
        statement="""
You must compute the product `A₁ · A₂ · … · Aₙ` of `n` matrices, where `Aᵢ`
has `pᵢ₋₁` rows and `pᵢ` columns. Matrix multiplication is associative, so you
may choose any parenthesisation; multiplying an `x × y` matrix by a `y × z`
matrix costs `x · y · z` scalar multiplications.

Find the minimum total number of scalar multiplications.
""",
        input_format="""
First line: `n` (1 ≤ n ≤ 120).
Second line: `n + 1` integers `p₀ p₁ … pₙ` (1 ≤ pᵢ ≤ 1000).
""",
        output_format="One integer: the minimum cost (0 when n = 1).",
        hints=[
            "**Interval DP**: let `dp[i][j]` = cheapest cost to multiply `Aᵢ … Aⱼ` into one matrix "
            "(of size `pᵢ₋₁ × pⱼ`). Single matrices cost 0.",
            "The last multiplication splits the range at some `k` (i ≤ k < j): "
            "`dp[i][j] = min over k of dp[i][k] + dp[k+1][j] + p[i−1]·p[k]·p[j]`.",
            "Fill the table by increasing interval **length**, so both halves are already known. "
            "Total work is about n³/6 — fine for n = 120.",
            "Costs reach ~10¹¹: use `long long` in C++. Python: `min(... for k in range(i, j))` keeps the inner loop short.",
        ],
        samples=[
            "3\n10 30 5 60",
            "4\n40 20 30 10 30",
        ],
        tests=[
            "1\n5 7",
            "2\n1 1000 1",
            "2\n1000 1000 1000",
            "5\n5 4 3 2 1 6",
        ],
        gen=_gen_chain,
        starter_python="""import sys

def main():
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    p = data[1:n + 2]
    # TODO: interval DP over dp[i][j]
    print(0)

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> p(n + 1);
    for (auto &x : p) cin >> x;
    // TODO: interval DP over dp[i][j]
    cout << 0 << "\\n";
    return 0;
}
""",
        solution_python="""import sys

def main():
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    p = data[1:n + 2]
    # dp[i][j] for matrices i..j (0-based); col[j][i] mirrors dp[i][j] for fast column access
    dp = [[0] * n for _ in range(n)]
    col = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            row, cj = dp[i], col[j]
            a, c = p[i], p[j + 1]
            best = min(row[k] + cj[k + 1] + a * p[k + 1] * c for k in range(i, j))
            row[j] = best
            cj[i] = best
    print(dp[0][n - 1])

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> p(n + 1);
    for (auto &x : p) cin >> x;
    vector<vector<long long>> dp(n, vector<long long>(n, 0));
    for (int len = 2; len <= n; len++)
        for (int i = 0; i + len - 1 < n; i++) {
            int j = i + len - 1;
            long long best = -1;
            for (int k = i; k < j; k++) {
                long long c = dp[i][k] + dp[k + 1][j] + p[i] * p[k + 1] * p[j + 1];
                if (best < 0 || c < best) best = c;
            }
            dp[i][j] = best;
        }
    cout << dp[0][n - 1] << "\\n";
    return 0;
}
""",
    ),
    dict(
        id="knapsack-huge-capacity",
        title="Knapsack with a Huge Backpack",
        difficulty="hard",
        category="Dynamic Programming",
        tags=["knapsack", "dp", "change-the-state"],
        inspired_by="AtCoder Educational DP Contest E (Knapsack 2)",
        statement="""
There are `n` items; item `i` weighs `wᵢ` and is worth `vᵢ`. Choose a subset with
total weight **at most `W`** and maximum total value. Each item can be taken at
most once.

The twist: weights and the capacity are huge (up to 10⁹), so the textbook DP over
capacities is impossible. The values, however, are small.
""",
        input_format="""
First line: `n W` (1 ≤ n ≤ 100, 1 ≤ W ≤ 10⁹).
Next `n` lines: `wᵢ vᵢ` (1 ≤ wᵢ ≤ 10⁹, 1 ≤ vᵢ ≤ 200).
""",
        output_format="One integer: the maximum total value.",
        hints=[
            "Swap the roles of weight and value: the total value is at most 100 · 200 = 20 000, so index the DP by **value**.",
            "Let `dp[v]` = the minimum total weight needed to collect **exactly** value `v` (INF if impossible). "
            "`dp[0] = 0`.",
            "For each item, update `dp[v] = min(dp[v], dp[v − vᵢ] + wᵢ)` for `v` going **downwards** "
            "(so the item is used at most once) — or compute the whole new row from the old one.",
            "The answer is the largest `v` with `dp[v] ≤ W`. In C++ weights sum to 10¹¹: use `long long`.",
        ],
        samples=[
            "3 8\n3 30\n4 50\n5 60",
            "1 1000000000\n1000000000 10",
        ],
        tests=[
            "1 5\n6 100",
            "2 10\n10 1\n10 2",
            "6 15\n6 5\n5 6\n6 4\n6 6\n3 5\n7 2",
            "3 1000000000\n1000000000 200\n1000000000 200\n1 1",
        ],
        gen=_gen_knapsack,
        starter_python="""import sys

def main():
    data = list(map(int, sys.stdin.read().split()))
    n, W = data[0], data[1]
    items = [(data[2 + 2 * i], data[3 + 2 * i]) for i in range(n)]   # (weight, value)
    # TODO: dp[v] = minimum weight to reach value exactly v
    print(0)

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    long long W;
    cin >> n >> W;
    vector<long long> w(n);
    vector<int> v(n);
    for (int i = 0; i < n; i++) cin >> w[i] >> v[i];
    // TODO: dp[val] = minimum weight to reach value exactly val
    cout << 0 << "\\n";
    return 0;
}
""",
        solution_python="""import sys

def main():
    data = list(map(int, sys.stdin.read().split()))
    n, W = data[0], data[1]
    items = [(data[2 + 2 * i], data[3 + 2 * i]) for i in range(n)]
    total = sum(v for _, v in items)
    INF = 1 << 62
    dp = [0] + [INF] * total
    top = 0
    for w, v in items:
        top += v
        # new dp[val] = min(dp[val], old dp[val - v] + w); the slice on the right uses the OLD row
        dp[v:top + 1] = [x if x <= y + w else y + w for x, y in zip(dp[v:top + 1], dp[0:top + 1 - v])]
    print(max(val for val in range(total + 1) if dp[val] <= W))

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    long long W;
    cin >> n >> W;
    vector<long long> w(n);
    vector<int> v(n);
    int total = 0;
    for (int i = 0; i < n; i++) { cin >> w[i] >> v[i]; total += v[i]; }
    const long long INF = (long long)4e18;
    vector<long long> dp(total + 1, INF);
    dp[0] = 0;
    for (int i = 0; i < n; i++)
        for (int val = total; val >= v[i]; val--)
            if (dp[val - v[i]] != INF) dp[val] = min(dp[val], dp[val - v[i]] + w[i]);
    int best = 0;
    for (int val = 0; val <= total; val++) if (dp[val] <= W) best = val;
    cout << best << "\\n";
    return 0;
}
""",
    ),
]
