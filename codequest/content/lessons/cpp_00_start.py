"""C++ track - Unit 0: Getting Started."""

LESSONS = [
    dict(
        id="cpp-hello",
        track="cpp",
        unit="Getting Started",
        title="Hello, C++",
        summary="The anatomy of a C++ program: #include, main, cout, and compile-then-run.",
        body=r"""
Every C++ program starts running in a function called `main`. Here is the
smallest useful one:

```cpp
#include <iostream>    // brings in cout and cin
using namespace std;   // lets us write cout instead of std::cout

int main() {
    cout << "Hello, world!" << "\n";
    return 0;          // 0 means "everything went fine"
}
```

Line by line:

- `#include <iostream>` pulls in the input/output library. C++ has very little
  built in: almost every feature lives in a **header** that you include.
- `int main()` is the entry point. Unlike Python, loose statements outside a
  function are not allowed; execution begins at the top of `main`.
- `cout << x` sends `x` to standard output. Chain as many `<<` as you like.
  Nothing is added automatically: no spaces, no newline. `"\n"` ends the line.
- Every statement ends with `;`, and blocks live inside `{ }`. Indentation is
  only for humans.

**Compile, then run.** Python reads your file and runs it straight away. C++ is
first translated by a **compiler** (clang++ or g++) into a native program, and
only then executed:

```text
clang++ -std=c++17 hello.cpp -o hello   # 1. compile
./hello                                  # 2. run
```

CodeQuest does both steps for you. If the compiler finds a mistake, **nothing
runs** and you get a compile error instead. A forgotten `;` gives something
like `error: expected ';' after expression` along with a line number. Always
fix the **first** error first: later ones are often just follow-on noise.
""",
        examples=[
            dict(title="Hello, world",
                 code=r"""#include <iostream>
using namespace std;

int main() {
    cout << "Hello, world!" << "\n";
    return 0;
}
"""),
            dict(title="Chaining <<",
                 code=r"""#include <iostream>
using namespace std;

int main() {
    cout << "2 + 3 = " << 2 + 3 << "\n";
    cout << "no" << "spaces" << "added" << "\n";
    cout << "one line, " << "same line\n";
    return 0;
}
""",
                 explain="Unlike Python's print, cout never inserts spaces or newlines for you."),
        ],
        challenge=dict(
            prompt="Print exactly `I am learning C++!` (there is no input).",
            starter=r"""#include <iostream>
using namespace std;

int main() {
    // print the sentence here
    return 0;
}
""",
            solution=r"""#include <iostream>
using namespace std;

int main() {
    cout << "I am learning C++!\n";
    return 0;
}
""",
            samples=[""],
            checker="exact",
        ),
    ),
    dict(
        id="cpp-input",
        track="cpp",
        unit="Getting Started",
        title="Reading Input with cin",
        summary="cin >> reads typed values; getline reads whole lines.",
        body=r"""
In C++ a variable must be **declared with a type** before you can store
anything in it. Then `cin >>` reads the next value from standard input and
converts it to that type:

```cpp
int age;
cin >> age;          // reads e.g. "42" and stores the number 42
```

`cin >>` skips any whitespace (spaces, tabs, newlines) and then reads one
**token**. It does not care about line breaks, so chaining works whether the
numbers are on one line or several:

```cpp
int a, b;
cin >> a >> b;       // "6 7" or "6\n7": both work
```

Python's `input()` works one *line* at a time, and you convert with `int()`.
In C++ the conversion comes from the variable's type: reading into an `int`
parses a number, and reading into a `string` grabs one word.

**Whole lines.** To read a line that contains spaces, use `getline` from
`<string>`:

```cpp
string full;
getline(cin, full);  // "Ada Lovelace"
```

**Pitfall:** `cin >> n` leaves the newline after the number unread. A
`getline` straight after it returns an empty string! Skip the leftover
whitespace with `cin >> ws` before calling `getline`.

**Reading until the input runs out:** `while (cin >> x) { ... }` keeps going
as long as a value was read successfully.
""",
        examples=[
            dict(title="Greeting",
                 code=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    string name;
    cin >> name;
    cout << "Hi " << name << "\n";
    return 0;
}
""",
                 stdin="Ada\n"),
            dict(title="Two numbers",
                 code=r"""#include <iostream>
using namespace std;

int main() {
    int a, b;
    cin >> a >> b;
    cout << a * b << "\n";
    return 0;
}
""",
                 stdin="6\n7\n",
                 explain="The numbers are on separate lines, but cin >> does not care."),
            dict(title="Number, then a whole line",
                 code=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    int n;
    string line;
    cin >> n;
    cin >> ws;              // skip the newline left after the number
    getline(cin, line);
    cout << n << " -> [" << line << "]\n";
    return 0;
}
""",
                 stdin="3\nAda Lovelace\n",
                 explain="Delete the `cin >> ws;` line and `line` comes out empty."),
        ],
        challenge=dict(
            prompt=("Read a name on the first line and a birth year on the second. "
                    "Print `<name> is <age> in 2030`."),
            starter=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    string name;
    int year;
    // read both values, then print the sentence
    return 0;
}
""",
            solution=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    string name;
    int year;
    cin >> name >> year;
    cout << name << " is " << 2030 - year << " in 2030\n";
    return 0;
}
""",
            samples=["Ada\n1990\n"],
            tests=["Linus\n2001\n", "Grace\n2030\n", "Bjarne\n1950\n"],
            checker="exact",
        ),
    ),
    dict(
        id="cpp-comments-errors",
        track="cpp",
        unit="Getting Started",
        title="Comments, std:: and Compiler Errors",
        summary="Comments, namespaces, endl vs \\n, headers, and how to read an error message.",
        body=r"""
**Comments** come in two flavours:

```cpp
// a line comment, like Python's #
/* a block comment
   that can span lines */
```

**Namespaces.** Everything in the standard library lives inside the namespace
`std`, so its full name is `std::cout`, `std::string`, and so on.
`using namespace std;` lets you drop the prefix. That is fine for small
programs like ours. In big projects people prefer writing `std::`, because it
avoids name clashes.

**`endl` vs `"\n"`.** Both end a line, but `endl` also *flushes* the output
buffer, which is slow when you print many lines. Use `"\n"`.

**Include what you use.** Each library feature needs its own header:
`<iostream>` (cin/cout), `<string>`, `<vector>`, `<algorithm>`, `<cmath>`.
You will see `#include <bits/stdc++.h>` in competitive code. That is a
GCC-only shortcut that includes everything. CodeQuest ships a stand-in so it
works here too, but explicit headers are portable and compile faster.

**Reading compiler errors.** The two errors you will meet most often:

- `use of undeclared identifier 'cout'` (clang) or `'cout' was not declared`
  (gcc) means a missing `#include`, a missing `std::`, or a typo.
- `expected ';'` means you forgot a semicolon, usually at the **end of the
  previous line**, not the line that is reported.

The compiler checks types too. `int x = "hello";` is rejected before your
program ever runs, while Python would only complain once that line executed.
""",
        examples=[
            dict(title="Without using namespace",
                 code=r"""#include <iostream>
#include <string>

int main() {
    std::string lang = "C++";
    std::cout << "Hello from " << lang << "\n";   // full names, no 'using'
    return 0;
}
"""),
            dict(title="Comments everywhere",
                 code=r"""#include <iostream>
using namespace std;

/* This program prints the area of a 3 x 4 rectangle.
   Block comments are handy for longer notes. */
int main() {
    int w = 3, h = 4;          // width and height
    cout << w * h << "\n";     // area
    // cout << "this line is ignored\n";
    return 0;
}
""",
                 explain="Commenting a line out is a quick way to switch it off while debugging."),
        ],
        challenge=dict(
            prompt=("Read three integers. Print them **in reverse order** on one line, separated "
                    "by spaces, and then print their sum on a second line."),
            starter=r"""#include <iostream>
using namespace std;

int main() {
    int a, b, c;
    cin >> a >> b >> c;
    // print c b a, then the sum
    return 0;
}
""",
            solution=r"""#include <iostream>
using namespace std;

int main() {
    int a, b, c;
    cin >> a >> b >> c;
    cout << c << " " << b << " " << a << "\n";
    cout << a + b + c << "\n";
    return 0;
}
""",
            samples=["1 2 3\n"],
            tests=["10\n-4\n7\n", "0 0 0\n", "100 200 -300\n"],
        ),
    ),
]
