"""C++ track - Unit 4: Vectors & Strings."""

LESSONS = [
    dict(
        id="cpp-vectors",
        track="cpp",
        unit="Vectors & Strings",
        title="std::vector",
        summary="C++'s resizable list: push_back, size, indexing and range-based for.",
        body=r"""
`std::vector` (from `<vector>`) is the C++ counterpart of a Python list, with
one difference: **all elements have the same type**, which you write in angle
brackets.

```cpp
vector<int> v;              // empty
vector<int> w = {3, 1, 4};  // with values
vector<int> z(5);           // five zeros
vector<int> f(5, -1);       // five copies of -1
```

| Python | C++ |
|---|---|
| `v.append(x)` | `v.push_back(x)` |
| `len(v)` | `v.size()` |
| `v[i]` | `v[i]` (unchecked) or `v.at(i)` (checked) |
| `v[-1]` | `v.back()` |
| `v.pop()` | `v.pop_back()` (returns nothing!) |
| `not v` | `v.empty()` |

**Range-based for** loops over the elements, just like `for x in v:`. Add `&`
when you want to *modify* them:

```cpp
for (int x : v) cout << x << " ";   // x is a copy
for (int& x : v) x *= 2;            // x is the real element
```

**No safety net.** `v[10]` on a 3-element vector does not raise an
IndexError. It reads random memory: you may get garbage, a crash, or worse,
nothing visible at all. `v.at(10)` checks the index and throws an exception
instead, which is useful while debugging. Negative indices do not wrap
around.

**The unsigned trap.** `v.size()` returns an *unsigned* number, so on an
empty vector `v.size() - 1` is not -1 but about 1.8·10¹⁹. If you write
`for (int i = 0; i < (int)v.size() - 1; i++)`, the cast to `int` *before*
subtracting keeps you safe.

Reading `n` numbers into a vector:

```cpp
int n; cin >> n;
vector<int> a(n);
for (int& x : a) cin >> x;
```
""",
        examples=[
            dict(title="Building and looping",
                 code=r"""#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {3, 1, 4};
    v.push_back(1);
    v.push_back(5);
    cout << "size " << v.size() << ", first " << v[0] << ", last " << v.back() << "\n";
    for (int& x : v) x *= 10;
    for (int x : v) cout << x << " ";
    cout << "\n";
    v.pop_back();
    cout << "after pop_back: " << v.size() << " elements\n";
    return 0;
}
"""),
            dict(title="Read into a vector",
                 code=r"""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int& x : a) cin >> x;
    long long sum = 0;
    for (int x : a) sum += x;
    cout << "sum " << sum << ", middle element " << a[n / 2] << "\n";
    return 0;
}
""",
                 stdin="5\n10 20 30 40 50\n"),
            dict(title="at() catches bad indices",
                 code=r"""#include <iostream>
#include <stdexcept>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {1, 2, 3};
    try {
        cout << v.at(10) << "\n";
    } catch (const out_of_range& e) {
        cout << "caught out_of_range\n";
    }
    vector<int> empty;
    cout << "empty.size() - 1 = " << empty.size() - 1 << "\n";
    return 0;
}
""",
                 explain="v[10] would silently read garbage. Also note the huge unsigned 'minus one'."),
        ],
        challenge=dict(
            prompt=("Read `n` (1 ≤ n ≤ 10^5) and then `n` integers. Print them in **reverse "
                    "order**, separated by spaces."),
            starter=r"""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    // read into a, then print from the back
    return 0;
}
""",
            solution=r"""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int& x : a) cin >> x;
    for (int i = n - 1; i >= 0; i--) {
        cout << a[i] << (i > 0 ? " " : "\n");
    }
    return 0;
}
""",
            samples=["5\n1 2 3 4 5\n"],
            tests=["1\n42\n", "4\n-1 0 -1 7\n", "3\n1000000000 -1000000000 5\n"],
        ),
    ),
    dict(
        id="cpp-2d-vectors",
        track="cpp",
        unit="Vectors & Strings",
        title="2D Vectors & Grids",
        summary="vector<vector<int>> for grids and matrices.",
        body=r"""
A grid is a **vector of vectors**. The Python idiom
`[[0] * cols for _ in range(rows)]` becomes:

```cpp
vector<vector<int>> grid(rows, vector<int>(cols, 0));
grid[r][c] = 7;          // row r, column c
```

Read that as: "`rows` copies of a row, where each row is `cols` zeros". Each
row is a separate vector, so changing one row never affects another. (That
is a classic Python bug with `[[0] * cols] * rows`, which C++ does not have.)

Sizes:

```cpp
int rows = grid.size();
int cols = grid[0].size();
```

Reading an `r × c` grid of numbers:

```cpp
for (int i = 0; i < r; i++)
    for (int j = 0; j < c; j++)
        cin >> grid[i][j];
```

For character maps (mazes, game boards), a `vector<string>` is often handier:
`board[i][j]` is then a `char`.

```cpp
vector<string> board(r);
for (auto& row : board) cin >> row;   // each row is one word like "#..#"
```

**Pass grids by reference.** A function taking `vector<vector<int>> g` copies
every element on each call. Use `const vector<vector<int>>& g` to read it, or
`vector<vector<int>>& g` to modify it.

Neighbours in a grid are usually visited with two small arrays of offsets,
and you must check that you stay inside the bounds before indexing:

```cpp
int dr[] = {-1, 1, 0, 0}, dc[] = {0, 0, -1, 1};
for (int k = 0; k < 4; k++) {
    int nr = r + dr[k], nc = c + dc[k];
    if (nr >= 0 && nr < rows && nc >= 0 && nc < cols) { /* use grid[nr][nc] */ }
}
```
""",
        examples=[
            dict(title="Multiplication table",
                 code=r"""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n = 4;
    vector<vector<int>> t(n, vector<int>(n));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            t[i][j] = (i + 1) * (j + 1);
    for (const auto& row : t) {
        for (int x : row) cout << x << "\t";
        cout << "\n";
    }
    return 0;
}
""",
                 explain="const auto& row avoids copying each row while printing."),
            dict(title="Counting neighbours on a board",
                 code=r"""#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    int r, c;
    cin >> r >> c;
    vector<string> b(r);
    for (auto& row : b) cin >> row;
    int dr[] = {-1, 1, 0, 0}, dc[] = {0, 0, -1, 1};
    for (int i = 0; i < r; i++) {
        for (int j = 0; j < c; j++) {
            int cnt = 0;
            for (int k = 0; k < 4; k++) {
                int ni = i + dr[k], nj = j + dc[k];
                if (ni >= 0 && ni < r && nj >= 0 && nj < c && b[ni][nj] == '#') cnt++;
            }
            cout << cnt;
        }
        cout << "\n";
    }
    return 0;
}
""",
                 stdin="3 4\n#..#\n.##.\n....\n",
                 explain="For every cell, count the '#' cells directly above, below, left and right."),
        ],
        challenge=dict(
            prompt=("Read `r` and `c` (1 ≤ r, c ≤ 100), then an `r × c` matrix of integers. "
                    "Print its **transpose**: `c` lines with `r` numbers each, where line `j` "
                    "is column `j` of the input."),
            starter=r"""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int r, c;
    cin >> r >> c;
    vector<vector<int>> m(r, vector<int>(c));
    // read m, then print column by column
    return 0;
}
""",
            solution=r"""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int r, c;
    cin >> r >> c;
    vector<vector<int>> m(r, vector<int>(c));
    for (int i = 0; i < r; i++)
        for (int j = 0; j < c; j++)
            cin >> m[i][j];
    for (int j = 0; j < c; j++) {
        for (int i = 0; i < r; i++) {
            cout << m[i][j] << (i + 1 < r ? " " : "\n");
        }
    }
    return 0;
}
""",
            samples=["2 3\n1 2 3\n4 5 6\n"],
            tests=["1 1\n9\n", "1 4\n1 2 3 4\n", "3 2\n-1 -2\n-3 -4\n-5 -6\n"],
            checker="exact",
        ),
    ),
    dict(
        id="cpp-strings",
        track="cpp",
        unit="Vectors & Strings",
        title="std::string",
        summary="length, +, substr, find and npos, comparison, and getline.",
        body=r"""
`std::string` (from `<string>`) is a sequence of `char`s. Unlike Python's
`str`, it is **mutable**: `s[0] = 'J';` simply changes the first letter.

| Python | C++ |
|---|---|
| `len(s)` | `s.size()` or `s.length()` |
| `s + t` | `s + t` (also `s += t`) |
| `s[i:i+k]` | `s.substr(i, k)` (start, **length**!) |
| `s[i:]` | `s.substr(i)` |
| `s.find(t)` | `s.find(t)` returns `string::npos` if absent |
| `t in s` | `s.find(t) != string::npos` |
| `str(42)` | `to_string(42)` |
| `int(s)` | `stoi(s)` / `stoll(s)` |

**`substr` takes a length, not an end index.** `s.substr(2, 3)` means "3
characters starting at index 2", whereas Python's `s[2:3]` is one character.
This is a very common slip.

**`npos`.** When `find` fails it does not return -1 but `string::npos`, a
huge unsigned value. Always compare with `npos`. To search again *after* a
match, pass a start position: `s.find(t, pos + 1)`.

**Comparing:** `==`, `<`, `>` work on whole strings, alphabetically by
character code. In that order uppercase letters come before lowercase ones.

**Literals are not strings.** `"ab" + "cd"` does not compile, because both
are plain C character arrays. Make at least one side a `string`:
`string("ab") + "cd"`.

`cin >> s` reads one **word**. Use `getline(cin, s)` for a whole line, and
remember the leftover-newline trap after `cin >>` (fix it with `cin >> ws`).
""",
        examples=[
            dict(title="The everyday operations",
                 code=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    string s = "hello world";
    cout << s.size() << "\n";            // 11
    cout << s.substr(6) << "\n";         // world
    cout << s.substr(0, 4) << "\n";      // hell (length 4)
    cout << s.find("o") << "\n";         // 4
    if (s.find("xyz") == string::npos) cout << "not found\n";
    s[0] = 'J';
    s += "!";
    cout << s << "\n";
    cout << to_string(6 * 7) + "?" << " " << stoi("123") + 1 << "\n";
    return 0;
}
"""),
            dict(title="All occurrences",
                 code=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    string text, word;
    getline(cin, text);
    cin >> word;
    size_t pos = text.find(word);
    while (pos != string::npos) {
        cout << "found at " << pos << "\n";
        pos = text.find(word, pos + 1);
    }
    return 0;
}
""",
                 stdin="the cat sat on the mat\nat\n",
                 explain="size_t is the unsigned type that find returns."),
        ],
        challenge=dict(
            prompt=("The first line is a text (it may contain spaces), and the second line is a "
                    "pattern without spaces. Print every index where the pattern starts in the "
                    "text (overlaps count), separated by spaces, or `-1` if it never occurs."),
            starter=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    string text, pat;
    getline(cin, text);
    getline(cin, pat);
    // loop with text.find(pat, start)
    return 0;
}
""",
            solution=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    string text, pat;
    getline(cin, text);
    getline(cin, pat);
    size_t pos = text.find(pat);
    if (pos == string::npos) {
        cout << -1 << "\n";
        return 0;
    }
    bool first = true;
    while (pos != string::npos) {
        if (!first) cout << " ";
        cout << pos;
        first = false;
        pos = text.find(pat, pos + 1);
    }
    cout << "\n";
    return 0;
}
""",
            samples=["banana\nana\n", "hello world\nxyz\n"],
            tests=["aaaa\naa\n", "the cat sat on the mat\nat\n", "abc\nabc\n", "a b a b\nb\n"],
        ),
    ),
    dict(
        id="cpp-chars",
        track="cpp",
        unit="Vectors & Strings",
        title="Characters & char Arithmetic",
        summary="chars are small numbers: 'a' + 1, c - '0', and <cctype> helpers.",
        body=r"""
A `char` is really a **small integer**, namely the character's code (ASCII).
`'A'` is 65 and `'a'` is 97, and the letters and digits are consecutive. So
arithmetic works directly, with no `ord()` or `chr()` needed:

```cpp
char c = 'a' + 2;        // 'c'
int pos = 'e' - 'a';     // 4: the letter's index in the alphabet
int d = '7' - '0';       // 7: digit character to number
char up = c - 'a' + 'A'; // 'C'
```

`'a'` (single quotes) is a `char`, while `"a"` (double quotes) is a string.
They are not interchangeable: `s == 'a'` will not compile when `s` is a
string.

**Printing gotcha:** `cout << 'a' + 1` prints `98`, because `char + int` is
an `int`. Convert back to see the letter: `cout << char('a' + 1)`.

`<cctype>` has the usual tests and conversions:

```cpp
isdigit(c)  isalpha(c)  isupper(c)  islower(c)  isspace(c)
toupper(c)  tolower(c)          // these return int: wrap in char(...) to print
```

**Looping over a string** works like looping over a vector. Use `char&` to
change characters in place:

```cpp
for (char& ch : s) ch = toupper(ch);
```

**Wrapping around the alphabet** (Caesar cipher style) combines everything:
first get the index, then shift with `%`, and finally convert back.

```cpp
char shifted = 'a' + (c - 'a' + k) % 26;
```

A **counting array** is often simpler than a map for letters:
`int cnt[26] = {0}; cnt[c - 'a']++;`
""",
        examples=[
            dict(title="chars are numbers",
                 code=r"""#include <iostream>
using namespace std;

int main() {
    char c = 'a';
    cout << c << " " << int(c) << "\n";      // a 97
    cout << 'a' + 1 << "\n";                 // 98 (an int!)
    cout << char('a' + 1) << "\n";           // b
    cout << '7' - '0' << "\n";               // 7
    cout << char('q' - 'a' + 'A') << "\n";   // Q
    return 0;
}
"""),
            dict(title="Letter statistics",
                 code=r"""#include <cctype>
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s;
    getline(cin, s);
    int letters = 0, digits = 0;
    int cnt[26] = {0};
    for (char ch : s) {
        if (isalpha(ch)) {
            letters++;
            cnt[tolower(ch) - 'a']++;
        } else if (isdigit(ch)) {
            digits++;
        }
    }
    cout << letters << " letters, " << digits << " digits, "
         << cnt['o' - 'a'] << " o's\n";
    for (char& ch : s) ch = toupper(ch);
    cout << s << "\n";
    return 0;
}
""",
                 stdin="Hello World 2024, good to go\n"),
        ],
        challenge=dict(
            prompt=("**Caesar cipher.** The first line holds a shift `k` (0 ≤ k ≤ 1000) and the "
                    "second line a text. Shift every letter `k` places forward in the alphabet, "
                    "wrapping from z to a. Keep the case, and leave all other characters unchanged. "
                    "Print the result."),
            starter=r"""#include <cctype>
#include <iostream>
#include <string>
using namespace std;

int main() {
    int k;
    string s;
    cin >> k;
    // careful: skip the newline before getline!
    getline(cin, s);
    // shift the letters of s, then print it
    return 0;
}
""",
            solution=r"""#include <cctype>
#include <iostream>
#include <string>
using namespace std;

int main() {
    int k;
    string s;
    cin >> k >> ws;
    getline(cin, s);
    k %= 26;
    for (char& ch : s) {
        if (islower(ch)) ch = 'a' + (ch - 'a' + k) % 26;
        else if (isupper(ch)) ch = 'A' + (ch - 'A' + k) % 26;
    }
    cout << s << "\n";
    return 0;
}
""",
            samples=["3\nHello, World!\n"],
            tests=["1\nxyz XYZ\n", "0\nunchanged 123\n", "1000\nabc\n", "25\nThe quick brown fox.\n"],
            checker="exact",
        ),
    ),
]
