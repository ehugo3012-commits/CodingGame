"""Hard data-structure problems: Fenwick tree, segment tree, union-find."""


def _gen_ledger(rng):
    tests = []
    for n, q, xmax in [(100000, 1800, 10**9), (1000, 800, 10**9), (5, 300, 10)]:
        ops = []
        for _ in range(q):
            if rng.random() < 0.5:
                ops.append(f"1 {rng.randint(1, n)} {rng.randint(-xmax, xmax)}")
            else:
                l = rng.randint(1, n)
                r = rng.randint(l, n) if rng.random() < 0.8 else l
                ops.append(f"2 {l} {r}")
        tests.append(f"{n} {q}\n" + "\n".join(ops))
    return tests


def _gen_rmq(rng):
    tests = []
    for n, q, vmax in [(3000, 1400, 10000), (500, 600, 5), (1, 50, 100)]:
        a = [rng.randint(1, vmax) for _ in range(n)]
        ops = []
        for _ in range(q):
            if rng.random() < 0.4:
                ops.append(f"1 {rng.randint(1, n)} {rng.randint(1, vmax)}")
            else:
                l = rng.randint(1, n)
                ops.append(f"2 {l} {rng.randint(l, n)}")
        tests.append(f"{n} {q}\n" + " ".join(map(str, a)) + "\n" + "\n".join(ops))
    return tests


def _gen_dsu(rng):
    tests = []
    for n, q, local in [(2000, 1500, False), (100000, 400, False), (300, 600, True), (2, 5, False)]:
        ops = []
        for _ in range(q):
            a = rng.randint(1, n)
            b = rng.randint(max(1, a - 20), min(n, a + 20)) if local else rng.randint(1, n)
            ops.append(f"{a} {b}")
        tests.append(f"{n} {q}\n" + "\n".join(ops))
    return tests


PROBLEMS = [
    dict(
        id="fenwick-bank-ledger",
        title="Bank Ledger Queries",
        difficulty="hard",
        category="Data Structures",
        tags=["fenwick-tree", "binary-indexed-tree", "prefix-sums"],
        inspired_by="CSES 1648 Dynamic Range Sum Queries / LeetCode #307 Range Sum Query - Mutable",
        statement="""
A bank keeps `n` accounts numbered `1..n`, all starting with balance 0. The
ledger processes `q` operations in order:

* `1 i x` — add `x` to account `i` (`x` may be negative: a withdrawal),
* `2 l r` — report the **total balance** of accounts `l, l+1, …, r`.

Answer every report.

Recomputing a sum over up to 10⁵ accounts for every report is wasteful; a
**Fenwick tree** answers both operations in O(log n).
""",
        input_format="""
First line: `n q` (1 ≤ n ≤ 10⁵, 1 ≤ q ≤ 2000).
Next `q` lines: `1 i x` (1 ≤ i ≤ n, |x| ≤ 10⁹) or `2 l r` (1 ≤ l ≤ r ≤ n).
""",
        output_format="For every operation of type 2, one line with the total.",
        hints=[
            "A **Fenwick tree** (binary indexed tree) stores partial sums in an array `bit[1..n]` so that both "
            "\"add to one position\" and \"sum of a prefix\" take O(log n).",
            "Update: `while i <= n: bit[i] += x; i += i & (-i)`. "
            "Prefix sum: `while i > 0: s += bit[i]; i -= i & (-i)`. `i & (-i)` is the lowest set bit of `i`.",
            "A range sum is a difference of two prefix sums: `sum(l..r) = prefix(r) − prefix(l − 1)`.",
            "Totals can reach 2·10¹² — use `long long` in C++. Collect the answers and print them at the end.",
        ],
        samples=[
            "5 6\n1 2 10\n1 4 -3\n2 1 5\n1 1 7\n2 1 2\n2 3 4",
        ],
        tests=[
            "1 2\n1 1 1000000000\n2 1 1",
            "3 3\n2 1 3\n1 3 -1000000000\n2 2 3",
            "4 5\n1 1 1000000000\n1 2 1000000000\n1 3 1000000000\n1 4 1000000000\n2 1 4",
        ],
        gen=_gen_ledger,
        starter_python="""import sys

def main():
    data = sys.stdin.read().split()
    n, q = int(data[0]), int(data[1])
    bit = [0] * (n + 1)
    out = []
    pos = 2
    for _ in range(q):
        t, a, b = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        pos += 3
        if t == 1:
            pass  # TODO: add b to account a
        else:
            out.append(0)  # TODO: total of accounts a..b
    print("\\n".join(map(str, out)))

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<long long> bit(n + 1, 0);
    while (q--) {
        int t; long long a, b;
        cin >> t >> a >> b;
        if (t == 1) {
            // TODO: add b to account a
        } else {
            cout << 0 << "\\n";  // TODO: total of accounts a..b
        }
    }
    return 0;
}
""",
        solution_python="""import sys

def main():
    data = sys.stdin.read().split()
    n, q = int(data[0]), int(data[1])
    bit = [0] * (n + 1)

    def prefix(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    out = []
    pos = 2
    for _ in range(q):
        t, a, b = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        pos += 3
        if t == 1:
            i = a
            while i <= n:
                bit[i] += b
                i += i & -i
        else:
            out.append(prefix(b) - prefix(a - 1))
    print("\\n".join(map(str, out)))

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
using namespace std;

int n;
vector<long long> bit;

void add(int i, long long x) { for (; i <= n; i += i & -i) bit[i] += x; }
long long prefix(int i) { long long s = 0; for (; i > 0; i -= i & -i) s += bit[i]; return s; }

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> n >> q;
    bit.assign(n + 1, 0);
    while (q--) {
        int t; long long a, b;
        cin >> t >> a >> b;
        if (t == 1) add((int)a, b);
        else cout << prefix((int)b) - prefix((int)a - 1) << "\\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="segment-tree-min-count",
        title="Coldest Days Tracker",
        difficulty="hard",
        category="Data Structures",
        tags=["segment-tree", "range-minimum-query", "point-update"],
        inspired_by="CSES 1649 Dynamic Range Minimum Queries / Codeforces EDU Segment Tree (number of minimums)",
        statement="""
A weather station stores the temperatures `a₁ … aₙ` of `n` days (as integers).
Meteorologists correct and query the data with `q` operations:

* `1 i x` — the temperature of day `i` is corrected to `x`,
* `2 l r` — report the **minimum** temperature among days `l..r` **and how many** of those days had exactly that temperature.

Answer every query.
""",
        input_format="""
First line: `n q` (1 ≤ n ≤ 3000, 1 ≤ q ≤ 1500).
Second line: `n` integers `a₁ … aₙ` (1 ≤ aᵢ ≤ 10⁴).
Next `q` lines: `1 i x` (1 ≤ x ≤ 10⁴) or `2 l r` (1 ≤ l ≤ r ≤ n).
""",
        output_format="For every query of type 2, one line `min count`.",
        hints=[
            "A **segment tree** stores, for every node covering a range of days, a small summary of that range. "
            "Here the summary is the pair `(minimum, number of times it occurs)`.",
            "Combining two children: if their minima differ, keep the smaller one with its count; "
            "if they are equal, keep that minimum and **add** the counts.",
            "Iterative (bottom-up) tree: leaves at `size + i`, parent of node `v` is `v // 2`. "
            "A point update rewrites the leaf and recomputes its ancestors. A range query walks `l` and `r` inwards, "
            "combining the nodes that fall completely inside.",
            "Use a neutral element like `(INF, 0)` so combining with it changes nothing.",
        ],
        samples=[
            "6 5\n3 1 4 1 5 9\n2 1 6\n2 3 6\n1 2 7\n2 1 6\n2 5 5",
        ],
        tests=[
            "1 3\n5\n2 1 1\n1 1 2\n2 1 1",
            "4 3\n2 2 2 2\n2 1 4\n1 3 1\n2 1 4",
            "5 4\n5 4 3 2 1\n2 1 4\n1 5 3\n2 3 5\n2 1 5",
        ],
        gen=_gen_rmq,
        starter_python="""import sys

def main():
    data = list(map(int, sys.stdin.read().split()))
    n, q = data[0], data[1]
    a = data[2:2 + n]
    pos = 2 + n
    out = []
    for _ in range(q):
        t, x, y = data[pos], data[pos + 1], data[pos + 2]
        pos += 3
        if t == 1:
            pass  # TODO: a[x-1] = y, update the tree
        else:
            out.append("0 0")  # TODO: min and count on days x..y
    print("\\n".join(out))

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <utility>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<int> a(n);
    for (auto &x : a) cin >> x;
    while (q--) {
        int t, x, y;
        cin >> t >> x >> y;
        if (t == 1) {
            // TODO: a[x-1] = y, update the tree
        } else {
            cout << "0 0\\n";  // TODO: min and count on days x..y
        }
    }
    return 0;
}
""",
        solution_python="""import sys

def main():
    data = list(map(int, sys.stdin.read().split()))
    n, q = data[0], data[1]
    size = 1
    while size < n:
        size *= 2
    INF = 1 << 60
    mn = [INF] * (2 * size)
    ct = [0] * (2 * size)
    for i in range(n):
        mn[size + i] = data[2 + i]
        ct[size + i] = 1

    def pull(v):
        l, r = 2 * v, 2 * v + 1
        if mn[l] < mn[r]:
            mn[v], ct[v] = mn[l], ct[l]
        elif mn[r] < mn[l]:
            mn[v], ct[v] = mn[r], ct[r]
        else:
            mn[v], ct[v] = mn[l], ct[l] + ct[r]

    for v in range(size - 1, 0, -1):
        pull(v)
    pos = 2 + n
    out = []
    for _ in range(q):
        t, x, y = data[pos], data[pos + 1], data[pos + 2]
        pos += 3
        if t == 1:
            v = size + x - 1
            mn[v] = y
            v //= 2
            while v:
                pull(v)
                v //= 2
        else:
            best, cnt = INF, 0
            l, r = size + x - 1, size + y   # half-open [l, r)
            while l < r:
                if l & 1:
                    if mn[l] < best: best, cnt = mn[l], ct[l]
                    elif mn[l] == best: cnt += ct[l]
                    l += 1
                if r & 1:
                    r -= 1
                    if mn[r] < best: best, cnt = mn[r], ct[r]
                    elif mn[r] == best: cnt += ct[r]
                l //= 2
                r //= 2
            out.append(f"{best} {cnt}")
    print("\\n".join(out))

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <utility>
using namespace std;

typedef pair<int,int> Node;   // (min, count)
const Node NEUTRAL = {1 << 30, 0};

Node combine(const Node &a, const Node &b) {
    if (a.first < b.first) return a;
    if (b.first < a.first) return b;
    return {a.first, a.second + b.second};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    int size = 1;
    while (size < n) size *= 2;
    vector<Node> tree(2 * size, NEUTRAL);
    for (int i = 0; i < n; i++) { int x; cin >> x; tree[size + i] = {x, 1}; }
    for (int v = size - 1; v > 0; v--) tree[v] = combine(tree[2 * v], tree[2 * v + 1]);
    while (q--) {
        int t, x, y;
        cin >> t >> x >> y;
        if (t == 1) {
            int v = size + x - 1;
            tree[v] = {y, 1};
            for (v /= 2; v; v /= 2) tree[v] = combine(tree[2 * v], tree[2 * v + 1]);
        } else {
            Node res = NEUTRAL;
            for (int l = size + x - 1, r = size + y; l < r; l /= 2, r /= 2) {
                if (l & 1) res = combine(res, tree[l++]);
                if (r & 1) res = combine(res, tree[--r]);
            }
            cout << res.first << " " << res.second << "\\n";
        }
    }
    return 0;
}
""",
    ),
    dict(
        id="dsu-merging-groups",
        title="Growing Friend Circles",
        difficulty="hard",
        category="Data Structures",
        tags=["union-find", "disjoint-set-union", "union-by-size"],
        inspired_by="CSES 1676 Road Construction",
        statement="""
A new social network has `n` users and no friendships yet. Then `q` friendships
are created one after another. A **circle** is a group of users connected
through chains of friendships.

After each new friendship, report the number of circles and the size of the
largest circle. (A friendship between two users already in the same circle — or a
user befriending themself — changes nothing, but still needs a report.)
""",
        input_format="""
First line: `n q` (1 ≤ n ≤ 10⁵, 1 ≤ q ≤ 1500).
Next `q` lines: `a b` (1 ≤ a, b ≤ n).
""",
        output_format="`q` lines, each `circles largest`.",
        hints=[
            "Maintain a **union-find** (disjoint set union): `parent[v]` pointers forming trees, one tree per circle, "
            "and `size[root]` for every root.",
            "`find(v)` follows parents up to the root; **path compression** (point nodes closer to the root while you walk) "
            "keeps the trees flat.",
            "**Union by size**: hang the smaller tree under the larger one's root and add the sizes. Every successful "
            "union reduces the number of circles by one.",
            "The largest circle never shrinks, so `largest = max(largest, size[new_root])` after each union is enough.",
        ],
        samples=[
            "5 4\n1 2\n3 4\n2 4\n5 5",
        ],
        tests=[
            "1 1\n1 1",
            "3 3\n1 2\n2 1\n3 3",
            "4 3\n1 2\n3 4\n1 3",
        ],
        gen=_gen_dsu,
        starter_python="""import sys

def main():
    data = sys.stdin.read().split()
    n, q = int(data[0]), int(data[1])
    parent = list(range(n + 1))
    size = [1] * (n + 1)
    out = []
    for i in range(q):
        a, b = int(data[2 + 2 * i]), int(data[3 + 2 * i])
        # TODO: union a and b, then report
        out.append(f"{n} 1")
    print("\\n".join(out))

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <numeric>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<int> parent(n + 1), sz(n + 1, 1);
    iota(parent.begin(), parent.end(), 0);
    while (q--) {
        int a, b;
        cin >> a >> b;
        // TODO: union a and b, then report
        cout << n << " " << 1 << "\\n";
    }
    return 0;
}
""",
        solution_python="""import sys

def main():
    data = sys.stdin.read().split()
    n, q = int(data[0]), int(data[1])
    parent = list(range(n + 1))
    size = [1] * (n + 1)

    def find(x):
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    circles, largest = n, 1
    out = []
    for i in range(q):
        a, b = find(int(data[2 + 2 * i])), find(int(data[3 + 2 * i]))
        if a != b:
            if size[a] < size[b]:
                a, b = b, a
            parent[b] = a
            size[a] += size[b]
            circles -= 1
            if size[a] > largest:
                largest = size[a]
        out.append(f"{circles} {largest}")
    print("\\n".join(out))

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;

vector<int> parent, sz;

int find(int x) {
    int root = x;
    while (parent[root] != root) root = parent[root];
    while (parent[x] != root) { int nx = parent[x]; parent[x] = root; x = nx; }
    return root;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    parent.resize(n + 1); sz.assign(n + 1, 1);
    iota(parent.begin(), parent.end(), 0);
    int circles = n, largest = 1;
    while (q--) {
        int a, b;
        cin >> a >> b;
        a = find(a); b = find(b);
        if (a != b) {
            if (sz[a] < sz[b]) swap(a, b);
            parent[b] = a;
            sz[a] += sz[b];
            circles--;
            largest = max(largest, sz[a]);
        }
        cout << circles << " " << largest << "\\n";
    }
    return 0;
}
""",
    ),
]
