"""Hard / expert data-structure problems: LRU cache, trie, heaps, k-th smallest by binary search."""


def _gen_lru(rng):
    tests = []
    for c, q, keyspace in [(50, 2200, 120), (1, 400, 5), (300, 600, 200)]:
        ops = []
        for _ in range(q):
            k = rng.randint(1, keyspace)
            if rng.random() < 0.5:
                ops.append(f"get {k}")
            else:
                ops.append(f"put {k} {rng.randint(0, 10**6)}")
        tests.append(f"{c} {q}\n" + "\n".join(ops))
    return tests


def _gen_trie(rng):
    tests = []
    # many short words over a tiny alphabet: lots of shared prefixes
    words = ["".join(rng.choice("ab") for _ in range(rng.randint(1, 6))) for _ in range(5000)]
    tests.append(f"{len(words)}\n" + "\n".join(words))
    # a few long words sharing long prefixes
    base = "".join(rng.choice("xyz") for _ in range(2000))
    words = [base[:rng.randint(1500, 2000)] + "".join(rng.choice("xyz") for _ in range(rng.randint(0, 50)))
             for _ in range(6)]
    tests.append(f"{len(words)}\n" + "\n".join(words))
    # medium random words over the full alphabet, with duplicates
    pool = ["".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(rng.randint(1, 8))) for _ in range(300)]
    words = [rng.choice(pool) if rng.random() < 0.5 else rng.choice(pool)[:rng.randint(1, 4)] + "q"
             for _ in range(1500)]
    tests.append(f"{len(words)}\n" + "\n".join(words))
    return tests


def _gen_median(rng):
    tests = []
    for n, lo, hi in [(1800, -10**9, 10**9), (800, 1, 10), (600, -50, 50)]:
        tests.append(f"{n}\n" + " ".join(str(rng.randint(lo, hi)) for _ in range(n)))
    # increasing then decreasing
    vals = list(range(1, 301)) + list(range(300, 0, -1))
    tests.append(f"{len(vals)}\n" + " ".join(map(str, vals)))
    return tests


def _gen_kth(rng):
    tests = []
    for n, m, hi, kind in [(1500, 1500, 10**6, "any"), (700, 300, 1000, "last"), (1, 2000, 10**6, "any"),
                           (400, 400, 3, "any"), (300, 300, 10**6, "small")]:
        a = [rng.randint(1, hi) for _ in range(n)]
        b = [rng.randint(1, hi) for _ in range(m)]
        k = {"any": rng.randint(1, n * m), "last": n * m, "small": rng.randint(1, 50)}[kind]
        tests.append(f"{n} {m} {k}\n" + " ".join(map(str, a)) + "\n" + " ".join(map(str, b)))
    return tests


PROBLEMS = [
    dict(
        id="lru-cache-simulator",
        title="LRU Cache Simulator",
        difficulty="hard",
        category="Data Structures",
        tags=["design", "hash-map", "linked-list", "lru"],
        inspired_by="LeetCode #146 LRU Cache",
        statement="""
Simulate a **least-recently-used** (LRU) cache that holds at most `c` key→value pairs.
It receives `q` commands:

* `get k` — if key `k` is in the cache, print its value and mark `k` as **most recently used**; otherwise print `-1`.
* `put k v` — store value `v` under key `k` (overwriting any old value) and mark `k` as most recently used.
  If the cache now holds more than `c` keys, **evict** the least recently used key.

Both operations should take O(1) time.
""",
        input_format="""
First line: `c q` (1 ≤ c ≤ 1000, 1 ≤ q ≤ 2500).
Next `q` lines: `get k` or `put k v` (1 ≤ k ≤ 10⁶, 0 ≤ v ≤ 10⁶).
""",
        output_format="For every `get`, one line with the value or `-1`.",
        hints=[
            "You need two things at once: find a key fast (a **hash map**) and know the usage **order** (a list where "
            "you can move any element to the front and remove from the back in O(1)).",
            "Classic design: a doubly linked list ordered by recency + a hash map from key to its list node.",
            "Python: `collections.OrderedDict` is exactly that — `od.move_to_end(k)` marks as recent, "
            "`od.popitem(last=False)` evicts the oldest.",
            "C++: `list<pair<int,int>>` for the order plus `unordered_map<int, list<pair<int,int>>::iterator>`; "
            "`lst.splice(lst.begin(), lst, it)` moves a node to the front without invalidating iterators. "
            "Remember that `put` on an existing key also refreshes it.",
        ],
        samples=[
            "2 9\nput 1 10\nput 2 20\nget 1\nput 3 30\nget 2\nget 3\nput 1 11\nget 1\nget 3",
        ],
        tests=[
            "1 4\nget 5\nput 5 0\nget 5\nget 6",
            "1 4\nput 1 1\nput 2 2\nget 1\nget 2",
            "2 6\nput 1 1\nput 2 2\nput 1 5\nput 3 3\nget 2\nget 1",
        ],
        gen=_gen_lru,
        starter_python="""import sys
from collections import OrderedDict

def main():
    data = sys.stdin.read().split()
    c, q = int(data[0]), int(data[1])
    cache = OrderedDict()
    out = []
    pos = 2
    for _ in range(q):
        if data[pos] == "get":
            k = int(data[pos + 1])
            pos += 2
            out.append(-1)  # TODO
        else:
            k, v = int(data[pos + 1]), int(data[pos + 2])
            pos += 3
            # TODO
    print("\\n".join(map(str, out)))

main()
""",
        starter_cpp="""#include <iostream>
#include <string>
#include <list>
#include <unordered_map>
#include <utility>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int c, q;
    cin >> c >> q;
    while (q--) {
        string op;
        cin >> op;
        if (op == "get") {
            int k; cin >> k;
            cout << -1 << "\\n";  // TODO
        } else {
            int k, v; cin >> k >> v;
            // TODO
        }
    }
    return 0;
}
""",
        solution_python="""import sys
from collections import OrderedDict

def main():
    data = sys.stdin.read().split()
    c, q = int(data[0]), int(data[1])
    cache = OrderedDict()
    out = []
    pos = 2
    for _ in range(q):
        if data[pos] == "get":
            k = int(data[pos + 1])
            pos += 2
            if k in cache:
                cache.move_to_end(k)
                out.append(cache[k])
            else:
                out.append(-1)
        else:
            k, v = int(data[pos + 1]), int(data[pos + 2])
            pos += 3
            cache[k] = v
            cache.move_to_end(k)
            if len(cache) > c:
                cache.popitem(last=False)
    print("\\n".join(map(str, out)))

main()
""",
        solution_cpp="""#include <iostream>
#include <string>
#include <list>
#include <unordered_map>
#include <utility>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int c, q;
    cin >> c >> q;
    list<pair<int,int>> order;   // front = most recent
    unordered_map<int, list<pair<int,int>>::iterator> where;
    while (q--) {
        string op;
        cin >> op;
        if (op == "get") {
            int k; cin >> k;
            auto it = where.find(k);
            if (it == where.end()) { cout << -1 << "\\n"; continue; }
            order.splice(order.begin(), order, it->second);
            cout << it->second->second << "\\n";
        } else {
            int k, v; cin >> k >> v;
            auto it = where.find(k);
            if (it != where.end()) {
                it->second->second = v;
                order.splice(order.begin(), order, it->second);
            } else {
                order.push_front({k, v});
                where[k] = order.begin();
                if ((int)order.size() > c) {
                    where.erase(order.back().first);
                    order.pop_back();
                }
            }
        }
    }
    return 0;
}
""",
    ),
    dict(
        id="trie-pairwise-lcp",
        title="Total Prefix Affinity",
        difficulty="expert",
        category="Data Structures",
        tags=["trie", "strings", "counting"],
        inspired_by="Codeforces / AtCoder ABC 287 E-style LCP sums; LeetCode #208 Implement Trie",
        statement="""
A dictionary contains `n` words (possibly with repeats). The **affinity** of two
words is the length of their longest common prefix: `affinity("carpet", "cart") = 3`,
`affinity("dog", "cat") = 0`, and a word repeated twice has affinity equal to its length.

Compute the sum of affinities over **all pairs** `i < j` of dictionary entries.
""",
        input_format="""
First line: `n` (1 ≤ n ≤ 10⁴).
Next `n` lines: one word each (lowercase letters, length ≥ 1). The total length of all words is at most 3·10⁴.
""",
        output_format="One integer: the total affinity.",
        hints=[
            "Comparing every pair is up to 5·10⁷ pairs. Instead, flip the sum around: a pair with common prefix "
            "length L contributes 1 for **each** of the L shared prefixes.",
            "So the answer is `Σ over every non-empty prefix p of C(cnt(p), 2)`, where `cnt(p)` is how many words start with `p`.",
            "A **trie** gives you all those counts: insert every word, incrementing a counter on every node you pass "
            "(each node = one prefix). Then add `cnt·(cnt−1)/2` over all nodes except the root.",
            "Python: store children as a list of dicts (`children[node].get(ch)`). C++: `vector<array<int,26>>` "
            "with `-1`/0 for missing children. The answer can exceed 2³¹ — use `long long`.",
        ],
        samples=[
            "4\ncarpet\ncart\ncat\ndog",
            "3\naa\naa\na",
        ],
        tests=[
            "1\nhello",
            "2\nabc\nxyz",
            "5\nz\nz\nz\nz\nz",
            "3\nabcdefghij\nabcdefghij\nabcdefghij",
        ],
        gen=_gen_trie,
        starter_python="""import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    words = data[1:1 + n]
    children = [{}]   # children[node] maps a letter to a child node
    cnt = [0]         # cnt[node] = number of words passing through
    # TODO: insert the words, then sum cnt*(cnt-1)//2 over non-root nodes
    print(0)

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <string>
#include <array>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<string> words(n);
    for (auto &w : words) cin >> w;
    vector<array<int,26>> child(1);
    child[0].fill(0);           // 0 = no child (node 0 is the root)
    vector<long long> cnt(1, 0);
    // TODO: insert the words, then sum cnt*(cnt-1)/2 over non-root nodes
    cout << 0 << "\\n";
    return 0;
}
""",
        solution_python="""import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    children = [{}]
    cnt = [0]
    for w in data[1:1 + n]:
        v = 0
        for ch in w:
            nxt = children[v].get(ch)
            if nxt is None:
                nxt = len(cnt)
                children[v][ch] = nxt
                children.append({})
                cnt.append(0)
            v = nxt
            cnt[v] += 1
    print(sum(c * (c - 1) // 2 for c in cnt[1:]))

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <string>
#include <array>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<array<int,26>> child(1);
    child[0].fill(0);
    vector<long long> cnt(1, 0);
    for (int i = 0; i < n; i++) {
        string w;
        cin >> w;
        int v = 0;
        for (char ch : w) {
            int c = ch - 'a';
            if (!child[v][c]) {
                child[v][c] = child.size();
                child.emplace_back();
                child.back().fill(0);
                cnt.push_back(0);
            }
            v = child[v][c];
            cnt[v]++;
        }
    }
    long long ans = 0;
    for (size_t v = 1; v < cnt.size(); v++) ans += cnt[v] * (cnt[v] - 1) / 2;
    cout << ans << "\\n";
    return 0;
}
""",
    ),
    dict(
        id="running-median-stream",
        title="Running Median",
        difficulty="hard",
        category="Data Structures",
        tags=["heap", "priority-queue", "median", "streaming"],
        inspired_by="LeetCode #295 Find Median from Data Stream",
        statement="""
Numbers arrive one at a time. After each arrival, report the **median** of all
numbers received so far. When the count is even there are two middle values;
report the **smaller** one (the "lower median").

For example, after `5, 2, 8, 1` the sorted numbers are `1 2 5 8`, the middle
values are 2 and 5, so the answer is `2`.
""",
        input_format="""
First line: `n` (1 ≤ n ≤ 2000).
Second line: `n` integers (|x| ≤ 10⁹), in order of arrival.
""",
        output_format="`n` integers separated by spaces: the median after each arrival.",
        hints=[
            "Re-sorting after every arrival costs O(n² log n) in total. Keep the data split into two halves instead.",
            "**Two heaps**: a max-heap `low` with the smaller half and a min-heap `high` with the larger half. "
            "Invariant: every element of `low` ≤ every element of `high`, and `len(low)` is `len(high)` or `len(high) + 1`.",
            "Insert into `low` if `x ≤ max(low)`, else into `high`; then move one element across if the sizes break "
            "the invariant. The lower median is always the top of `low`.",
            "Python's `heapq` is a min-heap only: store negatives (`heappush(low, -x)`) to get a max-heap. "
            "C++: `priority_queue<long long>` (max) and `priority_queue<long long, vector<long long>, greater<long long>>` (min).",
        ],
        samples=[
            "4\n5 2 8 1",
            "6\n1 2 3 4 5 6",
        ],
        tests=[
            "1\n-7",
            "5\n3 3 3 3 3",
            "4\n1000000000 -1000000000 1000000000 -1000000000",
            "5\n10 9 8 7 6",
        ],
        gen=_gen_median,
        starter_python="""import sys
import heapq

def main():
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    low, high = [], []    # low: max-heap via negatives, high: min-heap
    out = []
    for x in data[1:1 + n]:
        # TODO: insert x, rebalance, record the lower median
        out.append(x)
    print(" ".join(map(str, out)))

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <queue>
#include <functional>
using namespace std;

int main() {
    int n;
    cin >> n;
    priority_queue<long long> low;                                       // max-heap
    priority_queue<long long, vector<long long>, greater<long long>> high; // min-heap
    for (int i = 0; i < n; i++) {
        long long x;
        cin >> x;
        // TODO: insert x, rebalance, print the lower median
        cout << x << (i + 1 < n ? ' ' : '\\n');
    }
    return 0;
}
""",
        solution_python="""import sys
import heapq

def main():
    data = list(map(int, sys.stdin.read().split()))
    n = data[0]
    low, high = [], []
    out = []
    for x in data[1:1 + n]:
        if not low or x <= -low[0]:
            heapq.heappush(low, -x)
        else:
            heapq.heappush(high, x)
        if len(low) > len(high) + 1:
            heapq.heappush(high, -heapq.heappop(low))
        elif len(high) > len(low):
            heapq.heappush(low, -heapq.heappop(high))
        out.append(-low[0])
    print(" ".join(map(str, out)))

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <queue>
#include <functional>
using namespace std;

int main() {
    int n;
    cin >> n;
    priority_queue<long long> low;
    priority_queue<long long, vector<long long>, greater<long long>> high;
    for (int i = 0; i < n; i++) {
        long long x;
        cin >> x;
        if (low.empty() || x <= low.top()) low.push(x); else high.push(x);
        if (low.size() > high.size() + 1) { high.push(low.top()); low.pop(); }
        else if (high.size() > low.size()) { low.push(high.top()); high.pop(); }
        cout << low.top() << (i + 1 < n ? ' ' : '\\n');
    }
    return 0;
}
""",
    ),
    dict(
        id="kth-smallest-pair-sum",
        title="K-th Cheapest Combo Meal",
        difficulty="expert",
        category="Data Structures",
        tags=["binary-search-on-answer", "two-pointers", "heap", "k-th-smallest"],
        inspired_by="LeetCode #373 Find K Pairs with Smallest Sums / #719 Find K-th Smallest Pair Distance",
        statement="""
A diner sells `n` main dishes with prices `a₁ … aₙ` and `m` drinks with prices
`b₁ … bₘ`. A combo is one main dish plus one drink; there are `n · m` combos
(different dishes or drinks give different combos, even when prices coincide).

List all combo prices in non-decreasing order. What is the `k`-th price in that list?

`k` can be as large as `n · m` = 4·10⁶, so generating the combos in order one by one may be too slow.
""",
        input_format="""
First line: `n m k` (1 ≤ n, m ≤ 2000, 1 ≤ k ≤ n·m).
Second line: `n` integers `aᵢ`; third line: `m` integers `bⱼ` (1 ≤ aᵢ, bⱼ ≤ 10⁶).
""",
        output_format="One integer: the `k`-th smallest combo price.",
        hints=[
            "For small `k` a min-heap works: start with `(a[i] + b[0], i, 0)` for each `i` (after sorting) and pop `k` times, "
            "pushing `(a[i] + b[j+1], i, j+1)`. But `k` may be 4·10⁶ — think differently.",
            "**Binary search on the answer**: for a price `S`, let `count(S)` = number of combos costing ≤ S. "
            "`count` is non-decreasing in `S`, and the answer is the smallest `S` with `count(S) ≥ k`.",
            "After sorting both arrays, `count(S)` is a **two-pointer** sweep: as `a[i]` increases, the number of drinks "
            "with `b[j] ≤ S − a[i]` can only decrease. That is O(n + m) per check.",
            "Search `S` in `[min a + min b, max a + max b]` — about 21 iterations. "
            "(Python alternative for the count: `sum(bisect_right(b, S - x) for x in a)`.)",
        ],
        samples=[
            "3 3 4\n1 7 11\n2 4 6",
            "2 2 4\n5 5\n1 1",
        ],
        tests=[
            "1 1 1\n1000000\n1000000",
            "3 1 2\n3 1 2\n10",
            "2 3 6\n1 2\n3 3 3",
            "4 4 1\n9 8 7 6\n5 4 3 2",
        ],
        gen=_gen_kth,
        starter_python="""import sys
from bisect import bisect_right

def main():
    data = list(map(int, sys.stdin.read().split()))
    n, m, k = data[0], data[1], data[2]
    a = sorted(data[3:3 + n])
    b = sorted(data[3 + n:3 + n + m])
    # TODO: binary search on the price S, counting combos with price <= S
    print(0)

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n, m;
    long long k;
    cin >> n >> m >> k;
    vector<long long> a(n), b(m);
    for (auto &x : a) cin >> x;
    for (auto &x : b) cin >> x;
    sort(a.begin(), a.end());
    sort(b.begin(), b.end());
    // TODO: binary search on the price S, counting combos with price <= S
    cout << 0 << "\\n";
    return 0;
}
""",
        solution_python="""import sys

def main():
    data = list(map(int, sys.stdin.read().split()))
    n, m, k = data[0], data[1], data[2]
    a = sorted(data[3:3 + n])
    b = sorted(data[3 + n:3 + n + m])

    def count(S):
        total, j = 0, m
        for x in a:
            while j > 0 and x + b[j - 1] > S:
                j -= 1
            if j == 0:
                break
            total += j
        return total

    lo, hi = a[0] + b[0], a[-1] + b[-1]
    while lo < hi:
        mid = (lo + hi) // 2
        if count(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    print(lo)

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n, m;
    long long k;
    cin >> n >> m >> k;
    vector<long long> a(n), b(m);
    for (auto &x : a) cin >> x;
    for (auto &x : b) cin >> x;
    sort(a.begin(), a.end());
    sort(b.begin(), b.end());
    auto count = [&](long long S) {
        long long total = 0;
        int j = m;
        for (long long x : a) {
            while (j > 0 && x + b[j - 1] > S) j--;
            if (j == 0) break;
            total += j;
        }
        return total;
    };
    long long lo = a[0] + b[0], hi = a[n - 1] + b[m - 1];
    while (lo < hi) {
        long long mid = (lo + hi) / 2;
        if (count(mid) >= k) hi = mid; else lo = mid + 1;
    }
    cout << lo << "\\n";
    return 0;
}
""",
    ),
]
