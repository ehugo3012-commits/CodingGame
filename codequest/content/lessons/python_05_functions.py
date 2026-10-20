"""Python track - Unit 5: Functions."""

LESSONS = [
    dict(
        id="py-functions",
        track="python",
        unit="Functions",
        title="Defining Functions",
        summary="def, parameters, return values and default arguments.",
        body=r"""
A **function** packages code under a name so you can reuse it and test it
on its own:

```python
def area(width, height):
    return width * height

print(area(3, 4))     # 12
```

- `def` starts the definition; `width, height` are **parameters**.
- `return` hands a value back to the caller and **ends** the function.
- Calling `area(3, 4)` passes the **arguments** 3 and 4.

### return is not print

> **Pitfall:** a function that only `print`s gives back `None`. If the
> caller needs the value (to add it, compare it, store it), you must
> `return` it. A function with no `return` returns `None`.

### Default and keyword arguments

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Ada")                    # 'Hello, Ada!'
greet("Ada", "Hi")              # 'Hi, Ada!'
greet(greeting="Hey", name="Bo")  # keywords: any order
```

Parameters with defaults must come after those without.

> **Pitfall: mutable defaults.** The default value is created **once**,
> when `def` runs - not on every call:
>
> ```python
> def add(item, bag=[]):    # BAD: one shared list
>     bag.append(item)
>     return bag
> ```
>
> Every call without `bag` reuses the same list, so items pile up. Use
> `bag=None` and inside write `if bag is None: bag = []`.

Good functions do **one thing**, have a descriptive verb name
(`count_vowels`, `is_prime`) and get everything they need through
parameters.
""",
        examples=[
            dict(title="return a value",
                 code="""\
def area(width, height):
    return width * height

def show_area(width, height):
    print(width * height)

a = area(3, 4)
b = show_area(3, 4)
print("a =", a, "b =", b)
""",
                 explain="show_area prints but returns None, so b is None."),
            dict(title="Defaults & keywords",
                 code="""\
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Ada"))
print(greet("Ada", "Hi"))
print(greet(greeting="Hey", name=input()))
""",
                 stdin="Bo\n"),
            dict(title="Mutable default trap",
                 code="""\
def bad(item, bag=[]):
    bag.append(item)
    return bag

def good(item, bag=None):
    if bag is None:
        bag = []
    bag.append(item)
    return bag

print(bad(1), bad(2))
print(good(1), good(2))
""",
                 explain="bad() keeps reusing the single list created when def ran."),
        ],
        challenge=dict(
            prompt=("Write a function `clamp(x, lo=0, hi=100)` that returns `lo` if `x < lo`, "
                    "`hi` if `x > hi`, and `x` otherwise. Read a line of integers and print each "
                    "one clamped (space separated)."),
            starter=("def clamp(x, lo=0, hi=100):\n    # return the clamped value\n    return x\n\n"
                     "nums = list(map(int, input().split()))\n"
                     "out = []\nfor n in nums:\n    out.append(str(clamp(n)))\nprint(' '.join(out))\n"),
            solution=("def clamp(x, lo=0, hi=100):\n    if x < lo:\n        return lo\n"
                      "    if x > hi:\n        return hi\n    return x\n\n"
                      "nums = list(map(int, input().split()))\n"
                      "out = []\nfor n in nums:\n    out.append(str(clamp(n)))\nprint(' '.join(out))\n"),
            samples=["-5 50 150\n"],
            tests=["0 100\n", "101 -1 99 1\n", "42\n"],
        ),
    ),
    dict(
        id="py-scope",
        track="python",
        unit="Functions",
        title="Scope",
        summary="Local vs global names, UnboundLocalError, and why to pass values in and out.",
        body=r"""
Names created inside a function are **local**: they exist only while the
function runs and are invisible outside.

```python
def f():
    secret = 42
f()
print(secret)     # NameError
```

A function **can read** a global (module-level) name:

```python
rate = 0.25
def tax(price):
    return price * rate     # fine: just reading
```

### The assignment rule

If a function **assigns** to a name anywhere in its body, Python treats
that name as local for the **whole** function:

```python
total = 0
def add(x):
    total = total + x   # UnboundLocalError!
```

Python decided `total` is local (because of the assignment), so reading it
on the right-hand side fails - the local has no value yet.

You *could* write `global total` inside the function, but that is usually a
design smell: hidden shared state makes functions hard to test and reason
about. The clean fix is to **pass values in and return results out**:

```python
def add(total, x):
    return total + x

total = add(total, 5)
```

> **Mutating vs assigning:** `items.append(x)` inside a function changes a
> global list *without* any `global` keyword, because you are not
> re-assigning the name - you are calling a method on the object it points
> to. Convenient, but also a source of surprises.

For a function nested inside another, `nonlocal name` lets the inner one
re-assign the outer one's variable - you will rarely need it.

Rule of thumb: a function should depend only on its parameters and
communicate only through its return value.
""",
        examples=[
            dict(title="Reading a global",
                 code="""\
rate = 0.25
def tax(price):
    return price * rate
print(tax(100))
""",
                 explain="Reading is fine; Python finds rate in the global scope."),
            dict(title="UnboundLocalError",
                 code="""\
total = 0
def add(x):
    total = total + x
try:
    add(5)
except UnboundLocalError as e:
    print("error:", e)
""",
                 explain="The assignment makes total local, so the right-hand side has nothing to read."),
            dict(title="Pass in, return out",
                 code="""\
def add(total, x):
    return total + x

total = 0
for x in map(int, input().split()):
    total = add(total, x)
print(total)
""",
                 stdin="1 2 3 4\n",
                 explain="No globals needed: the function is easy to test in isolation."),
        ],
        challenge=dict(
            prompt=("The starter code crashes with `UnboundLocalError`. Fix it **without** using "
                    "`global`: change `add` so it takes the running total and returns the new "
                    "one. Input is a line of integers; print their sum."),
            starter=("total = 0\n\ndef add(x):\n    total = total + x\n\n"
                     "for tok in input().split():\n    add(int(tok))\nprint(total)\n"),
            solution=("total = 0\n\ndef add(total, x):\n    return total + x\n\n"
                      "for tok in input().split():\n    total = add(total, int(tok))\nprint(total)\n"),
            samples=["1 2 3 4\n"],
            tests=["0\n", "-5 5 10\n", "100 200 300\n"],
        ),
    ),
    dict(
        id="py-lambda-sorted",
        track="python",
        unit="Functions",
        title="lambda & sorted(key=...)",
        summary="Functions are values: pass them to sorted, max and min to customise ordering.",
        body=r"""
In Python a function is a value like any other - you can store it in a
variable or pass it to another function:

```python
def by_length(word):
    return len(word)

sorted(["kiwi", "fig", "banana"], key=by_length)
# ['fig', 'kiwi', 'banana']
```

`key=` tells `sorted` to compare items by `key(item)` instead of the item
itself. `min`, `max` and `list.sort` accept `key=` too.

### lambda

For tiny one-off functions, a **lambda** saves you the `def`:

```python
sorted(words, key=lambda w: len(w))
max(people, key=lambda p: p[1])      # tuple with the biggest score
```

`lambda args: expression` - no `return`, no statements, just one
expression. If it grows complicated, use a normal `def` with a name.

### Sorting by several things

Return a **tuple** from the key. Tuples compare element by element, so this
sorts by length and breaks ties alphabetically:

```python
sorted(words, key=lambda w: (len(w), w))
```

To sort one part descending and another ascending, negate the number:
`key=lambda p: (-p[1], p[0])` for `(name, score)` pairs.

`reverse=True` flips the whole order. Python's sort is **stable**: items
with equal keys keep their original relative order.

> **Pitfall:** `key=len()` calls `len` immediately (with no argument) and
> fails. Pass the function itself: `key=len`.

> **Pitfall:** sorting numbers that are still strings: `sorted(["10", "9"])`
> gives `['10', '9']` (alphabetical). Convert first, or use `key=int`.
""",
        examples=[
            dict(title="key functions",
                 code="""\
words = ["kiwi", "fig", "banana", "apple"]
print(sorted(words))
print(sorted(words, key=len))
print(sorted(words, key=lambda w: w[-1]))
print(max(words, key=len))
""",
                 explain="key=len passes the built-in len function; lambda sorts by last letter."),
            dict(title="Multi-key sort",
                 code="""\
people = [("Bob", 91), ("Ada", 85), ("Al", 91)]
print(sorted(people, key=lambda p: p[1], reverse=True))
print(sorted(people, key=lambda p: (-p[1], p[0])))
""",
                 explain="Negate the score for descending; the name ascending breaks ties."),
            dict(title="Strings that look like numbers",
                 code="""\
vals = input().split()
print(sorted(vals))
print(sorted(vals, key=int))
""",
                 stdin="10 9 100 1\n",
                 explain="Text sorts character by character; key=int compares numerically."),
        ],
        challenge=dict(
            prompt=("Read a line of words. Print them sorted by length (shortest first); words "
                    "of the same length go in alphabetical order. Output on one line, separated "
                    "by spaces."),
            starter="words = input().split()\n# sorted(words, key=lambda w: ...)\n",
            solution="words = input().split()\nprint(' '.join(sorted(words, key=lambda w: (len(w), w))))\n",
            samples=["pear fig apple kiwi date\n"],
            tests=["one\n", "bb aa c ccc a\n", "zebra ant moose cat\n"],
        ),
    ),
    dict(
        id="py-recursion",
        track="python",
        unit="Functions",
        title="Recursion",
        summary="Functions that call themselves: base case, recursive case, and the call stack.",
        body=r"""
A **recursive** function solves a problem by calling itself on a *smaller*
version of the same problem:

```python
def factorial(n):
    if n == 0:              # base case: answer known directly
        return 1
    return n * factorial(n - 1)   # recursive case: smaller problem
```

Every recursive function needs:

1. a **base case** that stops the recursion, and
2. a **recursive case** that moves *towards* the base case.

Forget either and you get infinite recursion, which Python stops with a
`RecursionError` after about 1000 nested calls.

### How it runs

Each call waits on a **call stack** until the inner call returns:
`factorial(3)` -> `3 * factorial(2)` -> `3 * 2 * factorial(1)` -> ... -> `6`.

> **Pitfall:** Python's default depth limit (~1000) is low. Recursing once
> per element of a 100 000-item list will crash; use a loop there, or
> `sys.setrecursionlimit` with care.

### Where recursion shines

Problems that branch naturally - trees, nested structures, generating all
combinations:

```python
def binary(prefix, n):
    if n == 0:
        print(prefix)
        return
    binary(prefix + "0", n - 1)
    binary(prefix + "1", n - 1)
```

### Memoisation

Naive Fibonacci recomputes the same values exponentially many times. Cache
results with `functools.lru_cache` and it becomes instant:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

This "recursion + cache" idea is the doorway to dynamic programming.
""",
        examples=[
            dict(title="Factorial",
                 code="""\
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

print(factorial(5))
print(factorial(int(input())))
""",
                 stdin="20\n",
                 explain="Each call handles one n and delegates the rest to a smaller call."),
            dict(title="Memoised Fibonacci",
                 code="""\
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(10), fib(90))
""",
                 explain="Without the cache fib(90) would take longer than the age of the universe."),
            dict(title="Depth limit",
                 code="""\
def depth(n):
    return 0 if n == 0 else 1 + depth(n - 1)

print(depth(500))
try:
    depth(100000)
except RecursionError:
    print("RecursionError: too deep")
""",
                 explain="Deep linear recursion is better written as a loop in Python."),
        ],
        challenge=dict(
            prompt=("Read `n` (1 <= n <= 4). Using recursion, print every binary string of length "
                    "`n` in increasing order, one per line (`n = 2` gives `00`, `01`, `10`, `11`)."),
            starter=("def gen(prefix, n):\n    # base case: n == 0 -> print prefix\n"
                     "    # otherwise recurse with prefix + '0' and prefix + '1'\n    pass\n\n"
                     "gen('', int(input()))\n"),
            solution=("def gen(prefix, n):\n    if n == 0:\n        print(prefix)\n        return\n"
                      "    gen(prefix + '0', n - 1)\n    gen(prefix + '1', n - 1)\n\n"
                      "gen('', int(input()))\n"),
            samples=["2\n"],
            tests=["1\n", "3\n", "4\n"],
            checker="exact",
        ),
    ),
]
