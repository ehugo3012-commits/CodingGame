"""Recursion & backtracking: enumerate in a canonical order, count solutions, flood fill."""


def _arr(xs):
    return " ".join(map(str, xs))


def _perm_gen(rng):
    out = []
    for n, alpha in ((1, "z"), (3, "ab"), (5, "abc"), (6, "abcdefghij"), (6, "aabbcz"), (4, "qrst")):
        out.append("".join(rng.choice(alpha) for _ in range(n)))
    return out


def _subset_gen(rng):
    out = []
    for n in (1, 3, 5, 7, 8):
        xs = rng.sample(range(-50, 100), n)
        out.append(f"{n}\n{_arr(xs)}")
    return out


def _combo_gen(rng):
    out = []
    for n, vmax, target in ((1, 5, 5), (6, 6, 8), (12, 10, 25), (20, 30, 60), (20, 8, 40), (20, 50, 1)):
        a = [rng.randint(1, vmax) for _ in range(n)]
        out.append(f"{n} {target}\n{_arr(a)}")
    return out


def _grid_case(rng, r, c, colors):
    rows = ["".join(rng.choice(colors) for _ in range(c)) for _ in range(r)]
    sr, sc = rng.randrange(r), rng.randrange(c)
    k = rng.randint(0, 9)
    return f"{r} {c}\n" + "\n".join(rows) + f"\n{sr} {sc} {k}"


def _fill_gen(rng):
    return [_grid_case(rng, 1, 1, "5"), _grid_case(rng, 4, 6, "01"), _grid_case(rng, 15, 20, "012"),
            _grid_case(rng, 50, 60, "0001"), _grid_case(rng, 50, 50, "0")]


PROBLEMS = [
    dict(
        id="distinct-letter-arrangements",
        title="Distinct Letter Arrangements",
        difficulty="medium",
        category="Recursion",
        tags=["backtracking", "permutations", "lexicographic"],
        inspired_by="LeetCode #47 Permutations II; CSES Creating Strings",
        statement="""
Given a short word, print every **distinct** rearrangement of its letters, in
**alphabetical (lexicographic) order**, one per line.

The letters may repeat: `aab` has only three distinct arrangements —
`aab`, `aba`, `baa`.
""",
        input_format="One line: a word of 1 to 6 lowercase letters.",
        output_format="All distinct arrangements in lexicographic order, one per line.",
        hints=[
            "Backtracking: build the answer one position at a time. At each step try every letter that is still "
            "available, recurse, then undo the choice.",
            "If you try the available letters in sorted order, the outputs come out already sorted. To avoid "
            "duplicates, work with a *count* per letter (e.g. `collections.Counter`, or `int cnt[26]`) instead of "
            "with positions — then each distinct letter is tried once per level.",
            "C++ fans: `sort` the string and loop with `std::next_permutation` (header `<algorithm>`) — it skips "
            "duplicates for you. Still worth writing the recursive version once!",
        ],
        samples=["aab", "abc"],
        tests=["a", "zz", "abcdef", "aaaaab", "banana", "aabbcc"],
        gen=_perm_gen,
        starter_python="""word = input().strip()
letters = sorted(word)
out = []

def build(prefix):
    # TODO: if prefix is complete, record it; otherwise try each unused letter
    pass

build("")
print("\\n".join(out))
""",
        starter_cpp="""#include <iostream>
#include <string>
#include <vector>
using namespace std;

int cnt[26];
int n;
vector<string> out;

void build(string &prefix) {
    // TODO: if prefix has n letters, store it; otherwise try letters 'a'..'z' with cnt > 0
}

int main() {
    string w;
    cin >> w;
    n = w.size();
    for (char c : w) cnt[c - 'a']++;
    string prefix;
    build(prefix);
    for (auto &s : out) cout << s << "\\n";
    return 0;
}
""",
        solution_python=r"""from collections import Counter

word = input().strip()
n = len(word)
cnt = Counter(word)
keys = sorted(cnt)
out = []
cur = []

def build():
    if len(cur) == n:
        out.append("".join(cur))
        return
    for ch in keys:
        if cnt[ch]:
            cnt[ch] -= 1
            cur.append(ch)
            build()
            cur.pop()
            cnt[ch] += 1

build()
print("\n".join(out))
""",
        solution_cpp=r"""#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    string w;
    cin >> w;
    sort(w.begin(), w.end());
    do {
        cout << w << "\n";
    } while (next_permutation(w.begin(), w.end()));
    return 0;
}
""",
    ),
    dict(
        id="subsets-in-dictionary-order",
        title="Subsets in Dictionary Order",
        difficulty="medium",
        category="Recursion",
        tags=["backtracking", "subsets", "lexicographic"],
        inspired_by="LeetCode #78 Subsets",
        statement="""
Given `n` **distinct** integers, list all `2ⁿ` subsets. Write each subset with
its elements in increasing order, and list the subsets in **lexicographic
order** of these sequences (the empty subset comes first, and a sequence comes
before any longer sequence it is a prefix of).

For the set `{3, 1, 2}` the order is:

```
(empty)
1
1 2
1 2 3
1 3
2
2 3
3
```

To make the output unambiguous, start each line with the subset's **size**:
so the lines are `0`, `1 1`, `2 1 2`, `3 1 2 3`, `2 1 3`, `1 2`, `2 2 3`, `1 3`.
""",
        input_format="First line: `n` (1 ≤ n ≤ 10). Second line: `n` distinct integers (|aᵢ| ≤ 100).",
        output_format="`2ⁿ` lines; each line is the size `k` of a subset followed by its `k` elements in increasing order.",
        hints=[
            "Sort the numbers first. Then a recursive `go(start)` that has a current list `cur`: print `cur`, and for "
            "each `i` from `start` to `n − 1` append `a[i]`, call `go(i + 1)`, and remove it again.",
            "Printing *before* the loop (pre-order) is exactly what produces the 'prefix first' dictionary order.",
            "Python: `print(len(cur), *cur)`. C++: pass `cur` by reference (`vector<int>&`) and use `push_back` / "
            "`pop_back` to undo.",
        ],
        samples=["3\n3 1 2", "1\n-7"],
        tests=["2\n5 -5", "4\n10 20 30 40", "10\n9 8 7 6 5 4 3 2 1 0"],
        gen=_subset_gen,
        starter_python="""n = int(input())
a = sorted(map(int, input().split()))
cur = []
out = []

def go(start):
    # TODO: record cur, then try adding each a[i] with i >= start
    pass

go(0)
print("\\n".join(out))
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int n;
vector<int> a, cur;

void go(int start) {
    // TODO: print cur (size first), then extend it with a[i] for i >= start
}

int main() {
    cin >> n;
    a.resize(n);
    for (auto &x : a) cin >> x;
    sort(a.begin(), a.end());
    go(0);
    return 0;
}
""",
        solution_python=r"""n = int(input())
a = sorted(map(int, input().split()))
cur = []
out = []

def go(start):
    out.append(" ".join(map(str, [len(cur)] + cur)))
    for i in range(start, n):
        cur.append(a[i])
        go(i + 1)
        cur.pop()

go(0)
print("\n".join(out))
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int n;
vector<int> a, cur;

void go(int start) {
    cout << cur.size();
    for (int x : cur) cout << ' ' << x;
    cout << '\n';
    for (int i = start; i < n; i++) {
        cur.push_back(a[i]);
        go(i + 1);
        cur.pop_back();
    }
}

int main() {
    cin >> n;
    a.resize(n);
    for (auto &x : a) cin >> x;
    sort(a.begin(), a.end());
    go(0);
    return 0;
}
""",
    ),
    dict(
        id="peaceful-queens-count",
        title="Peaceful Queens",
        difficulty="medium",
        category="Recursion",
        tags=["backtracking", "n-queens", "bitmask"],
        inspired_by="LeetCode #52 N-Queens II; CSES Chessboard and Queens",
        statement="""
Place `n` queens on an `n × n` chessboard so that **no two attack each other**
— no two share a row, a column, or a diagonal. In how many ways can it be
done?

For `n = 4` there are exactly **2** ways:

```
. Q . .      . . Q .
. . . Q      Q . . .
Q . . .      . . . Q
. . Q .      . Q . .
```

Trying all placements of `n` queens on `n²` squares is hopeless. Place one
queen per row and **backtrack** as soon as a queen is attacked.
""",
        input_format="One integer `n` (1 ≤ n ≤ 10).",
        output_format="One integer: the number of peaceful placements.",
        hints=[
            "Recursive `place(row)`: try every column `c` for the queen in this row; if it's safe, mark it and call "
            "`place(row + 1)`. Reaching `row == n` means one full solution.",
            "A square `(r, c)` is attacked through its column `c`, its diagonal `r − c` and its anti-diagonal `r + c`. "
            "Keep three boolean arrays (or sets) so the safety check is O(1).",
            "Speed-up (optional): store the three sets as bitmasks; `free = ~(cols | d1 | d2) & ((1 << n) − 1)` and peel "
            "off one bit at a time with `bit = free & -free`.",
        ],
        samples=["4", "1"],
        tests=["2", "3", "5", "6", "7", "8", "9", "10"],
        starter_python="""n = int(input())
cols, diag1, diag2 = set(), set(), set()
count = 0

def place(row):
    global count
    # TODO: if row == n, count one solution; else try each column
    pass

place(0)
print(count)
""",
        starter_cpp="""#include <iostream>
#include <vector>
using namespace std;

int n;
long long countWays = 0;
vector<bool> col, d1, d2;

void place(int row) {
    // TODO: if row == n, count a solution; else try each column c
}

int main() {
    cin >> n;
    col.assign(n, false);
    d1.assign(2 * n, false);
    d2.assign(2 * n, false);
    place(0);
    cout << countWays << "\\n";
    return 0;
}
""",
        solution_python=r"""n = int(input())
full = (1 << n) - 1

def place(cols, d1, d2):
    if cols == full:
        return 1
    total = 0
    free = ~(cols | d1 | d2) & full
    while free:
        bit = free & -free
        free ^= bit
        total += place(cols | bit, ((d1 | bit) << 1) & full, (d2 | bit) >> 1)
    return total

print(place(0, 0, 0))
""",
        solution_cpp=r"""#include <iostream>
using namespace std;

int n, full;

long long place(int cols, int d1, int d2) {
    if (cols == full) return 1;
    long long total = 0;
    int freeMask = ~(cols | d1 | d2) & full;
    while (freeMask) {
        int bit = freeMask & -freeMask;
        freeMask ^= bit;
        total += place(cols | bit, ((d1 | bit) << 1) & full, (d2 | bit) >> 1);
    }
    return total;
}

int main() {
    cin >> n;
    full = (1 << n) - 1;
    cout << place(0, 0, 0) << "\n";
    return 0;
}
""",
    ),
    dict(
        id="combo-sum-each-once",
        title="Combination Sum, Each Once",
        difficulty="medium",
        category="Recursion",
        tags=["backtracking", "pruning", "duplicates"],
        inspired_by="LeetCode #40 Combination Sum II",
        statement="""
You have `n` number cards (values may repeat) and a target `T`. Count the
**distinct combinations** of cards whose values add up to exactly `T`, using
each card at most once.

Combinations are compared by their *values*, not by which physical card was
used, and order doesn't matter. With cards `10 1 2 7 6 1 5` and `T = 8` there
are **4** combinations: `1 1 6`, `1 2 5`, `1 7`, `2 6`.
""",
        input_format="""First line: `n T` (1 ≤ n ≤ 20, 1 ≤ T ≤ 60).
Second line: `n` card values (1 ≤ vᵢ ≤ 50).""",
        output_format="One integer: the number of distinct combinations.",
        hints=[
            "Sort the cards. Backtrack with `go(start, remaining)`: try each card `i >= start` as the next (largest-so-far) "
            "card and recurse with `go(i + 1, remaining − v[i])`.",
            "**Prune**: because the cards are sorted, once `v[i] > remaining` no later card fits either — `break`.",
            "**Skip duplicates**: at the same depth, if `i > start` and `v[i] == v[i − 1]`, skip `i` — choosing an equal "
            "card in the same slot would create the same combination again.",
        ],
        samples=["7 8\n10 1 2 7 6 1 5", "5 5\n2 5 2 1 2"],
        tests=["1 5\n5", "1 4\n5", "4 2\n1 1 1 1", "20 60\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20",
               "20 20\n1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1"],
        gen=_combo_gen,
        starter_python="""n, T = map(int, input().split())
v = sorted(map(int, input().split()))

def go(start, remaining):
    # TODO: return the number of combinations using cards v[start:] summing to remaining
    return 0

print(go(0, T))
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int n, T;
vector<int> v;

long long go(int start, int remaining) {
    // TODO: count combinations from v[start..] that sum to remaining
    return 0;
}

int main() {
    cin >> n >> T;
    v.resize(n);
    for (auto &x : v) cin >> x;
    sort(v.begin(), v.end());
    cout << go(0, T) << "\\n";
    return 0;
}
""",
        solution_python=r"""from collections import Counter

n, T = map(int, input().split())
cnt = Counter(map(int, input().split()))
# ways[s] = number of distinct multisets (within the available copies) summing to s
ways = [0] * (T + 1)
ways[0] = 1
for val, c in cnt.items():
    new = [0] * (T + 1)
    for s in range(T + 1):
        if ways[s]:
            for k in range(c + 1):
                t = s + k * val
                if t > T:
                    break
                new[t] += ways[s]
    ways = new
print(ways[T])
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int n, T;
vector<int> v;

long long go(int start, int remaining) {
    if (remaining == 0) return 1;
    long long total = 0;
    for (int i = start; i < n; i++) {
        if (v[i] > remaining) break;
        if (i > start && v[i] == v[i - 1]) continue;
        total += go(i + 1, remaining - v[i]);
    }
    return total;
}

int main() {
    cin >> n >> T;
    v.resize(n);
    for (auto &x : v) cin >> x;
    sort(v.begin(), v.end());
    cout << go(0, T) << "\n";
    return 0;
}
""",
    ),
    dict(
        id="paint-bucket-fill",
        title="Paint Bucket Fill",
        difficulty="medium",
        category="Recursion",
        tags=["flood-fill", "dfs", "grid"],
        inspired_by="LeetCode #733 Flood Fill (the paint-bucket tool)",
        statement="""
An image is a grid of `R × C` pixels, each a colour digit `0`–`9`. You click
the paint bucket on pixel `(r, c)` with colour `k`.

The bucket recolours the clicked pixel and every pixel **connected** to it
through up/down/left/right neighbours that has the **same original colour**.
Print the resulting image.

If the clicked pixel already has colour `k`, nothing changes.
""",
        input_format="""First line: `R C` (1 ≤ R, C ≤ 60).
Next `R` lines: a string of `C` digits.
Last line: `r c k` — 0-based row and column of the click (0 ≤ r < R, 0 ≤ c < C), and the new colour (0 ≤ k ≤ 9).""",
        output_format="The `R` rows of the new image.",
        hints=[
            "Remember the original colour `old = grid[r][c]`. If `old == k` you're done; otherwise start a DFS/BFS "
            "from `(r, c)`.",
            "Visiting a pixel: if it's inside the grid and still has colour `old`, paint it `k` and visit its four "
            "neighbours. Painting it *is* the 'visited' mark, so no extra array is needed.",
            "Recursion depth can reach `R·C` = 3600. That's fine in C++; in Python, prefer an explicit stack "
            "(`stack = [(r, c)]`, `while stack: ... stack.pop()`). Store rows as lists: `grid = [list(row) for ...]`.",
        ],
        samples=["3 3\n111\n110\n101\n1 1 2", "2 3\n000\n000\n0 0 0"],
        tests=["1 1\n7\n0 0 3", "3 4\n1212\n2121\n1212\n1 1 9", "4 4\n0000\n0110\n0110\n0000\n0 0 5"],
        gen=_fill_gen,
        starter_python="""R, C = map(int, input().split())
grid = [list(input().strip()) for _ in range(R)]
r, c, k = input().split()
r, c = int(r), int(c)
# TODO: flood fill from (r, c) with colour k
print("\\n".join("".join(row) for row in grid))
""",
        starter_cpp="""#include <iostream>
#include <string>
#include <vector>
using namespace std;

int R, C;
vector<string> g;

int main() {
    cin >> R >> C;
    g.resize(R);
    for (auto &row : g) cin >> row;
    int r, c;
    char k;
    cin >> r >> c >> k;
    // TODO: flood fill from (r, c) with colour k
    for (auto &row : g) cout << row << "\\n";
    return 0;
}
""",
        solution_python=r"""R, C = map(int, input().split())
grid = [list(input().strip()) for _ in range(R)]
r, c, k = input().split()
r, c = int(r), int(c)
old = grid[r][c]
if old != k:
    stack = [(r, c)]
    grid[r][c] = k
    while stack:
        y, x = stack.pop()
        for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if 0 <= ny < R and 0 <= nx < C and grid[ny][nx] == old:
                grid[ny][nx] = k
                stack.append((ny, nx))
print("\n".join("".join(row) for row in grid))
""",
        solution_cpp=r"""#include <iostream>
#include <string>
#include <vector>
using namespace std;

int R, C;
vector<string> g;
char oldc, newc;

void fill(int y, int x) {
    if (y < 0 || y >= R || x < 0 || x >= C || g[y][x] != oldc) return;
    g[y][x] = newc;
    fill(y + 1, x);
    fill(y - 1, x);
    fill(y, x + 1);
    fill(y, x - 1);
}

int main() {
    cin >> R >> C;
    g.resize(R);
    for (auto &row : g) cin >> row;
    int r, c;
    cin >> r >> c >> newc;
    oldc = g[r][c];
    if (oldc != newc) fill(r, c);
    for (auto &row : g) cout << row << "\n";
    return 0;
}
""",
    ),
]
