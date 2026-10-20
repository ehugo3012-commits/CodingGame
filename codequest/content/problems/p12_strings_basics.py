"""Strings, part 1: characters, case, palindromes, words, anagrams."""

import string

LOW = string.ascii_lowercase


def _word(rng, lo, hi, alpha=LOW):
    return "".join(rng.choice(alpha) for _ in range(rng.randint(lo, hi)))


def _palin_case(rng):
    half = _word(rng, 0, 30, "abc" if rng.random() < 0.5 else LOW)
    kind = rng.randrange(3)
    if kind == 0:
        w = half + half[::-1]
    elif kind == 1:
        w = half + rng.choice(LOW) + half[::-1]
    else:
        w = _word(rng, 1, 60, "ab")
    return w or "a"


def _sentence(rng, words, alpha=string.ascii_letters):
    return " ".join(_word(rng, 1, 10, alpha) for _ in range(words))


def _anagram_case(rng):
    a = _word(rng, 1, 40, "abcde" if rng.random() < 0.6 else LOW)
    kind = rng.randrange(3)
    if kind == 0:
        b = "".join(rng.sample(a, len(a)))
    elif kind == 1:  # same length, one letter changed
        b = list(rng.sample(a, len(a)))
        i = rng.randrange(len(b))
        b[i] = LOW[(LOW.index(b[i]) + 1) % 26]
        b = "".join(b)
    else:
        b = _word(rng, 1, 40, "abcde")
    return f"{a} {b}"


PROBLEMS = [
    dict(
        id="count-vowels",
        title="Count the Vowels",
        difficulty="beginner",
        category="Strings",
        tags=["strings", "loops", "characters"],
        inspired_by="Classic string exercise (Codewars 'Vowel Count')",
        statement="""
For each line of text, count how many of its letters are vowels. The vowels
are `a`, `e`, `i`, `o`, `u` — in **either case** (`A` counts too). The letter
`y` is not a vowel here.
""",
        input_format="First line: `t` (1 ≤ t ≤ 50). Then `t` lines, each a sentence of 1 to 200 characters "
                     "made of English letters and single spaces (no leading/trailing spaces).",
        output_format="For each sentence print the number of vowels on its own line.",
        hints=[
            "Loop over the characters of the string: Python `for ch in s:`; C++ `for (char ch : s)`.",
            "Turn each character into lowercase first so you only check five letters: Python `ch.lower()`, "
            "C++ `tolower(ch)` from `<cctype>`.",
            "Python: `ch in \"aeiou\"` tests membership. C++: compare against each vowel, or use "
            "`string(\"aeiou\").find(c) != string::npos`.",
        ],
        samples=["2\nHello World\nA quick brown fox"],
        tests=["1\nrhythm", "1\nAEIOU aeiou", "1\nY", "3\nb\nE\nxyz XYZ"],
        gen=lambda rng: ["15\n" + "\n".join(_sentence(rng, rng.randint(1, 18)) for _ in range(15))
                         for _ in range(2)],
        starter_python=r"""t = int(input())
for _ in range(t):
    s = input()
    count = 0
    # TODO: count the vowels in s
    print(count)
""",
        starter_cpp=r"""#include <iostream>
#include <string>
#include <cctype>
using namespace std;

int main() {
    int t;
    cin >> t;
    string s;
    getline(cin, s);  // finish the line containing t
    while (t--) {
        getline(cin, s);  // read a whole line, spaces included
        int count = 0;
        // TODO: count the vowels in s
        cout << count << "\n";
    }
    return 0;
}
""",
        solution_python=r"""t = int(input())
for _ in range(t):
    s = input()
    print(sum(1 for ch in s.lower() if ch in "aeiou"))
""",
        solution_cpp=r"""#include <iostream>
#include <string>
#include <cctype>
using namespace std;

int main() {
    int t;
    cin >> t;
    string s;
    getline(cin, s);
    while (t--) {
        getline(cin, s);
        int count = 0;
        for (char ch : s) {
            char c = (char)tolower((unsigned char)ch);
            if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') count++;
        }
        cout << count << "\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="palindrome-word",
        title="Palindrome Words",
        difficulty="beginner",
        category="Strings",
        tags=["strings", "palindrome", "reversal"],
        inspired_by="Classic exercise (LeetCode #125 Valid Palindrome, simplified)",
        statement="""
A word is a **palindrome** if it reads the same forwards and backwards, like
`level` or `noon`. Single letters are palindromes too.

Decide for each word whether it is a palindrome.
""",
        input_format="First line: `t` (1 ≤ t ≤ 100). Then `t` lines, each with one word of 1 to 100 lowercase letters.",
        output_format="For each word print `YES` if it is a palindrome and `NO` otherwise.",
        hints=[
            "Compare the word with its reverse. Python: `s[::-1]` reverses a string.",
            "C++: `string(s.rbegin(), s.rend())` is the reverse of `s`.",
            "Alternative without building a new string: compare `s[i]` with `s[n - 1 - i]` for every i in the first half.",
        ],
        samples=["3\nlevel\nhello\na"],
        tests=["1\nab", "1\naa", "2\nabba\nabca", "1\n" + "ab" * 50, "1\n" + "z" * 100],
        gen=lambda rng: ["30\n" + "\n".join(_palin_case(rng) for _ in range(30)) for _ in range(2)],
        starter_python=r"""t = int(input())
for _ in range(t):
    s = input().strip()
    # TODO: print YES if s is a palindrome, otherwise NO
""",
        starter_cpp=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        string s;
        cin >> s;
        // TODO: print YES if s is a palindrome, otherwise NO
    }
    return 0;
}
""",
        solution_python=r"""t = int(input())
for _ in range(t):
    s = input().strip()
    print("YES" if s == s[::-1] else "NO")
""",
        solution_cpp=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        string s;
        cin >> s;
        cout << (s == string(s.rbegin(), s.rend()) ? "YES" : "NO") << "\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="swap-case",
        title="Swap the Case",
        difficulty="beginner",
        category="Strings",
        tags=["strings", "characters", "ascii"],
        inspired_by="HackerRank 'sWAP cASE'",
        statement="""
Your friend typed a message with Caps Lock accidentally on. Fix it by turning
every lowercase letter into uppercase and every uppercase letter into
lowercase. Digits and punctuation stay as they are.
""",
        input_format="One line of 1 to 1000 characters: letters, digits, spaces and the punctuation `.,!?-`.",
        output_format="The same line with the case of every letter swapped.",
        hints=[
            "Read the whole line, spaces included: Python `input()`; C++ `getline(cin, s)`.",
            "Python strings have `.isupper()`, `.lower()` and `.upper()`. (There is even a built-in `.swapcase()`, "
            "but try it by hand first!)",
            "C++ `<cctype>` has `isupper(c)`, `islower(c)`, `toupper(c)` and `tolower(c)`. You can change "
            "`s[i]` in place.",
        ],
        samples=["hELLO wORLD!", "CodeQuest 2024 rocks"],
        tests=["a", "Z", "12345 ?!", "aBcDeFgHiJ - KlMnOp."],
        gen=lambda rng: ["".join(rng.choice(string.ascii_letters + string.digits + "   .,!?-")
                                 for _ in range(rng.randint(50, 300))).strip() or "x" for _ in range(3)],
        starter_python=r"""s = input()
result = ""
# TODO: build result by swapping the case of every letter in s
print(result)
""",
        starter_cpp=r"""#include <iostream>
#include <string>
#include <cctype>
using namespace std;

int main() {
    string s;
    getline(cin, s);
    // TODO: swap the case of every letter in s
    return 0;
}
""",
        solution_python=r"""s = input()
out = []
for ch in s:
    if ch.isupper():
        out.append(ch.lower())
    elif ch.islower():
        out.append(ch.upper())
    else:
        out.append(ch)
print("".join(out))
""",
        solution_cpp=r"""#include <iostream>
#include <string>
#include <cctype>
using namespace std;

int main() {
    string s;
    getline(cin, s);
    for (char &ch : s) {
        unsigned char c = (unsigned char)ch;
        if (isupper(c)) ch = (char)tolower(c);
        else if (islower(c)) ch = (char)toupper(c);
    }
    cout << s << "\n";
    return 0;
}
""",
    ),
    dict(
        id="reverse-words",
        title="Reverse the Words",
        difficulty="easy",
        category="Strings",
        tags=["strings", "split", "join"],
        inspired_by="LeetCode #151 Reverse Words in a String",
        statement="""
Given a sentence, print its words in **reverse order**. The words themselves
are not changed — only their order.

`the sky is blue` becomes `blue is sky the`.

Words are separated by one or more spaces; in your output separate them by a
single space.
""",
        input_format="One line of 1 to 2000 characters containing at least one word. A word is a maximal run of "
                     "letters and digits; words are separated by one or more spaces, "
                     "and there may be extra spaces at the start or end.",
        output_format="The words in reverse order, separated by single spaces, on one line.",
        hints=[
            "Python: `s.split()` (with no argument) splits on any run of spaces and drops empty pieces.",
            "Reverse a list with `words[::-1]` or `reversed(words)`, then glue with `\" \".join(...)`.",
            "C++: `cin >> w` skips spaces automatically — read words in a loop `while (cin >> w)` into a "
            "`vector<string>`, then print it backwards.",
        ],
        samples=["the sky is blue", "  hello    world  "],
        tests=["single", "a b", "1 2 3 4 5 6 7 8 9 10", "x  y   z"],
        gen=lambda rng: [" " * rng.randint(0, 2) + "".join(
            _word(rng, 1, 8, LOW + "0123456789") + " " * rng.randint(1, 3)
            for _ in range(rng.randint(5, 150))).rstrip() for _ in range(3)],
        starter_python=r"""s = input()
# TODO: print the words of s in reverse order
""",
        starter_cpp=r"""#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    vector<string> words;
    string w;
    while (cin >> w) words.push_back(w);
    // TODO: print the words in reverse order, separated by single spaces
    return 0;
}
""",
        solution_python=r"""print(" ".join(input().split()[::-1]))
""",
        solution_cpp=r"""#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    vector<string> words;
    string w;
    while (cin >> w) words.push_back(w);
    for (int i = (int)words.size() - 1; i >= 0; i--) {
        cout << words[i] << (i > 0 ? " " : "\n");
    }
    return 0;
}
""",
    ),
    dict(
        id="anagram-check",
        title="Anagram Check",
        difficulty="easy",
        category="Strings",
        tags=["strings", "sorting", "counting"],
        inspired_by="LeetCode #242 Valid Anagram",
        statement="""
Two words are **anagrams** if one can be rearranged to form the other, using
every letter exactly once. `listen` and `silent` are anagrams; `apple` and
`paple` are too; `rat` and `car` are not.

Check several pairs of words.
""",
        input_format="First line: `t` (1 ≤ t ≤ 100). Then `t` lines, each with two words `a b` "
                     "(1 to 100 lowercase letters each).",
        output_format="For each pair print `YES` if they are anagrams and `NO` otherwise.",
        hints=[
            "If the lengths differ, the answer is certainly NO.",
            "Idea 1: sort the letters of both words and compare. Python `sorted(a) == sorted(b)`; "
            "C++ `sort(a.begin(), a.end())` from `<algorithm>`.",
            "Idea 2 (faster for long words): count each letter with an array of 26 counters — `cnt[c - 'a']++` "
            "for the first word and `--` for the second, then check all counters are zero.",
        ],
        samples=["3\nlisten silent\nrat car\napple paple"],
        tests=["1\na a", "1\na b", "1\nab abc", "2\naab abb\nabc cba", "1\n" + "ab" * 50 + " " + "ba" * 50],
        gen=lambda rng: ["30\n" + "\n".join(_anagram_case(rng) for _ in range(30)) for _ in range(2)],
        starter_python=r"""t = int(input())
for _ in range(t):
    a, b = input().split()
    # TODO: print YES if a and b are anagrams, otherwise NO
""",
        starter_cpp=r"""#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        string a, b;
        cin >> a >> b;
        // TODO: print YES if a and b are anagrams, otherwise NO
    }
    return 0;
}
""",
        solution_python=r"""t = int(input())
for _ in range(t):
    a, b = input().split()
    print("YES" if sorted(a) == sorted(b) else "NO")
""",
        solution_cpp=r"""#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        string a, b;
        cin >> a >> b;
        sort(a.begin(), a.end());
        sort(b.begin(), b.end());
        cout << (a == b ? "YES" : "NO") << "\n";
    }
    return 0;
}
""",
    ),
]
