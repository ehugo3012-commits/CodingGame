"""C++ track - Unit 7: Going Deeper (pointers, classes, memory, templates, pitfalls)."""

LESSONS = [
    dict(
        id="cpp-pointers",
        track="cpp",
        unit="Going Deeper",
        title="Pointers & References",
        summary="Addresses with &, dereferencing with *, nullptr, and how pointers differ from references.",
        body=r"""
Every variable lives at some **address** in memory. A **pointer** is a
variable that stores such an address:

```cpp
int x = 10;
int* p = &x;     // &x = "address of x";  p points to x
cout << *p;      // *p = "the int p points to": 10
*p = 20;         // writes through the pointer: x is now 20
```

Note that the symbols do double duty. In a **declaration**, `int*` means
"pointer to int" and `int&` means "reference to int". In an **expression**,
`&x` takes an address and `*p` follows one (*dereferences* it).

**`nullptr`** means "points at nothing". Dereferencing a null pointer, or one
that points at memory which no longer exists, is undefined behaviour and
typically ends in a *segmentation fault*. Python has no such thing: every
name refers to a live object, or the lookup raises an error.

**Pointer vs reference:**

| | reference `int& r = x;` | pointer `int* p = &x;` |
|---|---|---|
| can be null? | no | yes (`nullptr`) |
| can be re-pointed? | no, bound forever | yes, `p = &y;` |
| syntax to use | just `r` | `*p`, or `p->field` |

So prefer references, and use a pointer when "nothing" is a valid answer,
for example a search that can fail, or an optional link in a linked list.

**Arrays and pointers.** A built-in array decays to a pointer to its first
element, and `p + i` steps `i` elements forward. That is how `v.data()` and
`begin()` work under the hood, and also why going out of bounds silently
reads neighbouring memory.

**Python intuition:** a Python variable is a bit like a pointer that is
dereferenced automatically and can never dangle. C++ makes the indirection
explicit, and leaves the safety to you.
""",
        examples=[
            dict(title="Address-of and dereference",
                 code=r"""#include <iostream>
using namespace std;

int main() {
    int x = 10, y = 99;
    int* p = &x;
    cout << *p << "\n";       // 10
    *p = 20;
    cout << x << "\n";        // 20: x changed through p
    p = &y;                   // re-point to y
    cout << *p << "\n";       // 99
    int* none = nullptr;
    if (none == nullptr) cout << "none points nowhere\n";
    return 0;
}
""",
                 explain="We print values, not the addresses themselves, which differ on every run."),
            dict(title="A search that can fail",
                 code=r"""#include <iostream>
#include <vector>
using namespace std;

// returns a pointer to the first negative element, or nullptr
int* firstNegative(vector<int>& v) {
    for (int& x : v)
        if (x < 0) return &x;
    return nullptr;
}

int main() {
    vector<int> v = {4, 7, -3, 8, -1};
    int* p = firstNegative(v);
    if (p != nullptr) {
        cout << "found " << *p << " at index " << p - v.data() << "\n";
        *p = 0;                         // fix it in place
    }
    for (int x : v) cout << x << " ";
    cout << "\n";
    return 0;
}
""",
                 explain="p - v.data() is pointer arithmetic: how many ints p lies past the first element."),
        ],
        challenge=dict(
            prompt=("Complete `void minMax(const vector<int>& v, int* lo, int* hi)` so that it "
                    "**writes** the minimum into `*lo` and the maximum into `*hi`. `main` (given) "
                    "reads `n` and `n` integers and prints both."),
            starter=r"""#include <iostream>
#include <vector>
using namespace std;

void minMax(const vector<int>& v, int* lo, int* hi) {
    // TODO: write through the pointers, e.g. *lo = ...
}

int main() {
    int n;
    cin >> n;
    vector<int> v(n);
    for (int& x : v) cin >> x;
    int a = 0, b = 0;
    minMax(v, &a, &b);
    cout << a << " " << b << "\n";
    return 0;
}
""",
            solution=r"""#include <iostream>
#include <vector>
using namespace std;

void minMax(const vector<int>& v, int* lo, int* hi) {
    *lo = *hi = v[0];
    for (int x : v) {
        if (x < *lo) *lo = x;
        if (x > *hi) *hi = x;
    }
}

int main() {
    int n;
    cin >> n;
    vector<int> v(n);
    for (int& x : v) cin >> x;
    int a = 0, b = 0;
    minMax(v, &a, &b);
    cout << a << " " << b << "\n";
    return 0;
}
""",
            samples=["5\n3 -2 9 4 0\n"],
            tests=["1\n7\n", "3\n5 5 5\n", "4\n-1 -9 -3 -4\n"],
        ),
    ),
    dict(
        id="cpp-structs-classes",
        track="cpp",
        unit="Going Deeper",
        title="Structs & Classes",
        summary="Your own types: fields, constructors, methods, const methods and private data.",
        body=r"""
A `struct` groups named fields into a new type. It is much clearer than
juggling `.first` and `.second`:

```cpp
struct Point {
    int x = 0, y = 0;                       // default values
    int dist2() const { return x*x + y*y; } // a method
};

Point p{3, 4};
cout << p.x << " " << p.dist2();            // 3 25
```

**Constructors** set an object up. The *member initialiser list* after `:`
is the idiomatic way to fill the fields. It is C++'s version of Python's
`__init__`:

```cpp
class Account {
public:
    Account(string owner, long long balance)
        : owner_(owner), balance_(balance) {}
    void deposit(long long amount) { balance_ += amount; }
    long long balance() const { return balance_; }
private:
    string owner_;
    long long balance_;
};
```

- **`public:`** members can be used by anyone, while **`private:`** ones only
  by the class's own methods. Python relies on a `_name` convention; C++
  *enforces* it, and outside access fails with `'balance_' is a private member`.
- `struct` and `class` are nearly identical. The only difference is that
  `struct` members are public by default and `class` members private. By
  convention, `struct` is used for plain data bundles.
- There is no `self`. Inside a method, fields are reached directly (or via
  `this->`).
- A **`const` method** (`... const {`) promises not to modify the object.
  Only const methods can be called on a `const` object or `const&` parameter.

**Don't forget the `;`** after the closing brace of a struct or class. Leaving
it out produces confusing errors on the *next* line.

Structs work well with containers: `vector<Point>`, and sorting with a lambda
comparator like `[](const Point& a, const Point& b) { return a.x < b.x; }`.
""",
        examples=[
            dict(title="A struct in a vector",
                 code=r"""#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

struct Student {
    string name;
    int grade;
};

int main() {
    vector<Student> s = {{"Ada", 91}, {"Linus", 78}, {"Grace", 97}};
    sort(s.begin(), s.end(), [](const Student& a, const Student& b) {
        return a.grade > b.grade;
    });
    for (const auto& st : s) cout << st.name << " " << st.grade << "\n";
    return 0;
}
"""),
            dict(title="A class with private state",
                 code=r"""#include <iostream>
#include <string>
using namespace std;

class Counter {
public:
    Counter(string label, int start = 0) : label_(label), value_(start) {}
    void tick() { value_++; }
    int value() const { return value_; }
    string label() const { return label_; }
private:
    string label_;
    int value_;
};

int main() {
    Counter c("clicks", 10);
    for (int i = 0; i < 5; i++) c.tick();
    cout << c.label() << ": " << c.value() << "\n";
    // c.value_ = 0;   // error: 'value_' is a private member of 'Counter'
    return 0;
}
""",
                 explain="The only way to change value_ is through the class's own methods."),
        ],
        challenge=dict(
            prompt=("Complete the `Account` class. The input has `q` commands, one per line:\n\n"
                    "- `deposit x`: add x to the balance\n"
                    "- `withdraw x`: subtract x, but **only** if the balance is at least x; "
                    "otherwise print `denied` and change nothing\n"
                    "- `balance`: print the current balance\n\n"
                    "The account starts at 0, and amounts are up to 10^9."),
            starter=r"""#include <iostream>
#include <string>
using namespace std;

class Account {
public:
    void deposit(long long x) { /* TODO */ }
    bool withdraw(long long x) { /* TODO: return false if not enough */ return false; }
    long long balance() const { return balance_; }
private:
    long long balance_ = 0;
};

int main() {
    int q;
    cin >> q;
    Account acc;
    while (q--) {
        string cmd;
        cin >> cmd;
        // handle deposit / withdraw / balance
    }
    return 0;
}
""",
            solution=r"""#include <iostream>
#include <string>
using namespace std;

class Account {
public:
    void deposit(long long x) { balance_ += x; }
    bool withdraw(long long x) {
        if (x > balance_) return false;
        balance_ -= x;
        return true;
    }
    long long balance() const { return balance_; }
private:
    long long balance_ = 0;
};

int main() {
    int q;
    cin >> q;
    Account acc;
    while (q--) {
        string cmd;
        cin >> cmd;
        if (cmd == "deposit") {
            long long x;
            cin >> x;
            acc.deposit(x);
        } else if (cmd == "withdraw") {
            long long x;
            cin >> x;
            if (!acc.withdraw(x)) cout << "denied\n";
        } else {
            cout << acc.balance() << "\n";
        }
    }
    return 0;
}
""",
            samples=["5\ndeposit 100\nwithdraw 30\nbalance\nwithdraw 100\nbalance\n"],
            tests=["1\nbalance\n", "2\nwithdraw 1\nbalance\n",
                   "4\ndeposit 1000000000\ndeposit 1000000000\nwithdraw 2000000000\nbalance\n"],
        ),
    ),
    dict(
        id="cpp-smart-pointers",
        track="cpp",
        unit="Going Deeper",
        title="Dynamic Memory & unique_ptr",
        summary="new/delete, leaks, RAII, and letting unique_ptr clean up for you.",
        body=r"""
Local variables live on the **stack** and vanish automatically when their
scope ends. Sometimes an object must outlive the function that creates it,
or its size is only known at runtime. Then it goes on the **heap**:

```cpp
int* p = new int(42);   // allocate
cout << *p;
delete p;               // you MUST free it yourself
```

Python's garbage collector frees memory for you. With raw `new`/`delete`,
**you** are the garbage collector, and the classic bugs follow: forgetting
`delete` (a *leak*), deleting twice, or using memory after `delete` (a
*dangling pointer*).

**RAII** ("Resource Acquisition Is Initialisation") is C++'s answer: tie the
resource to an object whose **destructor** frees it automatically when the
object goes out of scope. You already rely on this, because `vector` and
`string` free their memory on their own.

For single heap objects, use **`unique_ptr`** from `<memory>`:

```cpp
auto p = make_unique<int>(42);   // owns the int
cout << *p;                      // use it like a pointer
// no delete: freed automatically when p goes out of scope
```

- A `unique_ptr` has exactly **one owner**. It cannot be copied (a compile
  error), only *moved*: `auto q = move(p);` transfers ownership, and leaves
  `p` null.
- `shared_ptr` (via `make_shared`) allows several owners and frees the object
  when the last one disappears. It is handy, but costlier, so reach for it
  only when ownership really is shared.

**Modern rule of thumb:** you should almost never write `new` or `delete`.
For many objects, use a `vector`. For one object with an owner, use
`unique_ptr`. For a linked structure, use nodes holding
`unique_ptr<Node> next`.

A *destructor* is written `~ClassName()` and runs automatically when the
object dies. That is the hook RAII builds on.
""",
        examples=[
            dict(title="Destructors run automatically",
                 code=r"""#include <iostream>
#include <memory>
#include <string>
#include <utility>
using namespace std;

struct Noisy {
    string name;
    Noisy(string n) : name(n) { cout << "  create " << name << "\n"; }
    ~Noisy() { cout << "  destroy " << name << "\n"; }
};

int main() {
    cout << "start\n";
    {
        Noisy a("stack object");
        auto b = make_unique<Noisy>("heap object");
        cout << "  using " << b->name << "\n";
    }   // both are cleaned up here, in reverse order
    cout << "end of scope passed\n";
    auto c = make_unique<Noisy>("moved object");
    auto d = move(c);                          // ownership moves to d
    cout << "c is " << (c ? "set" : "null") << "\n";
    return 0;
}
""",
                 explain="No delete anywhere, yet every object is destroyed exactly once."),
            dict(title="A linked list with unique_ptr",
                 code=r"""#include <iostream>
#include <memory>
#include <utility>
using namespace std;

struct Node {
    int val;
    unique_ptr<Node> next;
};

int main() {
    unique_ptr<Node> head;
    for (int x = 3; x >= 1; x--) {
        auto n = make_unique<Node>();
        n->val = x;
        n->next = move(head);   // new node takes over the old list
        head = move(n);
    }
    for (Node* cur = head.get(); cur != nullptr; cur = cur->next.get())
        cout << cur->val << " ";
    cout << "\n";
    return 0;
}
""",
                 explain="get() gives a plain, non-owning pointer for walking the list."),
        ],
        challenge=dict(
            prompt=("Implement a **stack as a linked list** of `unique_ptr<Node>`. The input has `q` "
                    "commands: `push x` pushes x; `pop` prints the top value and removes it, or "
                    "prints `empty` if the stack is empty. At the end, print the number of elements "
                    "left."),
            starter=r"""#include <iostream>
#include <memory>
#include <string>
#include <utility>
using namespace std;

struct Node {
    int val;
    unique_ptr<Node> next;
};

int main() {
    unique_ptr<Node> head;
    int size = 0;
    int q;
    cin >> q;
    while (q--) {
        string cmd;
        cin >> cmd;
        // push: new node whose next takes over head (use move)
        // pop:  print head->val, then head = move(head->next)
    }
    cout << size << "\n";
    return 0;
}
""",
            solution=r"""#include <iostream>
#include <memory>
#include <string>
#include <utility>
using namespace std;

struct Node {
    int val;
    unique_ptr<Node> next;
};

int main() {
    unique_ptr<Node> head;
    int size = 0;
    int q;
    cin >> q;
    while (q--) {
        string cmd;
        cin >> cmd;
        if (cmd == "push") {
            auto n = make_unique<Node>();
            cin >> n->val;
            n->next = move(head);
            head = move(n);
            size++;
        } else if (!head) {
            cout << "empty\n";
        } else {
            cout << head->val << "\n";
            head = move(head->next);
            size--;
        }
    }
    cout << size << "\n";
    return 0;
}
""",
            samples=["6\npush 1\npush 2\npop\npush 3\npop\npop\n"],
            tests=["1\npop\n", "3\npush 5\npush 6\npush 7\n", "4\npush -1\npop\npop\npush 9\n"],
        ),
    ),
    dict(
        id="cpp-templates",
        track="cpp",
        unit="Going Deeper",
        title="Templates",
        summary="Write a function or class once and use it with many types.",
        body=r"""
Python functions are generic for free: `def biggest(xs)` works on any list
whose items can be compared. In C++ every parameter has a type, so to avoid
writing `biggest` once for `int`, again for `double` and again for `string`,
you write a **template**:

```cpp
template <typename T>
T biggest(const vector<T>& v) {
    T best = v[0];
    for (const T& x : v)
        if (x > best) best = x;
    return best;
}
```

`T` is a placeholder type. When you call `biggest(nums)` with a
`vector<int>`, the compiler **deduces** `T = int` and generates a real `int`
version for you. Calling it with a `vector<string>` generates a second
version. You can also be explicit: `biggest<double>(...)`.

This happens at **compile time**, so templates cost nothing at runtime. That
is exactly how `vector<T>`, `map<K, V>` and `sort` are written.

**Class templates** work the same way:

```cpp
template <typename T>
struct Box {
    T value;
    T get() const { return value; }
};
Box<int> a{5};
Box<string> b{"hi"};
```

**Duck typing, checked at compile time.** A template accepts any type that
supports the operations it uses. If you call `biggest` on a type without `>`,
the compiler stops with an error, often a long one pointing deep inside the
template. Look for the line mentioning *your* code ("in instantiation of ...
requested here") to find the call that caused it.

Templates normally live in headers, because the compiler needs to see the
full code to generate each version.
""",
        examples=[
            dict(title="One function, many types",
                 code=r"""#include <iostream>
#include <string>
#include <vector>
using namespace std;

template <typename T>
T biggest(const vector<T>& v) {
    T best = v[0];
    for (const T& x : v)
        if (x > best) best = x;
    return best;
}

int main() {
    vector<int> a = {3, 9, 2};
    vector<double> b = {1.5, -2.25, 0.75};
    vector<string> c = {"pear", "apple", "zucchini", "fig"};
    cout << biggest(a) << " " << biggest(b) << " " << biggest(c) << "\n";
    return 0;
}
"""),
            dict(title="A class template",
                 code=r"""#include <iostream>
#include <string>
using namespace std;

template <typename A, typename B>
struct Duo {
    A first;
    B second;
    void show() const { cout << "(" << first << ", " << second << ")\n"; }
};

template <typename T>
T clampTo(T x, T lo, T hi) {
    return x < lo ? lo : (x > hi ? hi : x);
}

int main() {
    Duo<string, int> d{"age", 36};
    d.show();
    Duo<char, double> e{'x', 2.5};
    e.show();
    cout << clampTo(15, 0, 10) << " " << clampTo(-0.5, 0.0, 1.0) << "\n";
    // clampTo(15, 0.0, 10) would fail: T can't be both int and double
    return 0;
}
""",
                 explain="All arguments for the same T must agree; mixing int and double breaks deduction."),
        ],
        challenge=dict(
            prompt=("Write one template `T smallest(const vector<T>& v)`. The input holds `n` "
                    "integers, then `m` words. Print the smallest integer on "
                    "the first line and the alphabetically smallest word on the second, using "
                    "your template both times.\n\nInput: `n`, the `n` integers, `m`, the `m` words."),
            starter=r"""#include <iostream>
#include <string>
#include <vector>
using namespace std;

// template <typename T>
// T smallest(const vector<T>& v) { ... }

int main() {
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int& x : nums) cin >> x;
    int m;
    cin >> m;
    vector<string> words(m);
    for (string& w : words) cin >> w;
    // print smallest(nums) and smallest(words)
    return 0;
}
""",
            solution=r"""#include <iostream>
#include <string>
#include <vector>
using namespace std;

template <typename T>
T smallest(const vector<T>& v) {
    T best = v[0];
    for (const T& x : v)
        if (x < best) best = x;
    return best;
}

int main() {
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int& x : nums) cin >> x;
    int m;
    cin >> m;
    vector<string> words(m);
    for (string& w : words) cin >> w;
    cout << smallest(nums) << "\n" << smallest(words) << "\n";
    return 0;
}
""",
            samples=["4\n5 -2 9 0\n3\npear apple fig\n"],
            tests=["1\n7\n1\nsolo\n", "3\n-1 -1 -5\n4\nb a B A\n"],
        ),
    ),
    dict(
        id="cpp-pitfalls",
        track="cpp",
        unit="Going Deeper",
        title="Common Pitfalls",
        summary="The bugs every C++ beginner meets, and how to spot them fast.",
        body=r"""
C++ trusts you, so many mistakes compile fine and misbehave at runtime. Here
are the usual suspects, roughly in order of how often they bite:

1. **Uninitialised variables.** `int sum;` holds garbage, not 0. Always write
   `int sum = 0;`.
2. **`=` instead of `==`.** `if (x = 0)` assigns 0 and tests false, so the
   branch *never* runs and `x` is overwritten in the process.
3. **Signed overflow.** `int` stops at about 2.1·10⁹. Use `long long` for sums,
   products and anything that might grow, and write `1LL * a * b`.
4. **Integer division.** `sum / n` truncates before it is stored in a
   `double`. Use `static_cast<double>(sum) / n`.
5. **Out-of-bounds access.** `v[n]` on a vector of size `n`, or a loop with
   `i <= n`, reads memory that isn't yours, with no IndexError. Use `v.at(i)`
   while debugging.
6. **Unsigned underflow.** `v.size() - 1` on an empty vector is huge. Cast
   first: `(int)v.size() - 1`.
7. **`getline` after `cin >>`** returns an empty line. Use `cin >> ws`.
8. **Missing `return`** in a non-void function, or returning a reference to a
   local variable that is destroyed when the function ends.
9. **Copying big things** by value in function parameters or `for (auto x : v)`.
   Use `const auto&`.

**Undefined behaviour (UB)** is the real enemy. For bugs like 1, 3, 5 and 8
the C++ standard promises *nothing*. The program may work on your phone, fail
on the judge, or change behaviour when you add a `cout`. If output looks
"impossible", suspect UB first.

**Tools that help** on a desktop: compile with `-Wall -Wextra` to get warnings
about most of these, and `-fsanitize=address,undefined` to catch
out-of-bounds and overflow at runtime with a precise report.
""",
        examples=[
            dict(title="Bugs that compile",
                 code=r"""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int x = 5;
    if (x = 0) cout << "never printed\n";      // assignment, not comparison!
    cout << "x is now " << x << "\n";

    int sum = 7, n = 2;
    double bad = sum / n, good = static_cast<double>(sum) / n;
    cout << bad << " vs " << good << "\n";

    vector<int> v;                               // empty
    cout << "v.size() - 1 = " << v.size() - 1 << "\n";
    cout << "(int)v.size() - 1 = " << (int)v.size() - 1 << "\n";
    return 0;
}
""",
                 explain="Every one of these compiles; only the output reveals the bug."),
            dict(title="at() turns silent bugs into loud ones",
                 code=r"""#include <iostream>
#include <stdexcept>
#include <vector>
using namespace std;

int main() {
    vector<int> v = {1, 2, 3};
    long long total = 0;
    try {
        for (int i = 0; i <= 3; i++) total += v.at(i);   // off-by-one: i <= 3
    } catch (const out_of_range& e) {
        cout << "out of range! (total so far " << total << ")\n";
    }
    return 0;
}
""",
                 explain="With v[i] this would quietly add a garbage value or crash; at() reports it."),
        ],
        challenge=dict(
            prompt=("**Fix the bugs.** The starter program should read `n` (1 ≤ n ≤ 10^5) and `n` "
                    "integers (0 ≤ value ≤ 10^9), then print the **sum**, the **number of zeros**, "
                    "and the **average** with exactly 2 decimals, separated by spaces. It compiles, "
                    "but it hides **five** classic bugs (one line contains two of them). Find "
                    "and fix them all."),
            starter=r"""#include <iomanip>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i <= n; i++) cin >> a[i];
    int sum;
    int zeros = 0;
    for (int i = 0; i < n; i++) {
        sum += a[i];
        if (a[i] = 0) zeros++;
    }
    double avg = sum / n;
    cout << sum << " " << zeros << " " << fixed << setprecision(2) << avg << "\n";
    return 0;
}
""",
            solution=r"""#include <iomanip>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];
    long long sum = 0;
    int zeros = 0;
    for (int i = 0; i < n; i++) {
        sum += a[i];
        if (a[i] == 0) zeros++;
    }
    double avg = static_cast<double>(sum) / n;
    cout << sum << " " << zeros << " " << fixed << setprecision(2) << avg << "\n";
    return 0;
}
""",
            samples=["4\n1 0 4 0\n"],
            tests=["1\n7\n", "3\n1000000000 1000000000 1000000000\n", "5\n0 0 0 0 1\n",
                   "2\n1 2\n"],
        ),
    ),
]
