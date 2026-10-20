"""C++ track - Unit 2: Control Flow."""

LESSONS = [
    dict(
        id="cpp-if-else",
        track="cpp",
        unit="Control Flow",
        title="if / else & Logic",
        summary="Conditions, else if, &&, ||, !, the ternary operator, and the = vs == trap.",
        body=r"""
The condition goes in **parentheses** and the body in **braces**:

```cpp
if (score >= 90) {
    cout << "A\n";
} else if (score >= 80) {     // two words, not elif
    cout << "B\n";
} else {
    cout << "C\n";
}
```

Logical operators are symbols rather than words:

- Python `and` is `&&` in C++
- Python `or` is `||`
- Python `not` is `!`

Like Python, `&&` and `||` short-circuit: in `b != 0 && a / b > 2`, the
division only happens when `b` is not zero.

**Trap 1: `=` vs `==`.** `if (x = 5)` *assigns* 5 to `x` and then tests it.
Any non-zero value counts as true, so the branch always runs. This compiles
(often with only a warning), so stay alert. Use `==` to compare.

**Trap 2: chained comparisons.** Python's `1 < x < 10` does not mean the same
in C++. It evaluates `(1 < x)` to 0 or 1 and then compares *that* with 10, so
it is always true. Write `1 < x && x < 10`.

**Braces are optional** for a one-statement body, as in `if (x < 0) x = -x;`.
However, only that single statement is controlled, so adding a second
indented line later silently escapes the `if`. When in doubt, use braces.

The **ternary operator** picks between two values:

```cpp
string label = (n % 2 == 0) ? "even" : "odd";
```
""",
        examples=[
            dict(title="Grades",
                 code=r"""#include <iostream>
using namespace std;

int main() {
    int score;
    cin >> score;
    if (score >= 90) {
        cout << "A\n";
    } else if (score >= 80) {
        cout << "B\n";
    } else {
        cout << "C or below\n";
    }
    cout << (score % 2 == 0 ? "even" : "odd") << "\n";
    return 0;
}
""",
                 stdin="85\n"),
            dict(title="The chained-comparison trap",
                 code=r"""#include <iostream>
using namespace std;

int main() {
    int x = 50;
    cout << (1 < x < 10) << "\n";          // 1 (true!): (1 < x) is 1, and 1 < 10
    cout << (1 < x && x < 10) << "\n";     // 0: what we meant
    return 0;
}
""",
                 explain="A comparison produces a bool (0 or 1), which the next comparison then uses."),
        ],
        challenge=dict(
            prompt=("Read a year and print `leap` if it is a leap year, otherwise `common`. "
                    "A year is a leap year if it is divisible by 4, except that years divisible "
                    "by 100 are not, unless they are also divisible by 400."),
            starter=r"""#include <iostream>
using namespace std;

int main() {
    int year;
    cin >> year;
    // combine the rules with && and ||
    return 0;
}
""",
            solution=r"""#include <iostream>
using namespace std;

int main() {
    int year;
    cin >> year;
    if ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0) {
        cout << "leap\n";
    } else {
        cout << "common\n";
    }
    return 0;
}
""",
            samples=["2024\n", "1900\n"],
            tests=["2000\n", "2023\n", "2100\n", "4\n"],
        ),
    ),
    dict(
        id="cpp-loops",
        track="cpp",
        unit="Control Flow",
        title="while & for Loops",
        summary="while, the three-part for loop, do-while, and off-by-one errors.",
        body=r"""
A `while` loop repeats as long as its condition is true:

```cpp
int n = 3;
while (n > 0) {
    cout << n << "\n";
    n--;
}
```

The C++ `for` loop has **three parts**: `init; condition; step`. It is the
direct replacement for Python's `for i in range(...)`:

| Python | C++ |
|---|---|
| `for i in range(n):` | `for (int i = 0; i < n; i++)` |
| `for i in range(1, n + 1):` | `for (int i = 1; i <= n; i++)` |
| `for i in range(n - 1, -1, -1):` | `for (int i = n - 1; i >= 0; i--)` |
| `for i in range(0, n, 2):` | `for (int i = 0; i < n; i += 2)` |

A variable declared in the `for` header (`int i`) only exists inside the
loop.

**Off-by-one errors** are the classic bug: `i <= n` versus `i < n` decides
whether the loop runs n or n+1 times. When you index into a container later,
one step too far reads memory that is not yours. Unlike Python, C++ does not
raise an IndexError to stop you.

`do { ... } while (cond);` runs the body **at least once** before it checks
the condition. Note the semicolon at the end.

The typical input pattern is: read a count `n`, then loop `n` times and read
one value each time:

```cpp
int n;
cin >> n;
for (int i = 0; i < n; i++) {
    int x;
    cin >> x;
    // use x
}
```
""",
        examples=[
            dict(title="Sum of 1..n",
                 code=r"""#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    long long total = 0;
    for (int i = 1; i <= n; i++) {
        total += i;
    }
    cout << total << "\n";
    return 0;
}
""",
                 stdin="100\n"),
            dict(title="Counting down and by twos",
                 code=r"""#include <iostream>
using namespace std;

int main() {
    for (int i = 5; i >= 1; i--) cout << i << " ";
    cout << "\n";
    for (int i = 0; i < 10; i += 2) cout << i << " ";
    cout << "\n";
    int k = 100;
    do {
        cout << "runs once even though k >= 10\n";
    } while (k < 10);
    return 0;
}
"""),
            dict(title="Read n values",
                 code=r"""#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    int evens = 0;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        if (x % 2 == 0) evens++;
    }
    cout << evens << " even numbers\n";
    return 0;
}
""",
                 stdin="5\n3 8 10 7 2\n"),
        ],
        challenge=dict(
            prompt=("Read `n` (1 ≤ n ≤ 10^5), then `n` integers (each up to 10^9 in absolute "
                    "value). Print their **sum**, **minimum** and **maximum** separated by spaces."),
            starter=r"""#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    // loop n times; keep a running sum, min and max
    return 0;
}
""",
            solution=r"""#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;
    long long sum = 0;
    int mn = 0, mx = 0;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        sum += x;
        if (i == 0 || x < mn) mn = x;
        if (i == 0 || x > mx) mx = x;
    }
    cout << sum << " " << mn << " " << mx << "\n";
    return 0;
}
""",
            samples=["5\n3 -1 4 1 5\n"],
            tests=["1\n-7\n", "3\n1000000000 1000000000 1000000000\n",
                   "4\n-5 -2 -9 -3\n"],
        ),
    ),
    dict(
        id="cpp-break-continue",
        track="cpp",
        unit="Control Flow",
        title="break, continue & Reading to the End",
        summary="Leave a loop early, skip an iteration, and loop until input runs out.",
        body=r"""
These work just like in Python:

- `break` leaves the innermost loop immediately.
- `continue` skips the rest of this iteration and jumps to the next one.

```cpp
for (int i = 1; i <= 10; i++) {
    if (i % 3 == 0) continue;   // skip multiples of 3
    if (i > 7) break;           // stop entirely after 7
    cout << i << " ";           // 1 2 4 5 7
}
```

**Nested loops:** `break` only exits the *inner* loop. To escape both, set a
flag and check it in the outer loop, or put the loops in a function and
`return`. (C++ has no `for ... else` like Python.)

**Reading until the input ends.** `cin >> x` evaluates to something that is
true when the read succeeded and false at end of input (or when the text is
not a number). That makes this pattern very common when you don't know the
count in advance:

```cpp
int x;
long long sum = 0;
while (cin >> x) {
    sum += x;
}
```

**Sentinel values.** Some inputs end with a special marker such as `0`.
Combine an endless loop with `break`:

```cpp
while (true) {
    int x;
    cin >> x;
    if (x == 0) break;
    // process x
}
```

`while (true)` is C++'s spelling of Python's `while True:`.
""",
        examples=[
            dict(title="Skip and stop",
                 code=r"""#include <iostream>
using namespace std;

int main() {
    for (int i = 1; i <= 10; i++) {
        if (i % 3 == 0) continue;
        if (i > 7) break;
        cout << i << " ";
    }
    cout << "\n";
    return 0;
}
"""),
            dict(title="Read until end of input",
                 code=r"""#include <iostream>
using namespace std;

int main() {
    int x, count = 0;
    long long sum = 0;
    while (cin >> x) {
        sum += x;
        count++;
    }
    cout << count << " numbers, sum " << sum << "\n";
    return 0;
}
""",
                 stdin="4 8 15\n16 23\n42\n",
                 explain="No count was given; the loop ends when cin has nothing left to read."),
            dict(title="Escaping nested loops with a flag",
                 code=r"""#include <iostream>
using namespace std;

int main() {
    // find the first pair (a, b) with a * b == 42 and a < b
    bool found = false;
    for (int a = 1; a <= 10 && !found; a++) {
        for (int b = a + 1; b <= 50; b++) {
            if (a * b == 42) {
                cout << a << " * " << b << "\n";
                found = true;
                break;          // leaves only the inner loop...
            }
        }
    }                           // ...and !found stops the outer one
    return 0;
}
"""),
        ],
        challenge=dict(
            prompt=("Read integers until you meet a `0` (the 0 is not data). **Skip** negative "
                    "numbers. Print the sum of the positive numbers and how many there were, "
                    "separated by a space."),
            starter=r"""#include <iostream>
using namespace std;

int main() {
    // while (true) { read x; break on 0; continue on negatives; ... }
    return 0;
}
""",
            solution=r"""#include <iostream>
using namespace std;

int main() {
    long long sum = 0;
    int count = 0;
    while (true) {
        int x;
        cin >> x;
        if (x == 0) break;
        if (x < 0) continue;
        sum += x;
        count++;
    }
    cout << sum << " " << count << "\n";
    return 0;
}
""",
            samples=["5 -3 10 -1 2 0\n"],
            tests=["0\n", "-1 -2 -3 0\n", "1000000000 1000000000 1000000000 0 99\n",
                   "7\n0\n"],
        ),
    ),
    dict(
        id="cpp-switch",
        track="cpp",
        unit="Control Flow",
        title="switch",
        summary="Branch on an integer or char value, and beware of fall-through.",
        body=r"""
When you compare **one integer or `char` value** against several constants,
`switch` is tidier than a chain of `else if`:

```cpp
switch (op) {
    case '+': cout << a + b; break;
    case '-': cout << a - b; break;
    case 'x':
    case '*': cout << a * b; break;   // two labels share one body
    default:  cout << "unknown";       // like a final else
}
```

**Always end a case with `break`.** Without it, execution *falls through*
into the next case's code. That is occasionally intended (as with `'x'` and
`'*'` above), but usually it is a bug. Python's `match` has no fall-through,
so this one catches Python programmers.

Rules the compiler enforces:

- The value must be an integer type, a `char`, or an `enum`. A **`string`
  does not work**: `switch (s)` fails with an error like *statement requires
  expression of integer type*. Use `if / else if` for strings.
- Case labels must be **compile-time constants** (`case 3:`, `case 'a':`), not
  variables.
- Declaring a variable inside a case needs its own braces:
  `case 1: { int t = 5; ... break; }`. Otherwise you get the error *jump to
  case label crosses initialization*.
""",
        examples=[
            dict(title="Day names",
                 code=r"""#include <iostream>
using namespace std;

int main() {
    int d;
    cin >> d;
    switch (d) {
        case 1: cout << "Monday\n"; break;
        case 2: cout << "Tuesday\n"; break;
        case 6:
        case 7: cout << "Weekend!\n"; break;
        default: cout << "Some other weekday\n";
    }
    return 0;
}
""",
                 stdin="6\n"),
            dict(title="Fall-through surprise",
                 code=r"""#include <iostream>
using namespace std;

int main() {
    int level = 2;
    switch (level) {
        case 1: cout << "one ";
        case 2: cout << "two ";     // starts here...
        case 3: cout << "three ";   // ...and keeps going: no break!
        default: cout << "default";
    }
    cout << "\n";
    return 0;
}
""",
                 explain="Without break, every case after the matching one runs too."),
        ],
        challenge=dict(
            prompt=("Read an expression `a op b` where `a` and `b` are integers (up to 10^9 in "
                    "absolute value) and `op` is one of `+ - * / %`. Print the result using "
                    "integer arithmetic. If `op` is `/` or `%` and `b` is 0, print `error` instead."),
            starter=r"""#include <iostream>
using namespace std;

int main() {
    long long a, b;
    char op;
    cin >> a >> op >> b;
    // switch (op) { case '+': ... }
    return 0;
}
""",
            solution=r"""#include <iostream>
using namespace std;

int main() {
    long long a, b;
    char op;
    cin >> a >> op >> b;
    switch (op) {
        case '+': cout << a + b << "\n"; break;
        case '-': cout << a - b << "\n"; break;
        case '*': cout << a * b << "\n"; break;
        case '/':
            if (b == 0) cout << "error\n";
            else cout << a / b << "\n";
            break;
        case '%':
            if (b == 0) cout << "error\n";
            else cout << a % b << "\n";
            break;
    }
    return 0;
}
""",
            samples=["7 + 5\n", "17 % 5\n"],
            tests=["1000000000 * 1000000000\n", "-7 / 2\n", "3 / 0\n", "3 % 0\n", "10 - 25\n"],
        ),
    ),
]
