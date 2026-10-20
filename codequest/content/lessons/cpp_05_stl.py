"""C++ track - Unit 5: STL Containers."""

LESSONS = [
    dict(
        id="cpp-pair-tuple",
        track="cpp",
        unit="STL Containers",
        title="pair, tuple & Structured Bindings",
        summary="Bundle values together, compare them lexicographically, and unpack them.",
        body=r"""
`pair<A, B>` (from `<utility>`) holds two values, possibly of different types.
It is the C++ version of a 2-tuple:

```cpp
pair<string, int> p = {"Ada", 36};
cout << p.first << " " << p.second;   // Ada 36
auto q = make_pair(3, 4.5);           // pair<int, double>
```

**Pairs compare lexicographically**, just like Python tuples: first by
`.first`, and on a tie by `.second`. That makes `min`, `max` and sorting work
out of the box, and a trick like "sort by score, then by name" becomes
`pair<int, string>`.

`tuple` (from `<tuple>`) holds any number of values. You access them with
`get<index>`, and the index must be a compile-time constant:

```cpp
tuple<int, string, double> t = {1, "x", 2.5};
cout << get<1>(t);                    // x
```

**Structured bindings** (C++17) unpack them, much like `a, b = pair` in
Python:

```cpp
auto [name, age] = p;                 // copies
auto& [x, y] = p;                     // references: changes affect p
```

They also work in loops, which you will use constantly with maps:
`for (auto& [key, value] : m)`.

**When to use what?** `pair` is perfect for quick "two values" jobs such as
coordinates or (value, index). Once `.first` and `.second` stop being
obvious, a `struct` with real field names (coming in a later unit) reads
better. A `tuple` is handy for returning several values from a function:
`return {sum, mn, mx};`.
""",
        examples=[
            dict(title="Pairs and comparison",
                 code=r"""#include <algorithm>
#include <iostream>
#include <string>
#include <utility>
using namespace std;

int main() {
    pair<string, int> p = {"Ada", 36};
    cout << p.first << " is " << p.second << "\n";
    pair<int, int> a = {2, 9}, b = {2, 3};
    cout << (a < b) << "\n";                 // 0: first equal, 9 > 3
    auto m = min(a, b);
    cout << m.first << "," << m.second << "\n";
    auto [x, y] = a;
    cout << "x=" << x << " y=" << y << "\n";
    return 0;
}
"""),
            dict(title="Returning a tuple",
                 code=r"""#include <algorithm>
#include <iostream>
#include <tuple>
#include <vector>
using namespace std;

tuple<long long, int, int> stats(const vector<int>& v) {
    long long sum = 0;
    int mn = v[0], mx = v[0];
    for (int x : v) {
        sum += x;
        mn = min(mn, x);
        mx = max(mx, x);
    }
    return {sum, mn, mx};
}

int main() {
    vector<int> v = {5, -2, 8, 1};
    auto [sum, mn, mx] = stats(v);
    cout << sum << " " << mn << " " << mx << "\n";
    return 0;
}
""",
                 explain="A function can return several values at once, unpacked with structured bindings."),
        ],
        challenge=dict(
            prompt=("Read `n` points as `x y` pairs (integers). Print the point that is "
                    "**smallest in lexicographic order** (smallest x, and among those the smallest y), "
                    "followed by the **largest** one, each on its own line as `x y`. Use `pair` "
                    "and its built-in comparison."),
            starter=r"""#include <iostream>
#include <utility>
using namespace std;

int main() {
    int n;
    cin >> n;
    // read pairs; track the smallest and largest with < or min/max
    return 0;
}
""",
            solution=r"""#include <algorithm>
#include <iostream>
#include <utility>
using namespace std;

int main() {
    int n;
    cin >> n;
    pair<int, int> lo, hi;
    for (int i = 0; i < n; i++) {
        pair<int, int> p;
        cin >> p.first >> p.second;
        if (i == 0) lo = hi = p;
        lo = min(lo, p);
        hi = max(hi, p);
    }
    cout << lo.first << " " << lo.second << "\n";
    cout << hi.first << " " << hi.second << "\n";
    return 0;
}
""",
            samples=["4\n3 1\n1 5\n1 2\n3 0\n"],
            tests=["1\n0 0\n", "3\n-5 10\n-5 -10\n7 7\n", "2\n4 4\n4 4\n"],
        ),
    ),
    dict(
        id="cpp-maps",
        track="cpp",
        unit="STL Containers",
        title="map & unordered_map",
        summary="Key-value dictionaries, counting with m[key]++, and the [] insertion trap.",
        body=r"""
C++ has two dictionary types:

- `map<K, V>` (from `<map>`) keeps keys **sorted**, and each operation takes
  O(log n) time.
- `unordered_map<K, V>` (from `<unordered_map>`) is a hash table like
  Python's `dict`. It is O(1) on average, but iteration order is arbitrary.

```cpp
map<string, int> age;
age["Ada"] = 36;
age["Alan"] = 41;
cout << age["Ada"];
```

**Counting is a one-liner.** `m[key]` creates a missing key with value `0`,
so `cnt[word]++` works without the `dict.get(word, 0)` dance from Python.

**The trap:** `m[key]` *always* inserts when the key is absent, even when you
only meant to *look*. `if (m["bob"] > 0)` silently adds `"bob"` with value 0.
To test whether a key exists without inserting it, use:

```cpp
if (m.count(key)) ...                // 1 if present, 0 if not
auto it = m.find(key);               // m.end() if absent
if (it != m.end()) cout << it->second;
```

**Iterating** gives `pair<const K, V>` elements, which unpack nicely with
structured bindings. With a `map` they come out in sorted key order:

```cpp
for (const auto& [word, c] : cnt) cout << word << " " << c << "\n";
```

Remove a key with `m.erase(key)`, and get the number of keys with `m.size()`.

Which one should you pick? Use `map` when you need sorted output or ordered
queries. Otherwise use `unordered_map` for raw speed.
""",
        examples=[
            dict(title="Word counting",
                 code=r"""#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    map<string, int> cnt;
    string w;
    while (cin >> w) cnt[w]++;
    for (const auto& [word, c] : cnt) {
        cout << word << ": " << c << "\n";
    }
    return 0;
}
""",
                 stdin="the cat and the hat and the bat\n",
                 explain="A map iterates in sorted key order, so the output is alphabetical."),
            dict(title="Looking without inserting",
                 code=r"""#include <iostream>
#include <string>
#include <unordered_map>
using namespace std;

int main() {
    unordered_map<string, int> stock = {{"apple", 3}, {"pear", 0}};
    cout << "size " << stock.size() << "\n";
    if (stock.count("kiwi") == 0) cout << "no kiwi\n";
    auto it = stock.find("apple");
    if (it != stock.end()) cout << it->first << " -> " << it->second << "\n";
    int oops = stock["banana"];      // inserts banana = 0 !
    cout << "oops = " << oops << ", size now " << stock.size() << "\n";
    return 0;
}
""",
                 explain="count and find never insert; operator[] does."),
        ],
        challenge=dict(
            prompt=("Read `n` and then `n` words. Print every **distinct** word with the number "
                    "of times it appears, as `word count`, one per line, in **alphabetical** order."),
            starter=r"""#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    int n;
    cin >> n;
    // count with a map, then loop over it
    return 0;
}
""",
            solution=r"""#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    int n;
    cin >> n;
    map<string, int> cnt;
    for (int i = 0; i < n; i++) {
        string w;
        cin >> w;
        cnt[w]++;
    }
    for (const auto& [w, c] : cnt) cout << w << " " << c << "\n";
    return 0;
}
""",
            samples=["6\npear apple pear fig apple pear\n"],
            tests=["1\nsolo\n", "4\nb a B A\n", "5\nx x x x x\n"],
        ),
    ),
    dict(
        id="cpp-sets",
        track="cpp",
        unit="STL Containers",
        title="set & unordered_set",
        summary="Unique elements: insert, count, erase, and always-sorted iteration.",
        body=r"""
A `set<T>` (from `<set>`) stores **unique** values, always in **sorted
order**. `unordered_set<T>` (from `<unordered_set>`) is the hash-based
version, closer to Python's `set`: faster on average, but unordered.

```cpp
set<int> s;
s.insert(5);
s.insert(1);
s.insert(5);            // already there: ignored
cout << s.size();       // 2
```

| Python | C++ |
|---|---|
| `s.add(x)` | `s.insert(x)` |
| `x in s` | `s.count(x)` (0 or 1) |
| `s.discard(x)` | `s.erase(x)` |
| `len(s)` | `s.size()` |
| `min(s)` / `max(s)` | `*s.begin()` / `*s.rbegin()` |

That last row shows a superpower of the ordered `set`: the smallest and
largest elements are always at hand, even as you keep inserting and erasing.
Python has no built-in equivalent. (The `*` *dereferences* an iterator, which
the next lessons explain.)

`insert` returns a pair whose `.second` says whether the value was new. That
is handy for "first time I've seen this?" checks:

```cpp
if (seen.insert(x).second) { /* x was new */ }
```

Building a set from a vector removes duplicates in one step:

```cpp
set<int> uniq(v.begin(), v.end());
```

`multiset<T>` allows duplicates while staying sorted. Careful there:
`ms.erase(x)` removes **all** copies of `x`. To remove one copy, use
`ms.erase(ms.find(x))`.
""",
        examples=[
            dict(title="A set in action",
                 code=r"""#include <iostream>
#include <set>
using namespace std;

int main() {
    set<int> s = {7, 3, 9, 3, 1};
    s.insert(4);
    s.erase(9);
    for (int x : s) cout << x << " ";        // sorted, no duplicates
    cout << "\n";
    cout << "has 3? " << s.count(3) << ", has 9? " << s.count(9) << "\n";
    cout << "min " << *s.begin() << ", max " << *s.rbegin() << "\n";
    return 0;
}
"""),
            dict(title="First repeat",
                 code=r"""#include <iostream>
#include <unordered_set>
using namespace std;

int main() {
    unordered_set<int> seen;
    int x;
    while (cin >> x) {
        if (!seen.insert(x).second) {
            cout << "first repeated value: " << x << "\n";
            return 0;
        }
    }
    cout << "no repeats\n";
    return 0;
}
""",
                 stdin="4 8 15 16 8 42 4\n",
                 explain="insert(...).second is false when the value was already present."),
        ],
        challenge=dict(
            prompt=("Read `n` and then `n` integers. On the first line print how many **distinct** "
                    "values there are. On the second line print the distinct values in increasing "
                    "order, separated by spaces."),
            starter=r"""#include <iostream>
#include <set>
using namespace std;

int main() {
    int n;
    cin >> n;
    // insert everything into a set<int>
    return 0;
}
""",
            solution=r"""#include <iostream>
#include <set>
using namespace std;

int main() {
    int n;
    cin >> n;
    set<int> s;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        s.insert(x);
    }
    cout << s.size() << "\n";
    bool first = true;
    for (int x : s) {
        if (!first) cout << " ";
        cout << x;
        first = false;
    }
    cout << "\n";
    return 0;
}
""",
            samples=["7\n5 3 5 1 3 3 9\n"],
            tests=["1\n42\n", "4\n-1 -1 -1 -1\n", "5\n10 -10 0 10 -10\n"],
        ),
    ),
    dict(
        id="cpp-stack-queue",
        track="cpp",
        unit="STL Containers",
        title="stack, queue & priority_queue",
        summary="LIFO, FIFO and always-the-largest-first containers.",
        body=r"""
These three **container adapters** give you a deliberately small interface:

| | header | add | look | remove |
|---|---|---|---|---|
| `stack<T>` (LIFO) | `<stack>` | `push(x)` | `top()` | `pop()` |
| `queue<T>` (FIFO) | `<queue>` | `push(x)` | `front()` | `pop()` |
| `priority_queue<T>` | `<queue>` | `push(x)` | `top()` | `pop()` |

**`pop()` returns nothing.** Python's `list.pop()` hands you the element, but
in C++ you read it first and then remove it:

```cpp
int x = st.top();
st.pop();
```

Calling `top()`, `front()` or `pop()` on an **empty** container is undefined
behaviour, usually a crash, so check `empty()` first.

**`priority_queue` is a max-heap**: `top()` is always the *largest* element.
Python's `heapq` is a *min*-heap. To get a min-heap in C++, pass the
`greater` comparator (from `<functional>`):

```cpp
priority_queue<int> maxHeap;
priority_queue<int, vector<int>, greater<int>> minHeap;
```

A common trick avoids the long type: push negated numbers into a max-heap.
Heaps of pairs order by `.first`, then `.second`, exactly like comparing
pairs.

Typical uses:

- **stack**: matching brackets, undo history, depth-first search
- **queue**: breadth-first search, simulations of a waiting line
- **priority_queue**: "always process the cheapest or most urgent next",
  as in Dijkstra's algorithm, scheduling, or keeping the top k values

Both `push` and `pop` on a heap are O(log n), and `top()` is O(1).
""",
        examples=[
            dict(title="All three side by side",
                 code=r"""#include <functional>
#include <iostream>
#include <queue>
#include <stack>
#include <vector>
using namespace std;

int main() {
    stack<int> st;
    queue<int> q;
    priority_queue<int> maxH;
    priority_queue<int, vector<int>, greater<int>> minH;
    for (int x : {3, 1, 4, 1, 5}) {
        st.push(x); q.push(x); maxH.push(x); minH.push(x);
    }
    cout << "stack: ";
    while (!st.empty()) { cout << st.top() << " "; st.pop(); }
    cout << "\nqueue: ";
    while (!q.empty()) { cout << q.front() << " "; q.pop(); }
    cout << "\nmax-heap: ";
    while (!maxH.empty()) { cout << maxH.top() << " "; maxH.pop(); }
    cout << "\nmin-heap: ";
    while (!minH.empty()) { cout << minH.top() << " "; minH.pop(); }
    cout << "\n";
    return 0;
}
"""),
            dict(title="Keep the 3 largest",
                 code=r"""#include <functional>
#include <iostream>
#include <queue>
#include <vector>
using namespace std;

int main() {
    // a min-heap of size k: its top is the smallest of the k largest
    priority_queue<int, vector<int>, greater<int>> best;
    int x;
    while (cin >> x) {
        best.push(x);
        if (best.size() > 3) best.pop();
    }
    while (!best.empty()) { cout << best.top() << " "; best.pop(); }
    cout << "\n";
    return 0;
}
""",
                 stdin="5 1 9 3 7 2 8\n",
                 explain="Each new number pushes out the weakest of the current top 3."),
        ],
        challenge=dict(
            prompt=("Read `t`, then `t` strings made of the brackets `()[]{}`. For each one, print "
                    "`YES` if the brackets are **balanced** (every opener is closed by the matching "
                    "closer in the correct order) and `NO` otherwise."),
            starter=r"""#include <iostream>
#include <stack>
#include <string>
using namespace std;

bool balanced(const string& s) {
    stack<char> st;
    // push openers; on a closer, the top must be its partner
    return false;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        string s;
        cin >> s;
        cout << (balanced(s) ? "YES" : "NO") << "\n";
    }
    return 0;
}
""",
            solution=r"""#include <iostream>
#include <stack>
#include <string>
using namespace std;

bool balanced(const string& s) {
    stack<char> st;
    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') {
            st.push(c);
        } else {
            char want = c == ')' ? '(' : c == ']' ? '[' : '{';
            if (st.empty() || st.top() != want) return false;
            st.pop();
        }
    }
    return st.empty();
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        string s;
        cin >> s;
        cout << (balanced(s) ? "YES" : "NO") << "\n";
    }
    return 0;
}
""",
            samples=["3\n([]{})\n([)]\n((\n"],
            tests=["2\n)\n()\n", "1\n{[()()]}[]\n", "3\n]\n{{}}\n([{}])}\n"],
        ),
    ),
    dict(
        id="cpp-iterators",
        track="cpp",
        unit="STL Containers",
        title="Iterators",
        summary="begin/end, *it and ++it, and lower_bound on sets and maps.",
        body=r"""
An **iterator** is a position inside a container. It is what makes the
standard algorithms work the same way on vectors, strings, sets and maps.

```cpp
vector<int> v = {10, 20, 30};
auto it = v.begin();   // points at 10
cout << *it;           // * reads the element: 10
++it;                  // move to 20
```

- `c.begin()` is the first element.
- `c.end()` is **one past the last** element. It is not an element, so never
  dereference it.
- The range `[begin, end)` is half-open, like Python's `range(0, n)`.
- For a map, `it->first` and `it->second` reach the key and value
  (`it->x` is shorthand for `(*it).x`).

The range-based `for` is just this loop with the details hidden:

```cpp
for (auto it = v.begin(); it != v.end(); ++it) cout << *it << " ";
```

**Ordered containers can search for neighbours.** `s.lower_bound(x)` returns
an iterator to the first element `>= x`, and `s.upper_bound(x)` to the first
element `> x`. Both take O(log n), and you have to check them against
`s.end()`:

```cpp
auto it = s.lower_bound(x);
if (it != s.end()) cout << "next >= x is " << *it;
if (it != s.begin()) cout << "previous < x is " << *prev(it);
```

**Invalidation.** Changing a container can make existing iterators dangle.
After a `push_back`, old vector iterators may point at freed memory.
Erasing during a loop needs the iterator that `erase` returns:

```cpp
for (auto it = s.begin(); it != s.end(); )
    if (*it % 2) it = s.erase(it); else ++it;
```
""",
        examples=[
            dict(title="Walking with an iterator",
                 code=r"""#include <iostream>
#include <map>
#include <string>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {10, 20, 30};
    for (auto it = v.begin(); it != v.end(); ++it) cout << *it << " ";
    cout << "\n";
    map<string, int> m = {{"b", 2}, {"a", 1}};
    for (auto it = m.begin(); it != m.end(); ++it)
        cout << it->first << "=" << it->second << " ";
    cout << "\n";
    return 0;
}
"""),
            dict(title="Neighbours in a set",
                 code=r"""#include <iostream>
#include <iterator>
#include <set>
using namespace std;

int main() {
    set<int> s = {10, 20, 30, 40};
    for (int x : {25, 30, 5, 99}) {
        auto it = s.lower_bound(x);
        cout << x << ": ";
        if (it != s.end()) cout << "next>= " << *it << " ";
        else cout << "next>= none ";
        if (it != s.begin()) cout << "prev< " << *prev(it);
        else cout << "prev< none";
        cout << "\n";
    }
    return 0;
}
""",
                 explain="prev(it) (from <iterator>) is the position just before it."),
            dict(title="Erasing while iterating",
                 code=r"""#include <iostream>
#include <set>
using namespace std;

int main() {
    set<int> s = {1, 2, 3, 4, 5, 6};
    for (auto it = s.begin(); it != s.end(); ) {
        if (*it % 2 == 1) it = s.erase(it);   // erase returns the next position
        else ++it;
    }
    for (int x : s) cout << x << " ";
    cout << "\n";
    return 0;
}
"""),
        ],
        challenge=dict(
            prompt=("Read `n` integers into a `set`. Then read `q` queries. For each query `x`, "
                    "print the **smallest stored value that is >= x**, or `-1` if there is none. "
                    "(n, q ≤ 10^5; values fit in an int.)\n\nInput: `n`, the `n` values, `q`, then "
                    "the `q` queries."),
            starter=r"""#include <iostream>
#include <set>
using namespace std;

int main() {
    int n;
    cin >> n;
    set<int> s;
    // read values, then answer queries with s.lower_bound(x)
    return 0;
}
""",
            solution=r"""#include <iostream>
#include <set>
using namespace std;

int main() {
    int n;
    cin >> n;
    set<int> s;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        s.insert(x);
    }
    int q;
    cin >> q;
    while (q--) {
        int x;
        cin >> x;
        auto it = s.lower_bound(x);
        cout << (it == s.end() ? -1 : *it) << "\n";
    }
    return 0;
}
""",
            samples=["4\n10 30 20 40\n4\n15 30 41 -100\n"],
            tests=["1\n5\n2\n5 6\n", "3\n-5 -5 -1\n3\n-6 -4 0\n", "2\n0 1000000000\n2\n1 999999999\n"],
        ),
    ),
]
