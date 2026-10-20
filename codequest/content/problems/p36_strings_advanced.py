"""Hard / expert string algorithms: prefix function (KMP), Manacher, suffix sorting / hashing."""


def _rand_str(rng, n, alpha):
    return "".join(rng.choice(alpha) for _ in range(n))


def _gen_shortest_pal(rng):
    tests = []
    half = _rand_str(rng, 5000, "ab")
    tests.append(half + half[::-1] + _rand_str(rng, 3, "ab"))          # long palindromic prefix
    tests.append("a" * 9999 + "b" + "a" * 5000)                         # classic worst case for naive checks
    tests.append(_rand_str(rng, 8000, "abc"))
    p = _rand_str(rng, 1500, "xy")
    tests.append(p + "z" + p[::-1])                                     # already a palindrome
    return tests


def _gen_borders(rng):
    tests = []
    block = _rand_str(rng, 7, "ab")
    tests.append((block * 2000)[:7000])                                 # very periodic: many borders
    tests.append("a" * 1000)
    unit = _rand_str(rng, 40, "abc")
    tests.append(unit + _rand_str(rng, 3000, "abc") + unit)
    fib = ["b", "a"]
    while len(fib[-1]) < 4000:
        fib.append(fib[-1] + fib[-2])
    tests.append(fib[-1])                                               # Fibonacci word
    return tests


def _gen_manacher(rng):
    tests = []
    tests.append("a" * 12000)
    tests.append(_rand_str(rng, 15000, "ab"))
    core = _rand_str(rng, 1200, "abc")
    tests.append(_rand_str(rng, 3000, "abc") + core + core[::-1] + _rand_str(rng, 3000, "abc"))
    tests.append("ab" * 2500)
    return tests


def _gen_distinct(rng):
    return [
        _rand_str(rng, 2000, "ab"),
        _rand_str(rng, 2000, "abcdefghijklmnopqrstuvwxyz"),
        "a" * 2000,
        ("abcab" * 400)[:1999],
        _rand_str(rng, 50, "abc") * 30,
    ]


PROBLEMS = [
    dict(
        id="shortest-palindrome-front",
        title="Shortest Palindrome by Prepending",
        difficulty="hard",
        category="Strings",
        tags=["kmp", "prefix-function", "palindrome"],
        inspired_by="LeetCode #214 Shortest Palindrome",
        statement="""
You may add letters **only to the front** of a string `s`. What is the smallest
number of letters you must add to turn `s` into a palindrome?

For `s = "aacecaaa"` the answer is 1 (`"a" + s = "aaacecaaa"`); for `s = "abcd"` it is 3
(`"dcbabcd"`).

With |s| up to 2·10⁴, testing every prefix for being a palindrome can take ~n²/2 steps.
""",
        input_format="One line: the string `s` (lowercase letters, 1 ≤ |s| ≤ 2·10⁴).",
        output_format="One integer: the minimum number of letters to prepend.",
        hints=[
            "Prepending letters keeps `s` at the end, so what you can reuse is the **longest prefix of `s` that is a "
            "palindrome**. If its length is `L`, the answer is `|s| − L`.",
            "A prefix of `s` is a palindrome exactly when it equals the matching suffix of `reverse(s)`. "
            "\"Longest prefix of A that is also a suffix of B\" is what the KMP **prefix function** computes.",
            "Build `t = s + '#' + reverse(s)` (the separator stops matches from running past `s`) and compute the prefix function "
            "`pi`; `pi[last]` is `L`.",
            "Prefix function: `pi[i]` = length of the longest proper prefix of `t[0..i]` that is also its suffix. "
            "Compute it with `k = pi[i−1]; while k > 0 and t[i] != t[k]: k = pi[k−1]` and then extend `k` by one if `t[i] == t[k]`.",
        ],
        samples=["aacecaaa", "abcd"],
        tests=["a", "ab", "aa", "aba", "abb", "baaa"],
        gen=_gen_shortest_pal,
        starter_python="""s = input().strip()
# TODO: longest palindromic prefix via the prefix function of s + '#' + s[::-1]
print(0)
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    string s;
    cin >> s;
    // TODO: longest palindromic prefix via the prefix function of s + '#' + reverse(s)
    cout << 0 << "\\n";
    return 0;
}
""",
        solution_python="""s = input().strip()
t = s + "#" + s[::-1]
pi = [0] * len(t)
for i in range(1, len(t)):
    k = pi[i - 1]
    while k > 0 and t[i] != t[k]:
        k = pi[k - 1]
    if t[i] == t[k]:
        k += 1
    pi[i] = k
print(len(s) - pi[-1])
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    string s;
    cin >> s;
    string r(s.rbegin(), s.rend());
    string t = s + "#" + r;
    vector<int> pi(t.size(), 0);
    for (size_t i = 1; i < t.size(); i++) {
        int k = pi[i - 1];
        while (k > 0 && t[i] != t[k]) k = pi[k - 1];
        if (t[i] == t[k]) k++;
        pi[i] = k;
    }
    cout << (int)s.size() - pi.back() << "\\n";
    return 0;
}
""",
    ),
    dict(
        id="border-occurrences",
        title="Borders and Their Echoes",
        difficulty="expert",
        category="Strings",
        tags=["kmp", "prefix-function", "z-function", "counting"],
        inspired_by="Codeforces 432D Prefixes and Suffixes",
        statement="""
A **border** of a string `s` is a prefix of `s` that is also a suffix of `s`.
Here we count the whole string `s` as a border too (but not the empty string).

For every border, report its length and how many times it occurs **anywhere** in `s`
as a substring (occurrences may overlap).

For `s = "ababa"`: the borders are `a` (occurs 3 times), `aba` (2 times) and `ababa` (once).
""",
        input_format="One line: the string `s` (lowercase letters, 1 ≤ |s| ≤ 2·10⁴).",
        output_format="""
First line: `k`, the number of borders. Then `k` lines `length count`, by increasing length.
""",
        hints=[
            "Compute the **prefix function** `pi` of `s`. The borders are exactly `n`, `pi[n−1]`, `pi[pi[n−1]−1]`, … "
            "(follow the chain until 0).",
            "Counting occurrences of *every* prefix at once: an occurrence of prefix length `L` ending at position `i` exists "
            "iff `L` is in the chain `pi[i], pi[pi[i]−1], …` of that position.",
            "So first set `cnt[pi[i]] += 1` for every `i`; then push counts down the chain from long to short: "
            "`for L = n … 1: cnt[pi[L−1]] += cnt[L]`. Finally add 1 to every `cnt[L]` for the prefix itself.",
            "Alternative: the **Z-function** — the prefix of length `L` occurs at position `i` iff `z[i] ≥ L`; "
            "count how many `z` values are ≥ L with a suffix sum over a histogram.",
        ],
        samples=["ababa", "aaa"],
        tests=["a", "ab", "abcab", "abacaba", "aabaa"],
        gen=_gen_borders,
        starter_python="""s = input().strip()
n = len(s)
# TODO: prefix function, occurrence counts of every prefix, then walk the border chain
print(0)
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    string s;
    cin >> s;
    int n = s.size();
    // TODO: prefix function, occurrence counts of every prefix, then walk the border chain
    cout << 0 << "\\n";
    return 0;
}
""",
        solution_python="""s = input().strip()
n = len(s)
pi = [0] * n
for i in range(1, n):
    k = pi[i - 1]
    while k > 0 and s[i] != s[k]:
        k = pi[k - 1]
    if s[i] == s[k]:
        k += 1
    pi[i] = k
cnt = [0] * (n + 1)
for v in pi:
    cnt[v] += 1
for L in range(n, 0, -1):
    cnt[pi[L - 1]] += cnt[L]
borders = []
L = n
while L > 0:
    borders.append(L)
    L = pi[L - 1]
borders.reverse()
print(len(borders))
print("\\n".join(f"{L} {cnt[L] + 1}" for L in borders))
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    string s;
    cin >> s;
    int n = s.size();
    vector<int> pi(n, 0);
    for (int i = 1; i < n; i++) {
        int k = pi[i - 1];
        while (k > 0 && s[i] != s[k]) k = pi[k - 1];
        if (s[i] == s[k]) k++;
        pi[i] = k;
    }
    vector<long long> cnt(n + 1, 0);
    for (int v : pi) cnt[v]++;
    for (int L = n; L >= 1; L--) cnt[pi[L - 1]] += cnt[L];
    vector<int> borders;
    for (int L = n; L > 0; L = pi[L - 1]) borders.push_back(L);
    reverse(borders.begin(), borders.end());
    cout << borders.size() << "\\n";
    for (int L : borders) cout << L << " " << cnt[L] + 1 << "\\n";
    return 0;
}
""",
    ),
    dict(
        id="longest-palindrome-manacher",
        title="Longest Mirror Segment",
        difficulty="hard",
        category="Strings",
        tags=["manacher", "palindrome", "strings"],
        inspired_by="LeetCode #5 Longest Palindromic Substring / CSES 1111 Longest Palindrome",
        statement="""
Find the longest **contiguous** substring of `s` that reads the same forwards and
backwards. Print its length and its starting position (1-based). If several
longest palindromes exist, report the **leftmost** one.
""",
        input_format="One line: the string `s` (lowercase letters, 1 ≤ |s| ≤ 1.5·10⁴).",
        output_format="Two integers: `length start`.",
        hints=[
            "Expanding around each of the 2n−1 centres is simple but O(n²) on strings like `aaaa…a`. "
            "**Manacher's algorithm** does it in O(n).",
            "Handle odd and even lengths uniformly: insert a separator between letters, e.g. `t = '^#' + '#'.join(s) + '#$'`. "
            "Now every palindrome of `s` is an odd palindrome of `t` and `p[i]` (the radius in `t`) equals its length in `s`.",
            "Keep the palindrome `[c − p[c], c + p[c]]` that reaches furthest right. For a new centre `i` inside it, its "
            "mirror `2c − i` tells you a safe starting radius: `p[i] = min(right − i, p[2c − i])`; then try to expand.",
            "The palindrome of radius `p[i]` around `t`-index `i` starts at index `(i − 1 − p[i]) // 2` of `s` (0-based). "
            "Scanning centres left to right and updating only on a **strictly** longer palindrome gives the leftmost one.",
        ],
        samples=["babad", "cbbd"],
        tests=["a", "ab", "aa", "abacdfgdcaba", "forgeeksskeegfor"],
        gen=_gen_manacher,
        starter_python="""s = input().strip()
# TODO: Manacher's algorithm
print(1, 1)
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    string s;
    cin >> s;
    // TODO: Manacher's algorithm
    cout << 1 << " " << 1 << "\\n";
    return 0;
}
""",
        solution_python="""s = input().strip()
t = "^#" + "#".join(s) + "#$"
p = [0] * len(t)
c = right = 0
best_len, best_start = 0, 0
for i in range(1, len(t) - 1):
    if i < right:
        p[i] = min(right - i, p[2 * c - i])
    while t[i + p[i] + 1] == t[i - p[i] - 1]:
        p[i] += 1
    if i + p[i] > right:
        c, right = i, i + p[i]
    if p[i] > best_len:
        best_len, best_start = p[i], (i - 1 - p[i]) // 2
print(best_len, best_start + 1)
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    string s;
    cin >> s;
    string t = "^#";
    for (char ch : s) { t += ch; t += '#'; }
    t += '$';
    int m = t.size();
    vector<int> p(m, 0);
    int c = 0, right = 0, bestLen = 0, bestStart = 0;
    for (int i = 1; i < m - 1; i++) {
        if (i < right) p[i] = min(right - i, p[2 * c - i]);
        while (t[i + p[i] + 1] == t[i - p[i] - 1]) p[i]++;
        if (i + p[i] > right) { c = i; right = i + p[i]; }
        if (p[i] > bestLen) { bestLen = p[i]; bestStart = (i - 1 - p[i]) / 2; }
    }
    cout << bestLen << " " << bestStart + 1 << "\\n";
    return 0;
}
""",
    ),
    dict(
        id="distinct-substrings-count",
        title="How Many Different Snippets?",
        difficulty="expert",
        category="Strings",
        tags=["rolling-hash", "suffix-array", "lcp", "strings"],
        inspired_by="CSES 2105 Distinct Substrings / SPOJ DISUBSTR",
        statement="""
Count the **distinct** non-empty substrings of `s`. For `s = "abab"` the distinct
substrings are `a, b, ab, ba, aba, bab, abab` — 7 of them.

A string of length 2000 has about two million substrings with a total length of more
than a billion characters, so storing them as strings is not an option.
""",
        input_format="One line: the string `s` (lowercase letters, 1 ≤ |s| ≤ 2000).",
        output_format="One integer: the number of distinct non-empty substrings.",
        hints=[
            "**Rolling hash**: with prefix hashes `h[i] = (h[i−1]·B + s[i−1]) mod M`, the hash of `s[i..i+L)` is "
            "`h[i+L] − h[i]·B^L (mod M)` — O(1) per substring after O(n) preprocessing.",
            "For each length `L` collect the `n − L + 1` hashes, sort them and count the distinct values "
            "(or put them in a hash set). That is O(n² log n) integer work instead of O(n³) character work.",
            "Make collisions practically impossible with a large modulus such as `2⁶¹ − 1` "
            "(multiply with `__int128` in C++) or two independent moduli.",
            "Exact alternative (good for Python): sort all suffixes, then "
            "`answer = n(n+1)/2 − Σ LCP(adjacent suffixes in sorted order)`; Kasai's algorithm computes all LCPs in O(n).",
        ],
        samples=["abab", "aaa"],
        tests=["a", "ab", "abc", "zzzzzzzzzz"],
        gen=_gen_distinct,
        time_limit=4,
        starter_python="""s = input().strip()
n = len(s)
# TODO: count distinct substrings (rolling hash per length, or suffix sorting + LCP)
print(0)
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

typedef unsigned long long ull;

int main() {
    string s;
    cin >> s;
    int n = s.size();
    // TODO: count distinct substrings (rolling hash per length, or suffix sorting + LCP)
    cout << 0 << "\\n";
    return 0;
}
""",
        solution_python="""s = input().strip()
n = len(s)
sa = sorted(range(n), key=lambda i: s[i:])
rank = [0] * n
for r, i in enumerate(sa):
    rank[i] = r
# Kasai: LCP of each suffix with the previous one in sorted order
lcp_total = 0
h = 0
for i in range(n):
    r = rank[i]
    if r == 0:
        h = 0
        continue
    j = sa[r - 1]
    while i + h < n and j + h < n and s[i + h] == s[j + h]:
        h += 1
    lcp_total += h
    if h:
        h -= 1
print(n * (n + 1) // 2 - lcp_total)
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

typedef unsigned long long ull;
const ull MOD = (1ULL << 61) - 1;

ull mulmod(ull a, ull b) {
    unsigned __int128 p = (unsigned __int128)a * b;
    ull lo = (ull)(p & MOD), hi = (ull)(p >> 61);
    ull r = lo + hi;
    if (r >= MOD) r -= MOD;
    return r;
}

int main() {
    string s;
    cin >> s;
    int n = s.size();
    const ull B = 911382323ULL;
    vector<ull> h(n + 1, 0), pw(n + 1, 1);
    for (int i = 0; i < n; i++) {
        h[i + 1] = (mulmod(h[i], B) + (ull)(s[i] - 'a' + 1)) % MOD;
        pw[i + 1] = mulmod(pw[i], B);
    }
    long long total = 0;
    vector<ull> v;
    for (int L = 1; L <= n; L++) {
        v.clear();
        for (int i = 0; i + L <= n; i++) {
            ull x = (h[i + L] + MOD - mulmod(h[i], pw[L])) % MOD;
            v.push_back(x);
        }
        sort(v.begin(), v.end());
        total += unique(v.begin(), v.end()) - v.begin();
    }
    cout << total << "\\n";
    return 0;
}
""",
    ),
]
