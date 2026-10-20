"""Strings, part 2: classic interview string problems."""

import string

LOW = string.ascii_lowercase


def _word(rng, lo, hi, alpha=LOW):
    return "".join(rng.choice(alpha) for _ in range(rng.randint(lo, hi)))


def _text(rng, n):
    alpha = string.ascii_letters + string.digits + "     .,!?'-"
    return ("".join(rng.choice(alpha) for _ in range(n)).strip() or "Z")


def _rle_string(rng):
    parts = []
    letters = rng.choice(["ab", "abc", LOW])
    for _ in range(rng.randint(1, 60)):
        parts.append(rng.choice(letters) * rng.choice([1, 1, 2, 3, rng.randint(1, 30)]))
    return "".join(parts)


def _lcp_case(rng):
    n = rng.randint(1, 30)
    base = _word(rng, 0, 12, "ab" if rng.random() < 0.5 else LOW)
    words = []
    for _ in range(n):
        cut = rng.randint(max(0, len(base) - 3), len(base)) if rng.random() < 0.9 else rng.randint(0, len(base))
        w = base[:cut] + _word(rng, 0, 6, "ab")
        words.append(w or "a")
    return f"{n}\n" + "\n".join(words)


def _bracket_case(rng):
    pairs = ["()", "[]", "{}"]
    kind = rng.randrange(3)
    if kind == 0 or kind == 1:  # build a valid one, maybe corrupt it
        out, stack = [], []
        for _ in range(rng.randint(1, 60)):
            if stack and rng.random() < 0.5:
                out.append(stack.pop())
            else:
                o, c = rng.choice(pairs)
                out.append(o)
                stack.append(c)
        out += stack[::-1]
        if kind == 1:
            i = rng.randrange(len(out))
            out[i] = rng.choice("()[]{}".replace(out[i], ""))
        return "".join(out)
    return "".join(rng.choice("()[]{}") for _ in range(rng.randint(1, 40)))


PROBLEMS = [
    dict(
        id="caesar-cipher",
        title="Caesar Cipher",
        difficulty="easy",
        category="Strings",
        tags=["strings", "modulo", "ascii", "cipher"],
        inspired_by="HackerRank 'Caesar Cipher'",
        statement="""
Julius Caesar hid his messages by shifting every letter a fixed number of
places along the alphabet, wrapping around at the end. With a shift of 3,
`a → d`, `x → a`, `Z → C`.

Encrypt a message with shift `k`:

* lowercase letters stay lowercase and uppercase letters stay uppercase,
* every other character (digits, spaces, punctuation) is unchanged,
* `k` may be **negative** (shift backwards) or much larger than 26.
""",
        input_format="First line: the shift `k` (−10⁹ ≤ k ≤ 10⁹). Second line: the message, 1 to 1000 characters "
                     "of letters, digits, spaces and the punctuation `.,!?'-`.",
        output_format="The encrypted message on one line.",
        hints=[
            "Letters are numbers underneath: Python `ord('c') - ord('a')` is 2 and `chr(ord('a') + 2)` is `'c'`. "
            "In C++ `c - 'a'` and `char('a' + 2)` do the same.",
            "Wrap around with the remainder: new position = (old position + k) mod 26.",
            "Python's `%` always returns a non-negative result for a positive modulus, but C++'s does not "
            "(`-1 % 26 == -1`). In C++ first reduce `k = ((k % 26) + 26) % 26`.",
        ],
        samples=["3\nHello, World!", "-1\nabc xyz"],
        tests=["0\nUnchanged 123", "26\nfull circle", "-1000000000\nAbc Xyz", "1000000000\nThe quick brown fox.",
               "25\nzZ aA"],
        gen=lambda rng: [f"{rng.randint(-10**9, 10**9)}\n{_text(rng, rng.randint(20, 300))}" for _ in range(3)]
        + [f"{rng.randint(-30, 30)}\n{_text(rng, 50)}" for _ in range(2)],
        starter_python=r"""k = int(input())
s = input()
result = ""
# TODO: shift every letter of s by k places (keep case, leave other characters alone)
print(result)
""",
        starter_cpp=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    long long k;
    cin >> k;
    string s;
    getline(cin, s);  // finish the line containing k
    getline(cin, s);  // the message, spaces included
    // TODO: shift every letter of s by k places (keep case, leave other characters alone)
    return 0;
}
""",
        solution_python=r"""k = int(input())
s = input()
out = []
for ch in s:
    if "a" <= ch <= "z":
        out.append(chr((ord(ch) - 97 + k) % 26 + 97))
    elif "A" <= ch <= "Z":
        out.append(chr((ord(ch) - 65 + k) % 26 + 65))
    else:
        out.append(ch)
print("".join(out))
""",
        solution_cpp=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    long long k;
    cin >> k;
    string s;
    getline(cin, s);
    getline(cin, s);
    int sh = (int)(((k % 26) + 26) % 26);
    for (char &ch : s) {
        if (ch >= 'a' && ch <= 'z') ch = char('a' + (ch - 'a' + sh) % 26);
        else if (ch >= 'A' && ch <= 'Z') ch = char('A' + (ch - 'A' + sh) % 26);
    }
    cout << s << "\n";
    return 0;
}
""",
    ),
    dict(
        id="run-length-encoding",
        title="Run-Length Encoding",
        difficulty="easy",
        category="Strings",
        tags=["strings", "compression", "loops"],
        inspired_by="Classic compression exercise (LeetCode #443 String Compression theme)",
        statement="""
**Run-length encoding** compresses a string by replacing every maximal run of
equal characters with the character followed by the length of the run.

`aaabccdddd` → `a3b1c2d4`

Note that runs of length 1 still get their count, and a letter can appear in
several separate runs: `aabaa` → `a2b1a2`.
""",
        input_format="One line: a string `s` of 1 to 2000 lowercase letters.",
        output_format="The encoded string on one line.",
        hints=[
            "Walk through the string while remembering the current character and how many times in a row you have seen it.",
            "When the next character differs (or the string ends), output the current character and its count, then start a new run.",
            "Python: `str(count)` turns a number into text; C++: `to_string(count)` (from `<string>`) does the same.",
        ],
        samples=["aaabccdddd", "aabaa"],
        tests=["a", "z" * 2000, "abcdefghijklmnopqrstuvwxyz", "aaaaaaaaaab", "abababab"],
        gen=lambda rng: [_rle_string(rng) for _ in range(5)],
        starter_python=r"""s = input().strip()
result = ""
# TODO: build the run-length encoding of s
print(result)
""",
        starter_cpp=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    string s;
    cin >> s;
    string result;
    // TODO: build the run-length encoding of s
    cout << result << "\n";
    return 0;
}
""",
        solution_python=r"""s = input().strip()
out = []
i = 0
while i < len(s):
    j = i
    while j < len(s) and s[j] == s[i]:
        j += 1
    out.append(s[i] + str(j - i))
    i = j
print("".join(out))
""",
        solution_cpp=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    string s;
    cin >> s;
    string result;
    size_t i = 0;
    while (i < s.size()) {
        size_t j = i;
        while (j < s.size() && s[j] == s[i]) j++;
        result += s[i];
        result += to_string(j - i);
        i = j;
    }
    cout << result << "\n";
    return 0;
}
""",
    ),
    dict(
        id="longest-common-prefix",
        title="Longest Common Prefix",
        difficulty="easy",
        category="Strings",
        tags=["strings", "prefix", "loops"],
        inspired_by="LeetCode #14 Longest Common Prefix",
        statement="""
Given a list of words, find the longest string that **all** of them start
with.

For `flower`, `flow`, `flight` the answer is `fl`. For `dog`, `car` there is no
common prefix at all — print `NONE` in that case.
""",
        input_format="First line: `n` (1 ≤ n ≤ 100). Then `n` lines, each with one word of 1 to 100 lowercase letters.",
        output_format="The longest common prefix, or `NONE` if it is empty.",
        hints=[
            "The prefix can never be longer than the shortest word.",
            "Idea: take the first word as a candidate prefix; for each other word, chop the candidate's last letter "
            "until the word starts with it. Python: `w.startswith(p)`; C++: `w.compare(0, p.size(), p) == 0`.",
            "Another idea: check position 0, 1, 2, … and stop at the first index where some word is too short "
            "or has a different letter there.",
        ],
        samples=["3\nflower\nflow\nflight", "2\ndog\ncar"],
        tests=["1\nalone", "2\nsame\nsame", "3\nabc\nab\na", "2\nab\nb", "3\nprefix\nprefixes\npre"],
        gen=lambda rng: [_lcp_case(rng) for _ in range(5)],
        starter_python=r"""n = int(input())
words = [input().strip() for _ in range(n)]
prefix = ""
# TODO: find the longest common prefix of all words
print(prefix if prefix else "NONE")
""",
        starter_cpp=r"""#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<string> words(n);
    for (auto &w : words) cin >> w;
    string prefix;
    // TODO: find the longest common prefix of all words
    cout << (prefix.empty() ? "NONE" : prefix) << "\n";
    return 0;
}
""",
        solution_python=r"""n = int(input())
words = [input().strip() for _ in range(n)]
prefix = words[0]
for w in words[1:]:
    while not w.startswith(prefix):
        prefix = prefix[:-1]
print(prefix if prefix else "NONE")
""",
        solution_cpp=r"""#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<string> words(n);
    for (auto &w : words) cin >> w;
    size_t len = words[0].size();
    for (int i = 1; i < n; i++) {
        size_t k = 0;
        while (k < len && k < words[i].size() && words[i][k] == words[0][k]) k++;
        len = k;
    }
    string prefix = words[0].substr(0, len);
    cout << (prefix.empty() ? "NONE" : prefix) << "\n";
    return 0;
}
""",
    ),
    dict(
        id="valid-parentheses",
        title="Balanced Brackets",
        difficulty="easy",
        category="Strings",
        tags=["strings", "stack", "brackets"],
        inspired_by="LeetCode #20 Valid Parentheses",
        statement="""
A string made of the brackets `()`, `[]` and `{}` is **balanced** when every
opening bracket is closed by a bracket of the same type, and they close in the
correct order.

* `([]{})` and `{[()]}` are balanced,
* `(]` is not (wrong type), `([)]` is not (wrong order), `((` is not (never closed),
  and `)(` is not (closed before opened).
""",
        input_format="First line: `t` (1 ≤ t ≤ 100). Then `t` lines, each a string of 1 to 200 characters from `()[]{}`.",
        output_format="For each string print `YES` if it is balanced and `NO` otherwise.",
        hints=[
            "Use a **stack**: push every opening bracket; when you meet a closing one, the top of the stack must be its partner.",
            "Python: a list is a stack — `st.append(c)`, `st[-1]`, `st.pop()`. C++: `std::stack<char>` from `<stack>` "
            "or a `string` with `push_back` / `back` / `pop_back`.",
            "Two easy-to-miss cases: a closing bracket when the stack is empty, and a stack that is not empty when the string ends.",
        ],
        samples=["4\n([]{})\n(]\n([)]\n{[()]}"],
        tests=["1\n(", "1\n)", "2\n()\n)(", "1\n" + "(" * 100 + ")" * 100, "1\n" + "[]" * 100,
               "3\n{{}}\n{{}\n}}{{"],
        gen=lambda rng: ["40\n" + "\n".join(_bracket_case(rng) for _ in range(40)) for _ in range(2)],
        starter_python=r"""t = int(input())
for _ in range(t):
    s = input().strip()
    # TODO: print YES if s is balanced, otherwise NO
""",
        starter_cpp=r"""#include <iostream>
#include <string>
#include <stack>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        string s;
        cin >> s;
        // TODO: print YES if s is balanced, otherwise NO
    }
    return 0;
}
""",
        solution_python=r"""match = {")": "(", "]": "[", "}": "{"}
t = int(input())
for _ in range(t):
    s = input().strip()
    st = []
    ok = True
    for c in s:
        if c in "([{":
            st.append(c)
        elif not st or st.pop() != match[c]:
            ok = False
            break
    print("YES" if ok and not st else "NO")
""",
        solution_cpp=r"""#include <iostream>
#include <string>
#include <stack>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        string s;
        cin >> s;
        stack<char> st;
        bool ok = true;
        for (char c : s) {
            if (c == '(' || c == '[' || c == '{') {
                st.push(c);
            } else {
                char want = (c == ')') ? '(' : (c == ']') ? '[' : '{';
                if (st.empty() || st.top() != want) { ok = false; break; }
                st.pop();
            }
        }
        cout << (ok && st.empty() ? "YES" : "NO") << "\n";
    }
    return 0;
}
""",
    ),
]
