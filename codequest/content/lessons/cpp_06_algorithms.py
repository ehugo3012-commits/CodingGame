"""C++ track - Unit 6: Algorithms from <algorithm> and <numeric>, plus fast I/O."""

LESSONS = [
    dict(
        id="cpp-sort",
        track="cpp",
        unit="Algorithms",
        title="Sorting & Lambdas",
        summary="std::sort, greater<>, lambdas and custom comparators.",
        body=r"""
`sort` (from `<algorithm>`) sorts any range given by two iterators:

```cpp
sort(v.begin(), v.end());                   // ascending
sort(v.begin(), v.end(), greater<int>());   // descending
sort(s.begin(), s.end());                   // works on strings too
```

Python's `sorted(v, key=...)` takes a *key function*. C++ instead takes a
**comparator**: a function `cmp(a, b)` that returns `true` when `a` must come
**before** `b`. The quickest way to write one is a **lambda**, an inline,
unnamed function:

```cpp
// by length, shortest first
sort(words.begin(), words.end(), [](const string& a, const string& b) {
    return a.size() < b.size();
});
```

The parts are `[]` (the capture list, explained below), then the parameters,
then the body. A lambda can **capture** surrounding variables: `[&]` captures
them by reference, and `[=]` makes copies.

**Several criteria.** Compare the first key, and only fall through on a tie:

```cpp
// score descending, then name ascending
[](const pair<string,int>& a, const pair<string,int>& b) {
    if (a.second != b.second) return a.second > b.second;
    return a.first < b.first;
}
```

**Never use `<=` in a comparator.** It must be a *strict* "comes before"
relation, and `cmp(x, x)` must be false. With `<=`, `sort` may read outside
the vector and crash, a nasty bug that only shows up on some inputs.

`sort` is not stable: equal elements may be reordered. When you need ties to
keep their original order, use `stable_sort`. Both take O(n log n).
""",
        examples=[
            dict(title="The basics",
                 code=r"""#include <algorithm>
#include <functional>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {5, 2, 9, 1, 7};
    sort(v.begin(), v.end());
    for (int x : v) cout << x << " ";
    cout << "\n";
    sort(v.begin(), v.end(), greater<int>());
    for (int x : v) cout << x << " ";
    cout << "\n";
    string s = "banana";
    sort(s.begin(), s.end());
    cout << s << "\n";
    return 0;
}
"""),
            dict(title="Lambda comparators",
                 code=r"""#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    vector<string> w = {"kiwi", "fig", "banana", "apple", "date"};
    sort(w.begin(), w.end(), [](const string& a, const string& b) {
        if (a.size() != b.size()) return a.size() < b.size();
        return a < b;                     // tie: alphabetical
    });
    for (const auto& s : w) cout << s << " ";
    cout << "\n";

    int target = 10;
    vector<int> v = {3, 14, 9, 22, 11};
    sort(v.begin(), v.end(), [&](int a, int b) {   // captures target
        return abs(a - target) < abs(b - target);
    });
    for (int x : v) cout << x << " ";
    cout << "\n";
    return 0;
}
""",
                 explain="The second lambda uses [&] to read target, sorting by distance from 10."),
        ],
        challenge=dict(
            prompt=("Read `n`, then `n` lines `name score`. Print the names sorted by **score "
                    "descending**; names with equal scores go in **alphabetical** order. Print one "
                    "`name score` per line."),
            starter=r"""#include <algorithm>
#include <iostream>
#include <string>
#include <utility>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<pair<string, int>> v(n);
    for (auto& p : v) cin >> p.first >> p.second;
    // sort(v.begin(), v.end(), [](...) { ... });
    return 0;
}
""",
            solution=r"""#include <algorithm>
#include <iostream>
#include <string>
#include <utility>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<pair<string, int>> v(n);
    for (auto& p : v) cin >> p.first >> p.second;
    sort(v.begin(), v.end(), [](const pair<string, int>& a, const pair<string, int>& b) {
        if (a.second != b.second) return a.second > b.second;
        return a.first < b.first;
    });
    for (const auto& [name, score] : v) cout << name << " " << score << "\n";
    return 0;
}
""",
            samples=["4\nbob 80\nalice 95\ncarol 80\ndave 60\n"],
            tests=["1\nsolo 0\n", "3\nzed 5\namy 5\nmia 5\n", "3\nx -1\ny 0\nz -2\n"],
        ),
    ),
    dict(
        id="cpp-binary-search",
        track="cpp",
        unit="Algorithms",
        title="Binary Search: lower_bound & upper_bound",
        summary="Search a sorted vector in O(log n) and count values in a range.",
        body=r"""
On a **sorted** range, `<algorithm>` offers three O(log n) searches:

```cpp
binary_search(v.begin(), v.end(), x)   // bool: is x present?
lower_bound(v.begin(), v.end(), x)     // iterator to first element >= x
upper_bound(v.begin(), v.end(), x)     // iterator to first element >  x
```

These match Python's `bisect_left` and `bisect_right`, except that they
return **iterators**. Subtract `v.begin()` to turn one into an index:

```cpp
int idx = lower_bound(v.begin(), v.end(), x) - v.begin();
```

If every element is smaller than `x`, you get `v.end()`, which means index
`v.size()`. Check for that before reading `*it`.

Combining the two gives powerful one-liners:

```cpp
// how many copies of x?
upper_bound(v.begin(), v.end(), x) - lower_bound(v.begin(), v.end(), x)
// how many elements <= x?
upper_bound(v.begin(), v.end(), x) - v.begin()
// how many in [lo, hi]?
upper_bound(..., hi) - lower_bound(..., lo)
```

**The input must be sorted** (with the same ordering you search by). On
unsorted data these functions do not complain, they just return nonsense. So
sort once, then answer many queries quickly. That is the standard pattern
when `n` and the number of queries are both around 10⁵: a linear scan per
query would be 10¹⁰ steps, while binary search needs about 17 steps per
query.

For a `set` or `map`, use the member functions `s.lower_bound(x)` instead.
The free function works on them too, but it is O(n) there.

You can also binary-search on the *answer*: if a condition is false up to some
value and true after it, halve the range `lo..hi` in a loop. This is a
classic technique for optimisation problems.
""",
        examples=[
            dict(title="The three searches",
                 code=r"""#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {1, 3, 3, 3, 7, 9};
    cout << binary_search(v.begin(), v.end(), 7) << " "
         << binary_search(v.begin(), v.end(), 4) << "\n";            // 1 0
    cout << lower_bound(v.begin(), v.end(), 3) - v.begin() << "\n";  // 1
    cout << upper_bound(v.begin(), v.end(), 3) - v.begin() << "\n";  // 4
    cout << "copies of 3: "
         << upper_bound(v.begin(), v.end(), 3) - lower_bound(v.begin(), v.end(), 3) << "\n";
    auto it = lower_bound(v.begin(), v.end(), 100);
    if (it == v.end()) cout << "nothing >= 100\n";
    return 0;
}
"""),
            dict(title="Binary search on the answer",
                 code=r"""#include <iostream>
using namespace std;

int main() {
    // largest r with r * r <= n, without floating point
    long long n;
    cin >> n;
    long long lo = 0, hi = 2000000000;
    while (lo < hi) {
        long long mid = lo + (hi - lo + 1) / 2;
        if (mid * mid <= n) lo = mid;
        else hi = mid - 1;
    }
    cout << lo << "\n";
    return 0;
}
""",
                 stdin="999999999999\n",
                 explain="The condition mid*mid <= n is true up to the answer and false after it."),
        ],
        challenge=dict(
            prompt=("Read `n` integers (not sorted) and then `q` queries. For each query `x` print "
                    "**how many of the numbers are <= x**. Both n and q can be 10^5, so sort once "
                    "and use `upper_bound`.\n\nInput: `n`, the `n` numbers, `q`, then the `q` queries."),
            starter=r"""#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int& x : a) cin >> x;
    // sort, then answer each query with upper_bound
    return 0;
}
""",
            solution=r"""#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> a(n);
    for (int& x : a) cin >> x;
    sort(a.begin(), a.end());
    int q;
    cin >> q;
    while (q--) {
        int x;
        cin >> x;
        cout << upper_bound(a.begin(), a.end(), x) - a.begin() << "\n";
    }
    return 0;
}
""",
            samples=["5\n5 1 3 3 9\n4\n3 0 9 4\n"],
            tests=["1\n7\n2\n6 7\n", "4\n-2 -2 -2 -2\n3\n-3 -2 100\n",
                   "3\n1000000000 -1000000000 0\n3\n0 -1 999999999\n"],
        ),
    ),
    dict(
        id="cpp-algorithm-toolbox",
        track="cpp",
        unit="Algorithms",
        title="The Algorithm Toolbox",
        summary="accumulate, min_element, max_element, count, reverse, unique and friends.",
        body=r"""
Before you write a loop, check whether `<algorithm>` or `<numeric>` already
has it. These all take a `begin, end` range:

| Python | C++ | header |
|---|---|---|
| `sum(v)` | `accumulate(b, e, 0LL)` | `<numeric>` |
| `min(v)` / `max(v)` | `*min_element(b, e)` / `*max_element(b, e)` | `<algorithm>` |
| `v.index(min(v))` | `min_element(b, e) - b` | `<algorithm>` |
| `v.count(x)` | `count(b, e, x)` | `<algorithm>` |
| `v.reverse()` | `reverse(b, e)` | `<algorithm>` |
| `list(range(1, n+1))` | `iota(b, e, 1)` | `<numeric>` |
| `any(p(x) for x in v)` | `any_of(b, e, p)` | `<algorithm>` |

**The `accumulate` trap.** The type of the *initial value* decides the type
of the running total. `accumulate(v.begin(), v.end(), 0)` adds in `int` and
overflows on large sums, and `accumulate(..., 0)` over doubles truncates them
to integers! Pass `0LL` for big integer sums and `0.0` for doubles.

`min_element` and `max_element` return **iterators**: use `*` to get the
value, or subtract `v.begin()` to get its index. On an empty range they
return `end`, and dereferencing that is undefined.

**Removing duplicates** is a two-step idiom. First `sort`. Then `unique`
moves the distinct values to the front and returns the new logical end, and
`erase` chops off the leftovers:

```cpp
sort(v.begin(), v.end());
v.erase(unique(v.begin(), v.end()), v.end());
```

Some other gems: `next_permutation` steps through all orderings, `fill` sets
a range to one value, `count_if` counts with a predicate lambda, and for two
values `min(a, b)` / `max(a, b)` (or `max({a, b, c})` for several) do what
you'd expect.
""",
        examples=[
            dict(title="One-liners",
                 code=r"""#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {4, 1000000000, 7, 1500000000, 2, 7};
    cout << "int sum (overflows): " << accumulate(v.begin(), v.end(), 0) << "\n";
    cout << "long long sum:       " << accumulate(v.begin(), v.end(), 0LL) << "\n";
    auto mn = min_element(v.begin(), v.end());
    cout << "min " << *mn << " at index " << mn - v.begin() << "\n";
    cout << "max " << *max_element(v.begin(), v.end()) << "\n";
    cout << "count of 7: " << count(v.begin(), v.end(), 7) << "\n";
    cout << "evens: " << count_if(v.begin(), v.end(), [](int x) { return x % 2 == 0; }) << "\n";
    reverse(v.begin(), v.end());
    for (int x : v) cout << x << " ";
    cout << "\n";
    return 0;
}
"""),
            dict(title="Dedupe and permutations",
                 code=r"""#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {3, 1, 3, 2, 1, 3};
    sort(v.begin(), v.end());
    v.erase(unique(v.begin(), v.end()), v.end());
    for (int x : v) cout << x << " ";
    cout << "\n";

    vector<int> p(3);
    iota(p.begin(), p.end(), 1);          // 1 2 3
    do {
        for (int x : p) cout << x;
        cout << " ";
    } while (next_permutation(p.begin(), p.end()));
    cout << "\n";
    return 0;
}
""",
                 explain="next_permutation returns false after the last ordering, which ends the do-while."),
        ],
        challenge=dict(
            prompt=("Read `n` (≥ 1) and `n` integers (each up to 10^9 in absolute value). Print "
                    "three lines: the **sum**, then the **minimum** and its first index (0-based), "
                    "then the **maximum** and its first index. Try to use `accumulate`, "
                    "`min_element` and `max_element` instead of a hand-written loop."),
            starter=r"""#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> v(n);
    for (int& x : v) cin >> x;
    // accumulate (watch the initial value!), min_element, max_element
    return 0;
}
""",
            solution=r"""#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> v(n);
    for (int& x : v) cin >> x;
    cout << accumulate(v.begin(), v.end(), 0LL) << "\n";
    auto mn = min_element(v.begin(), v.end());
    auto mx = max_element(v.begin(), v.end());
    cout << *mn << " " << mn - v.begin() << "\n";
    cout << *mx << " " << mx - v.begin() << "\n";
    return 0;
}
""",
            samples=["5\n3 1 4 1 5\n"],
            tests=["1\n-8\n", "4\n1000000000 1000000000 1000000000 1000000000\n",
                   "6\n2 -3 7 -3 7 0\n"],
        ),
    ),
    dict(
        id="cpp-fast-io",
        track="cpp",
        unit="Algorithms",
        title="Fast Input & Output",
        summary="sync_with_stdio(false), cin.tie(nullptr), and why endl is slow.",
        body=r"""
By default `cin` and `cout` stay synchronised with C's `scanf` and `printf`,
and `cin` flushes `cout` before every read. That is safe, but slow: reading
10⁶ numbers can take longer than solving the problem. Two lines at the top of
`main` fix it:

```cpp
int main() {
    ios::sync_with_stdio(false);  // stop syncing with C stdio
    cin.tie(nullptr);             // don't flush cout before each cin
    ...
}
```

You will see this in nearly every competitive C++ solution (and in
CodeQuest's starter code). It is the equivalent of switching from Python's
`input()` to `sys.stdin.readline`.

**Rules once you have done this:**

- **Don't mix** `cin`/`cout` with `scanf`/`printf`/`puts` any more. The two
  systems now buffer separately, so output can come out in the wrong order.
- **Use `"\n"`, not `endl`.** `endl` forces a flush every time, which throws
  away the benefit of buffering. Printing 10⁵ lines with `endl` can be several
  times slower.
- In an *interactive* program, where you must see output before the next
  input arrives, you need to flush explicitly with `cout.flush()` or `endl`.
  CodeQuest's problems are not interactive.

**Build output, then print.** For huge outputs it is fine to `cout <<`
inside a loop now, because the stream is buffered. There is no need to glue
a giant string together first, as you might in Python with `"\n".join(...)`.

**Watch the input size.** At 2·10⁵ numbers, each up to 10⁹, sums need
`long long`. Reading with `cin >> x` into the right type is still all you
need.
""",
        examples=[
            dict(title="The standard template",
                 code=r"""#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<long long> a(n);
    for (auto& x : a) cin >> x;
    long long best = a[0], cur = 0;
    for (long long x : a) {            // maximum subarray sum (Kadane)
        cur = max(x, cur + x);
        best = max(best, cur);
    }
    cout << best << "\n";
    return 0;
}
""",
                 stdin="8\n-2 1 -3 4 -1 2 1 -5\n"),
            dict(title="Lots of output, no endl",
                 code=r"""#include <iostream>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long total = 0;
    for (int i = 1; i <= 100000; i++) {
        total += 1LL * i * i;
        if (i % 25000 == 0) cout << i << " " << total << "\n";
    }
    return 0;
}
""",
                 explain="'\\n' just appends to the buffer; the stream writes it out in big chunks."),
        ],
        challenge=dict(
            prompt=("Read `n` (up to 2·10^5) and `n` integers (each up to 10^9 in absolute value). "
                    "Print the **prefix sums**: the i-th output line is the sum of the first i "
                    "numbers. Use fast I/O and `\"\\n\"`."),
            starter=r"""#include <iostream>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    // keep a running long long total and print it after each number
    return 0;
}
""",
            solution=r"""#include <iostream>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    long long total = 0;
    for (int i = 0; i < n; i++) {
        long long x;
        cin >> x;
        total += x;
        cout << total << "\n";
    }
    return 0;
}
""",
            samples=["4\n1 2 3 4\n"],
            tests=["1\n-5\n", "3\n1000000000 1000000000 1000000000\n",
                   "2000\n" + " ".join(str((i * 7919) % 2001 - 1000) for i in range(2000)) + "\n"],
        ),
    ),
]
