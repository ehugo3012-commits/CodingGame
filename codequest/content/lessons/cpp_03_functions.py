"""C++ track - Unit 3: Functions."""

LESSONS = [
    dict(
        id="cpp-functions",
        track="cpp",
        unit="Functions",
        title="Writing Functions",
        summary="Return types, typed parameters, void, and declare-before-use.",
        body=r"""
A C++ function states its **return type** and the **type of every
parameter**:

```cpp
int square(int x) {        // returns an int, takes an int
    return x * x;
}

void greet(string name) {  // void: returns nothing
    cout << "Hi " << name << "\n";
}
```

Compare this with Python's `def square(x):`. The types are not decoration:
calling `square("hi")` is a **compile error**, caught before the program
runs.

**Declare before use.** The compiler reads your file top to bottom. If `main`
calls `square` but `square` is defined *below* `main`, you get
`use of undeclared identifier 'square'`. You can fix that in two ways:

1. Define helper functions above `main` (the usual style for short programs).
2. Put a **prototype** (just the signature plus `;`) near the top, and the
   full definition anywhere below:

```cpp
bool isPrime(int n);       // prototype: "this exists, trust me"

int main() { cout << isPrime(7); }

bool isPrime(int n) { ... }   // definition
```

**Every path must return.** If a non-`void` function can reach its closing
`}` without hitting a `return`, the behaviour is undefined, and you may get
garbage or a crash. Compilers only *warn* about this, so check your branches
yourself.

Like Python, `return` exits the function immediately, which is handy for
early exits (`if (n < 2) return false;`). A `void` function can use a bare
`return;`.
""",
        examples=[
            dict(title="Helpers above main",
                 code=r"""#include <iostream>
#include <string>
using namespace std;

int square(int x) {
    return x * x;
}

void greet(const string& name) {
    cout << "Hi " << name << "!\n";
}

int main() {
    greet("Ada");
    cout << square(12) << "\n";
    return 0;
}
"""),
            dict(title="Prototype first, definition later",
                 code=r"""#include <iostream>
using namespace std;

bool isPrime(int n);   // prototype

int main() {
    for (int i = 1; i <= 20; i++) {
        if (isPrime(i)) cout << i << " ";
    }
    cout << "\n";
    return 0;
}

bool isPrime(int n) {
    if (n < 2) return false;
    for (int d = 2; d * d <= n; d++) {
        if (n % d == 0) return false;
    }
    return true;
}
""",
                 explain="Testing divisors only up to the square root (d * d <= n) is enough."),
        ],
        challenge=dict(
            prompt=("Write a function `bool isPrime(int n)`. Then read `n` and `n` integers "
                    "(each between 1 and 10^6) and print **how many of them are prime**."),
            starter=r"""#include <iostream>
using namespace std;

bool isPrime(int n) {
    // TODO
    return false;
}

int main() {
    int n;
    cin >> n;
    // read n numbers, count the primes with isPrime, print the count
    return 0;
}
""",
            solution=r"""#include <iostream>
using namespace std;

bool isPrime(int n) {
    if (n < 2) return false;
    for (int d = 2; d * d <= n; d++) {
        if (n % d == 0) return false;
    }
    return true;
}

int main() {
    int n;
    cin >> n;
    int count = 0;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        if (isPrime(x)) count++;
    }
    cout << count << "\n";
    return 0;
}
""",
            samples=["6\n1 2 3 4 5 6\n"],
            tests=["1\n1\n", "3\n999983 1000000 97\n", "5\n4 6 8 9 10\n",
                   "4\n2 2 2 2\n"],
        ),
    ),
    dict(
        id="cpp-references",
        track="cpp",
        unit="Functions",
        title="Pass by Value vs Reference",
        summary="Copies, & references, and const & for big objects.",
        body=r"""
By default C++ passes arguments **by value**: the function gets its own
*copy*, and changing that copy does not affect the caller.

```cpp
void addOne(int x) { x++; }      // modifies a copy
int n = 5; addOne(n);            // n is still 5
```

Put `&` after the type to pass **by reference**. The parameter then becomes
another name (an alias) for the caller's variable:

```cpp
void addOne(int& x) { x++; }     // modifies the original
int n = 5; addOne(n);            // n is now 6
```

That is how a C++ function can "return" several results: it writes them into
reference parameters. A classic example is `swap(a, b)`.

**How does this compare with Python?** In Python, passing a list lets the
function mutate it, but rebinding an `int` parameter never affects the
caller. In C++ *you* choose, per parameter, and that applies to every type:
an `int` can be modified by reference, and a `vector` is **copied** if you
pass it by value!

**`const &` for big read-only objects.** Copying a vector of a million
elements on each call is slow. Pass it as `const vector<int>& v`: no copy is
made, and `const` promises (enforced by the compiler) that the function will
not modify it.

Rules of thumb:

- small types (`int`, `double`, `char`): pass by value
- big things you only read (`string`, `vector`): pass by `const &`
- anything the function must change: pass by `&`

A reference parameter needs a real variable. `addOne(5)` with `int&` fails to
compile, because you cannot modify the literal 5.
""",
        examples=[
            dict(title="Value vs reference",
                 code=r"""#include <iostream>
using namespace std;

void byValue(int x)      { x = 100; }
void byReference(int& x) { x = 100; }

int main() {
    int a = 1, b = 1;
    byValue(a);
    byReference(b);
    cout << "a = " << a << ", b = " << b << "\n";
    return 0;
}
"""),
            dict(title="Returning two results",
                 code=r"""#include <iostream>
#include <vector>
using namespace std;

// v is read-only and not copied; lo and hi are written for the caller
void minMax(const vector<int>& v, int& lo, int& hi) {
    lo = hi = v[0];
    for (int x : v) {
        if (x < lo) lo = x;
        if (x > hi) hi = x;
    }
}

int main() {
    vector<int> v = {4, -2, 9, 7};
    int lo, hi;
    minMax(v, lo, hi);
    cout << lo << " " << hi << "\n";
    return 0;
}
""",
                 explain="You'll meet vector properly soon; note how const & avoids copying it."),
        ],
        challenge=dict(
            prompt=("Complete `void sortThree(int& a, int& b, int& c)` so that afterwards "
                    "`a <= b <= c`. Then `main` reads three integers, calls it and prints them "
                    "(already written for you)."),
            starter=r"""#include <iostream>
using namespace std;

void sortThree(int& a, int& b, int& c) {
    // TODO: swap values around until a <= b <= c
}

int main() {
    int a, b, c;
    cin >> a >> b >> c;
    sortThree(a, b, c);
    cout << a << " " << b << " " << c << "\n";
    return 0;
}
""",
            solution=r"""#include <iostream>
#include <utility>
using namespace std;

void sortThree(int& a, int& b, int& c) {
    if (a > b) swap(a, b);
    if (b > c) swap(b, c);
    if (a > b) swap(a, b);
}

int main() {
    int a, b, c;
    cin >> a >> b >> c;
    sortThree(a, b, c);
    cout << a << " " << b << " " << c << "\n";
    return 0;
}
""",
            samples=["3 1 2\n"],
            tests=["1 2 3\n", "3 2 1\n", "5 5 -1\n", "-7 10 -7\n"],
        ),
    ),
    dict(
        id="cpp-overloading",
        track="cpp",
        unit="Functions",
        title="Overloading & Default Arguments",
        summary="Several functions with one name, chosen by argument types.",
        body=r"""
In Python, defining a second `def area(...)` replaces the first. In C++ you
can have **several functions with the same name**, as long as their parameter
lists differ. This is called **overloading**:

```cpp
int area(int side)         { return side * side; }   // square
int area(int w, int h)     { return w * h; }         // rectangle
double area(double r)      { return 3.14159 * r * r; } // circle
```

The compiler picks the version whose parameters best match the arguments:
`area(3)` calls the first, `area(3, 4)` calls the second, and `area(2.0)`
calls the third. This happens at **compile time**, so there is no runtime
cost.

Some limits:

- The return type alone does not count. `int f(int)` and `double f(int)`
  conflict, with an error like *functions that differ only in their return
  type cannot be overloaded*.
- **Ambiguity is an error.** With only `f(long)` and `f(double)`, the call
  `f(5)` is an `int` that converts equally well to both, and the compiler
  refuses to guess (*call to 'f' is ambiguous*).

**Default arguments** cover the simple case where you just want an optional
parameter, like Python's `def f(x, times=1)`:

```cpp
void repeat(string s, int times = 1);
repeat("hi");      // times = 1
repeat("hi", 3);   // times = 3
```

Defaults must come **last** in the parameter list. Put them in the prototype
(or the definition if there's no prototype), but not in both.

You've already used overloading without noticing: `cout <<` is overloaded for
`int`, `double`, `string`, `char`, and more.
""",
        examples=[
            dict(title="Three areas",
                 code=r"""#include <iostream>
using namespace std;

int area(int side)     { return side * side; }
int area(int w, int h) { return w * h; }
double area(double r)  { return 3.14159 * r * r; }

int main() {
    cout << area(3) << "\n";      // square
    cout << area(3, 4) << "\n";   // rectangle
    cout << area(2.0) << "\n";    // circle: 2.0 is a double
    return 0;
}
"""),
            dict(title="Default arguments",
                 code=r"""#include <iostream>
#include <string>
using namespace std;

void repeat(const string& s, int times = 1, char sep = ' ') {
    for (int i = 0; i < times; i++) {
        if (i > 0) cout << sep;
        cout << s;
    }
    cout << "\n";
}

int main() {
    repeat("hi");
    repeat("hi", 3);
    repeat("hi", 3, '-');
    return 0;
}
"""),
        ],
        challenge=dict(
            prompt=("Write two overloads: `long long area(long long side)` (a square) and "
                    "`long long area(long long w, long long h)` (a rectangle). The input starts "
                    "with `q`, followed by `q` shape lines: either `S side` or `R w h` (values up to "
                    "10^6). Print each area on its own line, calling the matching overload."),
            starter=r"""#include <iostream>
using namespace std;

// TODO: two functions both named area

int main() {
    int q;
    cin >> q;
    for (int i = 0; i < q; i++) {
        char kind;
        cin >> kind;
        // if kind == 'S' read one number, else read two
    }
    return 0;
}
""",
            solution=r"""#include <iostream>
using namespace std;

long long area(long long side) { return side * side; }
long long area(long long w, long long h) { return w * h; }

int main() {
    int q;
    cin >> q;
    for (int i = 0; i < q; i++) {
        char kind;
        cin >> kind;
        if (kind == 'S') {
            long long s;
            cin >> s;
            cout << area(s) << "\n";
        } else {
            long long w, h;
            cin >> w >> h;
            cout << area(w, h) << "\n";
        }
    }
    return 0;
}
""",
            samples=["3\nS 4\nR 2 5\nS 1\n"],
            tests=["1\nR 1000000 1000000\n", "2\nS 1000000\nR 7 3\n", "1\nS 0\n"],
        ),
    ),
    dict(
        id="cpp-recursion",
        track="cpp",
        unit="Functions",
        title="Recursion",
        summary="Functions that call themselves: base cases, the call stack, and memoisation.",
        body=r"""
A **recursive** function solves a problem by calling itself on a smaller
version of it. There are always two parts:

1. a **base case** that answers directly, with no further calls
2. a **recursive case** that moves *closer* to the base case

```cpp
long long factorial(int n) {
    if (n <= 1) return 1;            // base case
    return n * factorial(n - 1);     // smaller problem
}
```

Each call gets its own copy of the parameters on the **call stack**. If the
base case is missing or unreachable, the recursion never stops, and the stack
overflows with a crash (*segmentation fault*). Python would raise
`RecursionError` after about 1000 calls. C++ allows much deeper recursion
(often 10⁵ or more simple calls), but the limit is real, and on a phone it can
be smaller.

**Watch for repeated work.** Naive Fibonacci calls itself twice per level, so
`fib(45)` makes over a billion calls:

```cpp
long long fib(int n) { return n < 2 ? n : fib(n - 1) + fib(n - 2); }
```

**Memoisation** stores each answer the first time it is computed. In C++ that
is usually a `vector` passed by reference (or a global), much like Python's
`@lru_cache`:

```cpp
long long fib(int n, vector<long long>& memo) {
    if (n < 2) return n;
    if (memo[n] != -1) return memo[n];
    return memo[n] = fib(n - 1, memo) + fib(n - 2, memo);
}
```

Euclid's algorithm is a short, elegant recursion for the greatest common
divisor: `gcd(a, b) = gcd(b, a % b)`, with `gcd(a, 0) = a`. (C++17 also
offers `std::gcd` in `<numeric>`.)
""",
        examples=[
            dict(title="Factorial",
                 code=r"""#include <iostream>
using namespace std;

long long factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

int main() {
    for (int n = 0; n <= 20; n += 5) {
        cout << n << "! = " << factorial(n) << "\n";
    }
    return 0;
}
""",
                 explain="20! still fits in a long long; 21! would overflow."),
            dict(title="Memoised Fibonacci",
                 code=r"""#include <iostream>
#include <vector>
using namespace std;

long long fib(int n, vector<long long>& memo) {
    if (n < 2) return n;
    if (memo[n] != -1) return memo[n];
    return memo[n] = fib(n - 1, memo) + fib(n - 2, memo);
}

int main() {
    int n;
    cin >> n;
    vector<long long> memo(n + 1, -1);
    cout << "fib(" << n << ") = " << fib(n, memo) << "\n";
    return 0;
}
""",
                 stdin="90\n",
                 explain="Each value is computed once, so this is instant. The naive version would never finish."),
        ],
        challenge=dict(
            prompt=("Write a **recursive** `long long gcd(long long a, long long b)` using "
                    "Euclid's rule. Read `t`, then `t` pairs `a b` (0 ≤ a, b ≤ 10^18, not both 0), "
                    "and print the gcd of each pair on its own line."),
            starter=r"""#include <iostream>
using namespace std;

long long gcd(long long a, long long b) {
    // base case: b == 0
    return 0;
}

int main() {
    int t;
    cin >> t;
    // read pairs and print gcd(a, b)
    return 0;
}
""",
            solution=r"""#include <iostream>
using namespace std;

long long gcd(long long a, long long b) {
    if (b == 0) return a;
    return gcd(b, a % b);
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long a, b;
        cin >> a >> b;
        cout << gcd(a, b) << "\n";
    }
    return 0;
}
""",
            samples=["3\n12 18\n7 5\n0 9\n"],
            tests=["1\n1000000000000000000 999999999999999999\n",
                   "2\n1000000000000000000 250000000000000000\n48 0\n",
                   "1\n17 17\n"],
        ),
    ),
]
