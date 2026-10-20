"""Greedy: jump game, gas station, activity selection, canonical coin change."""


def _arr(xs):
    return " ".join(map(str, xs))


def _jump_gen(rng):
    out = []
    for n, amax, pz in ((1, 5, 0.0), (6, 3, 0.0), (100, 4, 0.1), (5000, 8, 0.1), (5000, 3, 0.4), (3000, 2, 0.0),
                        (4000, 100, 0.0)):
        a = [0 if rng.random() < pz else rng.randint(1, amax) for _ in range(n)]
        out.append(f"{n}\n{_arr(a)}")
    return out


def _gas_case(rng, n, lim, bias):
    g = [rng.randint(0, lim) for _ in range(n)]
    c = [max(0, rng.randint(0, lim) + bias) for _ in range(n)]
    return f"{n}\n{_arr(g)}\n{_arr(c)}"


def _gas_gen(rng):
    out = [_gas_case(rng, 1, 5, 0), _gas_case(rng, 5, 5, 0), _gas_case(rng, 50, 100, -3),
           _gas_case(rng, 1500, 10**4, -40), _gas_case(rng, 1500, 1000, 5)]
    # a case with total gas exactly equal to total cost
    n = 2000
    g = [rng.randint(0, 100) for _ in range(n)]
    c = g[:]
    rng.shuffle(c)
    out.append(f"{n}\n{_arr(g)}\n{_arr(c)}")
    return out


def _talk_case(rng, n, span, maxlen):
    lines = []
    for _ in range(n):
        s = rng.randint(0, span)
        lines.append(f"{s} {s + rng.randint(1, maxlen)}")
    return f"{n}\n" + "\n".join(lines)


def _talk_gen(rng):
    return [_talk_case(rng, 1, 10, 5), _talk_case(rng, 8, 20, 6), _talk_case(rng, 300, 1000, 50),
            _talk_case(rng, 2500, 10**6, 5000), _talk_case(rng, 2500, 1000, 3)]


def _coin_gen(rng):
    qs = [rng.randint(0, 10**9) for _ in range(40)] + [rng.randint(0, 1000) for _ in range(40)]
    return [f"{len(qs)}\n" + "\n".join(map(str, qs))]


PROBLEMS = [
    dict(
        id="hop-to-the-end",
        title="Hop to the End",
        difficulty="medium",
        category="Greedy",
        tags=["greedy", "arrays", "bfs-levels"],
        inspired_by="LeetCode #55 / #45 Jump Game I & II",
        statement="""
A frog sits on stone `0` of a row of `n` stones. Stone `i` carries a number
`a[i]`: from there the frog may hop forward by **any** distance from 1 to
`a[i]` stones (a stone with `0` is a dead end).

What is the **minimum number of hops** to reach the last stone `n − 1`?
Print `-1` if it can't be reached at all.

For `2 3 1 1 4` the answer is **2**: hop 1 stone to the `3`, then 3 stones to
the end. For `3 2 1 0 4` every path gets stuck on the `0`, so the answer is `-1`.
""",
        input_format="First line: `n` (1 ≤ n ≤ 10⁴). Second line: `n` integers (0 ≤ aᵢ ≤ 100).",
        output_format="One integer: the minimum number of hops, or `-1`.",
        hints=[
            "Think in 'rounds': after `h` hops the frog can be anywhere in some range `[0, end]`. "
            "The next round reaches up to `farthest = max(i + a[i])` over that range.",
            "Scan `i` from left to right keeping `farthest`. When `i` reaches the current `end` (and the goal is "
            "beyond it), you must hop: `hops += 1`, `end = farthest`.",
            "If at some point `i > farthest`, stone `i` is unreachable — print `-1`. And `n = 1` needs 0 hops.",
        ],
        samples=["5\n2 3 1 1 4", "5\n3 2 1 0 4", "1\n0"],
        tests=["2\n0 5", "2\n1 0", "6\n1 1 1 1 1 1", "4\n9 0 0 0", "5\n1 2 0 1 0"],
        gen=_jump_gen,
        starter_python="""n = int(input())
a = list(map(int, input().split()))
hops = 0
end = 0        # farthest stone reachable with `hops` hops
farthest = 0   # farthest stone reachable with one more hop
# TODO: scan the stones
print(hops)
""",
        starter_cpp="""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (auto &x : a) cin >> x;
    int hops = 0, end = 0, farthest = 0;
    // TODO: scan the stones
    cout << hops << "\\n";
    return 0;
}
""",
        solution_python=r"""n = int(input())
a = list(map(int, input().split()))
hops = end = farthest = 0
for i in range(n - 1):
    if i > farthest:
        break  # stone i can't be reached
    farthest = max(farthest, i + a[i])
    if i == end:
        hops += 1
        end = farthest
        if end >= n - 1:
            break
print(hops if end >= n - 1 else -1)
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (auto &x : a) cin >> x;
    int hops = 0, end = 0, farthest = 0;
    for (int i = 0; i < n - 1; i++) {
        if (i > farthest) break;
        farthest = max(farthest, i + a[i]);
        if (i == end) {
            hops++;
            end = farthest;
            if (end >= n - 1) break;
        }
    }
    cout << (end >= n - 1 ? hops : -1) << "\n";
    return 0;
}
""",
    ),
    dict(
        id="fuel-loop-start",
        title="Fuel Loop Start",
        difficulty="medium",
        category="Greedy",
        tags=["greedy", "prefix-sums", "circular"],
        inspired_by="LeetCode #134 Gas Station",
        statement="""
`n` fuel stations sit on a circular road, numbered `0 … n−1` in driving
order. Station `i` gives you `g[i]` litres, and driving from station `i` to the
next one (station `n − 1` leads back to station `0`) burns `c[i]` litres.

You start at some station with an **empty tank** (of unlimited capacity),
refuel, and want to drive one full loop back to the start without the tank
ever going negative.

Print the **smallest** index of a station you can start from, or `-1` if no
start works.
""",
        input_format="""First line: `n` (1 ≤ n ≤ 5000).
Second line: `n` integers `g[i]`. Third line: `n` integers `c[i]` (0 ≤ g[i], c[i] ≤ 10⁴).""",
        output_format="One integer: the smallest valid starting station, or `-1`.",
        hints=[
            "If `Σg < Σc` no start can work. Otherwise a valid start always exists.",
            "Greedy scan: drive from candidate `start = 0`, keeping `tank += g[i] − c[i]`. If the tank goes negative at "
            "station `i`, then **no** station between `start` and `i` can be a valid start either — so jump to "
            "`start = i + 1` and reset the tank to 0.",
            "One pass over the stations is enough; the candidate left at the end is the smallest valid start "
            "(when the totals allow one). Trying every start separately is O(n²).",
        ],
        samples=["5\n1 2 3 4 5\n3 4 5 1 2", "3\n2 3 4\n3 4 3"],
        tests=["1\n0\n0", "1\n3\n5", "2\n1 1\n1 1", "4\n0 0 0 9\n1 1 1 6", "3\n5 0 0\n1 2 2"],
        gen=_gas_gen,
        starter_python="""n = int(input())
g = list(map(int, input().split()))
c = list(map(int, input().split()))
start = 0
tank = 0
# TODO: one greedy pass; also check total gas vs total cost
print(start)
""",
        starter_cpp="""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> g(n), c(n);
    for (auto &x : g) cin >> x;
    for (auto &x : c) cin >> x;
    int start = 0;
    long long tank = 0;
    // TODO: one greedy pass; also check total gas vs total cost
    cout << start << "\\n";
    return 0;
}
""",
        solution_python=r"""n = int(input())
g = list(map(int, input().split()))
c = list(map(int, input().split()))
if sum(g) < sum(c):
    print(-1)
else:
    start = tank = 0
    for i in range(n):
        tank += g[i] - c[i]
        if tank < 0:
            start = i + 1
            tank = 0
    print(start)
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> g(n), c(n);
    long long total = 0;
    for (auto &x : g) { cin >> x; total += x; }
    for (auto &x : c) { cin >> x; total -= x; }
    if (total < 0) { cout << -1 << "\n"; return 0; }
    int start = 0;
    long long tank = 0;
    for (int i = 0; i < n; i++) {
        tank += g[i] - c[i];
        if (tank < 0) { start = i + 1; tank = 0; }
    }
    cout << start << "\n";
    return 0;
}
""",
    ),
    dict(
        id="most-talks-attended",
        title="Most Talks Attended",
        difficulty="medium",
        category="Greedy",
        tags=["greedy", "sorting", "intervals", "activity-selection"],
        inspired_by="Classic activity selection; CSES Movie Festival",
        statement="""
A conference has `n` talks. Talk `i` runs from time `s[i]` until `e[i]`
(the end is exclusive: you can leave a talk ending at 10 and catch one starting
at 10). You can only be in one talk at a time, and you must stay for a whole
talk to count it.

What is the **maximum number** of talks you can attend?
""",
        input_format="First line: `n` (1 ≤ n ≤ 2500). Next `n` lines: `s e` (0 ≤ s < e ≤ 1.1·10⁶).",
        output_format="One integer: the maximum number of talks.",
        hints=[
            "Which talk should be your first? Picking the one that **ends earliest** leaves the most time for the rest — "
            "and it never makes things worse (an exchange argument).",
            "Sort talks by end time. Walk through them, keeping `free_at` (when you're free again): take a talk if "
            "`s >= free_at`, then set `free_at = e`.",
            "Python: `talks.sort(key=lambda t: t[1])`. C++: store `(e, s)` pairs so plain `sort` orders by end.",
        ],
        samples=["3\n3 5\n4 9\n5 8", "4\n1 3\n2 4\n3 5\n0 7"],
        tests=["1\n0 1", "3\n1 2\n1 2\n1 2", "5\n0 10\n1 2\n2 3\n3 4\n4 5"],
        gen=_talk_gen,
        starter_python="""n = int(input())
talks = [tuple(map(int, input().split())) for _ in range(n)]
count = 0
# TODO: sort by end time, then pick greedily
print(count)
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<pair<int, int>> t(n);  // (end, start)
    for (auto &p : t) cin >> p.second >> p.first;
    int count = 0;
    // TODO: sort by end time, then pick greedily
    cout << count << "\\n";
    return 0;
}
""",
        solution_python=r"""import sys

data = list(map(int, sys.stdin.read().split()))
n = data[0]
talks = sorted(((data[2 + 2 * i], data[1 + 2 * i]) for i in range(n)))
count = 0
free_at = -1
for e, s in talks:
    if s >= free_at:
        count += 1
        free_at = e
print(count)
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<pair<int, int>> t(n);
    for (auto &p : t) cin >> p.second >> p.first;
    sort(t.begin(), t.end());
    int count = 0, freeAt = -1;
    for (auto &p : t) {
        if (p.second >= freeAt) {
            count++;
            freeAt = p.first;
        }
    }
    cout << count << "\n";
    return 0;
}
""",
    ),
    dict(
        id="euro-coin-change",
        title="Euro Coin Change",
        difficulty="easy",
        category="Greedy",
        tags=["greedy", "integer-division"],
        inspired_by="Classic greedy change-making (canonical coin systems)",
        statement="""
Euro coins come in `1, 2, 5, 10, 20, 50, 100` and `200` cents. For each
amount, print the **fewest coins** that add up to it exactly.

For this coin system the greedy rule — *always take the biggest coin that still
fits* — is optimal. (That's not true for every coin system: with coins
`1, 3, 4` greedy pays 6 as `4+1+1`, but `3+3` is better. Systems where greedy
works are called *canonical*.)

Amounts can be huge, so take many coins of one kind at a time.
""",
        input_format="First line: `t` (1 ≤ t ≤ 100). Next `t` lines: an amount `x` in cents (0 ≤ x ≤ 10⁹).",
        output_format="For each amount, the minimum number of coins on its own line.",
        hints=[
            "Go through the coins from largest to smallest.",
            "How many 200-cent coins fit into `x`? That's `x // 200` (C++: `x / 200`). The rest is `x % 200`.",
            "Add up the counts for every coin. The answer for 10⁹ is about 5·10⁶ — fits easily in an `int`, but "
            "`long long` never hurts.",
        ],
        samples=["3\n7\n289\n0"],
        tests=["1\n1", "4\n3\n4\n6\n9", "1\n1000000000", "2\n199\n388"],
        gen=_coin_gen,
        starter_python="""COINS = [200, 100, 50, 20, 10, 5, 2, 1]
t = int(input())
for _ in range(t):
    x = int(input())
    count = 0
    # TODO: greedy over COINS
    print(count)
""",
        starter_cpp="""#include <iostream>
using namespace std;

int main() {
    const int COINS[] = {200, 100, 50, 20, 10, 5, 2, 1};
    int t;
    cin >> t;
    while (t--) {
        long long x, count = 0;
        cin >> x;
        // TODO: greedy over COINS
        cout << count << "\\n";
    }
    return 0;
}
""",
        solution_python=r"""COINS = [200, 100, 50, 20, 10, 5, 2, 1]
t = int(input())
for _ in range(t):
    x = int(input())
    count = 0
    for c in COINS:
        count += x // c
        x %= c
    print(count)
""",
        solution_cpp=r"""#include <iostream>
using namespace std;

int main() {
    const int COINS[] = {200, 100, 50, 20, 10, 5, 2, 1};
    int t;
    cin >> t;
    while (t--) {
        long long x, count = 0;
        cin >> x;
        for (int c : COINS) {
            count += x / c;
            x %= c;
        }
        cout << count << "\n";
    }
    return 0;
}
""",
    ),
]
