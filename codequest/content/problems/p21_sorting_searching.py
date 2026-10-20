"""Sorting & Searching: binary search on the answer, rotated arrays, heaps, intervals."""


def _arr(xs):
    return " ".join(map(str, xs))


def _koko_gen(rng):
    out = []
    for n, pmax in ((1, 10), (5, 100), (200, 10**6), (3000, 10**9)):
        piles = [rng.randint(1, pmax) for _ in range(n)]
        h = rng.randint(n, n * 3 + 5)
        out.append(f"{n} {h}\n{_arr(piles)}")
    n = 2000
    piles = [rng.randint(1, 10**9) for _ in range(n)]
    out.append(f"{n} {10**9}\n{_arr(piles)}")
    return out


def _rot_case(rng, n, q):
    vals = sorted(rng.sample(range(-10**6, 10**6), n))
    k = rng.randrange(n)
    a = vals[k:] + vals[:k]
    qs = [rng.choice(a) if rng.random() < 0.6 else rng.randint(-10**6, 10**6) for _ in range(q)]
    return f"{n} {q}\n{_arr(a)}\n{_arr(qs)}"


def _rot_gen(rng):
    return [_rot_case(rng, 1, 3), _rot_case(rng, 2, 4), _rot_case(rng, 30, 30),
            _rot_case(rng, 2500, 2500)]


def _kth_gen(rng):
    out = []
    for n, k in ((1, 1), (10, 3), (200, 1), (2000, 50), (1500, 1200)):
        out.append(f"{n} {k}\n{_arr(rng.randint(-10**4, 10**4) for _ in range(n))}")
    return out


def _iv_case(rng, n, span, maxlen):
    lines = []
    for _ in range(n):
        l = rng.randint(0, span)
        lines.append(f"{l} {l + rng.randint(0, maxlen)}")
    return f"{n}\n" + "\n".join(lines)


def _merge_iv_gen(rng):
    return [_iv_case(rng, 1, 10, 5), _iv_case(rng, 8, 50, 6), _iv_case(rng, 200, 10000, 30),
            _iv_case(rng, 600, 10**9, 10**6), _iv_case(rng, 1000, 20000, 20)]


def _room_case(rng, n, span, maxlen):
    lines = []
    for _ in range(n):
        s = rng.randint(0, span)
        lines.append(f"{s} {s + rng.randint(1, maxlen)}")
    return f"{n}\n" + "\n".join(lines)


def _rooms_gen(rng):
    return [_room_case(rng, 1, 10, 5), _room_case(rng, 10, 20, 5), _room_case(rng, 300, 1000, 100),
            _room_case(rng, 2000, 10**6, 10**5), _room_case(rng, 2000, 500, 3)]


PROBLEMS = [
    dict(
        id="banana-feast-speed",
        title="Banana Feast Speed",
        difficulty="medium",
        category="Sorting & Searching",
        tags=["binary-search", "binary-search-on-answer"],
        inspired_by="LeetCode #875 Koko Eating Bananas",
        statement="""
A hungry orangutan finds `n` piles of bananas; pile `i` has `p[i]` bananas.
The keepers return in `h` hours.

The orangutan picks an eating speed `k` (bananas per hour). Every hour it
chooses one pile and eats `k` bananas from it; if the pile has fewer than `k`
left, it finishes that pile and waits for the rest of the hour. So a pile of
`p` bananas takes `⌈p / k⌉` hours.

Find the **minimum integer speed** `k` that lets it finish all piles within
`h` hours.

For piles `3 6 7 11` and `h = 8`, speed 4 takes 1 + 2 + 2 + 3 = 8 hours, and
speed 3 would take 10 hours, so the answer is 4.
""",
        input_format="""First line: `n h` (1 ≤ n ≤ 10⁴, n ≤ h ≤ 10⁹).
Second line: `n` integers `p[i]` (1 ≤ p[i] ≤ 10⁹).""",
        output_format="One integer: the minimum speed `k`.",
        hints=[
            "If speed `k` works, every faster speed works too. A yes/no property that flips once is the signal for "
            "**binary search on the answer**.",
            "Search `k` in `[1, max(p)]`. For a candidate `k`, total hours = Σ ⌈p[i] / k⌉ — compute the ceiling with "
            "integer math: `(p + k - 1) // k` (C++: `(p + k - 1) / k`).",
            "Loop `while lo < hi`: `mid = (lo + hi) // 2`; if `mid` is fast enough set `hi = mid`, else `lo = mid + 1`. "
            "In C++ keep the hour total in a `long long`.",
        ],
        samples=["4 8\n3 6 7 11", "5 5\n30 11 23 4 20", "5 6\n30 11 23 4 20"],
        tests=["1 1\n1", "1 1000000000\n1000000000", "1 1\n1000000000", "3 3\n1 1 1",
               "2 1000000000\n1000000000 1000000000"],
        gen=_koko_gen,
        starter_python="""n, h = map(int, input().split())
p = list(map(int, input().split()))

def hours_needed(k):
    # TODO: total hours at speed k
    return 0

# TODO: binary search the smallest k with hours_needed(k) <= h
print(1)
""",
        starter_cpp="""#include <iostream>
#include <vector>
using namespace std;

int main() {
    long long n, h;
    cin >> n >> h;
    vector<long long> p(n);
    for (auto &x : p) cin >> x;
    // TODO: binary search on k in [1, max(p)]
    cout << 1 << "\\n";
    return 0;
}
""",
        solution_python=r"""n, h = map(int, input().split())
p = list(map(int, input().split()))

def ok(k):
    return sum((x + k - 1) // k for x in p) <= h

lo, hi = 1, max(p)
while lo < hi:
    mid = (lo + hi) // 2
    if ok(mid):
        hi = mid
    else:
        lo = mid + 1
print(lo)
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    long long n, h;
    cin >> n >> h;
    vector<long long> p(n);
    for (auto &x : p) cin >> x;
    long long lo = 1, hi = *max_element(p.begin(), p.end());
    while (lo < hi) {
        long long mid = (lo + hi) / 2, t = 0;
        for (long long x : p) t += (x + mid - 1) / mid;
        if (t <= h) hi = mid; else lo = mid + 1;
    }
    cout << lo << "\n";
    return 0;
}
""",
    ),
    dict(
        id="rotated-sorted-lookup",
        title="Lookup in a Rotated List",
        difficulty="medium",
        category="Sorting & Searching",
        tags=["binary-search", "arrays"],
        inspired_by="LeetCode #33 Search in Rotated Sorted Array",
        statement="""
A list of **distinct** integers was sorted in increasing order and then
*rotated*: some prefix was cut off and moved to the end. For example
`1 3 5 7 9 11` might become `7 9 11 1 3 5`.

Answer `q` queries: for each value `x`, print its 0-based position in the
rotated list, or `-1` if it is not there.

Aim for **O(log n)** per query, without first undoing the rotation by sorting.
""",
        input_format="""First line: `n q` (1 ≤ n, q ≤ 5000).
Second line: the rotated list (`n` distinct integers, |aᵢ| ≤ 10⁶).
Third line: `q` query values (|x| ≤ 10⁶).""",
        output_format="`q` lines: the index of each query value, or `-1`.",
        hints=[
            "Binary search still works: for any `mid`, at least one of the halves `[lo, mid]` and `[mid, hi]` is "
            "sorted normally.",
            "If `a[lo] <= a[mid]` the left half is sorted: `x` lies in it exactly when `a[lo] <= x < a[mid]`. "
            "Otherwise the right half is sorted: check `a[mid] < x <= a[hi]`.",
            "Alternative: first binary-search the rotation point (the index of the minimum), then run an ordinary "
            "`bisect_left` / `lower_bound` on the correct sorted piece.",
        ],
        samples=["6 3\n7 9 11 1 3 5\n3 11 4", "1 2\n5\n5 0"],
        tests=["5 5\n1 2 3 4 5\n1 5 3 0 6", "5 5\n5 1 2 3 4\n5 4 1 2 3", "2 3\n2 1\n1 2 3"],
        gen=_rot_gen,
        starter_python="""n, q = map(int, input().split())
a = list(map(int, input().split()))
queries = list(map(int, input().split()))

def find(x):
    lo, hi = 0, n - 1
    # TODO: modified binary search
    return -1

print("\\n".join(str(find(x)) for x in queries))
""",
        starter_cpp="""#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<int> a(n);
    for (auto &x : a) cin >> x;
    while (q--) {
        int x;
        cin >> x;
        int ans = -1;
        // TODO: modified binary search for x
        cout << ans << "\\n";
    }
    return 0;
}
""",
        solution_python=r"""n, q = map(int, input().split())
a = list(map(int, input().split()))
queries = list(map(int, input().split()))

def find(x):
    lo, hi = 0, n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == x:
            return mid
        if a[lo] <= a[mid]:
            if a[lo] <= x < a[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if a[mid] < x <= a[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1

print("\n".join(str(find(x)) for x in queries))
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<int> a(n);
    for (auto &x : a) cin >> x;
    while (q--) {
        int x;
        cin >> x;
        int lo = 0, hi = n - 1, ans = -1;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;
            if (a[mid] == x) { ans = mid; break; }
            if (a[lo] <= a[mid]) {
                if (a[lo] <= x && x < a[mid]) hi = mid - 1; else lo = mid + 1;
            } else {
                if (a[mid] < x && x <= a[hi]) lo = mid + 1; else hi = mid - 1;
            }
        }
        cout << ans << "\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="leaderboard-kth-place",
        title="Leaderboard k-th Place",
        difficulty="medium",
        category="Sorting & Searching",
        tags=["heap", "priority-queue", "streaming"],
        inspired_by="LeetCode #215 / #703 Kth Largest Element (in a Stream)",
        statement="""
Scores arrive one at a time during a tournament. After each new score, the
organisers want to know the score currently in **k-th place**, i.e. the k-th
largest score so far (equal scores take separate places, so in `9 9 4` the
2nd place score is 9).

If fewer than `k` scores have arrived, print `-1` instead.

Re-sorting everything after every score is O(n² log n) — too slow for the big
tests. Keep just the information you need.
""",
        input_format="""First line: `n k` (1 ≤ k ≤ n ≤ 2000).
Second line: the `n` scores in arrival order (|sᵢ| ≤ 10⁴).""",
        output_format="`n` integers, one per line: the k-th largest score after each arrival (or `-1`).",
        hints=[
            "You only ever need the `k` largest scores seen so far — and of those, only the smallest one is printed.",
            "A **min-heap** of size `k` does exactly that: its top is the k-th largest. "
            "Python: `heapq.heappush`, `heapq.heappop`, `heap[0]`; C++: `priority_queue<int, vector<int>, greater<int>>`.",
            "Push every new score; if the heap grows to `k + 1` elements, pop the smallest. Print the top once the heap "
            "has `k` elements.",
        ],
        samples=["5 3\n4 5 8 2 3", "4 1\n-1 7 3 10"],
        tests=["1 1\n5", "3 3\n1 1 1", "6 2\n9 9 4 10 10 1", "4 4\n-5 -6 -7 -8"],
        gen=_kth_gen,
        starter_python="""import heapq

n, k = map(int, input().split())
scores = list(map(int, input().split()))
heap = []
out = []
for s in scores:
    # TODO: keep only the k largest scores in a min-heap
    out.append(-1)
print("\\n".join(map(str, out)))
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <queue>
#include <functional>
using namespace std;

int main() {
    int n, k;
    cin >> n >> k;
    priority_queue<int, vector<int>, greater<int>> heap;  // min-heap
    for (int i = 0; i < n; i++) {
        int s;
        cin >> s;
        // TODO: push s, keep size <= k, print the k-th largest or -1
        cout << -1 << "\\n";
    }
    return 0;
}
""",
        solution_python=r"""import heapq

n, k = map(int, input().split())
scores = list(map(int, input().split()))
heap = []
out = []
for s in scores:
    heapq.heappush(heap, s)
    if len(heap) > k:
        heapq.heappop(heap)
    out.append(heap[0] if len(heap) == k else -1)
print("\n".join(map(str, out)))
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <queue>
#include <functional>
using namespace std;

int main() {
    int n, k;
    cin >> n >> k;
    priority_queue<int, vector<int>, greater<int>> heap;
    for (int i = 0; i < n; i++) {
        int s;
        cin >> s;
        heap.push(s);
        if ((int)heap.size() > k) heap.pop();
        cout << ((int)heap.size() == k ? heap.top() : -1) << "\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="merge-busy-intervals",
        title="Merge Busy Intervals",
        difficulty="medium",
        category="Sorting & Searching",
        tags=["sorting", "intervals", "sweep"],
        inspired_by="LeetCode #56 Merge Intervals",
        statement="""
A calendar holds `n` busy intervals `[l, r]` (closed: both ends included).
Intervals may overlap and are given in no particular order.

Merge every group of overlapping intervals into one. Intervals that merely
**touch** (one ends at `t`, the next starts at `t`) also merge. For example
`[1,3] [2,6] [8,10] [10,12] [15,18]` becomes `[1,6] [8,12] [15,18]`.

Print the merged intervals sorted by their start.
""",
        input_format="First line: `n` (1 ≤ n ≤ 1000). Next `n` lines: `l r` (0 ≤ l ≤ r ≤ 2·10⁹).",
        output_format="First line: the number `m` of merged intervals. Then `m` lines `l r`, sorted by `l`.",
        hints=[
            "Sort the intervals by their start. After sorting, intervals that should merge sit next to each other.",
            "Walk through them keeping a *current* merged interval `[cl, cr]`. If the next `l <= cr` it overlaps: "
            "extend `cr = max(cr, r)`. Otherwise close the current one and start a new one.",
            "Python: `iv.sort()` sorts pairs by first element, then second. C++: `sort(v.begin(), v.end())` on a "
            "`vector<pair<long long,long long>>` does the same. Values reach 2·10⁹, so use `long long`.",
        ],
        samples=["5\n1 3\n2 6\n8 10\n10 12\n15 18", "2\n5 5\n1 4"],
        tests=["1\n0 0", "3\n1 10\n2 3\n4 5", "3\n1 2\n3 4\n5 6", "2\n0 2000000000\n2000000000 2000000000"],
        gen=_merge_iv_gen,
        starter_python="""n = int(input())
iv = [tuple(map(int, input().split())) for _ in range(n)]
merged = []
# TODO: sort, then sweep and merge
print(len(merged))
for l, r in merged:
    print(l, r)
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<pair<long long, long long>> iv(n);
    for (auto &p : iv) cin >> p.first >> p.second;
    vector<pair<long long, long long>> merged;
    // TODO: sort, then sweep and merge
    cout << merged.size() << "\\n";
    for (auto &p : merged) cout << p.first << " " << p.second << "\\n";
    return 0;
}
""",
        solution_python=r"""import sys

data = sys.stdin.read().split()
n = int(data[0])
iv = sorted((int(data[1 + 2 * i]), int(data[2 + 2 * i])) for i in range(n))
merged = []
for l, r in iv:
    if merged and l <= merged[-1][1]:
        if r > merged[-1][1]:
            merged[-1][1] = r
    else:
        merged.append([l, r])
out = [str(len(merged))] + [f"{l} {r}" for l, r in merged]
print("\n".join(out))
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<pair<long long, long long>> iv(n);
    for (auto &p : iv) cin >> p.first >> p.second;
    sort(iv.begin(), iv.end());
    vector<pair<long long, long long>> merged;
    for (auto &p : iv) {
        if (!merged.empty() && p.first <= merged.back().second)
            merged.back().second = max(merged.back().second, p.second);
        else
            merged.push_back(p);
    }
    cout << merged.size() << "\n";
    for (auto &p : merged) cout << p.first << " " << p.second << "\n";
    return 0;
}
""",
    ),
    dict(
        id="conference-rooms-needed",
        title="Conference Rooms Needed",
        difficulty="medium",
        category="Sorting & Searching",
        tags=["sorting", "heap", "sweep-line", "intervals"],
        inspired_by="LeetCode #253 Meeting Rooms II",
        statement="""
An office has `n` meetings planned for tomorrow. Meeting `i` occupies a room
from time `s[i]` up to (but not including) time `e[i]` — so a meeting ending
at 10 and another starting at 10 can share a room.

What is the **minimum number of rooms** needed so every meeting gets a room
for its whole duration?
""",
        input_format="First line: `n` (1 ≤ n ≤ 2000). Next `n` lines: `s e` (0 ≤ s < e ≤ 2·10⁶).",
        output_format="One integer: the minimum number of rooms.",
        hints=[
            "The answer is the largest number of meetings running at the same instant.",
            "Sweep line: make events `(s, +1)` and `(e, −1)`, sort them and keep a running sum. "
            "Ends must be processed **before** starts at the same time — sorting the pairs does this for free since −1 < +1.",
            "Alternative: sort meetings by start and keep a min-heap of end times of rooms in use "
            "(`heapq` / `priority_queue<int, vector<int>, greater<int>>`); reuse the room that frees up earliest.",
        ],
        samples=["3\n0 30\n5 10\n15 20", "2\n7 10\n2 4", "3\n1 10\n10 20\n5 10"],
        tests=["1\n0 1", "4\n1 5\n1 5\n1 5\n1 5", "4\n1 2\n2 3\n3 4\n4 5"],
        gen=_rooms_gen,
        starter_python="""n = int(input())
meetings = [tuple(map(int, input().split())) for _ in range(n)]
rooms = 0
# TODO: sweep over start/end events (or use a heap of end times)
print(rooms)
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<pair<int, int>> m(n);
    for (auto &p : m) cin >> p.first >> p.second;
    int rooms = 0;
    // TODO: sweep over start/end events
    cout << rooms << "\\n";
    return 0;
}
""",
        solution_python=r"""import sys

data = list(map(int, sys.stdin.read().split()))
n = data[0]
events = []
for i in range(n):
    events.append((data[1 + 2 * i], 1))
    events.append((data[2 + 2 * i], -1))
events.sort()
cur = best = 0
for _, d in events:
    cur += d
    if cur > best:
        best = cur
print(best)
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<pair<int, int>> ev;
    for (int i = 0; i < n; i++) {
        int s, e;
        cin >> s >> e;
        ev.push_back({s, 1});
        ev.push_back({e, -1});
    }
    sort(ev.begin(), ev.end());
    int cur = 0, best = 0;
    for (auto &p : ev) {
        cur += p.second;
        best = max(best, cur);
    }
    cout << best << "\n";
    return 0;
}
""",
    ),
]
