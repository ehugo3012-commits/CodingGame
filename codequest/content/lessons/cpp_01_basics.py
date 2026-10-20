"""C++ track - Unit 1: Basics (types, arithmetic, const/auto, formatting)."""

LESSONS = [
    dict(
        id="cpp-variables-types",
        track="cpp",
        unit="Basics",
        title="Variables & Types",
        summary="int, long long, double, char, bool, string, and why overflow bites.",
        body=r"""
C++ is **statically typed**: every variable has a fixed type, chosen when you
declare it. In Python `x = 5` followed by `x = "hi"` is fine. In C++ the
second assignment is a compile error.

| type | holds | example |
|---|---|---|
| `int` | whole numbers, about ±2.1·10⁹ | `int n = 42;` |
| `long long` | whole numbers, about ±9.2·10¹⁸ | `long long big = 5'000'000'000;` |
| `double` | decimals (~15 significant digits) | `double pi = 3.14159;` |
| `char` | one character, in **single** quotes | `char c = 'A';` |
| `bool` | `true` / `false` (prints as 1 / 0) | `bool ok = true;` |
| `string` | text, in **double** quotes (`<string>`) | `string s = "hi";` |

**Overflow.** Python integers grow forever, but an `int` has a fixed 32 bits.
If a result goes past about 2.1 billion, signed overflow is *undefined
behaviour*. In practice you usually get a silently wrong, often negative,
number. The rule of thumb: **if a value can exceed ~2·10⁹, use `long long`.**

A classic trap is that the type of the *result variable* does not help:

```cpp
int a = 100000, b = 100000;
long long p = a * b;        // WRONG: a * b is computed as int, then stored
long long q = 1LL * a * b;  // right: the multiplication happens in long long
```

**Always initialise.** `int x;` without a value contains whatever garbage was
in memory, not 0 as you might expect. Write `int x = 0;`.
""",
        examples=[
            dict(title="The basic types",
                 code=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    int n = 42;
    long long big = 5'000'000'000;   // ' separators are allowed since C++14
    double pi = 3.14159;
    char grade = 'A';
    bool ok = true;
    string name = "Ada";
    cout << n << " " << big << " " << pi << " " << grade << " "
         << ok << " " << name << "\n";
    cout << "an int uses " << sizeof(int) << " bytes, a long long "
         << sizeof(long long) << "\n";
    return 0;
}
""",
                 explain="bool prints as 1. sizeof tells you how many bytes a type occupies."),
            dict(title="Overflow in action",
                 code=r"""#include <iostream>
using namespace std;

int main() {
    int a, b;
    cin >> a >> b;
    int wrong = a * b;              // overflows: undefined behaviour
    long long right = 1LL * a * b;  // computed in 64 bits
    cout << "int:       " << wrong << "\n";
    cout << "long long: " << right << "\n";
    return 0;
}
""",
                 stdin="100000 100000\n",
                 explain="10^10 does not fit in an int. Here the result wraps around to garbage."),
        ],
        challenge=dict(
            prompt=("Read two integers `a` and `b` (each up to 10^9 in absolute value) and print "
                    "their product. It will not fit in an `int`!"),
            starter=r"""#include <iostream>
using namespace std;

int main() {
    int a, b;
    cin >> a >> b;
    // print a * b without overflowing
    return 0;
}
""",
            solution=r"""#include <iostream>
using namespace std;

int main() {
    long long a, b;
    cin >> a >> b;
    cout << a * b << "\n";
    return 0;
}
""",
            samples=["6 7\n", "100000 100000\n"],
            tests=["1000000000 1000000000\n", "-999999999 1000000000\n", "0 123\n"],
        ),
    ),
    dict(
        id="cpp-arithmetic",
        track="cpp",
        unit="Basics",
        title="Arithmetic & Casts",
        summary="Integer division, %, mixing int and double, and static_cast.",
        body=r"""
The operators look familiar (`+ - * / %`), but **the types decide the result**.

**Integer division truncates.** If both sides are integers, `/` throws away
the fractional part, so `7 / 2` is `3`. There is no separate `//` operator as
in Python. The truncation goes *toward zero*, which differs from Python for
negative numbers:

| expression | C++ | Python |
|---|---|---|
| `7 / 2` | `3` | `3.5` (`7 // 2` is `3`) |
| `-7 / 2` | `-3` | `-7 // 2` is `-4` |
| `-7 % 2` | `-1` | `1` |

To get a non-negative remainder in C++, write `((a % m) + m) % m`.

**Mixing types.** If either operand is a `double`, the whole operation is done
in `double`: `7 / 2.0` is `3.5`. To divide two `int` variables exactly,
**cast** one of them:

```cpp
int sum = 7, count = 2;
double avg = static_cast<double>(sum) / count;   // 3.5
double bad = sum / count;                         // 3 (already truncated!)
```

`static_cast<T>(x)` is the modern, explicit way to convert. The C-style form
`(double)sum` also works. Converting a `double` to an `int` truncates:
`static_cast<int>(3.99)` is `3`.

**Order matters** with integer division: `c * 9 / 5` and `9 / 5 * c` differ,
because `9 / 5` is already `1`.

Integer division or `%` by zero crashes the program (SIGFPE). Python would
raise `ZeroDivisionError` instead.
""",
        examples=[
            dict(title="Division table",
                 code=r"""#include <iostream>
using namespace std;

int main() {
    cout << 7 / 2 << " " << 7 % 2 << "\n";      // 3 1
    cout << -7 / 2 << " " << -7 % 2 << "\n";    // -3 -1
    cout << 7 / 2.0 << "\n";                    // 3.5
    int m = 5, a = -7;
    cout << ((a % m) + m) % m << "\n";          // 3, like Python's -7 % 5
    return 0;
}
"""),
            dict(title="Casting for an exact average",
                 code=r"""#include <iostream>
using namespace std;

int main() {
    int sum, count;
    cin >> sum >> count;
    double bad = sum / count;
    double good = static_cast<double>(sum) / count;
    cout << "bad:  " << bad << "\n";
    cout << "good: " << good << "\n";
    cout << "truncate 3.99 -> " << static_cast<int>(3.99) << "\n";
    return 0;
}
""",
                 stdin="7 2\n",
                 explain="In `bad` the division already happened in int, before the value was stored in the double."),
        ],
        challenge=dict(
            prompt=("Read a number of seconds `t` (0 ≤ t ≤ 10^9). Print how many whole hours, "
                    "minutes and seconds that is, as three numbers separated by spaces."),
            starter=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    // use / and % to split t into hours, minutes, seconds
    return 0;
}
""",
            solution=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    cout << t / 3600 << " " << t % 3600 / 60 << " " << t % 60 << "\n";
    return 0;
}
""",
            samples=["3725\n"],
            tests=["0\n", "59\n", "86399\n", "1000000000\n"],
        ),
    ),
    dict(
        id="cpp-const-auto",
        track="cpp",
        unit="Basics",
        title="const, auto & Shortcuts",
        summary="Constants the compiler enforces, type deduction with auto, and += / ++.",
        body=r"""
**`const`** marks a value that must never change. The compiler enforces this,
so it is more than a naming convention like Python's `MAX_SIZE`:

```cpp
const int MAX_N = 100000;
MAX_N = 5;   // error: cannot assign to variable 'MAX_N' with const-qualified type
```

`constexpr` goes further: the value is computed at **compile time**, so you
can use it, for example, as an array size.

**`auto`** asks the compiler to deduce the type from the initial value:

```cpp
auto n = 5;        // int
auto x = 5.0;      // double
auto big = 5LL;    // long long (LL suffix)
auto s = "hi";     // careful: const char*, NOT std::string
```

`auto` is not dynamic typing. The variable still gets one fixed type, which
you just do not have to spell out. It shines with long type names you will
meet later (`auto it = m.begin();`). For plain numbers, an explicit type is
often clearer.

**Shortcuts** (identical in spirit to Python, plus `++`/`--`):

```cpp
x += 3;   x -= 1;   x *= 2;   x /= 4;   x %= 7;
i++;      // add 1 (Python has no ++)
i--;      // subtract 1
```

`++i` (pre-increment) and `i++` (post-increment) differ only when you use the
value in the same expression. Keep `++` on its own line and you never have to
care.
""",
        examples=[
            dict(title="const and compound assignment",
                 code=r"""#include <iostream>
using namespace std;

int main() {
    const int BONUS = 10;
    int score = 50;
    score += BONUS;   // 60
    score *= 2;       // 120
    score -= 1;       // 119
    score %= 100;     // 19
    score++;          // 20
    cout << "score = " << score << "\n";
    return 0;
}
"""),
            dict(title="auto deduction",
                 code=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    auto a = 7;          // int
    auto b = 7 / 2;      // int: 3
    auto c = 7 / 2.0;    // double: 3.5
    auto d = 3000000000LL * 3;  // long long
    auto s = string("text");    // std::string
    cout << a << " " << b << " " << c << " " << d << " " << s.size() << "\n";
    return 0;
}
""",
                 explain="The deduced type follows the expression's type, so integer division still truncates."),
        ],
        challenge=dict(
            prompt=("Read an integer `x` (0 ≤ x ≤ 1000). Apply these steps in order and print "
                    "the value after **each** step, one per line:\n\n"
                    "1. add 7\n2. multiply by 3\n3. subtract 4\n4. integer-divide by 2\n"
                    "5. take the remainder modulo 10\n\nUse the compound operators (`+=`, `*=`, ...)."),
            starter=r"""#include <iostream>
using namespace std;

int main() {
    int x;
    cin >> x;
    // x += 7; then print x, and so on...
    return 0;
}
""",
            solution=r"""#include <iostream>
using namespace std;

int main() {
    int x;
    cin >> x;
    x += 7;  cout << x << "\n";
    x *= 3;  cout << x << "\n";
    x -= 4;  cout << x << "\n";
    x /= 2;  cout << x << "\n";
    x %= 10; cout << x << "\n";
    return 0;
}
""",
            samples=["5\n"],
            tests=["0\n", "1000\n", "42\n"],
        ),
    ),
    dict(
        id="cpp-formatting",
        track="cpp",
        unit="Basics",
        title="Formatting Output",
        summary="fixed, setprecision, setw and setfill from <iomanip>.",
        body=r"""
By default `cout` prints a `double` with **6 significant digits**, which
surprises Python users:

```cpp
cout << 3.14159265;   // 3.14159
cout << 1234567.0;    // 1.23457e+06  (!)
```

To control the digits, include `<iomanip>`:

```cpp
cout << fixed << setprecision(2) << 3.14159;   // 3.14
```

- `fixed` switches to plain decimal notation. With it, `setprecision(n)` means
  **n digits after the decimal point**, like Python's `f"{x:.2f}"`.
- Without `fixed`, `setprecision(n)` means n *significant* digits.
- Both settings are **sticky**: they stay in effect for everything printed
  afterwards.

For widths and padding:

```cpp
cout << setw(5) << 42;                      // "   42" (right-aligned, width 5)
cout << setfill('0') << setw(2) << 7;       // "07"
```

`setw` is the odd one out: it applies to the **next item only**, while
`setfill` is sticky.

If you know C, `printf("%.2f\n", x);` from `<cstdio>` works too. Just don't mix
it with `cout` after you have turned on fast I/O (you will meet that in a
later lesson).

Judges usually compare decimals with a tolerance, but when a problem says
"exactly two decimals", `fixed << setprecision(2)` is the tool.
""",
        examples=[
            dict(title="Precision",
                 code=r"""#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    double x = 1234567.891;
    cout << x << "\n";                           // default: 6 significant digits
    cout << fixed << setprecision(2) << x << "\n";
    cout << 2.0 / 3 << "\n";                     // still fixed, 2 decimals
    cout << setprecision(5) << 2.0 / 3 << "\n";
    return 0;
}
""",
                 explain="Once fixed and setprecision are set they stay set."),
            dict(title="A digital clock",
                 code=r"""#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    int h, m, s;
    cin >> h >> m >> s;
    cout << setfill('0') << setw(2) << h << ":" << setw(2) << m << ":"
         << setw(2) << s << "\n";
    return 0;
}
""",
                 stdin="7 5 9\n",
                 explain="setw must be repeated before every number; setfill('0') sticks."),
            dict(title="A right-aligned table",
                 code=r"""#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    cout << setw(6) << "item" << setw(8) << "price" << "\n";
    cout << fixed << setprecision(2);
    cout << setw(6) << "tea" << setw(8) << 2.5 << "\n";
    cout << setw(6) << "cake" << setw(8) << 12.75 << "\n";
    return 0;
}
"""),
        ],
        challenge=dict(
            prompt=("Read three integers and print their average with **exactly two** digits "
                    "after the decimal point."),
            starter=r"""#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    int a, b, c;
    cin >> a >> b >> c;
    // careful: (a + b + c) / 3 is integer division
    return 0;
}
""",
            solution=r"""#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    int a, b, c;
    cin >> a >> b >> c;
    double avg = (a + b + c) / 3.0;
    cout << fixed << setprecision(2) << avg << "\n";
    return 0;
}
""",
            samples=["1 2 4\n"],
            tests=["10 20 30\n", "0 0 1\n", "100 -5 7\n", "1000000 1000000 999999\n"],
            checker="exact",
        ),
    ),
]
