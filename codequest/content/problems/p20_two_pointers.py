"""Two Pointers: medium problems (plus two easy bridges)."""


def _arr(xs):
    return " ".join(map(str, xs))


def _water_gen(rng):
    out = []
    for n in (2, 3, 50, 800):
        out.append(f"{n}\n{_arr(rng.randint(0, 10**4) for _ in range(n))}")
    # one large test: a naive O(n^2) Python loop is far too slow here
    n = 6000
    out.append(f"{n}\n{_arr(rng.randint(0, 9999) for _ in range(n))}")
    return out


def _triplet_gen(rng):
    out = []
    for n, lim in ((10, 5), (60, 20), (300, 200), (600, 1000), (600, 50)):
        out.append(f"{n}\n{_arr(rng.randint(-lim, lim) for _ in range(n))}")
    return out


def _dedupe_gen(rng):
    out = []
    for n, lim in ((1, 5), (20, 5), (500, 100), (2000, 10**6)):
        xs = sorted(rng.randint(-lim, lim) for _ in range(n))
        out.append(f"{n}\n{_arr(xs)}")
    return out


def _merge_gen(rng):
    out = []
    for n, m in ((1, 1), (5, 0), (0, 4), (40, 70), (1500, 1200)):
        a = sorted(rng.randint(-10**6, 10**6) for _ in range(n))
        b = sorted(rng.randint(-10**6, 10**6) for _ in range(m))
        out.append(f"{n} {m}\n{_arr(a)}\n{_arr(b)}")
    return out


PROBLEMS = [
    dict(
        id="widest-reservoir",
        title="Widest Reservoir",
        difficulty="medium",
        category="Two Pointers",
        tags=["two-pointers", "greedy", "arrays"],
        inspired_by="LeetCode #11 Container With Most Water",
        statement="""
A row of `n` vertical walls stands along a valley floor, one metre apart. Wall
`i` has height `h[i]`.

Engineers want to build a reservoir by picking **two** walls `i < j` and
letting rain fill the space between them. The water level can't rise above the
lower of the two walls, so the stored amount (in a 2-D cross-section) is

    min(h[i], h[j]) × (j − i)

Walls standing between `i` and `j` are demolished, so they don't matter.
Find the largest amount of water any pair of walls can hold.

With heights `1 8 6 2 5 4 8 3 7`, picking the walls with heights 8 (index 1)
and 7 (index 8) holds `min(8, 7) × 7 = 49`.

Checking every pair is O(n²) — too slow for the largest tests in Python. Can
you do it in a single sweep?
""",
        input_format="First line: `n` (2 ≤ n ≤ 10⁴). Second line: `n` integers `h[i]` (0 ≤ h[i] ≤ 10⁴).",
        output_format="One integer: the maximum water held.",
        hints=[
            "Start with the widest pair: one pointer at the left end, one at the right end.",
            "The area is limited by the *shorter* wall. Moving the taller wall inwards can never help "
            "(the width shrinks and the height can't grow past the short wall).",
            "So: compute the area, then move the pointer at the shorter wall one step inwards. "
            "Repeat while `left < right`, keeping the best area seen.",
        ],
        samples=["9\n1 8 6 2 5 4 8 3 7", "2\n1 1"],
        tests=["2\n0 0", "5\n5 4 3 2 1", "4\n1 100 100 1", "6\n10000 1 1 1 1 10000"],
        gen=_water_gen,
        starter_python="""n = int(input())
h = list(map(int, input().split()))

# TODO: find the pair of walls holding the most water
best = 0
print(best)
""",
        starter_cpp="""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> h(n);
    for (auto &x : h) cin >> x;
    long long best = 0;
    // TODO: two pointers from both ends
    cout << best << "\\n";
    return 0;
}
""",
        solution_python=r"""n = int(input())
h = list(map(int, input().split()))
lo, hi = 0, n - 1
best = 0
while lo < hi:
    if h[lo] < h[hi]:
        area = h[lo] * (hi - lo)
        lo += 1
    else:
        area = h[hi] * (hi - lo)
        hi -= 1
    if area > best:
        best = area
print(best)
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> h(n);
    for (auto &x : h) cin >> x;
    int lo = 0, hi = n - 1;
    long long best = 0;
    while (lo < hi) {
        long long area = min(h[lo], h[hi]) * (hi - lo);
        best = max(best, area);
        if (h[lo] < h[hi]) lo++; else hi--;
    }
    cout << best << "\n";
    return 0;
}
""",
    ),
    dict(
        id="zero-sum-triplets",
        title="Zero-Sum Triplets",
        difficulty="medium",
        category="Two Pointers",
        tags=["two-pointers", "sorting", "duplicates"],
        inspired_by="LeetCode #15 3Sum",
        statement="""
Given `n` integers, count the **distinct** triplets of values `(a, b, c)` with
`a ≤ b ≤ c` and `a + b + c = 0`, such that the three values can be taken from
three *different positions* of the array.

Two triplets are the same if they consist of the same three values, so with
the array `-1 0 1 2 -1 -4` the answer is **2**: `(-1, -1, 2)` and `(-1, 0, 1)`
(the triplet `(-1, 0, 1)` can be picked in two ways but counts once).

A value may appear in a triplet as many times as it occurs in the array —
`(0, 0, 0)` needs at least three zeros.
""",
        input_format="First line: `n` (1 ≤ n ≤ 600). Second line: `n` integers (−1000 ≤ aᵢ ≤ 1000).",
        output_format="One integer: the number of distinct zero-sum triplets.",
        hints=[
            "Sort the array first. Then fix the smallest element `a = x[i]` and look for pairs in the part to its right.",
            "For a fixed `i`, two pointers `lo = i + 1`, `hi = n − 1`: if the sum is too small move `lo` right, "
            "if too big move `hi` left.",
            "To avoid counting the same triplet twice, skip over equal values: skip `i` when `x[i] == x[i−1]`, "
            "and after a match advance `lo` past all copies of `x[lo]`.",
        ],
        samples=["6\n-1 0 1 2 -1 -4", "3\n0 0 0"],
        tests=["1\n0", "2\n0 0", "4\n0 0 0 0", "5\n1 2 3 4 5", "7\n-2 -2 0 1 1 2 4"],
        gen=_triplet_gen,
        starter_python="""n = int(input())
a = list(map(int, input().split()))
a.sort()
count = 0
# TODO: fix a[i], then use two pointers on the rest (skip duplicate values!)
print(count)
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (auto &x : a) cin >> x;
    sort(a.begin(), a.end());
    long long count = 0;
    // TODO: fix a[i], two pointers lo/hi on the right part
    cout << count << "\\n";
    return 0;
}
""",
        solution_python=r"""from collections import Counter

n = int(input())
a = list(map(int, input().split()))
cnt = Counter(a)
vals = sorted(cnt)
count = 0
for i, x in enumerate(vals):
    if x > 0:
        break
    for y in vals[i:]:
        z = -x - y
        if z < y:
            break
        if z not in cnt:
            continue
        need = Counter((x, y, z))
        if all(cnt[v] >= k for v, k in need.items()):
            count += 1
print(count)
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
    sort(a.begin(), a.end());
    long long count = 0;
    for (int i = 0; i + 2 < n; i++) {
        if (i > 0 && a[i] == a[i - 1]) continue;
        int lo = i + 1, hi = n - 1;
        while (lo < hi) {
            int s = a[i] + a[lo] + a[hi];
            if (s < 0) lo++;
            else if (s > 0) hi--;
            else {
                count++;
                int v = a[lo];
                while (lo < hi && a[lo] == v) lo++;
            }
        }
    }
    cout << count << "\n";
    return 0;
}
""",
    ),
    dict(
        id="compact-sorted-list",
        title="Compact a Sorted List",
        difficulty="easy",
        category="Two Pointers",
        tags=["two-pointers", "in-place", "arrays"],
        inspired_by="LeetCode #26 Remove Duplicates from Sorted Array",
        statement="""
You get a list of `n` integers sorted in non-decreasing order. Remove the
repeated values so that every value appears once, keeping the order.

Try to do it **in place** with two pointers: a *read* pointer walks through
the list and a *write* pointer marks where the next new value goes. (The judge
only sees what you print, but this is the technique the problem is about.)
""",
        input_format="First line: `n` (1 ≤ n ≤ 2000). Second line: `n` sorted integers (|aᵢ| ≤ 10⁶).",
        output_format="First line: `k`, the number of distinct values. Second line: the `k` distinct values in order.",
        hints=[
            "Keep `w` = number of unique values written so far. The first element is always kept, so start with `w = 1`.",
            "For each `r` from 1 to n−1: if `a[r] != a[w − 1]` it is a new value — copy it to `a[w]` and increase `w`.",
            "At the end the answer is the prefix `a[0..w−1]`. Python: `print(*a[:w])`.",
        ],
        samples=["5\n1 1 2 3 3", "3\n7 7 7"],
        tests=["1\n42", "4\n-3 -1 0 2", "6\n-5 -5 -5 0 0 9"],
        gen=_dedupe_gen,
        starter_python="""n = int(input())
a = list(map(int, input().split()))
w = 1  # number of unique values kept so far
# TODO: walk a read pointer r through the list
print(w)
print(*a[:w])
""",
        starter_cpp="""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (auto &x : a) cin >> x;
    int w = 1;
    // TODO: for r in 1..n-1, copy new values to a[w]
    cout << w << "\\n";
    for (int i = 0; i < w; i++) cout << a[i] << (i + 1 < w ? ' ' : '\\n');
    return 0;
}
""",
        solution_python=r"""n = int(input())
a = list(map(int, input().split()))
w = 1
for r in range(1, n):
    if a[r] != a[w - 1]:
        a[w] = a[r]
        w += 1
print(w)
print(*a[:w])
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (auto &x : a) cin >> x;
    int w = 1;
    for (int r = 1; r < n; r++)
        if (a[r] != a[w - 1]) a[w++] = a[r];
    cout << w << "\n";
    for (int i = 0; i < w; i++) cout << a[i] << (i + 1 < w ? ' ' : '\n');
    return 0;
}
""",
    ),
    dict(
        id="zip-two-sorted-lists",
        title="Zip Two Sorted Lists",
        difficulty="easy",
        category="Two Pointers",
        tags=["two-pointers", "merge", "arrays"],
        inspired_by="LeetCode #88 Merge Sorted Array (the merge step of merge sort)",
        statement="""
Two lists of integers are each sorted in non-decreasing order. Print all their
elements as **one** sorted list.

Calling a sort function on the concatenation works, but the point here is the
linear-time *merge*: walk both lists with one pointer each and always take the
smaller front element. This is exactly the step that makes merge sort tick.
""",
        input_format="""First line: `n m` (0 ≤ n, m ≤ 1500, n + m ≥ 1).
Second line: `n` sorted integers. Third line: `m` sorted integers.
(A list of length 0 is given as an empty line.) All values satisfy |x| ≤ 10⁶.""",
        output_format="One line with the `n + m` merged values, separated by spaces.",
        hints=[
            "Keep indices `i` (into the first list) and `j` (into the second).",
            "While both lists still have elements, append the smaller of `a[i]` and `b[j]` and advance that pointer.",
            "When one list runs out, append everything left in the other one "
            "(Python: `merged.extend(a[i:])`; C++: a final `while (i < n)` loop).",
        ],
        samples=["3 3\n1 2 4\n1 3 4", "2 0\n5 9\n"],
        tests=["0 1\n\n-7", "4 4\n1 1 1 1\n1 1 1 1", "3 2\n10 20 30\n-5 -1"],
        gen=_merge_gen,
        starter_python="""import sys

data = sys.stdin.read().split()   # robust even when a list is empty
n, m = int(data[0]), int(data[1])
a = list(map(int, data[2:2 + n]))
b = list(map(int, data[2 + n:2 + n + m]))
merged = []
i = j = 0
# TODO: merge a and b into merged
print(*merged)
""",
        starter_cpp="""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<int> a(n), b(m);
    for (auto &x : a) cin >> x;
    for (auto &x : b) cin >> x;
    vector<int> merged;
    // TODO: merge with two indices i and j
    for (size_t k = 0; k < merged.size(); k++)
        cout << merged[k] << (k + 1 < merged.size() ? ' ' : '\\n');
    return 0;
}
""",
        solution_python=r"""import sys

data = sys.stdin.read().split()
n, m = int(data[0]), int(data[1])
a = list(map(int, data[2:2 + n]))
b = list(map(int, data[2 + n:2 + n + m]))
merged = []
i = j = 0
while i < n and j < m:
    if a[i] <= b[j]:
        merged.append(a[i]); i += 1
    else:
        merged.append(b[j]); j += 1
merged.extend(a[i:])
merged.extend(b[j:])
print(*merged)
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<int> a(n), b(m);
    for (auto &x : a) cin >> x;
    for (auto &x : b) cin >> x;
    vector<int> merged;
    int i = 0, j = 0;
    while (i < n && j < m) merged.push_back(a[i] <= b[j] ? a[i++] : b[j++]);
    while (i < n) merged.push_back(a[i++]);
    while (j < m) merged.push_back(b[j++]);
    for (size_t k = 0; k < merged.size(); k++)
        cout << merged[k] << (k + 1 < merged.size() ? ' ' : '\n');
    return 0;
}
""",
    ),
]
