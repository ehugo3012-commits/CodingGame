"""Hard / expert graph problems: shortest paths (BFS with state, Dijkstra, Floyd-Warshall)."""


def _grid(rng, n, m, density, alphabet=".#"):
    rows = []
    for _ in range(n):
        rows.append("".join(alphabet[1] if rng.random() < density else alphabet[0] for _ in range(m)))
    rows[0] = "." + rows[0][1:]
    rows[-1] = rows[-1][:-1] + "."
    return rows


def _breakthrough_ok(rows, k):
    n, m = len(rows), len(rows[0])
    best = {(0, 0): k}
    frontier = [(0, 0, k)]
    while frontier:
        nxt = []
        for r, c, rem in frontier:
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < n and 0 <= nc < m:
                    left = rem - (rows[nr][nc] == "#")
                    if left > best.get((nr, nc), -1):
                        best[(nr, nc)] = left
                        nxt.append((nr, nc, left))
        frontier = nxt
    return (n - 1, m - 1) in best or n * m == 1


def _gen_breakthrough(rng):
    tests = []
    for n, m, dens, k, want in [(60, 60, 0.3, 0, True), (60, 60, 0.38, 3, True), (60, 60, 0.45, 8, True),
                                (60, 60, 0.5, 10, True), (45, 60, 0.35, 1, True), (1, 60, 0.08, 4, True),
                                (60, 60, 0.3, 10, True), (60, 60, 0.45, 2, False)]:
        while True:
            rows = _grid(rng, n, m, dens)
            if _breakthrough_ok(rows, k) == want:
                break
        tests.append(f"{n} {m} {k}\n" + "\n".join(rows))
    # a maze-like serpentine with gaps: long detour vs. drilling through
    n, m = 59, 60
    rows = []
    for r in range(n):
        if r % 2 == 1:
            row = ["#"] * m
            row[m - 1 if (r // 2) % 2 == 0 else 0] = "."
            rows.append("".join(row))
        else:
            rows.append("." * m)
    tests.append(f"{n} {m} 5\n" + "\n".join(rows))
    return tests


def _gen_digit_grid(rng):
    tests = []
    for n, m in [(150, 150), (100, 120), (1, 150), (150, 1)]:
        rows = ["".join(rng.choice("123456789") for _ in range(m)) for _ in range(n)]
        tests.append(f"{n} {m}\n" + "\n".join(rows))
    # cheap snake forcing a detour that goes up and left
    n, m = 60, 60
    rows = []
    for r in range(n):
        row = ["9"] * m
        rows.append(row)
    for r in range(n):
        if r % 4 == 0:
            for c in range(m):
                rows[r][c] = "1"
        elif r % 4 == 1:
            rows[r][m - 1] = "1"
        elif r % 4 == 2:
            for c in range(m):
                rows[r][c] = "1"
        else:
            rows[r][0] = "1"
    tests.append(f"{n} {m}\n" + "\n".join("".join(r) for r in rows))
    return tests


def _gen_census(rng):
    tests = []
    for n, m, wmax in [(1500, 2200, 5), (400, 1600, 3), (200, 800, 2)]:
        edges = []
        # guarantee a path 1 -> n through a random chain
        chain = [1] + rng.sample(range(2, n), min(n - 2, 40)) + [n]
        for a, b in zip(chain, chain[1:]):
            edges.append((a, b, rng.randint(1, wmax)))
        while len(edges) < m:
            a, b = rng.randint(1, n), rng.randint(1, n)
            if a != b:
                edges.append((a, b, rng.randint(1, wmax)))
        rng.shuffle(edges)
        tests.append(f"{n} {len(edges)}\n" + "\n".join(f"{a} {b} {w}" for a, b, w in edges))
    # layered "diamond" graph: number of shortest routes explodes (needs the modulo)
    layers, width = 60, 4
    n = 2 + layers * width
    edges = []
    def node(layer, i):
        return 2 + layer * width + i
    for i in range(width):
        edges.append((1, node(0, i), 1))
        edges.append((node(layers - 1, i), n, 1))
    for layer in range(layers - 1):
        for i in range(width):
            for j in range(width):
                edges.append((node(layer, i), node(layer + 1, j), 1))
    # a few equal-cost shortcuts with fewer flights
    edges.append((1, node(10, 0), 11))
    edges.append((node(20, 1), n, 40))
    tests.append(f"{n} {len(edges)}\n" + "\n".join(f"{a} {b} {w}" for a, b, w in edges))
    return tests


def _gen_floyd(rng):
    tests = []
    for n, m, wmax, thr in [(100, 1400, 10000, 1500), (100, 300, 100, 230), (80, 1000, 50, 12),
                            (60, 59, 20, 100)]:
        edges = set()
        if m == n - 1:
            for v in range(2, n + 1):
                edges.add((rng.randint(1, v - 1), v))
        while len(edges) < m:
            a, b = rng.sample(range(1, n + 1), 2)
            if (b, a) not in edges:
                edges.add((a, b))
        lines = [f"{a} {b} {rng.randint(1, wmax)}" for a, b in edges]
        tests.append(f"{n} {m} {thr}\n" + "\n".join(lines))
    return tests


PROBLEMS = [
    dict(
        id="grid-breakthrough-walls",
        title="Breakthrough Rover",
        difficulty="hard",
        category="Graphs",
        tags=["bfs", "state-space", "grid"],
        inspired_by="LeetCode #1293 Shortest Path in a Grid with Obstacles Elimination",
        statement="""
A mining rover starts in the **top-left** cell of an `n × m` map and must reach
the **bottom-right** cell. Each cell is either open ground `.` or solid rock `#`.

Every minute the rover moves to one of the 4 neighbouring cells (up, down,
left, right) and never leaves the map. It carries `k` explosive charges:
moving **into** a rock cell uses up one charge (the rock is blasted away as
the rover enters it). Without a charge left it cannot enter rock.

What is the minimum number of moves needed to reach the bottom-right cell?
Print `-1` if it cannot be done.

The start and target cells are always open ground.
""",
        input_format="""
First line: `n m k` (1 ≤ n, m ≤ 60, 0 ≤ k ≤ 10).
Then `n` lines with `m` characters each, every character `.` or `#`.
""",
        output_format="One integer: the minimum number of moves, or `-1`.",
        hints=[
            "Plain BFS on cells is not enough: two visits to the same cell differ by how many charges are left. "
            "Run BFS on the **state** `(row, col, charges_left)`.",
            "There are at most `n·m·(k+1)` states, each with 4 moves — tiny. Mark states visited so none is expanded twice.",
            "A neat pruning: BFS reaches cells in increasing distance, so if you already reached a cell with `r` charges "
            "left, a later arrival with ≤ `r` charges is useless. Store `best[cell]` = most charges seen and only push if you beat it.",
            "Python: `collections.deque` with `popleft()`. C++: `std::queue<std::array<int,3>>`. "
            "Remember the 1×1 map: the answer is 0.",
        ],
        samples=[
            "3 3 1\n.#.\n##.\n##.",
            "3 4 0\n.#..\n.#.#\n..#.",
        ],
        tests=[
            "1 1 0\n.",
            "2 2 0\n.#\n#.",
            "2 2 1\n.#\n#.",
            "3 3 0\n.##\n###\n##.",
            "4 4 10\n.###\n####\n####\n###.",
            "1 5 1\n.##..",
        ],
        gen=_gen_breakthrough,
        starter_python="""import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    n, m, k = int(data[0]), int(data[1]), int(data[2])
    grid = data[3:3 + n]          # grid[r][c] is '.' or '#'
    # TODO: BFS over states (row, col, charges_left)
    print(-1)

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <string>
#include <queue>
using namespace std;

int main() {
    int n, m, k;
    cin >> n >> m >> k;
    vector<string> grid(n);
    for (auto &row : grid) cin >> row;
    // TODO: BFS over states (row, col, charges_left)
    cout << -1 << "\\n";
    return 0;
}
""",
        solution_python="""import sys

def main():
    data = sys.stdin.read().split()
    n, m, k = int(data[0]), int(data[1]), int(data[2])
    g = "".join(data[3:3 + n])
    total = n * m
    target = total - 1
    if target == 0:
        print(0)
        return
    best = [-1] * total          # most charges left on arrival so far
    best[0] = k
    frontier = [(0, k)]
    steps = 0
    while frontier:
        steps += 1
        nxt = []
        for cell, rem in frontier:
            r, c = divmod(cell, m)
            nbs = []
            if c > 0: nbs.append(cell - 1)
            if c < m - 1: nbs.append(cell + 1)
            if r > 0: nbs.append(cell - m)
            if r < n - 1: nbs.append(cell + m)
            for nb in nbs:
                nr = rem - (g[nb] == "#")
                if nr > best[nb]:
                    if nb == target:
                        print(steps)
                        return
                    best[nb] = nr
                    nxt.append((nb, nr))
        frontier = nxt
    print(-1)

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <string>
#include <utility>
using namespace std;

int main() {
    int n, m, k;
    cin >> n >> m >> k;
    vector<string> g(n);
    for (auto &row : g) cin >> row;
    int total = n * m, target = total - 1;
    if (target == 0) { cout << 0 << "\\n"; return 0; }
    vector<int> best(total, -1);
    best[0] = k;
    vector<pair<int,int>> frontier{{0, k}}, nxt;
    int dr[4] = {0, 0, 1, -1}, dc[4] = {1, -1, 0, 0};
    for (int steps = 1; !frontier.empty(); steps++) {
        nxt.clear();
        for (auto [cell, rem] : frontier) {
            int r = cell / m, c = cell % m;
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr < 0 || nr >= n || nc < 0 || nc >= m) continue;
                int nb = nr * m + nc;
                int left = rem - (g[nr][nc] == '#');
                if (left > best[nb]) {
                    if (nb == target) { cout << steps << "\\n"; return 0; }
                    best[nb] = left;
                    nxt.push_back({nb, left});
                }
            }
        }
        swap(frontier, nxt);
    }
    cout << -1 << "\\n";
    return 0;
}
""",
    ),
    dict(
        id="digit-grid-dijkstra",
        title="Cheapest Walk Across the Mosaic",
        difficulty="hard",
        category="Graphs",
        tags=["dijkstra", "priority-queue", "grid"],
        inspired_by="Project Euler #83 Path sum: four ways",
        statement="""
A mosaic floor is an `n × m` grid of tiles; each tile shows a digit from 1 to 9,
the effort needed to step on it. You start on the **top-left** tile and want to
reach the **bottom-right** tile, moving between tiles that share a side
(up, down, left **and** right are all allowed).

The cost of a walk is the sum of the digits of every tile you step on,
**including** the first and the last. Find the minimum possible cost.

Because you may walk up and left, a simple row-by-row DP is not enough.
""",
        input_format="""
First line: `n m` (1 ≤ n, m ≤ 150).
Then `n` lines, each a string of `m` digits `1`–`9` (no spaces).
""",
        output_format="One integer: the minimum total cost.",
        hints=[
            "Treat every tile as a graph node with edges to its 4 neighbours. Entering tile `v` costs `digit(v)`: "
            "this is a single-source shortest path with non-negative weights — **Dijkstra**.",
            "Initialise `dist[start] = digit(start)` and push it into a min-heap; pop the smallest, relax its neighbours "
            "with `dist[u] + digit(v)`.",
            "Skip stale heap entries: if the popped distance is larger than `dist[u]`, `continue`.",
            "Python: `heapq.heappush(pq, (d, cell))` with `cell = r*m + c`. "
            "C++: `priority_queue<pair<int,int>, vector<pair<int,int>>, greater<pair<int,int>>>`.",
        ],
        samples=[
            "3 3\n131\n912\n111",
            "3 4\n1999\n1919\n1119",
        ],
        tests=[
            "1 1\n7",
            "1 4\n5312",
            "2 2\n19\n91",
            "4 4\n1111\n9991\n1111\n1999",
        ],
        gen=_gen_digit_grid,
        starter_python="""import sys
import heapq

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    grid = data[2:2 + n]          # grid[r][c] is a digit character
    # TODO: Dijkstra from (0, 0) to (n-1, m-1)
    print(0)

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <string>
#include <queue>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<string> grid(n);
    for (auto &row : grid) cin >> row;
    // TODO: Dijkstra from (0, 0) to (n-1, m-1); cost of a tile is grid[r][c] - '0'
    cout << 0 << "\\n";
    return 0;
}
""",
        solution_python="""import sys
import heapq

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    cost = [ord(ch) - 48 for row in data[2:2 + n] for ch in row]
    total = n * m
    INF = float("inf")
    dist = [INF] * total
    dist[0] = cost[0]
    pq = [(cost[0], 0)]
    pop, push = heapq.heappop, heapq.heappush
    while pq:
        d, u = pop(pq)
        if d > dist[u]:
            continue
        if u == total - 1:
            break
        r, c = divmod(u, m)
        nbs = []
        if c > 0: nbs.append(u - 1)
        if c < m - 1: nbs.append(u + 1)
        if r > 0: nbs.append(u - m)
        if r < n - 1: nbs.append(u + m)
        for v in nbs:
            nd = d + cost[v]
            if nd < dist[v]:
                dist[v] = nd
                push(pq, (nd, v))
    print(dist[total - 1])

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <string>
#include <queue>
#include <utility>
#include <functional>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<string> g(n);
    for (auto &row : g) cin >> row;
    const int INF = 1 << 30;
    vector<int> dist(n * m, INF);
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<pair<int,int>>> pq;
    dist[0] = g[0][0] - '0';
    pq.push({dist[0], 0});
    int dr[4] = {0, 0, 1, -1}, dc[4] = {1, -1, 0, 0};
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (d > dist[u]) continue;
        int r = u / m, c = u % m;
        for (int k = 0; k < 4; k++) {
            int nr = r + dr[k], nc = c + dc[k];
            if (nr < 0 || nr >= n || nc < 0 || nc >= m) continue;
            int v = nr * m + nc, nd = d + (g[nr][nc] - '0');
            if (nd < dist[v]) { dist[v] = nd; pq.push({nd, v}); }
        }
    }
    cout << dist[n * m - 1] << "\\n";
    return 0;
}
""",
    ),
    dict(
        id="cheapest-route-census",
        title="Cheapest Route Census",
        difficulty="expert",
        category="Graphs",
        tags=["dijkstra", "counting", "dp-on-dag", "modulo"],
        inspired_by="CSES 1202 Investigation",
        statement="""
An airline network has `n` airports and `m` one-way flights; flight `i` goes
from `a` to `b` and costs `w`. You travel from airport `1` to airport `n`.

A route is **optimal** if its total cost is the minimum possible. Report four
facts about the optimal routes:

1. the minimum total cost,
2. how many different optimal routes there are, **modulo 10⁹ + 7**,
3. the fewest flights used by any optimal route,
4. the most flights used by any optimal route.

Two routes are different if their sequences of flights differ (parallel flights
between the same airports count separately). Airport `n` is always reachable from `1`.
""",
        input_format="""
First line: `n m` (2 ≤ n ≤ 2000, 1 ≤ m ≤ 3000).
Next `m` lines: `a b w` — a flight from `a` to `b` with cost `w`
(1 ≤ a, b ≤ n, a ≠ b, 1 ≤ w ≤ 1000).
""",
        output_format="Four integers on one line: cost, number of optimal routes mod 10⁹+7, min flights, max flights.",
        hints=[
            "Run Dijkstra from airport 1. Alongside `dist[v]` keep three more arrays: `ways[v]`, `fewest[v]`, `most[v]` "
            "describing the optimal routes to `v`.",
            "When relaxing `u → v` with `nd = dist[u] + w`: if `nd < dist[v]` the old information about `v` is thrown away "
            "(`ways[v] = ways[u]`, `fewest[v] = fewest[u] + 1`, …); if `nd == dist[v]` you **merge** instead "
            "(`ways += ways[u]`, take min / max).",
            "This is correct because all weights are positive: every predecessor of `v` on an optimal route is popped "
            "(finalised) before `v`, so its numbers are already final when they flow into `v`.",
            "Count routes modulo 10⁹+7 but compare **distances** exactly. Use a `done[]` flag so each node is "
            "expanded only once even if it sits in the heap several times.",
        ],
        samples=[
            "4 5\n1 4 5\n1 2 4\n2 4 5\n2 3 2\n3 4 3",
            "5 6\n1 2 1\n1 3 1\n2 4 1\n3 4 1\n4 5 2\n1 5 4",
        ],
        tests=[
            "2 1\n1 2 7",
            "2 3\n1 2 7\n1 2 7\n1 2 8",
            "3 3\n1 2 1\n2 3 1\n1 3 2",
            "4 4\n1 2 1\n2 1 1\n2 4 3\n1 4 4",
        ],
        gen=_gen_census,
        starter_python="""import sys
import heapq

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    for i in range(m):
        a, b, w = int(data[2 + 3 * i]), int(data[3 + 3 * i]), int(data[4 + 3 * i])
        adj[a].append((b, w))
    MOD = 10**9 + 7
    # TODO: Dijkstra from 1, tracking dist, ways, fewest and most flights
    print(0, 0, 0, 0)

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <queue>
#include <utility>
#include <functional>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<pair<int,int>>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int a, b, w;
        cin >> a >> b >> w;
        adj[a].push_back({b, w});
    }
    const long long MOD = 1000000007LL;
    // TODO: Dijkstra from 1, tracking dist, ways, fewest and most flights
    cout << "0 0 0 0\\n";
    return 0;
}
""",
        solution_python="""import sys
import heapq

def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    adj = [[] for _ in range(n + 1)]
    for i in range(m):
        a, b, w = int(data[2 + 3 * i]), int(data[3 + 3 * i]), int(data[4 + 3 * i])
        adj[a].append((b, w))
    MOD = 10**9 + 7
    INF = float("inf")
    dist = [INF] * (n + 1)
    ways = [0] * (n + 1)
    fewest = [0] * (n + 1)
    most = [0] * (n + 1)
    done = [False] * (n + 1)
    dist[1] = 0
    ways[1] = 1
    pq = [(0, 1)]
    while pq:
        d, u = heapq.heappop(pq)
        if done[u]:
            continue
        done[u] = True
        for v, w in adj[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                ways[v] = ways[u]
                fewest[v] = fewest[u] + 1
                most[v] = most[u] + 1
                heapq.heappush(pq, (nd, v))
            elif nd == dist[v]:
                ways[v] = (ways[v] + ways[u]) % MOD
                fewest[v] = min(fewest[v], fewest[u] + 1)
                most[v] = max(most[v], most[u] + 1)
    print(dist[n], ways[n], fewest[n], most[n])

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <queue>
#include <utility>
#include <functional>
#include <algorithm>
using namespace std;

int main() {
    int n, m;
    cin >> n >> m;
    vector<vector<pair<int,int>>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int a, b, w;
        cin >> a >> b >> w;
        adj[a].push_back({b, w});
    }
    const long long MOD = 1000000007LL, INF = (long long)4e18;
    vector<long long> dist(n + 1, INF), ways(n + 1, 0);
    vector<int> fewest(n + 1, 0), most(n + 1, 0);
    vector<bool> done(n + 1, false);
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<pair<long long,int>>> pq;
    dist[1] = 0; ways[1] = 1;
    pq.push({0, 1});
    while (!pq.empty()) {
        auto [d, u] = pq.top();
        pq.pop();
        if (done[u]) continue;
        done[u] = true;
        for (auto [v, w] : adj[u]) {
            long long nd = d + w;
            if (nd < dist[v]) {
                dist[v] = nd; ways[v] = ways[u];
                fewest[v] = fewest[u] + 1; most[v] = most[u] + 1;
                pq.push({nd, v});
            } else if (nd == dist[v]) {
                ways[v] = (ways[v] + ways[u]) % MOD;
                fewest[v] = min(fewest[v], fewest[u] + 1);
                most[v] = max(most[v], most[u] + 1);
            }
        }
    }
    cout << dist[n] << " " << ways[n] << " " << fewest[n] << " " << most[n] << "\\n";
    return 0;
}
""",
    ),
    dict(
        id="floyd-threshold-city",
        title="The Quietest Town",
        difficulty="hard",
        category="Graphs",
        tags=["floyd-warshall", "all-pairs-shortest-paths"],
        inspired_by="LeetCode #1334 Find the City With the Smallest Number of Neighbors at a Threshold Distance",
        statement="""
A region has `n` towns numbered `1..n` connected by `m` two-way roads, each with
a length. A courier company wants to open its quiet headquarters in the town
that has the **fewest other towns** within driving distance `T`
(shortest-path distance **≤ T**; the town itself does not count).

If several towns tie, choose the one with the **largest** number.
Print that town and how many towns are within distance `T` of it.
""",
        input_format="""
First line: `n m T` (2 ≤ n ≤ 100, 0 ≤ m ≤ 1500, 1 ≤ T ≤ 10⁶).
Next `m` lines: `a b w` — a road between towns `a ≠ b` of length `w` (1 ≤ w ≤ 10⁴).
There may be several roads between the same pair of towns.
""",
        output_format="Two integers: the chosen town and its number of towns within distance `T`.",
        hints=[
            "You need the shortest distance between **every** pair of towns. With n ≤ 100, the "
            "**Floyd–Warshall** algorithm (O(n³)) is the simplest tool.",
            "Start with `d[i][i] = 0`, `d[a][b] = min(existing, w)` for each road (both directions), INF elsewhere. "
            "Then for each intermediate `k`, for each `i`, `j`: `d[i][j] = min(d[i][j], d[i][k] + d[k][j])`.",
            "The loop order matters: `k` must be the **outermost** loop.",
            "Python tip: the innermost loop is the hot spot. Build each new row at once, e.g. "
            "`d[i] = [min(x, dik + y) for x, y in zip(d[i], d[k])]` after skipping rows where `d[i][k]` is INF.",
        ],
        samples=[
            "4 4 4\n1 2 3\n2 3 1\n2 4 4\n3 4 1",
            "5 6 2\n1 2 2\n1 5 8\n2 3 3\n2 5 2\n3 4 1\n4 5 1",
        ],
        tests=[
            "2 0 5",
            "2 1 5\n1 2 6",
            "2 2 5\n1 2 6\n2 1 5",
            "3 2 10\n1 2 5\n2 3 5",
        ],
        gen=_gen_floyd,
        starter_python="""import sys

def main():
    data = sys.stdin.read().split()
    n, m, T = int(data[0]), int(data[1]), int(data[2])
    INF = float("inf")
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for i in range(m):
        a, b, w = int(data[3 + 3 * i]) - 1, int(data[4 + 3 * i]) - 1, int(data[5 + 3 * i])
        # TODO: store the road (keep the shorter one if there are duplicates)
    # TODO: Floyd-Warshall, then pick the town
    print(0, 0)

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n, m;
    long long T;
    cin >> n >> m >> T;
    const long long INF = (long long)1e18;
    vector<vector<long long>> d(n, vector<long long>(n, INF));
    for (int i = 0; i < n; i++) d[i][i] = 0;
    for (int i = 0; i < m; i++) {
        int a, b; long long w;
        cin >> a >> b >> w;
        --a; --b;
        // TODO: store the road (keep the shorter one if there are duplicates)
    }
    // TODO: Floyd-Warshall, then pick the town
    cout << "0 0\\n";
    return 0;
}
""",
        solution_python="""import sys

def main():
    data = sys.stdin.read().split()
    n, m, T = int(data[0]), int(data[1]), int(data[2])
    INF = float("inf")
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for i in range(m):
        a, b, w = int(data[3 + 3 * i]) - 1, int(data[4 + 3 * i]) - 1, int(data[5 + 3 * i])
        if w < d[a][b]:
            d[a][b] = d[b][a] = w
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik == INF:
                continue
            d[i] = [x if x <= dik + y else dik + y for x, y in zip(d[i], dk)]
    best_town, best_cnt = -1, n + 1
    for i in range(n):
        cnt = sum(1 for j in range(n) if j != i and d[i][j] <= T)
        if cnt <= best_cnt:
            best_town, best_cnt = i + 1, cnt
    print(best_town, best_cnt)

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n, m;
    long long T;
    cin >> n >> m >> T;
    const long long INF = (long long)1e18;
    vector<vector<long long>> d(n, vector<long long>(n, INF));
    for (int i = 0; i < n; i++) d[i][i] = 0;
    for (int i = 0; i < m; i++) {
        int a, b; long long w;
        cin >> a >> b >> w;
        --a; --b;
        if (w < d[a][b]) d[a][b] = d[b][a] = w;
    }
    for (int k = 0; k < n; k++)
        for (int i = 0; i < n; i++) {
            if (d[i][k] == INF) continue;
            for (int j = 0; j < n; j++)
                if (d[k][j] != INF) d[i][j] = min(d[i][j], d[i][k] + d[k][j]);
        }
    int bestTown = -1, bestCnt = n + 1;
    for (int i = 0; i < n; i++) {
        int cnt = 0;
        for (int j = 0; j < n; j++) if (j != i && d[i][j] <= T) cnt++;
        if (cnt <= bestCnt) { bestTown = i + 1; bestCnt = cnt; }
    }
    cout << bestTown << " " << bestCnt << "\\n";
    return 0;
}
""",
    ),
]
