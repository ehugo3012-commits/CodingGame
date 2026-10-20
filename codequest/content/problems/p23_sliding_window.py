"""Sliding Window: variable-size windows with two moving ends."""

import string


def _arr(xs):
    return " ".join(map(str, xs))


_ALNUM = string.ascii_lowercase + string.digits


def _uniq_gen(rng):
    out = []
    for n, alpha in ((1, "a"), (12, "ab"), (200, "abcde"), (20000, _ALNUM), (15000, "abcdefghij")):
        out.append("".join(rng.choice(alpha) for _ in range(n)))
    # a long run of all 36 symbols in a row, hidden in noise
    out.append("aa" + "".join(rng.sample(_ALNUM, 36)) + "zz")
    return out


def _heavy_gen(rng):
    out = []
    for n, amax, frac in ((1, 10, 0.5), (10, 10, 0.4), (300, 100, 0.2), (4000, 10**4, 0.05),
                          (4000, 10**4, 2.0)):
        a = [rng.randint(1, amax) for _ in range(n)]
        s = max(1, int(sum(a) * frac))
        out.append(f"{n} {s}\n{_arr(a)}")
    return out


def _flip_gen(rng):
    out = []
    for n, p1, k in ((1, 0.5, 0), (15, 0.5, 2), (300, 0.7, 10), (20000, 0.6, 50), (10000, 0.1, 0),
                     (15000, 0.95, 300)):
        bits = "".join("1" if rng.random() < p1 else "0" for _ in range(n))
        out.append(f"{n} {k}\n{bits}")
    return out


PROBLEMS = [
    dict(
        id="longest-distinct-run",
        title="Longest Distinct Run",
        difficulty="medium",
        category="Sliding Window",
        tags=["sliding-window", "hashing", "strings"],
        inspired_by="LeetCode #3 Longest Substring Without Repeating Characters",
        statement="""
Given a string, find the length of the longest **contiguous** piece of it
(a substring) in which no character appears twice.

* `abcabcbb` → `abc` has length **3**.
* `pwwkew` → `wke` has length **3** (`pwke` is not contiguous).

Checking every substring is O(n²) or worse. Slide a window instead: grow it
on the right, shrink it on the left whenever a character repeats.
""",
        input_format="One line: the string `s` (1 ≤ |s| ≤ 2·10⁴), made of lowercase letters and digits.",
        output_format="One integer: the length of the longest substring with all-distinct characters.",
        hints=[
            "Keep a window `s[left..right]` that never contains a repeat, and remember where each character was last "
            "seen (a dict / `unordered_map<char,int>` or an array of size 128).",
            "When `s[right]` was last seen at index `j >= left`, the window must start after it: `left = j + 1`. "
            "Never move `left` backwards!",
            "After updating, the window length is `right − left + 1`; keep the maximum. Each index enters and leaves "
            "the window once, so the scan is O(n).",
        ],
        samples=["abcabcbb", "bbbbb", "pwwkew"],
        tests=["a", "ab", "abba", "dvdf", "tmmzuxt", "abcdefghijklmnopqrstuvwxyz0123456789"],
        gen=_uniq_gen,
        starter_python="""s = input().strip()
last = {}   # character -> last index where it was seen
left = 0
best = 0
for right, ch in enumerate(s):
    # TODO: move left past the previous copy of ch, update best
    pass
print(best)
""",
        starter_cpp="""#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    string s;
    cin >> s;
    vector<int> last(128, -1);  // last index of each character
    int left = 0, best = 0;
    for (int right = 0; right < (int)s.size(); right++) {
        // TODO: move left past the previous copy of s[right], update best
    }
    cout << best << "\\n";
    return 0;
}
""",
        solution_python=r"""s = input().strip()
last = {}
left = 0
best = 0
for right, ch in enumerate(s):
    j = last.get(ch, -1)
    if j >= left:
        left = j + 1
    last[ch] = right
    if right - left + 1 > best:
        best = right - left + 1
print(best)
""",
        solution_cpp=r"""#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    string s;
    cin >> s;
    vector<int> last(128, -1);
    int left = 0, best = 0;
    for (int right = 0; right < (int)s.size(); right++) {
        int c = (unsigned char)s[right];
        if (last[c] >= left) left = last[c] + 1;
        last[c] = right;
        best = max(best, right - left + 1);
    }
    cout << best << "\n";
    return 0;
}
""",
    ),
    dict(
        id="shortest-heavy-segment",
        title="Shortest Heavy Segment",
        difficulty="medium",
        category="Sliding Window",
        tags=["sliding-window", "two-pointers", "prefix-sums"],
        inspired_by="LeetCode #209 Minimum Size Subarray Sum",
        statement="""
A conveyor belt carries `n` crates in a row; crate `i` weighs `a[i]` kg (all
weights are **positive**). A crane can lift any contiguous group of crates.

Find the length of the **shortest** contiguous group whose total weight is
**at least** `S`. If even all crates together weigh less than `S`, print `0`.

For `S = 7` and weights `2 3 1 2 4 3`, the group `4 3` has weight 7 and
length **2**.
""",
        input_format="""First line: `n S` (1 ≤ n ≤ 5000, 1 ≤ S ≤ 10⁹).
Second line: `n` integers (1 ≤ aᵢ ≤ 10⁴).""",
        output_format="One integer: the minimal length, or `0` if no group is heavy enough.",
        hints=[
            "Because all weights are positive, extending a window makes it heavier and shrinking makes it lighter. "
            "That monotonicity is what makes a sliding window correct here.",
            "Move `right` one step at a time, adding `a[right]` to a running sum. While the sum is `>= S`, record the "
            "length and remove `a[left]` (then `left += 1`).",
            "Start the answer at 'infinity' (`float('inf')` / `n + 1`) and print `0` if it never changed.",
        ],
        samples=["6 7\n2 3 1 2 4 3", "3 4\n1 4 4", "8 11\n1 1 1 1 1 1 1 1"],
        tests=["1 1\n1", "1 2\n1", "5 15\n1 2 3 4 5", "5 5\n1 1 5 1 1", "4 1000000000\n10000 10000 10000 10000"],
        gen=_heavy_gen,
        starter_python="""n, S = map(int, input().split())
a = list(map(int, input().split()))
best = n + 1
left = 0
total = 0
for right in range(n):
    total += a[right]
    # TODO: shrink from the left while total >= S, updating best
print(best if best <= n else 0)
""",
        starter_cpp="""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    long long S;
    cin >> n >> S;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    int best = n + 1, left = 0;
    long long total = 0;
    for (int right = 0; right < n; right++) {
        total += a[right];
        // TODO: shrink from the left while total >= S
    }
    cout << (best <= n ? best : 0) << "\\n";
    return 0;
}
""",
        solution_python=r"""n, S = map(int, input().split())
a = list(map(int, input().split()))
best = n + 1
left = 0
total = 0
for right in range(n):
    total += a[right]
    while total >= S:
        if right - left + 1 < best:
            best = right - left + 1
        total -= a[left]
        left += 1
print(best if best <= n else 0)
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    long long S;
    cin >> n >> S;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    int best = n + 1, left = 0;
    long long total = 0;
    for (int right = 0; right < n; right++) {
        total += a[right];
        while (total >= S) {
            best = min(best, right - left + 1);
            total -= a[left++];
        }
    }
    cout << (best <= n ? best : 0) << "\n";
    return 0;
}
""",
    ),
    dict(
        id="longest-lit-streak",
        title="Longest Lit Streak",
        difficulty="medium",
        category="Sliding Window",
        tags=["sliding-window", "two-pointers", "binary-strings"],
        inspired_by="LeetCode #1004 Max Consecutive Ones III",
        statement="""
A street has `n` lamps in a row, given as a string of `1` (working) and `0`
(broken). You have spare parts to repair **at most `k`** broken lamps.

After the repairs, what is the longest run of consecutive working lamps you
can get?

For `1110001111` with `k = 2`: repairing the last two broken lamps gives
`1110111111`, whose final run has length **6**. Repairing the first two
instead gives `1111101111`, with a best run of only 5. The answer is **6**.
""",
        input_format="""First line: `n k` (1 ≤ n ≤ 2·10⁴, 0 ≤ k ≤ n).
Second line: a string of `n` characters, each `0` or `1`.""",
        output_format="One integer: the longest possible run of `1`s.",
        hints=[
            "Rephrase: find the longest window that contains **at most `k` zeros** — you repair exactly those.",
            "Grow the window with `right`, counting zeros inside it. While the count exceeds `k`, move `left` forward "
            "(decreasing the count when a `0` leaves).",
            "The window is valid after the inner loop, so update the answer with `right − left + 1` every step.",
        ],
        samples=["10 2\n1110001111", "6 0\n110111", "4 4\n0000"],
        tests=["1 0\n0", "1 0\n1", "1 1\n0", "5 1\n10101", "8 3\n00000000"],
        gen=_flip_gen,
        starter_python="""n, k = map(int, input().split())
s = input().strip()
left = 0
zeros = 0
best = 0
for right in range(n):
    # TODO: add s[right], shrink while zeros > k, update best
    pass
print(best)
""",
        starter_cpp="""#include <iostream>
#include <string>
using namespace std;

int main() {
    int n, k;
    string s;
    cin >> n >> k >> s;
    int left = 0, zeros = 0, best = 0;
    for (int right = 0; right < n; right++) {
        // TODO: add s[right], shrink while zeros > k, update best
    }
    cout << best << "\\n";
    return 0;
}
""",
        solution_python=r"""n, k = map(int, input().split())
s = input().strip()
left = 0
zeros = 0
best = 0
for right in range(n):
    if s[right] == "0":
        zeros += 1
    while zeros > k:
        if s[left] == "0":
            zeros -= 1
        left += 1
    if right - left + 1 > best:
        best = right - left + 1
print(best)
""",
        solution_cpp=r"""#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    int n, k;
    string s;
    cin >> n >> k >> s;
    int left = 0, zeros = 0, best = 0;
    for (int right = 0; right < n; right++) {
        if (s[right] == '0') zeros++;
        while (zeros > k) {
            if (s[left] == '0') zeros--;
            left++;
        }
        best = max(best, right - left + 1);
    }
    cout << best << "\n";
    return 0;
}
""",
    ),
]
