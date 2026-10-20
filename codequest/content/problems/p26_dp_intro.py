"""Dynamic Programming, first steps: 1-D recurrences, coin change, LCS, grids, knapsack."""


def _arr(xs):
    return " ".join(map(str, xs))


def _stairs_gen(rng):
    qs = [rng.randint(1, 10**5) for _ in range(30)] + [rng.randint(1, 50) for _ in range(10)]
    return [f"{len(qs)}\n" + "\n".join(map(str, qs))]


def _rob_gen(rng):
    out = []
    for n, lim in ((1, 10), (2, 10), (7, 100), (300, 10**4), (3000, 10**9)):
        out.append(f"{n}\n{_arr(rng.randint(0, lim) for _ in range(n))}")
    return out


def _coins_gen(rng):
    out = []
    for n, cmax, amount in ((1, 10, 30), (3, 20, 100), (5, 50, 999), (10, 500, 10**4), (20, 10**4, 10**4)):
        coins = rng.sample(range(1, cmax + 1), n)
        out.append(f"{n} {amount}\n{_arr(coins)}")
    # only even coins and an odd amount: impossible
    out.append(f"4 9999\n{_arr([2, 6, 10, 14])}")
    return out


def _lcs_gen(rng):
    out = []
    for n, m, alpha in ((1, 1, "ab"), (8, 6, "abc"), (60, 80, "acgt"), (500, 500, "acgt"),
                        (450, 500, "abcdefghijklmnopqrstuvwxyz")):
        a = "".join(rng.choice(alpha) for _ in range(n))
        b = "".join(rng.choice(alpha) for _ in range(m))
        out.append(f"{a}\n{b}")
    return out


def _grid_case(rng, r, c, p):
    rows = []
    for i in range(r):
        rows.append("".join("#" if rng.random() < p and (i, j) not in ((0, 0), (r - 1, c - 1)) else "."
                            for j in range(c)))
    return f"{r} {c}\n" + "\n".join(rows)


def _grid_gen(rng):
    return [_grid_case(rng, 1, 1, 0), _grid_case(rng, 3, 7, 0.1), _grid_case(rng, 20, 20, 0.15),
            _grid_case(rng, 100, 100, 0.0), _grid_case(rng, 80, 100, 0.08), _grid_case(rng, 60, 60, 0.45)]


def _knap_gen(rng):
    out = []
    for n, W, wmax in ((1, 10, 20), (5, 20, 10), (20, 100, 40), (50, 5000, 1000), (60, 5000, 300),
                       (40, 3000, 5000)):
        items = [f"{rng.randint(1, wmax)} {rng.randint(1, 10**6)}" for _ in range(n)]
        out.append(f"{n} {W}\n" + "\n".join(items))
    return out


PROBLEMS = [
    dict(
        id="stairway-step-ways",
        title="Stairway Step Ways",
        difficulty="easy",
        category="Dynamic Programming",
        tags=["dp", "fibonacci", "modulo"],
        inspired_by="LeetCode #70 Climbing Stairs; CSES Dice Combinations",
        statement="""
You climb a staircase of `n` steps. Each move you go up either **1** or **2**
steps. In how many different ways can you reach the top?

For `n = 3` there are 3 ways: `1+1+1`, `1+2`, `2+1`.

The counts grow very fast, so print each answer **modulo 1 000 000 007**.
There are several queries — compute the table once and answer them all.
""",
        input_format="First line: `t` (1 ≤ t ≤ 100). Next `t` lines: `n` (1 ≤ n ≤ 10⁵).",
        output_format="For each query, the number of ways modulo 10⁹ + 7.",
        hints=[
            "The last move onto step `n` was either a 1-step (from `n − 1`) or a 2-step (from `n − 2`). "
            "So `ways[n] = ways[n − 1] + ways[n − 2]`.",
            "Base cases: `ways[0] = 1` (standing at the bottom is one way) and `ways[1] = 1`.",
            "Build `ways` up to the largest `n` asked, taking `% 1_000_000_007` after every addition "
            "(C++: `const long long MOD = 1e9 + 7;`).",
        ],
        samples=["3\n1\n3\n5"],
        tests=["1\n2", "2\n10\n45", "1\n100000"],
        gen=_stairs_gen,
        starter_python="""MOD = 10**9 + 7
t = int(input())
qs = [int(input()) for _ in range(t)]
N = max(qs)
ways = [0] * (N + 1)
# TODO: fill the table
for n in qs:
    print(ways[n])
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    const long long MOD = 1000000007LL;
    int t;
    cin >> t;
    vector<int> qs(t);
    for (auto &q : qs) cin >> q;
    int N = *max_element(qs.begin(), qs.end());
    vector<long long> ways(N + 1, 0);
    // TODO: fill the table
    for (int n : qs) cout << ways[n] << "\\n";
    return 0;
}
""",
        solution_python=r"""MOD = 10**9 + 7
t = int(input())
qs = [int(input()) for _ in range(t)]
N = max(qs)
ways = [0] * (N + 1)
ways[0] = 1
ways[1] = 1
for i in range(2, N + 1):
    ways[i] = (ways[i - 1] + ways[i - 2]) % MOD
print("\n".join(str(ways[n]) for n in qs))
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    const long long MOD = 1000000007LL;
    int t;
    cin >> t;
    vector<int> qs(t);
    for (auto &q : qs) cin >> q;
    int N = *max_element(qs.begin(), qs.end());
    vector<long long> ways(N + 2, 0);
    ways[0] = ways[1] = 1;
    for (int i = 2; i <= N; i++) ways[i] = (ways[i - 1] + ways[i - 2]) % MOD;
    for (int n : qs) cout << ways[n] << "\n";
    return 0;
}
""",
    ),
    dict(
        id="quiet-street-heist",
        title="Quiet Street Heist",
        difficulty="medium",
        category="Dynamic Programming",
        tags=["dp", "house-robber"],
        inspired_by="LeetCode #198 House Robber",
        statement="""
A cat burglar plans a night on a street of `n` houses in a row. House `i` holds
`v[i]` coins. The houses have connected alarms: robbing **two adjacent houses**
triggers them.

What is the most money the burglar can take without ever robbing two
neighbouring houses?

For `2 7 9 3 1` the best is houses 1, 3 and 5: `2 + 9 + 1 = 12`.
""",
        input_format="First line: `n` (1 ≤ n ≤ 3000). Second line: `n` integers (0 ≤ vᵢ ≤ 10⁹).",
        output_format="One integer: the maximum total.",
        hints=[
            "Let `best[i]` be the best total using only the first `i` houses. For house `i` you either skip it "
            "(`best[i − 1]`) or rob it (`best[i − 2] + v[i]`).",
            "So `best[i] = max(best[i − 1], best[i − 2] + v[i])`. You only ever need the last two values — two "
            "variables are enough.",
            "Totals can reach 1.5·10¹² — use `long long` in C++.",
        ],
        samples=["5\n2 7 9 3 1", "4\n1 2 3 1"],
        tests=["1\n5", "2\n4 9", "3\n0 0 0", "6\n10 1 1 10 1 10", "3\n1000000000 1000000000 1000000000"],
        gen=_rob_gen,
        starter_python="""n = int(input())
v = list(map(int, input().split()))
prev2 = 0   # best total up to house i-2
prev1 = 0   # best total up to house i-1
for x in v:
    # TODO: update prev2, prev1
    pass
print(prev1)
""",
        starter_cpp="""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> v(n);
    for (auto &x : v) cin >> x;
    long long prev2 = 0, prev1 = 0;
    // TODO: one pass with the recurrence
    cout << prev1 << "\\n";
    return 0;
}
""",
        solution_python=r"""n = int(input())
v = list(map(int, input().split()))
prev2 = prev1 = 0
for x in v:
    prev2, prev1 = prev1, max(prev1, prev2 + x)
print(prev1)
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> v(n);
    for (auto &x : v) cin >> x;
    long long prev2 = 0, prev1 = 0;
    for (long long x : v) {
        long long cur = max(prev1, prev2 + x);
        prev2 = prev1;
        prev1 = cur;
    }
    cout << prev1 << "\n";
    return 0;
}
""",
    ),
    dict(
        id="fewest-coins-any-system",
        title="Fewest Coins, Any System",
        difficulty="medium",
        category="Dynamic Programming",
        tags=["dp", "coin-change", "unbounded-knapsack"],
        inspired_by="LeetCode #322 Coin Change; CSES Minimizing Coins",
        statement="""
A strange country uses `n` coin values `c₁ … cₙ` (you have unlimited coins of
each). Pay exactly `A` with the **fewest coins**, or report `-1` if `A` can't
be paid at all.

Greedy fails here: with coins `1 3 4` and `A = 6`, "biggest coin first" uses
`4+1+1` (3 coins), but `3+3` needs only **2**.
""",
        input_format="""First line: `n A` (1 ≤ n ≤ 20, 0 ≤ A ≤ 10⁴).
Second line: `n` distinct coin values (1 ≤ cᵢ ≤ 10⁴).""",
        output_format="One integer: the minimum number of coins, or `-1`.",
        hints=[
            "Let `dp[x]` = fewest coins that pay exactly `x`. Then `dp[0] = 0` and "
            "`dp[x] = 1 + min(dp[x − c])` over all coins `c <= x`.",
            "Fill `dp` for `x = 1, 2, …, A` in increasing order, so the smaller amounts are ready when you need them. "
            "Use a big sentinel such as `INF = A + 1` for 'impossible'.",
            "The table has `A + 1` entries and each looks at `n` coins: O(n·A) time. If `dp[A]` is still `INF`, print `-1`.",
        ],
        samples=["3 6\n1 3 4", "1 3\n2", "3 11\n1 2 5"],
        tests=["1 0\n7", "2 7\n2 4", "3 10000\n1 9999 5000", "4 63\n1 5 10 21", "2 1\n2 3"],
        gen=_coins_gen,
        starter_python="""n, A = map(int, input().split())
coins = list(map(int, input().split()))
INF = A + 1
dp = [INF] * (A + 1)
dp[0] = 0
# TODO: fill dp[1..A]
print(dp[A] if dp[A] < INF else -1)
""",
        starter_cpp="""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, A;
    cin >> n >> A;
    vector<int> coins(n);
    for (auto &c : coins) cin >> c;
    const int INF = A + 1;
    vector<int> dp(A + 1, INF);
    dp[0] = 0;
    // TODO: fill dp[1..A]
    cout << (dp[A] < INF ? dp[A] : -1) << "\\n";
    return 0;
}
""",
        solution_python=r"""n, A = map(int, input().split())
coins = list(map(int, input().split()))
INF = A + 1
dp = [INF] * (A + 1)
dp[0] = 0
for c in coins:
    for x in range(c, A + 1):
        y = dp[x - c] + 1
        if y < dp[x]:
            dp[x] = y
print(dp[A] if dp[A] < INF else -1)
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n, A;
    cin >> n >> A;
    vector<int> coins(n);
    for (auto &c : coins) cin >> c;
    const int INF = A + 1;
    vector<int> dp(A + 1, INF);
    dp[0] = 0;
    for (int x = 1; x <= A; x++)
        for (int c : coins)
            if (c <= x) dp[x] = min(dp[x], dp[x - c] + 1);
    cout << (dp[A] < INF ? dp[A] : -1) << "\n";
    return 0;
}
""",
    ),
    dict(
        id="common-subsequence-length",
        title="Longest Common Subsequence",
        difficulty="medium",
        category="Dynamic Programming",
        tags=["dp", "strings", "2d-dp", "lcs"],
        inspired_by="LeetCode #1143 Longest Common Subsequence; AtCoder DP F",
        statement="""
A **subsequence** of a string is what's left after deleting any characters
(possibly none) without reordering the rest: `ace` is a subsequence of
`abcde`, but `aec` is not.

Given two strings, find the length of their **longest common subsequence**
(LCS). This is the core of tools like `diff` and of DNA sequence comparison.

For `abcde` and `ace` the LCS is `ace`, length **3**.
""",
        input_format="Two lines, each a non-empty string of lowercase letters (length ≤ 500).",
        output_format="One integer: the length of the LCS.",
        hints=[
            "Let `dp[i][j]` = LCS length of the first `i` characters of `a` and the first `j` of `b`. "
            "Row 0 and column 0 are all zeros.",
            "If `a[i−1] == b[j−1]` the characters can be matched: `dp[i][j] = dp[i−1][j−1] + 1`. "
            "Otherwise drop one of them: `dp[i][j] = max(dp[i−1][j], dp[i][j−1])`.",
            "The answer is `dp[n][m]`. Each row only depends on the previous row, so two 1-D lists are enough "
            "(and faster in Python).",
        ],
        samples=["abcde\nace", "abc\ndef"],
        tests=["a\na", "a\nb", "abab\nbaba", "aaaa\naa", "programming\ngaming"],
        gen=_lcs_gen,
        starter_python="""a = input().strip()
b = input().strip()
n, m = len(a), len(b)
dp = [[0] * (m + 1) for _ in range(n + 1)]
# TODO: fill the table
print(dp[n][m])
""",
        starter_cpp="""#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    string a, b;
    cin >> a >> b;
    int n = a.size(), m = b.size();
    vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
    // TODO: fill the table
    cout << dp[n][m] << "\\n";
    return 0;
}
""",
        solution_python=r"""a = input().strip()
b = input().strip()
m = len(b)
prev = [0] * (m + 1)
for ch in a:
    cur = [0] * (m + 1)
    for j in range(1, m + 1):
        if ch == b[j - 1]:
            cur[j] = prev[j - 1] + 1
        else:
            cur[j] = prev[j] if prev[j] > cur[j - 1] else cur[j - 1]
    prev = cur
print(prev[m])
""",
        solution_cpp=r"""#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    string a, b;
    cin >> a >> b;
    int n = a.size(), m = b.size();
    vector<vector<int>> dp(n + 1, vector<int>(m + 1, 0));
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= m; j++)
            dp[i][j] = (a[i - 1] == b[j - 1]) ? dp[i - 1][j - 1] + 1
                                              : max(dp[i - 1][j], dp[i][j - 1]);
    cout << dp[n][m] << "\n";
    return 0;
}
""",
    ),
    dict(
        id="blocked-grid-routes",
        title="Blocked Grid Routes",
        difficulty="medium",
        category="Dynamic Programming",
        tags=["dp", "grid", "counting", "modulo"],
        inspired_by="LeetCode #62 / #63 Unique Paths (II); CSES Grid Paths",
        statement="""
A robot starts in the top-left cell of an `R × C` grid and wants to reach the
bottom-right cell. It may only move **right** or **down**, and it can't enter
cells marked `#`.

How many different routes are there? Print the answer **modulo
1 000 000 007** (on an empty 100 × 100 grid there are about 2.3·10⁵⁸ routes!).
""",
        input_format="""First line: `R C` (1 ≤ R, C ≤ 100).
Next `R` lines: `C` characters each, `.` (free) or `#` (blocked).""",
        output_format="One integer: the number of routes modulo 10⁹ + 7 (0 if there are none).",
        hints=[
            "Every route into cell `(i, j)` arrives either from above or from the left: "
            "`ways[i][j] = ways[i−1][j] + ways[i][j−1]`.",
            "A blocked cell has `ways = 0`. The start has `ways = 1` unless it is blocked itself.",
            "Fill the table row by row, left to right, so both neighbours are done before you need them. "
            "Reduce `% 1_000_000_007` after each addition.",
        ],
        samples=["3 3\n...\n.#.\n...", "2 2\n.#\n#."],
        tests=["1 1\n.", "1 1\n#", "1 5\n.....", "3 3\n...\n...\n..#", "2 3\n...\n..."],
        gen=_grid_gen,
        starter_python="""MOD = 10**9 + 7
R, C = map(int, input().split())
grid = [input().strip() for _ in range(R)]
ways = [[0] * C for _ in range(R)]
# TODO: fill ways[i][j] row by row
print(ways[R - 1][C - 1])
""",
        starter_cpp="""#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    const long long MOD = 1000000007LL;
    int R, C;
    cin >> R >> C;
    vector<string> g(R);
    for (auto &row : g) cin >> row;
    vector<vector<long long>> ways(R, vector<long long>(C, 0));
    // TODO: fill ways[i][j] row by row
    cout << ways[R - 1][C - 1] << "\\n";
    return 0;
}
""",
        solution_python=r"""MOD = 10**9 + 7
R, C = map(int, input().split())
grid = [input().strip() for _ in range(R)]
ways = [0] * C
for i in range(R):
    row = grid[i]
    for j in range(C):
        if row[j] == "#":
            ways[j] = 0
        elif i == 0 and j == 0:
            ways[j] = 1
        elif j > 0:
            ways[j] = (ways[j] + ways[j - 1]) % MOD
print(ways[C - 1])
""",
        solution_cpp=r"""#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    const long long MOD = 1000000007LL;
    int R, C;
    cin >> R >> C;
    vector<string> g(R);
    for (auto &row : g) cin >> row;
    vector<vector<long long>> ways(R, vector<long long>(C, 0));
    for (int i = 0; i < R; i++)
        for (int j = 0; j < C; j++) {
            if (g[i][j] == '#') continue;
            if (i == 0 && j == 0) { ways[i][j] = 1; continue; }
            long long w = 0;
            if (i > 0) w += ways[i - 1][j];
            if (j > 0) w += ways[i][j - 1];
            ways[i][j] = w % MOD;
        }
    cout << ways[R - 1][C - 1] << "\n";
    return 0;
}
""",
    ),
    dict(
        id="backpack-weight-limit",
        title="Backpack Weight Limit",
        difficulty="medium",
        category="Dynamic Programming",
        tags=["dp", "knapsack", "0-1-knapsack"],
        inspired_by="Classic 0/1 knapsack; AtCoder DP D; CSES Book Shop",
        statement="""
You're packing for a hike. There are `n` items; item `i` weighs `w[i]` and is
worth `v[i]` to you. Your backpack holds a total weight of at most `W`.

Each item is taken **whole or not at all** (and at most once). What is the
greatest total value you can carry?

With `W = 10` and items `(5, 10) (4, 40) (6, 30) (3, 50)` (weight, value), the
best choice is items 2 and 4: weight 7, value **90**.

There are up to 2⁶⁰ subsets of items — far too many to try. DP over the
capacity handles it in O(n·W).
""",
        input_format="""First line: `n W` (1 ≤ n ≤ 60, 1 ≤ W ≤ 5000).
Next `n` lines: `w v` (1 ≤ w ≤ 5000, 1 ≤ v ≤ 10⁶).""",
        output_format="One integer: the maximum total value.",
        hints=[
            "Let `best[c]` = the highest value achievable with total weight at most `c`, using the items seen so far. "
            "Start with all zeros.",
            "Adding item `(w, v)`: `best[c] = max(best[c], best[c − w] + v)` for every `c >= w`.",
            "Loop `c` **downwards** (from `W` to `w`) so each item is used at most once — going upwards would let the "
            "same item be added again and again. Values can sum to 6·10⁷, still fine for `int`, but `long long` is safe.",
        ],
        samples=["4 10\n5 10\n4 40\n6 30\n3 50", "1 3\n4 100"],
        tests=["1 5\n5 7", "3 5\n1 1\n1 1\n1 1", "2 5000\n5000 1000000\n2500 600000",
               "3 50\n10 60\n20 100\n30 120"],
        gen=_knap_gen,
        starter_python="""n, W = map(int, input().split())
items = [tuple(map(int, input().split())) for _ in range(n)]
best = [0] * (W + 1)
for w, v in items:
    # TODO: update best[] for this item (careful with the loop direction!)
    pass
print(best[W])
""",
        starter_cpp="""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, W;
    cin >> n >> W;
    vector<long long> best(W + 1, 0);
    for (int i = 0; i < n; i++) {
        int w;
        long long v;
        cin >> w >> v;
        // TODO: update best[] for this item (careful with the loop direction!)
    }
    cout << best[W] << "\\n";
    return 0;
}
""",
        solution_python=r"""n, W = map(int, input().split())
items = [tuple(map(int, input().split())) for _ in range(n)]
best = [0] * (W + 1)
for w, v in items:
    if w > W:
        continue
    # vectorised update: new[c] = max(old[c], old[c - w] + v) for c >= w
    shifted = [x + v for x in best[:W + 1 - w]]
    best[w:] = [a if a > b else b for a, b in zip(best[w:], shifted)]
print(best[W])
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n, W;
    cin >> n >> W;
    vector<long long> best(W + 1, 0);
    for (int i = 0; i < n; i++) {
        int w;
        long long v;
        cin >> w >> v;
        for (int c = W; c >= w; c--) best[c] = max(best[c], best[c - w] + v);
    }
    cout << best[W] << "\n";
    return 0;
}
""",
    ),
]
