"""Arrays, part 2: classic interview array problems."""


def _arr(rng, n, lo=-10**9, hi=10**9):
    return [rng.randint(lo, hi) for _ in range(n)]


def _case(a):
    return f"{len(a)}\n" + " ".join(map(str, a))


def _zeros_case(rng):
    n = rng.randint(1, 200)
    p = rng.random()
    return _case([0 if rng.random() < p else rng.randint(-10**9, 10**9) for _ in range(n)])


def _ones_case(rng):
    n = rng.randint(1, 1000)
    p = rng.choice([0.3, 0.5, 0.8, 0.95])
    return _case([1 if rng.random() < p else 0 for _ in range(n)])


def _stock_case(rng):
    n = rng.randint(1, 2000)
    kind = rng.randrange(3)
    if kind == 0:
        a = _arr(rng, n, 1, 10**4)
    elif kind == 1:  # random walk
        a, x = [], rng.randint(1, 10**4)
        for _ in range(n):
            x = min(10**4, max(1, x + rng.randint(-60, 60)))
            a.append(x)
    else:  # mostly falling
        a = sorted(_arr(rng, n, 1, 10**4), reverse=True)
        if n > 3:
            i = rng.randrange(n - 1)
            a[i], a[i + 1] = a[i + 1], a[i]
    return _case(a)


PROBLEMS = [
    dict(
        id="rotate-array-right",
        title="Rotate the Array",
        difficulty="easy",
        category="Arrays",
        tags=["arrays", "modulo", "rotation"],
        inspired_by="LeetCode #189 Rotate Array",
        statement="""
Rotating an array **to the right** by one step moves the last element to the
front: `1 2 3 4 5` → `5 1 2 3 4`.

Rotate the given array to the right by `k` steps. `k` can be much larger than
the length of the array!
""",
        input_format="First line: `n` and `k` (1 ≤ n ≤ 1000, 0 ≤ k ≤ 10⁹). Second line: `n` integers "
                     "(−10⁹ ≤ aᵢ ≤ 10⁹).",
        output_format="The rotated array on one line, separated by spaces.",
        hints=[
            "Rotating by `n` steps gives back the original array, so only `k % n` steps matter. "
            "Simulating 10⁹ single steps would be far too slow.",
            "After rotating by r = k % n, the element at index i moves to index (i + r) % n.",
            "Python slicing does it in one line: the last r elements followed by the first n − r, i.e. "
            "`a[n - r:] + a[:n - r]`. C++ has `std::rotate` in `<algorithm>`, or build a new vector by hand.",
        ],
        samples=["5 2\n1 2 3 4 5", "3 7\n10 20 30"],
        tests=["1 1000000000\n42", "4 0\n1 2 3 4", "4 4\n1 2 3 4", "4 1000000000\n-1 -2 -3 -4",
               "6 5\n1 2 3 4 5 6"],
        gen=lambda rng: [f"{n} {rng.randint(0, 10**9)}\n" + " ".join(map(str, _arr(rng, n)))
                         for n in (rng.randint(1, 200) for _ in range(4))],
        starter_python=r"""n, k = map(int, input().split())
a = list(map(int, input().split()))
# TODO: rotate a to the right by k steps and print it
""",
        starter_cpp=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    long long k;
    cin >> n >> k;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    // TODO: rotate a to the right by k steps and print it
    return 0;
}
""",
        solution_python=r"""n, k = map(int, input().split())
a = list(map(int, input().split()))
r = k % n
print(*(a[n - r:] + a[:n - r]))
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    long long k;
    cin >> n >> k;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    int r = (int)(k % n);
    vector<long long> b(n);
    for (int i = 0; i < n; i++) b[(i + r) % n] = a[i];
    for (int i = 0; i < n; i++) cout << b[i] << (i + 1 < n ? " " : "\n");
    return 0;
}
""",
    ),
    dict(
        id="move-zeroes",
        title="Move Zeroes to the End",
        difficulty="easy",
        category="Arrays",
        tags=["arrays", "two-pointers", "stable"],
        inspired_by="LeetCode #283 Move Zeroes",
        statement="""
Move all zeroes of the array to the end, while keeping the other elements in
their **original relative order**.

`0 1 0 3 12` → `1 3 12 0 0`
""",
        input_format="First line: `n` (1 ≤ n ≤ 1000). Second line: `n` integers (−10⁹ ≤ aᵢ ≤ 10⁹).",
        output_format="The rearranged array on one line, separated by spaces.",
        hints=[
            "Simple approach: first output every non-zero element in order, then output as many zeroes as you skipped.",
            "In-place approach: keep a 'write' index `w`. For each non-zero element, copy it to `a[w]` and increase `w`. "
            "Afterwards fill positions `w … n−1` with zeroes.",
            "Sorting won't work — it would change the order of the non-zero elements.",
        ],
        samples=["5\n0 1 0 3 12"],
        tests=["1\n0", "1\n-5", "4\n0 0 0 0", "4\n1 2 3 4", "6\n0 -1 0 -1 0 2", "3\n5 0 0"],
        gen=lambda rng: [_zeros_case(rng) for _ in range(5)],
        starter_python=r"""n = int(input())
a = list(map(int, input().split()))
# TODO: move all zeroes to the end (keep the order of the others), then print a
""",
        starter_cpp=r"""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    // TODO: move all zeroes to the end (keep the order of the others), then print a
    return 0;
}
""",
        solution_python=r"""n = int(input())
a = list(map(int, input().split()))
nz = [x for x in a if x != 0]
print(*(nz + [0] * (n - len(nz))))
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    int w = 0;
    for (int i = 0; i < n; i++)
        if (a[i] != 0) a[w++] = a[i];
    while (w < n) a[w++] = 0;
    for (int i = 0; i < n; i++) cout << a[i] << (i + 1 < n ? " " : "\n");
    return 0;
}
""",
    ),
    dict(
        id="stock-buy-sell-once",
        title="Buy Low, Sell High",
        difficulty="easy",
        category="Arrays",
        tags=["arrays", "greedy", "running-minimum"],
        inspired_by="LeetCode #121 Best Time to Buy and Sell Stock",
        statement="""
You know the price of a share for each of the next `n` days. You may buy
**one** share on some day and sell it on a **later** day. What is the biggest
profit you can make?

If prices only go down, the best plan is not to trade at all: the answer is
then `0`.
""",
        input_format="First line: `n` (1 ≤ n ≤ 10⁴). Second line: `n` prices `p₁ … pₙ` (1 ≤ pᵢ ≤ 10⁴).",
        output_format="A single integer: the maximum profit (0 if no profitable trade exists).",
        hints=[
            "Trying every pair (buy day, sell day) is O(n²) — fine for small n, but there is a one-pass solution.",
            "Walk through the days keeping the **lowest price seen so far**. If you sold today, the best buy day "
            "was that lowest earlier price.",
            "So for each day: profit candidate = price − lowest_so_far; keep the best candidate, then update lowest_so_far.",
        ],
        samples=["6\n7 1 5 3 6 4", "5\n7 6 4 3 1"],
        tests=["1\n5", "2\n1 10000", "2\n10000 1", "4\n3 3 3 3", "5\n2 9 1 3 8", "6\n5 1 6 2 4 9"],
        gen=lambda rng: [_stock_case(rng) for _ in range(5)],
        starter_python=r"""n = int(input())
p = list(map(int, input().split()))
best = 0
# TODO: find the maximum profit of one buy followed by one later sell
print(best)
""",
        starter_cpp=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> p(n);
    for (auto &x : p) cin >> x;
    int best = 0;
    // TODO: find the maximum profit of one buy followed by one later sell
    cout << best << "\n";
    return 0;
}
""",
        solution_python=r"""n = int(input())
p = list(map(int, input().split()))
best = 0
low = p[0]
for x in p:
    best = max(best, x - low)
    low = min(low, x)
print(best)
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> p(n);
    for (auto &x : p) cin >> x;
    int best = 0, low = p[0];
    for (int x : p) {
        best = max(best, x - low);
        low = min(low, x);
    }
    cout << best << "\n";
    return 0;
}
""",
    ),
    dict(
        id="max-consecutive-ones",
        title="Longest Streak of Ones",
        difficulty="easy",
        category="Arrays",
        tags=["arrays", "counting", "streaks"],
        inspired_by="LeetCode #485 Max Consecutive Ones",
        statement="""
A fitness app stores, for each day, `1` if you exercised and `0` if you did
not. Find your longest streak: the maximum number of **consecutive** `1`s.
""",
        input_format="First line: `n` (1 ≤ n ≤ 1000). Second line: `n` values, each `0` or `1`.",
        output_format="A single integer: the length of the longest run of consecutive 1s (0 if there are none).",
        hints=[
            "Keep a counter `cur` for the current streak: increase it on a 1, reset it to 0 on a 0.",
            "Keep a second variable `best` and update it with `max(best, cur)` after every step.",
        ],
        samples=["6\n1 1 0 1 1 1", "3\n0 0 0"],
        tests=["1\n1", "1\n0", "5\n1 1 1 1 1", "7\n1 0 1 0 1 0 1", "6\n0 1 1 1 0 0"],
        gen=lambda rng: [_ones_case(rng) for _ in range(4)],
        starter_python=r"""n = int(input())
a = list(map(int, input().split()))
best = 0
# TODO: find the longest run of consecutive 1s
print(best)
""",
        starter_cpp=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (auto &x : a) cin >> x;
    int best = 0;
    // TODO: find the longest run of consecutive 1s
    cout << best << "\n";
    return 0;
}
""",
        solution_python=r"""n = int(input())
a = list(map(int, input().split()))
best = cur = 0
for x in a:
    cur = cur + 1 if x == 1 else 0
    best = max(best, cur)
print(best)
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
    int best = 0, cur = 0;
    for (int x : a) {
        cur = (x == 1) ? cur + 1 : 0;
        best = max(best, cur);
    }
    cout << best << "\n";
    return 0;
}
""",
    ),
]
