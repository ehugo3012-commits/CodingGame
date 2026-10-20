"""Expert dynamic programming: bitmask DP, digit DP, counting paths with inclusion-exclusion."""


def _gen_tsp(rng):
    tests = []
    for n, missing in [(15, 0.0), (15, 0.5), (14, 0.2), (13, 0.0), (2, 0.0), (15, 0.75)]:
        d = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    d[i][j] = -1 if rng.random() < missing else rng.randint(1, 10**6)
        tests.append(f"{n}\n" + "\n".join(" ".join(map(str, row)) for row in d))
    # one city with no incoming roads: no tour exists
    n = 12
    d = [[0 if i == j else rng.randint(1, 1000) for j in range(n)] for i in range(n)]
    for i in range(n):
        if i != 5:
            d[i][5] = -1
    tests.append(f"{n}\n" + "\n".join(" ".join(map(str, row)) for row in d))
    return tests


def _gen_digit(rng):
    lines = []
    for _ in range(25):
        D = rng.choice([1, 2, 3, 7, 9, 10, 11, 13, 17, 45, 50, 81, 99, 100, rng.randint(1, 100)])
        kind = rng.random()
        if kind < 0.5:
            L = rng.randint(1, 10**18)
            R = rng.randint(L, 10**18)
        elif kind < 0.8:
            e = rng.randint(1, 18)
            L = rng.randint(1, 10**e)
            R = rng.randint(L, 10**e)
        else:
            L = rng.randint(1, 10**6)
            R = L + rng.randint(0, 1000)
        lines.append(f"{L} {R} {D}")
    return [f"{len(lines)}\n" + "\n".join(lines)]


def _gen_sinkholes(rng):
    tests = []
    for H, W, N in [(100000, 100000, 800), (2000, 3000, 800), (100000, 1, 0), (300, 300, 800),
                    (100000, 99999, 500)]:
        cells = set()
        while len(cells) < N:
            if H <= 2000 or rng.random() < 0.5:
                r, c = rng.randint(1, H), rng.randint(1, W)
            else:
                # cluster near the diagonal so that many sinkholes interact
                t = rng.random()
                r = max(1, min(H, int(t * H) + rng.randint(-300, 300)))
                c = max(1, min(W, int(t * W) + rng.randint(-300, 300)))
            if (r, c) not in ((1, 1), (H, W)):
                cells.add((r, c))
        cells = list(cells)
        rng.shuffle(cells)
        tests.append(f"{H} {W} {N}\n" + "\n".join(f"{r} {c}" for r, c in cells))
    # a full wall in a small grid -> 0 paths
    H, W = 50, 50
    cells = [(25, c) for c in range(1, W + 1)]
    tests.append(f"{H} {W} {len(cells)}\n" + "\n".join(f"{r} {c}" for r, c in cells))
    return tests


PROBLEMS = [
    dict(
        id="bitmask-tsp-tour",
        title="Grand Tour of the Islands",
        difficulty="expert",
        category="Dynamic Programming",
        tags=["bitmask-dp", "tsp", "held-karp"],
        inspired_by="Held–Karp algorithm; AtCoder ABC 180 E / CSES 1690 Hamiltonian Flights",
        statement="""
A ferry company serves `n` islands. A tourist starts on island `1`, wants to
visit every other island **exactly once**, and finally return to island `1`.

Ferry lines are one-way and may be priced differently in each direction
(`cost[i][j]` need not equal `cost[j][i]`); some pairs have no ferry at all.
Find the cheapest possible grand tour, or print `-1` if none exists.

Trying all (n − 1)! orders is hopeless for n = 15.
""",
        input_format="""
First line: `n` (2 ≤ n ≤ 15).
Next `n` lines: `n` integers each; the `j`-th number of line `i` is the cost of the
ferry from island `i` to island `j` (1 ≤ cost ≤ 10⁶), or `-1` if there is no such ferry.
The diagonal is `0`.
""",
        output_format="One integer: the minimum tour cost, or `-1`.",
        hints=[
            "**Bitmask DP** (Held–Karp): describe a partial tour by the *set* of islands visited so far "
            "(an n-bit mask) and the island you are standing on. The order inside the set no longer matters!",
            "`dp[mask][j]` = cheapest way to start at island 0, visit exactly the islands in `mask`, and end at `j`. "
            "Start: `dp[1][0] = 0`.",
            "Transition: from `dp[mask][j]` take a ferry `j → k` with `k` not in `mask`: "
            "update `dp[mask | (1 << k)][k]`. Processing masks in increasing numeric order is a valid order.",
            "Answer: `min over j of dp[full][j] + cost[j][0]` (only where that ferry exists). "
            "That is O(2ⁿ · n²) ≈ 7·10⁶ steps. In Python, skip states equal to INF and pre-build each island's "
            "list of outgoing ferries.",
        ],
        samples=[
            "4\n0 10 15 20\n5 0 9 10\n6 13 0 12\n8 8 9 0",
            "3\n0 1 -1\n-1 0 1\n-1 1 0",
        ],
        tests=[
            "2\n0 5\n7 0",
            "2\n0 5\n-1 0",
            "3\n0 1 100\n100 0 1\n1 100 0",
            "4\n0 1 1 1\n1 0 1 1\n1 1 0 1\n1 1 1 0",
        ],
        gen=_gen_tsp,
        time_limit=3,
        starter_python="""import sys

def main():
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    cost = [data[1 + i * n: 1 + (i + 1) * n] for i in range(n)]   # -1 = no ferry
    # TODO: dp[mask][j] over subsets of islands
    print(-1)

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<vector<long long>> cost(n, vector<long long>(n));
    for (auto &row : cost) for (auto &x : row) cin >> x;   // -1 = no ferry
    // TODO: dp[mask][j] over subsets of islands
    cout << -1 << "\\n";
    return 0;
}
""",
        solution_python="""import sys

def main():
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    cost = [data[1 + i * n: 1 + (i + 1) * n] for i in range(n)]
    INF = 1 << 60
    out = [[(k, 1 << k, cost[j][k]) for k in range(1, n) if k != j and cost[j][k] >= 0] for j in range(n)]
    full = 1 << n
    dp = [[INF] * n for _ in range(full)]
    dp[1][0] = 0
    for mask in range(1, full, 2):
        row = dp[mask]
        for j in range(n):
            v = row[j]
            if v == INF:
                continue
            for k, bit, w in out[j]:
                if mask & bit:
                    continue
                nv = v + w
                tgt = dp[mask | bit]
                if nv < tgt[k]:
                    tgt[k] = nv
    last = dp[full - 1]
    best = min((last[j] + cost[j][0] for j in range(1, n) if cost[j][0] >= 0 and last[j] < INF), default=-1)
    print(best)

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<vector<long long>> cost(n, vector<long long>(n));
    for (auto &row : cost) for (auto &x : row) cin >> x;
    const long long INF = (long long)4e18;
    int full = 1 << n;
    vector<vector<long long>> dp(full, vector<long long>(n, INF));
    dp[1][0] = 0;
    for (int mask = 1; mask < full; mask += 2)
        for (int j = 0; j < n; j++) {
            long long v = dp[mask][j];
            if (v == INF) continue;
            for (int k = 1; k < n; k++) {
                if ((mask >> k & 1) || cost[j][k] < 0) continue;
                long long &t = dp[mask | (1 << k)][k];
                t = min(t, v + cost[j][k]);
            }
        }
    long long best = INF;
    for (int j = 1; j < n; j++)
        if (dp[full - 1][j] != INF && cost[j][0] >= 0) best = min(best, dp[full - 1][j] + cost[j][0]);
    cout << (best == INF ? -1 : best) << "\\n";
    return 0;
}
""",
    ),
    dict(
        id="digit-sum-multiples",
        title="Lucky Digit Sums",
        difficulty="expert",
        category="Dynamic Programming",
        tags=["digit-dp", "counting"],
        inspired_by="AtCoder Educational DP Contest S (Digit Sum) / classic digit DP",
        statement="""
Call a number **D-lucky** if the sum of its decimal digits is a multiple of `D`.
For example, 1789 has digit sum 25, so it is 5-lucky but not 3-lucky.

Answer `T` questions: how many integers `x` with `L ≤ x ≤ R` are D-lucky?

The ranges reach 10¹⁸, so you cannot look at the numbers one by one.
""",
        input_format="""
First line: `T` (1 ≤ T ≤ 30).
Next `T` lines: `L R D` (1 ≤ L ≤ R ≤ 10¹⁸, 1 ≤ D ≤ 100).
""",
        output_format="For each question, one line with the count.",
        hints=[
            "Count with a prefix function: answer = `f(R) − f(L − 1)`, where `f(X)` counts lucky numbers in `[0, X]`.",
            "**Digit DP**: walk over the digits of `X` from the most significant. A number below `X` "
            "agrees with `X` on some prefix, then has a **smaller** digit, then anything at all. "
            "Track only the digit sum **modulo D** — that is all the future needs to know.",
            "Keep `cnt[r]` = how many prefixes are already strictly below X's prefix with digit-sum ≡ r (mod D), plus the single "
            "'tight' prefix equal to X's. At each new digit: free prefixes may append any digit 0–9; the tight one may append "
            "a digit smaller than X's digit (becoming free) or exactly X's digit (staying tight).",
            "At the end, `f(X) = cnt[0] + (1 if the tight prefix's sum ≡ 0)`. Leading zeros are harmless: "
            "they do not change the digit sum. Counts fit in a signed 64-bit integer.",
        ],
        samples=[
            "3\n1 20 5\n1 100 10\n10 99 9",
        ],
        tests=[
            "1\n1 1 1",
            "1\n1 1000000000000000000 1",
            "1\n1 1000000000000000000 100",
            "2\n999999999999999999 1000000000000000000 81\n999999999999999999 1000000000000000000 2",
            "3\n1 9 10\n5 5 5\n123456789 123456789 45",
        ],
        gen=_gen_digit,
        starter_python="""import sys

def count_upto(X, D):
    # how many x in [0, X] have digit sum divisible by D
    if X < 0:
        return 0
    # TODO: digit DP over the digits of X
    return 0

def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        L, R, D = int(data[1 + 3 * i]), int(data[2 + 3 * i]), int(data[3 + 3 * i])
        out.append(count_upto(R, D) - count_upto(L - 1, D))
    print("\\n".join(map(str, out)))

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <string>
using namespace std;

// how many x in [0, X] have digit sum divisible by D
long long countUpto(long long X, int D) {
    if (X < 0) return 0;
    string s = to_string(X);
    // TODO: digit DP over the digits of s
    return 0;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long L, R;
        int D;
        cin >> L >> R >> D;
        cout << countUpto(R, D) - countUpto(L - 1, D) << "\\n";
    }
    return 0;
}
""",
        solution_python="""import sys
from operator import add

def count_upto(X, D):
    if X < 0:
        return 0
    cnt = [0] * D      # prefixes already below X's prefix, by digit sum mod D
    tight = 0          # digit sum mod D of X's own prefix
    for ch in str(X):
        dig = int(ch)
        new = [0] * D
        for d in range(10):
            sh = d % D
            rotated = cnt[-sh:] + cnt[:-sh] if sh else cnt
            new = list(map(add, new, rotated))
        for d in range(dig):
            new[(tight + d) % D] += 1
        tight = (tight + dig) % D
        cnt = new
    return cnt[0] + (1 if tight == 0 else 0)

def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    out = []
    for i in range(t):
        L, R, D = int(data[1 + 3 * i]), int(data[2 + 3 * i]), int(data[3 + 3 * i])
        out.append(count_upto(R, D) - count_upto(L - 1, D))
    print("\\n".join(map(str, out)))

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

long long countUpto(long long X, int D) {
    if (X < 0) return 0;
    string s = to_string(X);
    vector<long long> cnt(D, 0), nw(D);
    int tight = 0;
    for (char ch : s) {
        int dig = ch - '0';
        fill(nw.begin(), nw.end(), 0);
        for (int r = 0; r < D; r++) {
            if (!cnt[r]) continue;
            for (int d = 0; d < 10; d++) nw[(r + d) % D] += cnt[r];
        }
        for (int d = 0; d < dig; d++) nw[(tight + d) % D] += 1;
        tight = (tight + dig) % D;
        swap(cnt, nw);
    }
    return cnt[0] + (tight == 0 ? 1 : 0);
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long L, R;
        int D;
        cin >> L >> R >> D;
        cout << countUpto(R, D) - countUpto(L - 1, D) << "\\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="grid-paths-sinkholes",
        title="Sinkholes on the Grid",
        difficulty="expert",
        category="Dynamic Programming",
        tags=["combinatorics", "inclusion-exclusion", "dp", "modular-inverse"],
        inspired_by="AtCoder Educational DP Contest Y (Grid 2) / CSES 1078 Grid Paths II",
        statement="""
A robot walks on an `H × W` grid from the top-left cell `(1, 1)` to the
bottom-right cell `(H, W)`, moving only **down** or **right**. `N` cells contain
sinkholes and must be avoided.

How many different paths are there? Print the answer **modulo 10⁹ + 7**.

The grid can be 10⁵ × 10⁵, so a cell-by-cell DP is impossible; but there are
only a few hundred sinkholes.
""",
        input_format="""
First line: `H W N` (1 ≤ H, W ≤ 10⁵, 0 ≤ N ≤ 800).
Next `N` lines: `r c` — a sinkhole at row `r`, column `c`. All sinkholes are distinct and
are never at `(1, 1)` or `(H, W)`.
""",
        output_format="One integer: the number of safe paths modulo 10⁹ + 7.",
        hints=[
            "Without sinkholes the count from `(r₁, c₁)` to `(r₂, c₂)` is the binomial `C((r₂−r₁) + (c₂−c₁), r₂−r₁)`. "
            "Precompute factorials and inverse factorials up to `H + W` (Fermat: `inv(x) = x^(p−2) mod p`).",
            "Sort the sinkholes by (row, column) and append the target `(H, W)` as the last point. Let `f[i]` = number of paths "
            "from the start to point `i` that touch **no earlier sinkhole**.",
            "Subtract the bad paths by their **first** sinkhole: "
            "`f[i] = paths(start → i) − Σ f[j] · paths(j → i)` over earlier points `j` with `r_j ≤ r_i` and `c_j ≤ c_i`.",
            "The answer is `f[last]`. That is O(N²) pairs, each an O(1) binomial — keep everything reduced mod 10⁹+7 "
            "(and add the modulus before taking `%` after a subtraction in C++).",
        ],
        samples=[
            "3 4 2\n2 2\n1 4",
            "5 2 2\n2 1\n4 2",
        ],
        tests=[
            "1 1 0",
            "1 5 1\n1 3",
            "2 2 2\n1 2\n2 1",
            "100000 100000 0",
            "3 3 1\n2 2",
        ],
        gen=_gen_sinkholes,
        starter_python="""import sys

MOD = 10**9 + 7

def main():
    data = list(map(int, sys.stdin.read().split()))
    H, W, N = data[0], data[1], data[2]
    holes = [(data[3 + 2 * i], data[4 + 2 * i]) for i in range(N)]
    # TODO: factorials, then f[i] over sorted sinkholes + the target
    print(0)

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <utility>
#include <algorithm>
using namespace std;

const long long MOD = 1000000007LL;

int main() {
    int H, W, N;
    cin >> H >> W >> N;
    vector<pair<int,int>> holes(N);
    for (auto &h : holes) cin >> h.first >> h.second;
    // TODO: factorials, then f[i] over sorted sinkholes + the target
    cout << 0 << "\\n";
    return 0;
}
""",
        solution_python="""import sys

MOD = 10**9 + 7

def main():
    data = list(map(int, sys.stdin.read().split()))
    H, W, N = data[0], data[1], data[2]
    pts = sorted((data[3 + 2 * i], data[4 + 2 * i]) for i in range(N))
    pts.append((H, W))
    top = H + W
    fact = [1] * (top + 1)
    for i in range(1, top + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv = [1] * (top + 1)
    inv[top] = pow(fact[top], MOD - 2, MOD)
    for i in range(top, 0, -1):
        inv[i - 1] = inv[i] * i % MOD

    def paths(dr, dc):
        return fact[dr + dc] * inv[dr] % MOD * inv[dc] % MOD

    f = []
    for i, (r, c) in enumerate(pts):
        total = paths(r - 1, c - 1)
        for j in range(i):
            rj, cj = pts[j]
            if cj <= c:   # rj <= r holds because the points are sorted
                dr, dc = r - rj, c - cj
                total -= f[j] * (fact[dr + dc] * inv[dr] % MOD * inv[dc] % MOD)
        f.append(total % MOD)
    print(f[-1])

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <utility>
#include <algorithm>
using namespace std;

const long long MOD = 1000000007LL;

long long power(long long b, long long e) {
    long long r = 1; b %= MOD;
    while (e) { if (e & 1) r = r * b % MOD; b = b * b % MOD; e >>= 1; }
    return r;
}

int main() {
    int H, W, N;
    cin >> H >> W >> N;
    vector<pair<int,int>> pts(N);
    for (auto &h : pts) cin >> h.first >> h.second;
    sort(pts.begin(), pts.end());
    pts.push_back({H, W});
    int top = H + W;
    vector<long long> fact(top + 1, 1), inv(top + 1, 1);
    for (int i = 1; i <= top; i++) fact[i] = fact[i - 1] * i % MOD;
    inv[top] = power(fact[top], MOD - 2);
    for (int i = top; i > 0; i--) inv[i - 1] = inv[i] * i % MOD;
    auto paths = [&](int dr, int dc) { return fact[dr + dc] * inv[dr] % MOD * inv[dc] % MOD; };
    int K = pts.size();
    vector<long long> f(K);
    for (int i = 0; i < K; i++) {
        auto [r, c] = pts[i];
        long long total = paths(r - 1, c - 1);
        for (int j = 0; j < i; j++) {
            auto [rj, cj] = pts[j];
            if (rj <= r && cj <= c) total = (total - f[j] * paths(r - rj, c - cj)) % MOD;
        }
        f[i] = (total + MOD) % MOD;
    }
    cout << f[K - 1] << "\\n";
    return 0;
}
""",
    ),
]
