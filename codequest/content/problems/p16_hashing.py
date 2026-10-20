"""Hashing: sets and dictionaries (Python) / unordered_set and unordered_map (C++)."""

import string

LOW = string.ascii_lowercase


def _case(a):
    return f"{len(a)}\n" + " ".join(map(str, a))


def _jewels_case(rng):
    letters = string.ascii_letters
    jewels = "".join(rng.sample(letters, rng.randint(1, 20)))
    pool = rng.choice([letters, "aAbBcCdD", jewels + "xyz"])
    stones = "".join(rng.choice(pool) for _ in range(rng.randint(1, 500)))
    return f"{jewels}\n{stones}"


def _dup_case(rng):
    n = rng.randint(1, 120)
    if rng.random() < 0.5:
        a = rng.sample(range(-10**9, 10**9), n)
    else:
        a = [rng.randint(-10**9, 10**9) for _ in range(n)]
        if n >= 2:
            a[rng.randrange(n)] = a[rng.randrange(n)]
    return _case(a)


def _pair_count(a, target):
    seen, cnt = {}, 0
    for x in a:
        cnt += seen.get(target - x, 0)
        seen[x] = seen.get(x, 0) + 1
    return cnt


def _two_sum_case(rng, n, lo=-10**9, hi=10**9):
    while True:
        a = [rng.randint(lo, hi) for _ in range(n)]
        i, j = rng.sample(range(n), 2)
        target = a[i] + a[j]
        if _pair_count(a, target) == 1:
            return f"{n} {target}\n" + " ".join(map(str, a))


def _unique_char_case(rng):
    n = rng.randint(1, 2000)
    alpha = LOW[:rng.randint(1, 26)]
    s = [rng.choice(alpha) for _ in range(n)]
    if rng.random() < 0.5 and n > 10:  # plant a unique letter late in a string without it
        s = [c if c != "z" else "a" for c in s]
        s[rng.randrange(n // 2, n)] = "z"
    return "".join(s)


def _majority_case(rng):
    n = rng.randint(1, 500)
    m = rng.randint(-10**9, 10**9)
    k = n // 2 + 1 + rng.randint(0, (n - 1) // 4)
    pool = [rng.randint(-10**9, 10**9) for _ in range(3)]
    a = [m] * k + [rng.choice(pool) for _ in range(n - k)]
    rng.shuffle(a)
    return _case(a)


def _words_case(rng):
    vocab = ["".join(rng.choice(LOW) for _ in range(rng.randint(1, 6))) for _ in range(rng.randint(1, 25))]
    n = rng.randint(1, 400)
    return _case([rng.choice(vocab) for _ in range(n)])


def _intersect_case(rng):
    hi = rng.choice([10, 100, 10**9])
    a = [rng.randint(-hi, hi) for _ in range(rng.randint(1, 150))]
    b = [rng.randint(-hi, hi) for _ in range(rng.randint(1, 150))]
    return _case(a) + "\n" + _case(b)


PROBLEMS = [
    dict(
        id="jewels-and-stones",
        title="Jewels and Stones",
        difficulty="beginner",
        category="Hashing",
        tags=["hashing", "set", "strings"],
        inspired_by="LeetCode #771 Jewels and Stones",
        statement="""
A string `J` lists the types of stone that are **jewels** (each character is
one type), and a string `S` lists the stones you own. How many of your stones
are jewels?

Letters are case-sensitive: `a` and `A` are different types.
""",
        input_format="First line: `J`, 1 to 52 distinct English letters. Second line: `S`, 1 to 1000 English letters.",
        output_format="A single integer: how many characters of `S` appear in `J`.",
        hints=[
            "For each stone you need a quick answer to \"is this a jewel?\" — that is exactly what a **set** is for.",
            "Python: `jewels = set(J)`, then `ch in jewels` is a fast membership test.",
            "C++: `unordered_set<char> jewels(J.begin(), J.end());` (from `<unordered_set>`) and "
            "`jewels.count(ch)` is 1 if present. A `bool isJewel[128]` array also works.",
        ],
        samples=["aA\naAAbbbb", "z\nZZ"],
        tests=["a\na", "abc\nabcabc", "Q\nqqqq", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\nHelloWorld"],
        gen=lambda rng: [_jewels_case(rng) for _ in range(4)],
        starter_python=r"""J = input().strip()
S = input().strip()
count = 0
# TODO: count the stones in S that are jewels
print(count)
""",
        starter_cpp=r"""#include <iostream>
#include <string>
#include <unordered_set>
using namespace std;

int main() {
    string J, S;
    cin >> J >> S;
    int count = 0;
    // TODO: count the stones in S that are jewels
    cout << count << "\n";
    return 0;
}
""",
        solution_python=r"""J = input().strip()
S = input().strip()
jewels = set(J)
print(sum(1 for ch in S if ch in jewels))
""",
        solution_cpp=r"""#include <iostream>
#include <string>
#include <unordered_set>
using namespace std;

int main() {
    string J, S;
    cin >> J >> S;
    unordered_set<char> jewels(J.begin(), J.end());
    int count = 0;
    for (char ch : S)
        if (jewels.count(ch)) count++;
    cout << count << "\n";
    return 0;
}
""",
    ),
    dict(
        id="contains-duplicate",
        title="Any Duplicates?",
        difficulty="easy",
        category="Hashing",
        tags=["hashing", "set", "duplicates"],
        inspired_by="LeetCode #217 Contains Duplicate",
        statement="""
For each list of numbers, decide whether **some value appears at least
twice**.
""",
        input_format="First line: `t` (1 ≤ t ≤ 20). Each test case has two lines: `n` (1 ≤ n ≤ 1000), then `n` "
                     "integers (−10⁹ ≤ aᵢ ≤ 10⁹).",
        output_format="For each test case print `YES` if there is a duplicate and `NO` otherwise.",
        hints=[
            "Comparing every pair is O(n²). A set lets you remember what you've seen in O(1) per element.",
            "Walk through the list: if the current value is already in the set you found a duplicate; otherwise add it.",
            "Python one-liner idea: a set drops duplicates, so compare `len(set(a))` with `len(a)`. "
            "C++: `unordered_set<long long>`; `insert(x).second` is `false` when x was already there.",
        ],
        samples=["3\n4\n1 2 3 1\n4\n1 2 3 4\n1\n7"],
        tests=["1\n2\n5 5", "1\n2\n-5 5", "1\n3\n1000000000 -1000000000 1000000000",
               "2\n5\n0 0 0 0 0\n6\n-1 -2 -3 -4 -5 -6"],
        gen=lambda rng: ["\n".join(["8"] + [_dup_case(rng) for _ in range(8)]) for _ in range(3)],
        starter_python=r"""t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    # TODO: print YES if a contains a duplicate, otherwise NO
""",
        starter_cpp=r"""#include <iostream>
#include <vector>
#include <unordered_set>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<long long> a(n);
        for (auto &x : a) cin >> x;
        // TODO: print YES if a contains a duplicate, otherwise NO
    }
    return 0;
}
""",
        solution_python=r"""t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print("YES" if len(set(a)) < len(a) else "NO")
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <unordered_set>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<long long> a(n);
        for (auto &x : a) cin >> x;
        unordered_set<long long> seen;
        bool dup = false;
        for (long long x : a)
            if (!seen.insert(x).second) dup = true;
        cout << (dup ? "YES" : "NO") << "\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="two-sum-indices",
        title="Two Sum",
        difficulty="easy",
        category="Hashing",
        tags=["hashing", "dictionary", "complement"],
        inspired_by="LeetCode #1 Two Sum",
        statement="""
Find two **different positions** `i < j` in the array whose values add up to
the given `target`. Positions are numbered from 1.

The input is chosen so that **exactly one** such pair of positions exists.
""",
        input_format="First line: `n` and `target` (2 ≤ n ≤ 10⁴, −2·10⁹ ≤ target ≤ 2·10⁹). Second line: `n` integers "
                     "(−10⁹ ≤ aᵢ ≤ 10⁹).",
        output_format="Two integers `i j` (1-based, `i < j`) with `aᵢ + aⱼ = target`.",
        hints=[
            "Brute force checks all pairs — O(n²). The trick: for each element x you are really asking "
            "\"have I already seen `target − x`?\"",
            "Use a dictionary from value to position. Python: `pos = {}` and `pos[x] = i`; "
            "C++: `unordered_map<long long, int> pos;` from `<unordered_map>`.",
            "Look up the complement **before** inserting the current element, so an element is never paired with itself.",
            "C++: `target` can be ±2·10⁹, which does not fit in `int` — use `long long`.",
        ],
        samples=["4 9\n2 7 11 15", "3 6\n3 2 4"],
        tests=["2 6\n3 3", "2 -2000000000\n-1000000000 -1000000000", "2 2000000000\n1000000000 1000000000",
               "5 0\n-3 1 2 4 3", "4 10\n1 2 3 7"],
        gen=lambda rng: [_two_sum_case(rng, rng.randint(2, 400)) for _ in range(3)]
        + [_two_sum_case(rng, 20, -100, 100) for _ in range(2)],
        starter_python=r"""n, target = map(int, input().split())
a = list(map(int, input().split()))
# TODO: find positions i < j (1-based) with a[i] + a[j] == target and print them
""",
        starter_cpp=r"""#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;

int main() {
    int n;
    long long target;
    cin >> n >> target;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    // TODO: find positions i < j (1-based) with a[i] + a[j] == target and print them
    return 0;
}
""",
        solution_python=r"""n, target = map(int, input().split())
a = list(map(int, input().split()))
pos = {}
for j, x in enumerate(a):
    if target - x in pos:
        print(pos[target - x] + 1, j + 1)
        break
    pos[x] = j
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;

int main() {
    int n;
    long long target;
    cin >> n >> target;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    unordered_map<long long, int> pos;
    for (int j = 0; j < n; j++) {
        auto it = pos.find(target - a[j]);
        if (it != pos.end()) {
            cout << it->second + 1 << " " << j + 1 << "\n";
            return 0;
        }
        pos[a[j]] = j;
    }
    return 0;
}
""",
    ),
    dict(
        id="first-unique-character",
        title="First Unique Character",
        difficulty="easy",
        category="Hashing",
        tags=["hashing", "counting", "strings"],
        inspired_by="LeetCode #387 First Unique Character in a String",
        statement="""
Find the first character in the string that occurs **exactly once**, and
print its position (positions are numbered from 1). If every character
repeats, print `-1`.

In `swiss` only `w` and `i` occur once; `w` comes first, at position `2`.
In `aabbc` the answer is `5`, and in `abab` it is `-1`.
""",
        input_format="One line: a string of 1 to 2000 lowercase letters.",
        output_format="The 1-based position of the first non-repeating character, or `-1`.",
        hints=[
            "Two passes: first count how often each letter occurs, then scan again and stop at the first letter with count 1.",
            "Python: `collections.Counter(s)` counts everything at once. C++: `int cnt[26] = {0};` and `cnt[c - 'a']++`.",
        ],
        samples=["swiss", "aabbc", "abab"],
        tests=["a", "aa", "z" * 1999 + "y", "abcabcd", "leetcode"],
        gen=lambda rng: [_unique_char_case(rng) for _ in range(5)],
        starter_python=r"""s = input().strip()
# TODO: print the 1-based position of the first character that occurs once, or -1
""",
        starter_cpp=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    string s;
    cin >> s;
    // TODO: print the 1-based position of the first character that occurs once, or -1
    return 0;
}
""",
        solution_python=r"""from collections import Counter

s = input().strip()
cnt = Counter(s)
ans = -1
for i, ch in enumerate(s):
    if cnt[ch] == 1:
        ans = i + 1
        break
print(ans)
""",
        solution_cpp=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    string s;
    cin >> s;
    int cnt[26] = {0};
    for (char c : s) cnt[c - 'a']++;
    int ans = -1;
    for (size_t i = 0; i < s.size(); i++) {
        if (cnt[s[i] - 'a'] == 1) { ans = (int)i + 1; break; }
    }
    cout << ans << "\n";
    return 0;
}
""",
    ),
    dict(
        id="majority-element",
        title="Majority Vote",
        difficulty="easy",
        category="Hashing",
        tags=["hashing", "counting", "boyer-moore"],
        inspired_by="LeetCode #169 Majority Element",
        statement="""
In an election every vote is a candidate number. One candidate received
**more than half** of all votes — find them.
""",
        input_format="First line: `n` (1 ≤ n ≤ 1000). Second line: `n` integers (−10⁹ ≤ aᵢ ≤ 10⁹). "
                     "It is guaranteed that some value occurs more than `n / 2` times.",
        output_format="The value that occurs more than `n / 2` times.",
        hints=[
            "Count the votes of every candidate with a dictionary (`dict` / `unordered_map`), then pick the one with the largest count.",
            "Python: `collections.Counter(a).most_common(1)` returns `[(value, count)]`.",
            "Bonus (no extra memory): Boyer–Moore voting — keep a candidate and a counter; equal votes add 1, "
            "different ones subtract 1, and when the counter hits 0 the next vote becomes the candidate.",
        ],
        samples=["3\n3 2 3", "7\n2 2 1 1 1 2 2"],
        tests=["1\n-1000000000", "2\n5 5", "5\n0 1 0 1 0", "6\n-7 -7 -7 -7 3 3"],
        gen=lambda rng: [_majority_case(rng) for _ in range(5)],
        starter_python=r"""n = int(input())
a = list(map(int, input().split()))
# TODO: print the value that occurs more than n / 2 times
""",
        starter_cpp=r"""#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    // TODO: print the value that occurs more than n / 2 times
    return 0;
}
""",
        solution_python=r"""from collections import Counter

n = int(input())
a = list(map(int, input().split()))
print(Counter(a).most_common(1)[0][0])
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    long long cand = 0;
    int cnt = 0;
    for (long long x : a) {
        if (cnt == 0) { cand = x; cnt = 1; }
        else if (x == cand) cnt++;
        else cnt--;
    }
    cout << cand << "\n";
    return 0;
}
""",
    ),
    dict(
        id="most-frequent-word",
        title="Most Frequent Word",
        difficulty="easy",
        category="Hashing",
        tags=["hashing", "dictionary", "counting", "tie-break"],
        inspired_by="Word-count classics (LeetCode #819 Most Common Word, simplified)",
        statement="""
Given a list of words, find the word that occurs **most often** and how many
times it occurs. If several words share the highest count, choose the one that
comes first in **alphabetical (lexicographic) order**.
""",
        input_format="First line: `n` (1 ≤ n ≤ 1000). Second line: `n` words separated by spaces, each of 1 to 10 "
                     "lowercase letters.",
        output_format="The chosen word and its count, separated by a space.",
        hints=[
            "Count with a dictionary: Python `cnt[w] = cnt.get(w, 0) + 1`; C++ `unordered_map<string, int> cnt; cnt[w]++;`.",
            "Then scan all (word, count) pairs and keep the best: higher count wins; equal count → smaller word wins.",
            "Strings compare alphabetically with `<` in both Python and C++. "
            "C++ alternative: a `map<string, int>` (from `<map>`) iterates in alphabetical order already.",
        ],
        samples=["6\nthe cat and the hat the", "4\nbanana apple banana apple"],
        tests=["1\nsolo", "3\nc b a", "5\nzz zz zz y y", "4\nab a ab a"],
        gen=lambda rng: [_words_case(rng) for _ in range(5)],
        starter_python=r"""n = int(input())
words = input().split()
# TODO: print the most frequent word (alphabetically first on ties) and its count
""",
        starter_cpp=r"""#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<string> words(n);
    for (auto &w : words) cin >> w;
    // TODO: print the most frequent word (alphabetically first on ties) and its count
    return 0;
}
""",
        solution_python=r"""n = int(input())
words = input().split()
cnt = {}
for w in words:
    cnt[w] = cnt.get(w, 0) + 1
best = min(cnt, key=lambda w: (-cnt[w], w))
print(best, cnt[best])
""",
        solution_cpp=r"""#include <iostream>
#include <string>
#include <vector>
#include <unordered_map>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<string> words(n);
    for (auto &w : words) cin >> w;
    unordered_map<string, int> cnt;
    for (auto &w : words) cnt[w]++;
    string best;
    int bc = 0;
    for (auto &kv : cnt) {
        if (kv.second > bc || (kv.second == bc && kv.first < best)) {
            best = kv.first;
            bc = kv.second;
        }
    }
    cout << best << " " << bc << "\n";
    return 0;
}
""",
    ),
    dict(
        id="array-intersection-distinct",
        title="Common Values",
        difficulty="easy",
        category="Hashing",
        tags=["hashing", "set", "intersection", "sorting"],
        inspired_by="LeetCode #349 Intersection of Two Arrays",
        statement="""
Given two lists of integers, print every value that appears in **both**
lists. Print each such value **once**, in increasing order. If there are none,
print `NONE`.
""",
        input_format="Line 1: `n` (1 ≤ n ≤ 1000). Line 2: `n` integers. Line 3: `m` (1 ≤ m ≤ 1000). Line 4: `m` integers. "
                     "All values satisfy −10⁹ ≤ value ≤ 10⁹.",
        output_format="The common values in increasing order separated by spaces, or `NONE`.",
        hints=[
            "Put the first list into a set; then a value of the second list is common if it is in that set.",
            "Python: sets support `&` for intersection: `set(a) & set(b)`. Then `sorted(...)`.",
            "C++: fill an `unordered_set` from the first list, collect matches from the second into a `set<long long>` "
            "(from `<set>`) — it removes duplicates and keeps them sorted.",
        ],
        samples=["4\n1 2 2 1\n2\n2 2", "3\n4 9 5\n5\n9 4 9 8 4", "2\n1 2\n2\n3 4"],
        tests=["1\n5\n1\n5", "1\n5\n1\n-5", "3\n-1000000000 0 1000000000\n3\n1000000000 0 -1000000000",
               "5\n3 3 3 3 3\n4\n3 3 1 1"],
        gen=lambda rng: [_intersect_case(rng) for _ in range(5)],
        starter_python=r"""n = int(input())
a = list(map(int, input().split()))
m = int(input())
b = list(map(int, input().split()))
# TODO: print the distinct common values in increasing order, or NONE
""",
        starter_cpp=r"""#include <iostream>
#include <vector>
#include <set>
#include <unordered_set>
using namespace std;

int main() {
    int n, m;
    cin >> n;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    cin >> m;
    vector<long long> b(m);
    for (auto &x : b) cin >> x;
    // TODO: print the distinct common values in increasing order, or NONE
    return 0;
}
""",
        solution_python=r"""n = int(input())
a = list(map(int, input().split()))
m = int(input())
b = list(map(int, input().split()))
common = sorted(set(a) & set(b))
print(*common if common else ["NONE"])
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <set>
#include <unordered_set>
using namespace std;

int main() {
    int n, m;
    cin >> n;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    cin >> m;
    vector<long long> b(m);
    for (auto &x : b) cin >> x;
    unordered_set<long long> inA(a.begin(), a.end());
    set<long long> common;
    for (long long x : b)
        if (inA.count(x)) common.insert(x);
    if (common.empty()) {
        cout << "NONE\n";
        return 0;
    }
    bool first = true;
    for (long long x : common) {
        if (!first) cout << " ";
        cout << x;
        first = false;
    }
    cout << "\n";
    return 0;
}
""",
    ),
]
