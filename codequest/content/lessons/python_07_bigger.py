"""Python track - Unit 7: Bigger Ideas (exceptions, classes, NumPy, SymPy)."""

LESSONS = [
    dict(
        id="py-exceptions",
        track="python",
        unit="Bigger Ideas",
        title="Exceptions: try / except",
        summary="Handle errors gracefully instead of crashing.",
        body=r"""
When something goes wrong, Python **raises an exception**: `ValueError`
for `int("abc")`, `ZeroDivisionError` for `1 / 0`, `KeyError`,
`IndexError`... Unhandled, it stops the program with a traceback. With
`try`/`except` you can catch it and carry on:

```python
try:
    n = int(input())
except ValueError:
    print("that was not a number")
    n = 0
```

Python runs the `try` block; if a matching exception happens, it jumps to
the `except` block. Optional extras:

```python
try:
    result = a / b
except ZeroDivisionError:
    print("can't divide by zero")
else:
    print(result)          # only if no exception
finally:
    print("always runs")   # cleanup, success or not
```

### Catch narrowly

> **Pitfall:** a bare `except:` (or `except Exception:`) also swallows the
> bugs you *didn't* expect - typos, wrong variable names - and hides them.
> Catch the specific exception you anticipate, and keep the `try` block
> small.

`except (ValueError, TypeError) as e:` catches several types and gives you
the exception object to print.

### Raising your own

```python
def withdraw(balance, amount):
    if amount > balance:
        raise ValueError("insufficient funds")
    return balance - amount
```

### "Easier to ask forgiveness"

Python style often just *tries* the operation and handles the failure
(EAFP), rather than checking everything first (LBYL). For instance,
attempting `int(token)` inside `try` is simpler and more reliable than
checking whether a string "looks like" an integer - think of `-5`, `+7` or
` 3`.
""",
        examples=[
            dict(title="Catching a ValueError",
                 code="""\
for text in ["42", "abc", "-7"]:
    try:
        print(int(text) * 2)
    except ValueError as e:
        print("bad input:", e)
""",
                 explain="The loop keeps going after the bad value."),
            dict(title="else and finally",
                 code="""\
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("can't divide by zero")
    else:
        print("result", result)
    finally:
        print("done")

divide(10, 4)
divide(1, 0)
""",
                 explain="else runs on success; finally runs every time."),
            dict(title="raise",
                 code="""\
def withdraw(balance, amount):
    if amount > balance:
        raise ValueError("insufficient funds")
    return balance - amount

print(withdraw(100, 30))
try:
    withdraw(10, 50)
except ValueError as e:
    print("refused:", e)
""",
                 explain="raise signals a problem; the caller decides how to handle it."),
        ],
        challenge=dict(
            prompt=("Each input line should contain an integer, but some lines are junk. Print "
                    "the sum of the valid integers, then (on the next line) how many lines were "
                    "invalid. Use `try` / `except ValueError`."),
            starter="import sys\ntotal = 0\nbad = 0\nfor line in sys.stdin:\n    # try int(line) ...\n    pass\nprint(total)\nprint(bad)\n",
            solution=("import sys\ntotal = 0\nbad = 0\nfor line in sys.stdin:\n    try:\n"
                      "        total += int(line)\n    except ValueError:\n        bad += 1\n"
                      "print(total)\nprint(bad)\n"),
            samples=["10\nabc\n-3\n4.5\n7\n"],
            tests=["1\n", "x\ny\n", " 5 \n+6\nfive\n12a\n"],
        ),
    ),
    dict(
        id="py-classes",
        track="python",
        unit="Bigger Ideas",
        title="Classes & Objects",
        summary="Bundle data and behaviour together with class, __init__ and methods.",
        body=r"""
A **class** is a blueprint; **objects** (instances) are things built from
it. Each object carries its own data (**attributes**) and shares the
class's functions (**methods**).

```python
class Counter:
    def __init__(self, start=0):
        self.value = start        # attribute

    def increment(self, step=1):  # method
        self.value += step

    def __repr__(self):
        return f"Counter({self.value})"

c = Counter()
c.increment()
c.increment(5)
print(c.value)    # 6
print(c)          # Counter(6)
```

- `__init__` runs automatically when you create an object; it sets up the
  attributes.
- `self` is the object the method was called on. `c.increment(5)` is
  really `Counter.increment(c, 5)`.
- `__repr__` (or `__str__`) controls how the object prints.

> **Pitfall:** forgetting `self`. Every method needs `self` as its first
> parameter, and attributes must be written `self.value` - a plain `value`
> inside a method is just a local variable that vanishes.

### Why classes?

When several pieces of data always travel together and have rules about
how they change - an account with a balance that must never go negative, a
game character with health and position - a class keeps the data and the
rules in one place. Code outside calls `account.withdraw(30)` instead of
poking at the balance directly.

For simple bundles of fields, `@dataclass` from the `dataclasses` module
writes `__init__` and `__repr__` for you.

Each object is independent: two `Counter()`s have separate `value`s.
""",
        examples=[
            dict(title="A Counter class",
                 code="""\
class Counter:
    def __init__(self, start=0):
        self.value = start

    def increment(self, step=1):
        self.value += step

    def __repr__(self):
        return f"Counter({self.value})"

a = Counter()
b = Counter(10)
a.increment()
a.increment(5)
print(a, b, a.value + b.value)
""",
                 explain="a and b are separate objects with their own value."),
            dict(title="Rules inside methods",
                 code="""\
class Account:
    def __init__(self, owner):
        self.owner = owner
        self.balance = 0

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

acc = Account(input())
acc.deposit(50)
print(acc.withdraw(80), acc.withdraw(20), acc.owner, acc.balance)
""",
                 stdin="Ada\n",
                 explain="The class guarantees the balance never goes negative."),
            dict(title="dataclass",
                 code="""\
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

    def dist2(self):
        return self.x ** 2 + self.y ** 2

p = Point(3, 4)
print(p, p.dist2(), p == Point(3, 4))
""",
                 explain="@dataclass generates __init__, __repr__ and == for you."),
        ],
        challenge=dict(
            prompt=("Complete the `Account` class. Each input line is a command: `deposit X`, "
                    "`withdraw X` or `balance`. A withdrawal larger than the balance is refused "
                    "and prints `insufficient`. `balance` prints the current balance. The account "
                    "starts at 0."),
            starter=("import sys\n\nclass Account:\n    def __init__(self):\n        self.balance = 0\n\n"
                     "    def deposit(self, amount):\n        pass\n\n"
                     "    def withdraw(self, amount):\n        # return False if not enough money\n        pass\n\n"
                     "acc = Account()\nfor line in sys.stdin:\n    parts = line.split()\n"
                     "    if not parts:\n        continue\n"
                     "    if parts[0] == 'deposit':\n        acc.deposit(int(parts[1]))\n"
                     "    elif parts[0] == 'withdraw':\n        if not acc.withdraw(int(parts[1])):\n"
                     "            print('insufficient')\n    else:\n        print(acc.balance)\n"),
            solution=("import sys\n\nclass Account:\n    def __init__(self):\n        self.balance = 0\n\n"
                      "    def deposit(self, amount):\n        self.balance += amount\n\n"
                      "    def withdraw(self, amount):\n        if amount > self.balance:\n"
                      "            return False\n        self.balance -= amount\n        return True\n\n"
                      "acc = Account()\nfor line in sys.stdin:\n    parts = line.split()\n"
                      "    if not parts:\n        continue\n"
                      "    if parts[0] == 'deposit':\n        acc.deposit(int(parts[1]))\n"
                      "    elif parts[0] == 'withdraw':\n        if not acc.withdraw(int(parts[1])):\n"
                      "            print('insufficient')\n    else:\n        print(acc.balance)\n"),
            samples=["deposit 50\nwithdraw 30\nwithdraw 100\nbalance\n"],
            tests=["balance\n", "withdraw 1\ndeposit 5\nwithdraw 5\nbalance\n",
                   "deposit 10\ndeposit 20\nbalance\nwithdraw 30\nbalance\n"],
        ),
    ),
    dict(
        id="py-numpy-intro",
        track="python",
        unit="Bigger Ideas",
        title="NumPy in 5 Minutes",
        summary="Fast arrays and vectorised maths - the foundation of scientific Python.",
        body=r"""
**NumPy** gives Python a fast array type, `ndarray`. All elements share one
type and live in one block of memory, and operations run in compiled C -
often 10-100x faster than Python loops.

```python
import numpy as np
a = np.array([1, 2, 3, 4])
a * 2          # array([2, 4, 6, 8])
a + a          # array([2, 4, 6, 8])
a ** 2         # array([ 1,  4,  9, 16])
```

Operations apply to **every element at once** - this is called
**vectorisation**. No loop needed.

> **Pitfall:** with Python lists, `[1, 2] * 2` is `[1, 2, 1, 2]`
> (repetition) and `[1, 2] + [3, 4]` concatenates. With arrays the same
> operators do element-wise maths.

### Summaries

```python
a.sum(), a.mean(), a.max(), a.min(), a.std()
np.arange(0, 10, 2)        # array([0, 2, 4, 6, 8]) - like range
np.linspace(0, 1, 5)       # 5 evenly spaced points from 0 to 1
```

### Boolean masks

Comparisons also work element-wise and give arrays of `True`/`False`,
which you can use to **filter**:

```python
a > 2              # array([False, False,  True,  True])
a[a > 2]           # array([3, 4])
(a > 2).sum()      # 2 - True counts as 1
```

### 2-D arrays

```python
m = np.array([[1, 2], [3, 4]])
m.shape            # (2, 2)
m.sum(axis=0)      # column sums: array([4, 6])
m @ m              # matrix multiplication
```

> **Pitfall:** NumPy integers have a fixed size (usually 64-bit) and can
> silently overflow, unlike Python ints. And printing a NumPy scalar may
> show `np.float64(2.5)` in `repr` - convert with `float()` or format with
> an f-string for clean output.
""",
        examples=[
            dict(title="Vectorised maths",
                 code="""\
import numpy as np
a = np.array([1, 2, 3, 4])
print(a * 2, a + a, a ** 2)
print([1, 2] * 2, np.array([1, 2]) * 2)
print(np.arange(0, 10, 2), np.linspace(0, 1, 5))
""",
                 explain="Lists repeat; arrays multiply each element."),
            dict(title="Statistics and masks",
                 code="""\
import numpy as np
a = np.array(list(map(float, input().split())))
print(f"sum={a.sum():.1f} mean={a.mean():.2f} max={a.max():.1f}")
print("above mean:", a[a > a.mean()])
print("count:", int((a > a.mean()).sum()))
""",
                 stdin="3 7 1 9 5 6\n",
                 explain="a > a.mean() is a True/False array used to filter."),
            dict(title="2-D arrays",
                 code="""\
import numpy as np
m = np.array([[1, 2], [3, 4]])
print(m.shape)
print(m.sum(axis=0), m.sum(axis=1))
print(m @ m)
""",
                 explain="axis=0 collapses rows (column sums); @ is matrix multiplication."),
        ],
        challenge=dict(
            prompt=("Read a line of numbers. Using NumPy, print their mean rounded to 2 decimals "
                    "(`f\"{x:.2f}\"`), and on the next line how many numbers are **strictly "
                    "greater** than the mean."),
            starter="import numpy as np\na = np.array(list(map(float, input().split())))\n# mean and a boolean mask\n",
            solution=("import numpy as np\na = np.array(list(map(float, input().split())))\nm = a.mean()\n"
                      "print(f\"{m:.2f}\")\nprint(int((a > m).sum()))\n"),
            samples=["3 7 1 9 5 6\n"],
            tests=["5\n", "1 2\n", "-1.5 2.25 10 0 0\n"],
            checker="float",
        ),
    ),
    dict(
        id="py-sympy-intro",
        track="python",
        unit="Bigger Ideas",
        title="SymPy: Algebra by Computer",
        summary="Exact symbolic maths: expand, factor, differentiate and solve equations.",
        body=r"""
NumPy crunches **numbers**. **SymPy** manipulates **symbols** - it does
algebra the way you would on paper, exactly, with no rounding.

```python
from sympy import symbols, expand, factor, diff, solve, sqrt, Rational
x, y = symbols("x y")
```

You must declare symbols before using them; a plain `x` is otherwise a
`NameError`.

### Algebra

```python
expand((x + 1) ** 2)        # x**2 + 2*x + 1
factor(x**2 - 5*x + 6)      # (x - 3)*(x - 2)
(x**2 - 1) / (x - 1)        # stays as written...
from sympy import simplify
simplify((x**2 - 1) / (x - 1))   # x + 1
```

### Calculus

```python
diff(x**3 + 2*x, x)         # 3*x**2 + 2
from sympy import integrate
integrate(2*x, x)           # x**2
```

### Solving equations

`solve(expr, x)` finds where `expr == 0`:

```python
solve(x**2 - 4, x)          # [-2, 2]
from sympy import Eq
solve(Eq(2*x + 1, 7), x)    # [3]
```

### Exact numbers

`sqrt(8)` gives `2*sqrt(2)`, not `2.828...`, and `Rational(1, 3)` is
exactly one third. Call `.evalf()` or `float(...)` when you want a decimal.
Substitute values with `expr.subs(x, 2)`.

> **Pitfall:** `1/3` in Python is already the float `0.333...` before SymPy
> sees it. Write `Rational(1, 3)` (or `x / 3`) to stay exact.

> **Pitfall:** `^` is XOR in Python, not power. Use `**`.

To turn text such as `"x**2 + 1"` into an expression, use `sympify(text)`.
""",
        examples=[
            dict(title="Expand, factor, simplify",
                 code="""\
from sympy import symbols, expand, factor, simplify
x = symbols("x")
print(expand((x + 1) ** 3))
print(factor(x**2 - 5*x + 6))
print(simplify((x**2 - 1) / (x - 1)))
""",
                 explain="SymPy rewrites expressions exactly, like algebra on paper."),
            dict(title="Calculus and solving",
                 code="""\
from sympy import symbols, diff, integrate, solve, Eq
x = symbols("x")
f = x**3 - 3*x
print(diff(f, x))
print(integrate(2*x, x))
print(solve(diff(f, x), x))
print(solve(Eq(2*x + 1, 7), x))
""",
                 explain="Setting the derivative to zero finds the turning points."),
            dict(title="From text, exactly",
                 code="""\
from sympy import sympify, symbols, sqrt, Rational
x = symbols("x")
expr = sympify(input())
print(expr, "at x=2:", expr.subs(x, 2))
print(sqrt(8), Rational(1, 3) + Rational(1, 6), (sqrt(2) ** 2))
print(sqrt(8).evalf(6))
""",
                 stdin="x**2 + 3*x - 1\n",
                 explain="sympify parses text; results stay exact until you call evalf."),
        ],
        challenge=dict(
            prompt=("Read a polynomial in `x` (written with `**` for powers). Print its derivative "
                    "on the first line, and the value of that derivative at `x = 2` on the "
                    "second line. Any algebraically equal form is accepted."),
            starter="from sympy import symbols, sympify, diff\nx = symbols('x')\nexpr = sympify(input())\n# differentiate and substitute\n",
            solution=("from sympy import symbols, sympify, diff\nx = symbols('x')\nexpr = sympify(input())\n"
                      "d = diff(expr, x)\nprint(d)\nprint(d.subs(x, 2))\n"),
            samples=["x**3 + 2*x\n"],
            tests=["5*x\n", "x**4 - 3*x**2 + 7\n", "(x + 1)**2\n"],
            checker="sympy",
        ),
    ),
]
