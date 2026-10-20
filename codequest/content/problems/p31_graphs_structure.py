"""Hard / expert graph problems: ordering, colouring, spanning trees, bridges, SCCs."""


def _edges_text(edges):
    return "\n".join(" ".join(map(str, e)) for e in edges)


def _gen_course_order(rng):
    tests = []
    for n, m, cyclic in [(1500, 2000, False), (500, 700, True), (300, 200, False)]:
        perm = list(range(1, n + 1))
        rng.shuffle(perm)
        edges = []
        while len(edges) < m:
            i, j = sorted(rng.sample(range(n), 2))
            edges.append((perm[i], perm[j]))
        if cyclic:
            i, j, k = sorted(rng.sample(range(n), 3))
            edges += [(perm[i], perm[j]), (perm[j], perm[k]), (perm[k], perm[i])]
        rng.shuffle(edges)
        tests.append(f"{n} {len(edges)}\n" + _edges_text(edges))
    return tests


def _gen_two_teams(rng):
    tests = []
    for n, m, odd in [(100000, 2000, False), (3000, 1500, False), (50, 0, False), (2000, 1000, True)]:
        side = [rng.randint(0, 1) for _ in range(n + 1)]
        edges = set()
        while len(edges) < m:
            a, b = rng.randint(1, n), rng.randint(1, n)
            if a != b and side[a] != side[b] and (b, a) not in edges:
                edges.add((a, b))
        edges = list(edges)
        if odd:
            # long odd cycle hidden among the vertices
            cyc = rng.sample(range(1, n + 1), 101)
            edges += [(cyc[i], cyc[(i + 1) % 101]) for i in range(101)]
        rng.shuffle(edges)
        tests.append(f"{n} {len(edges)}\n" + _edges_text(edges))
    return tests


def _gen_kruskal(rng):
    tests = []
    for n, m, wmax, connected in [(1200, 1800, 10**6, True), (400, 700, 10**6, True), (300, 600, 5, True),
                                  (250, 400, 1000, False)]:
        edges = []
        limit = n if connected else n - 3  # leave a few buildings unreachable
        for v in range(2, limit + 1):
            edges.append((rng.randint(1, v - 1), v, rng.randint(1, wmax)))
        while len(edges) < m:
            a, b = rng.randint(1, limit), rng.randint(1, limit)
            if a != b:
                edges.append((a, b, rng.randint(1, wmax)))
        rng.shuffle(edges)
        tests.append(f"{n} {len(edges)}\n" + _edges_text(edges))
    return tests


def _gen_bridges(rng):
    tests = []
    for n, blocks, extra in [(2000, 40, 150), (1500, 300, 50), (1200, 8, 300), (600, 300, 0)]:
        # random "cactus-ish" graph: chain of blocks; inside a block a cycle, blocks joined by single edges
        verts = list(range(1, n + 1))
        rng.shuffle(verts)
        cuts = sorted(rng.sample(range(1, n), blocks - 1))
        groups = [verts[a:b] for a, b in zip([0] + cuts, cuts + [n])]
        edges = []
        for g in groups:
            if len(g) >= 3 and rng.random() < 0.7:
                edges += [(g[i], g[(i + 1) % len(g)]) for i in range(len(g))]
            else:
                edges += [(g[i - 1], g[i]) for i in range(1, len(g))]
                if len(g) == 2 and rng.random() < 0.3:
                    edges.append((g[0], g[1]))  # doubled cable: not a bridge
        for i in range(1, len(groups)):
            if rng.random() < 0.85:
                a = rng.choice(groups[rng.randrange(i)])
                b = rng.choice(groups[i])
                edges.append((a, b))
        for _ in range(extra):
            a, b = rng.sample(range(1, n + 1), 2)
            edges.append((a, b))
        edges = edges[:4000]
        rng.shuffle(edges)
        edges = [(a, b) if rng.random() < 0.5 else (b, a) for a, b in edges]
        tests.append(f"{n} {len(edges)}\n" + _edges_text(edges))
    return tests


def _gen_scc(rng):
    tests = []
    for n, m, clusters in [(2000, 2200, 40), (1500, 1800, 300), (500, 1200, 1), (1000, 800, 400),
                           (300, 1000, 5)]:
        label = [rng.randrange(clusters) for _ in range(n + 1)]
        members = {}
        for v in range(1, n + 1):
            members.setdefault(label[v], []).append(v)
        edges = []
        # make each cluster strongly connected with a cycle
        for vs in members.values():
            if len(vs) > 1:
                edges += [(vs[i], vs[(i + 1) % len(vs)]) for i in range(len(vs))]
        order = list(range(clusters))
        rng.shuffle(order)
        rank = {c: i for i, c in enumerate(order)}
        while len(edges) < m:
            a, b = rng.randint(1, n), rng.randint(1, n)
            if a == b:
                continue
            if rank[label[a]] > rank[label[b]]:
                a, b = b, a  # keep cluster DAG acyclic
            edges.append((a, b))
        edges = edges[:m] if len(edges) > m else edges
        rng.shuffle(edges)
        tests.append(f"{n} {len(edges)}\n" + _edges_text(edges))
    return tests


PROBLEMS = [
    dict(
        id="course-order-lexicographic",
        title="Earliest Course Plan",
        difficulty="hard",
        category="Graphs",
        tags=["topological-sort", "kahn", "priority-queue", "cycle-detection"],
        inspired_by="LeetCode #210 Course Schedule II / CSES 1679 Course Schedule",
        statement="""
A university offers `n` courses numbered `1..n`. Some pairs `a b` say
"course `a` must be taken **before** course `b`".

Students take one course at a time. Among all orders that respect every rule,
print the **lexicographically smallest** one (the one that takes the
smallest-numbered available course whenever there is a choice).

If the rules contain a cycle, no valid order exists: print `-1`.
""",
        input_format="""
First line: `n m` (1 ≤ n ≤ 2000, 0 ≤ m ≤ 3000).
Next `m` lines: `a b` (1 ≤ a, b ≤ n, a ≠ b). A rule may be repeated.
""",
        output_format="`n` course numbers separated by spaces, or `-1`.",
        hints=[
            "This is a **topological sort**. Kahn's algorithm: repeatedly take a course whose remaining "
            "prerequisite count (in-degree) is 0, and decrease the in-degree of the courses it unlocks.",
            "To get the lexicographically smallest order, always take the **smallest** available course: "
            "keep the available ones in a min-heap instead of a plain queue.",
            "Cycle detection comes for free: if the heap empties before all `n` courses were taken, "
            "some courses wait on each other forever.",
            "Python: `heapq.heappush / heappop`. C++: `priority_queue<int, vector<int>, greater<int>>`. "
            "Repeated rules are fine as long as you add one to the in-degree for every copy.",
        ],
        samples=[
            "5 4\n2 1\n4 3\n2 3\n1 5",
            "3 3\n1 2\n2 3\n3 1",
        ],
        tests=[
            "1 0",
            "4 0",
            "3 2\n3 2\n3 2",
            "4 3\n4 3\n3 2\n2 1",
            "2 2\n1 2\n2 1",
        ],
        gen=_gen_course_order,
        starter_python="""import sys
import heapq

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for i in range(m):
        a, b = int(data[2 + 2 * i]), int(data[3 + 2 * i])
        adj[a].append(b)
        indeg[b] += 1
    # TODO: Kahn's algorithm with a min-heap
    print(-1)

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <queue>
#include <functional>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> adj(n + 1);
    vector<int> indeg(n + 1, 0);
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        indeg[b]++;
    }
    // TODO: Kahn's algorithm with a min-heap
    cout << -1 << "\\n";
    return 0;
}
""",
        solution_python="""import sys
import heapq

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for i in range(m):
        a, b = int(data[2 + 2 * i]), int(data[3 + 2 * i])
        adj[a].append(b)
        indeg[b] += 1
    heap = [v for v in range(1, n + 1) if indeg[v] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        u = heapq.heappop(heap)
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(heap, v)
    print(" ".join(map(str, order)) if len(order) == n else -1)

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <queue>
#include <functional>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> adj(n + 1);
    vector<int> indeg(n + 1, 0);
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        indeg[b]++;
    }
    priority_queue<int, vector<int>, greater<int>> pq;
    for (int v = 1; v <= n; v++) if (indeg[v] == 0) pq.push(v);
    vector<int> order;
    while (!pq.empty()) {
        int u = pq.top(); pq.pop();
        order.push_back(u);
        for (int v : adj[u]) if (--indeg[v] == 0) pq.push(v);
    }
    if ((int)order.size() != n) { cout << -1 << "\\n"; return 0; }
    for (int i = 0; i < n; i++) cout << order[i] << (i + 1 < n ? ' ' : '\\n');
    return 0;
}
""",
    ),
    dict(
        id="two-teams-colorings",
        title="Rival-Free Team Split",
        difficulty="hard",
        category="Graphs",
        tags=["bipartite", "bfs", "connected-components", "modulo"],
        inspired_by="CSES 1668 Building Teams / LeetCode #886 Possible Bipartition",
        statement="""
`n` players must be split into two teams, **Red** and **Blue** (a team may be empty).
There are `m` rivalries; two rivals must never play on the same team.

How many different splits are possible? Two splits differ if at least one
player is on a different team. Print the answer **modulo 10⁹ + 7**
(print `0` if no valid split exists).
""",
        input_format="""
First line: `n m` (1 ≤ n ≤ 10⁵, 0 ≤ m ≤ 3000).
Next `m` lines: `a b` — players `a` and `b` are rivals (a ≠ b). No pair appears twice.
""",
        output_format="One integer: the number of valid splits modulo 10⁹ + 7.",
        hints=[
            "Build the rivalry graph. A valid split is exactly a **2-colouring**: the graph must be **bipartite** "
            "(no cycle of odd length).",
            "Inside one connected component, once you fix the team of one player, everyone else's team is forced. "
            "So every component contributes a factor of exactly 2 — if it can be coloured at all.",
            "BFS from every uncoloured vertex, giving neighbours the opposite colour; finding an edge with both "
            "ends the same colour means the answer is 0. Otherwise the answer is `2^c mod (10⁹+7)` where `c` "
            "is the number of components — players with no rivals count as their own component!",
            "Python: `pow(2, c, 10**9 + 7)`. Use an explicit queue/stack, not recursion: components can be long chains.",
        ],
        samples=[
            "4 2\n1 2\n3 4",
            "3 3\n1 2\n2 3\n1 3",
        ],
        tests=[
            "1 0",
            "5 0",
            "6 6\n1 2\n2 3\n3 4\n4 5\n5 6\n6 1",
            "5 5\n1 2\n2 3\n3 4\n4 5\n5 1",
            "100000 1\n1 100000",
        ],
        gen=_gen_two_teams,
        starter_python="""import sys

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    for i in range(m):
        a, b = int(data[2 + 2 * i]), int(data[3 + 2 * i])
        adj[a].append(b)
        adj[b].append(a)
    MOD = 10**9 + 7
    # TODO: 2-colour each component (BFS); count components
    print(0)

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    const long long MOD = 1000000007LL;
    // TODO: 2-colour each component (BFS); count components
    cout << 0 << "\\n";
    return 0;
}
""",
        solution_python="""import sys

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    for i in range(m):
        a, b = int(data[2 + 2 * i]), int(data[3 + 2 * i])
        adj[a].append(b)
        adj[b].append(a)
    MOD = 10**9 + 7
    color = [-1] * (n + 1)
    comps = 0
    for s in range(1, n + 1):
        if color[s] != -1:
            continue
        comps += 1
        color[s] = 0
        stack = [s]
        while stack:
            u = stack.pop()
            cu = color[u]
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = cu ^ 1
                    stack.append(v)
                elif color[v] == cu:
                    print(0)
                    return
    print(pow(2, comps, MOD))

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    const long long MOD = 1000000007LL;
    vector<int> color(n + 1, -1), stack;
    long long ans = 1;
    for (int s = 1; s <= n; s++) {
        if (color[s] != -1) continue;
        ans = ans * 2 % MOD;
        color[s] = 0;
        stack.push_back(s);
        while (!stack.empty()) {
            int u = stack.back(); stack.pop_back();
            for (int v : adj[u]) {
                if (color[v] == -1) { color[v] = color[u] ^ 1; stack.push_back(v); }
                else if (color[v] == color[u]) { cout << 0 << "\\n"; return 0; }
            }
        }
    }
    cout << ans << "\\n";
    return 0;
}
""",
    ),
    dict(
        id="kruskal-cable-network",
        title="Campus Fibre Network",
        difficulty="hard",
        category="Graphs",
        tags=["minimum-spanning-tree", "kruskal", "union-find", "sorting"],
        inspired_by="CSES 1675 Road Reparation / classic MST",
        statement="""
A campus has `n` buildings. The IT department has a list of `m` possible fibre
cables; cable `i` would join buildings `a` and `b` at cost `c`.

Choose cables so that every building can reach every other one (directly or
through other buildings) with the **minimum total cost**. Print that cost, or
`-1` if even using every cable some buildings stay disconnected.
""",
        input_format="""
First line: `n m` (1 ≤ n ≤ 2000, 0 ≤ m ≤ 3000).
Next `m` lines: `a b c` (1 ≤ a, b ≤ n, a ≠ b, 1 ≤ c ≤ 10⁶). Several cables may join the same pair.
""",
        output_format="One integer: the minimum total cost, or `-1`.",
        hints=[
            "You want a **minimum spanning tree**. Kruskal's algorithm: sort the cables by cost and take each one "
            "that joins two buildings not yet connected.",
            "\"Are `a` and `b` already connected?\" is answered by a **union-find** (disjoint set union): "
            "`find(x)` returns the representative of x's group, `union` merges two groups.",
            "Make `find` fast with path compression (`parent[x] = find(parent[x])`, or iteratively halve the path) "
            "and union by size. Count accepted cables: you need exactly `n − 1`.",
            "The total can exceed 2³¹ (up to ~2·10⁹): use `long long` in C++.",
        ],
        samples=[
            "4 5\n1 2 3\n2 3 1\n3 4 4\n1 3 2\n2 4 5",
            "4 2\n1 2 7\n3 4 1",
        ],
        tests=[
            "1 0",
            "2 0",
            "2 3\n1 2 5\n2 1 3\n1 2 4",
            "3 3\n1 2 1000000\n2 3 1000000\n1 3 1000000",
        ],
        gen=_gen_kruskal,
        starter_python="""import sys

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    edges = []
    for i in range(m):
        a, b, c = int(data[2 + 3 * i]), int(data[3 + 3 * i]), int(data[4 + 3 * i])
        edges.append((c, a, b))
    parent = list(range(n + 1))
    # TODO: Kruskal with union-find
    print(-1)

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <array>
#include <algorithm>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<array<int,3>> edges(m);   // {cost, a, b}
    for (auto &e : edges) cin >> e[1] >> e[2] >> e[0];
    // TODO: Kruskal with union-find
    cout << -1 << "\\n";
    return 0;
}
""",
        solution_python="""import sys

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    edges = []
    for i in range(m):
        a, b, c = int(data[2 + 3 * i]), int(data[3 + 3 * i]), int(data[4 + 3 * i])
        edges.append((c, a, b))
    edges.sort()
    parent = list(range(n + 1))
    size = [1] * (n + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = used = 0
    for c, a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            continue
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        total += c
        used += 1
        if used == n - 1:
            break
    print(total if used == n - 1 else -1)

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <array>
#include <numeric>
#include <algorithm>
using namespace std;

vector<int> parent, sz;
int find(int x) {
    while (parent[x] != x) { parent[x] = parent[parent[x]]; x = parent[x]; }
    return x;
}

int main() {
    int n, m;
    cin >> n >> m;
    vector<array<int,3>> edges(m);
    for (auto &e : edges) cin >> e[1] >> e[2] >> e[0];
    sort(edges.begin(), edges.end());
    parent.resize(n + 1); sz.assign(n + 1, 1);
    iota(parent.begin(), parent.end(), 0);
    long long total = 0;
    int used = 0;
    for (auto &e : edges) {
        if (used == n - 1) break;
        int ra = find(e[1]), rb = find(e[2]);
        if (ra == rb) continue;
        if (sz[ra] < sz[rb]) swap(ra, rb);
        parent[rb] = ra; sz[ra] += sz[rb];
        total += e[0]; used++;
    }
    cout << (used == n - 1 ? total : -1) << "\\n";
    return 0;
}
""",
    ),
    dict(
        id="critical-cable-bridges",
        title="Critical Cables",
        difficulty="expert",
        category="Graphs",
        tags=["bridges", "dfs", "low-link", "tarjan"],
        inspired_by="LeetCode #1192 Critical Connections in a Network / CSES 2076 Necessary Roads",
        statement="""
A data centre has `n` servers and `m` two-way cables. A cable is **critical** if
cutting it alone would split some pair of servers that are currently connected
(in graph terms: it is a **bridge**).

List all critical cables. Note that two servers may be joined by **several**
parallel cables — then none of those cables is critical, since the others
still connect the pair. The network is not necessarily connected.
""",
        input_format="""
First line: `n m` (1 ≤ n ≤ 5000, 0 ≤ m ≤ 4000).
Next `m` lines: `a b` (1 ≤ a, b ≤ n, a ≠ b).
""",
        output_format="""
First line: `k`, the number of critical cables. Then `k` lines `u v` with `u < v`,
sorted by `u`, then by `v`. (Two parallel cables can never both be listed, so each pair appears at most once.)
""",
        hints=[
            "Use the DFS **low-link** technique (Tarjan). `tin[v]` = time v was discovered; `low[v]` = the "
            "smallest `tin` reachable from v's DFS subtree using at most one back edge.",
            "For a tree edge `p → v`: it is a bridge **iff** `low[v] > tin[p]` — nothing in v's subtree can climb "
            "back to p or above without that edge.",
            "Parallel cables: do not skip the edge back to the *parent vertex*; skip only the very **edge id** "
            "you came through. A second cable to the parent then counts as a back edge, as it should.",
            "Recursion depth can reach n. In Python write the DFS iteratively: keep a stack of vertices and a "
            "per-vertex index into its adjacency list; when a vertex is finished, push its `low` to its parent.",
        ],
        samples=[
            "5 5\n1 2\n2 3\n3 1\n3 4\n4 5",
            "4 4\n1 2\n2 1\n2 3\n3 4",
        ],
        tests=[
            "1 0",
            "2 1\n2 1",
            "2 2\n1 2\n1 2",
            "6 4\n1 2\n3 4\n4 5\n5 3",
            "4 3\n1 2\n1 3\n1 4",
        ],
        gen=_gen_bridges,
        starter_python="""import sys

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]   # adj[u] = list of (v, edge_id)
    ends = []
    for i in range(m):
        a, b = int(data[2 + 2 * i]), int(data[3 + 2 * i])
        adj[a].append((b, i))
        adj[b].append((a, i))
        ends.append((min(a, b), max(a, b)))
    # TODO: iterative DFS computing tin / low; collect bridge edge ids
    print(0)

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <utility>
#include <algorithm>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<pair<int,int>>> adj(n + 1);   // (neighbour, edge id)
    vector<pair<int,int>> ends(m);
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back({b, i});
        adj[b].push_back({a, i});
        ends[i] = {min(a, b), max(a, b)};
    }
    // TODO: DFS computing tin / low; collect bridge edge ids
    cout << 0 << "\\n";
    return 0;
}
""",
        solution_python="""import sys

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    ends = []
    for i in range(m):
        a, b = int(data[2 + 2 * i]), int(data[3 + 2 * i])
        adj[a].append((b, i))
        adj[b].append((a, i))
        ends.append((min(a, b), max(a, b)))
    tin = [-1] * (n + 1)
    low = [0] * (n + 1)
    pedge = [-1] * (n + 1)
    it = [0] * (n + 1)
    timer = 0
    bridges = []
    for s in range(1, n + 1):
        if tin[s] != -1:
            continue
        tin[s] = low[s] = timer
        timer += 1
        stack = [s]
        while stack:
            u = stack[-1]
            if it[u] < len(adj[u]):
                v, eid = adj[u][it[u]]
                it[u] += 1
                if eid == pedge[u]:
                    continue
                if tin[v] == -1:
                    pedge[v] = eid
                    tin[v] = low[v] = timer
                    timer += 1
                    stack.append(v)
                elif tin[v] < low[u]:
                    low[u] = tin[v]
            else:
                stack.pop()
                if stack:
                    p = stack[-1]
                    if low[u] < low[p]:
                        low[p] = low[u]
                    if low[u] > tin[p]:
                        bridges.append(ends[pedge[u]])
    bridges.sort()
    out = [str(len(bridges))] + [f"{a} {b}" for a, b in bridges]
    print("\\n".join(out))

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <utility>
#include <algorithm>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<pair<int,int>>> adj(n + 1);
    vector<pair<int,int>> ends(m);
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back({b, i});
        adj[b].push_back({a, i});
        ends[i] = {min(a, b), max(a, b)};
    }
    vector<int> tin(n + 1, -1), low(n + 1, 0), pedge(n + 1, -1), it(n + 1, 0), stack;
    vector<pair<int,int>> bridges;
    int timer = 0;
    for (int s = 1; s <= n; s++) {
        if (tin[s] != -1) continue;
        tin[s] = low[s] = timer++;
        stack.push_back(s);
        while (!stack.empty()) {
            int u = stack.back();
            if (it[u] < (int)adj[u].size()) {
                auto [v, eid] = adj[u][it[u]++];
                if (eid == pedge[u]) continue;
                if (tin[v] == -1) {
                    pedge[v] = eid;
                    tin[v] = low[v] = timer++;
                    stack.push_back(v);
                } else {
                    low[u] = min(low[u], tin[v]);
                }
            } else {
                stack.pop_back();
                if (!stack.empty()) {
                    int p = stack.back();
                    low[p] = min(low[p], low[u]);
                    if (low[u] > tin[p]) bridges.push_back(ends[pedge[u]]);
                }
            }
        }
    }
    sort(bridges.begin(), bridges.end());
    cout << bridges.size() << "\\n";
    for (auto [a, b] : bridges) cout << a << " " << b << "\\n";
    return 0;
}
""",
    ),
    dict(
        id="scc-one-way-roads-to-add",
        title="One-Way Town Repair",
        difficulty="expert",
        category="Graphs",
        tags=["strongly-connected-components", "kosaraju", "tarjan", "condensation"],
        inspired_by="Classic SCC condensation (POI / Codeforces 'make strongly connected'), CSES 1682 Flight Routes Check",
        statement="""
A town has `n` intersections and `m` **one-way** streets. The mayor wants every
intersection to be reachable from every other one. Streets cannot be removed,
but new one-way streets can be built between any two intersections.

What is the **minimum number of new streets** needed? (Print `0` if the town is
already fine.)
""",
        input_format="""
First line: `n m` (1 ≤ n ≤ 3000, 0 ≤ m ≤ 4000).
Next `m` lines: `a b` — a one-way street from `a` to `b` (a ≠ b).
""",
        output_format="One integer: the minimum number of streets to add.",
        hints=[
            "Group intersections into **strongly connected components** (SCCs): inside an SCC everyone already "
            "reaches everyone. Kosaraju (two DFS passes) or Tarjan finds them in O(n + m).",
            "Contract every SCC to a single node. The result (the **condensation**) is a DAG.",
            "In the DAG count `s` = components with no incoming edge (sources) and `t` = components with no "
            "outgoing edge (sinks). A known theorem: the answer is `max(s, t)` — except when there is only one SCC, "
            "where it is 0. An isolated intersection is both a source and a sink.",
            "Write the DFS iteratively (stack + per-vertex edge index) so long chains do not overflow the stack. "
            "Kosaraju: order vertices by finish time on the graph, then flood-fill the **reversed** graph in reverse finish order.",
        ],
        samples=[
            "4 3\n1 2\n2 3\n3 1",
            "3 3\n1 2\n2 3\n3 1",
        ],
        tests=[
            "1 0",
            "2 0",
            "2 1\n1 2",
            "5 4\n1 2\n1 3\n1 4\n1 5",
            "6 6\n1 2\n2 1\n3 4\n4 3\n5 6\n6 5",
        ],
        gen=_gen_scc,
        starter_python="""import sys

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    radj = [[] for _ in range(n + 1)]
    for i in range(m):
        a, b = int(data[2 + 2 * i]), int(data[3 + 2 * i])
        adj[a].append(b)
        radj[b].append(a)
    # TODO: find SCCs, count source and sink components of the condensation
    print(0)

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> adj(n + 1), radj(n + 1);
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        radj[b].push_back(a);
    }
    // TODO: find SCCs, count source and sink components of the condensation
    cout << 0 << "\\n";
    return 0;
}
""",
        solution_python="""import sys

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    radj = [[] for _ in range(n + 1)]
    edges = []
    for i in range(m):
        a, b = int(data[2 + 2 * i]), int(data[3 + 2 * i])
        adj[a].append(b)
        radj[b].append(a)
        edges.append((a, b))
    # pass 1: finish order
    seen = [False] * (n + 1)
    it = [0] * (n + 1)
    order = []
    for s in range(1, n + 1):
        if seen[s]:
            continue
        seen[s] = True
        stack = [s]
        while stack:
            u = stack[-1]
            if it[u] < len(adj[u]):
                v = adj[u][it[u]]
                it[u] += 1
                if not seen[v]:
                    seen[v] = True
                    stack.append(v)
            else:
                stack.pop()
                order.append(u)
    # pass 2: flood fill reversed graph
    comp = [-1] * (n + 1)
    c = 0
    for s in reversed(order):
        if comp[s] != -1:
            continue
        comp[s] = c
        stack = [s]
        while stack:
            u = stack.pop()
            for v in radj[u]:
                if comp[v] == -1:
                    comp[v] = c
                    stack.append(v)
        c += 1
    if c == 1:
        print(0)
        return
    has_in = [False] * c
    has_out = [False] * c
    for a, b in edges:
        if comp[a] != comp[b]:
            has_out[comp[a]] = True
            has_in[comp[b]] = True
    sources = has_in.count(False)
    sinks = has_out.count(False)
    print(max(sources, sinks))

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <utility>
#include <algorithm>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<int>> adj(n + 1), radj(n + 1);
    vector<pair<int,int>> edges(m);
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        adj[a].push_back(b);
        radj[b].push_back(a);
        edges[i] = {a, b};
    }
    vector<int> it(n + 1, 0), order, stack;
    vector<bool> seen(n + 1, false);
    for (int s = 1; s <= n; s++) {
        if (seen[s]) continue;
        seen[s] = true;
        stack.push_back(s);
        while (!stack.empty()) {
            int u = stack.back();
            if (it[u] < (int)adj[u].size()) {
                int v = adj[u][it[u]++];
                if (!seen[v]) { seen[v] = true; stack.push_back(v); }
            } else {
                stack.pop_back();
                order.push_back(u);
            }
        }
    }
    vector<int> comp(n + 1, -1);
    int c = 0;
    for (int i = n - 1; i >= 0; i--) {
        int s = order[i];
        if (comp[s] != -1) continue;
        comp[s] = c;
        stack.push_back(s);
        while (!stack.empty()) {
            int u = stack.back(); stack.pop_back();
            for (int v : radj[u]) if (comp[v] == -1) { comp[v] = c; stack.push_back(v); }
        }
        c++;
    }
    if (c == 1) { cout << 0 << "\\n"; return 0; }
    vector<bool> hasIn(c, false), hasOut(c, false);
    for (auto [a, b] : edges)
        if (comp[a] != comp[b]) { hasOut[comp[a]] = true; hasIn[comp[b]] = true; }
    int sources = 0, sinks = 0;
    for (int i = 0; i < c; i++) { sources += !hasIn[i]; sinks += !hasOut[i]; }
    cout << max(sources, sinks) << "\\n";
    return 0;
}
""",
    ),
]
