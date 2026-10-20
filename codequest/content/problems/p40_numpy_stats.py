"""Math & Data: first steps with NumPy arrays and descriptive statistics."""


def _nums(rng, n, lo, hi, decimals=False):
    if decimals:
        return [f"{rng.randint(lo * 100, hi * 100) / 100:.2f}" for _ in range(n)]
    return [str(rng.randint(lo, hi)) for _ in range(n)]


def _gen_stats(rng):
    out = []
    for decimals in (False, True, False, True):
        n = rng.randint(1, 40)
        out.append(f"{n}\n" + " ".join(_nums(rng, n, -1000, 1000, decimals)))
    return out


def _gen_vectors(rng):
    out = []
    for _ in range(3):
        n = rng.randint(1, 30)
        a = _nums(rng, n, -1000, 1000)
        b = _nums(rng, n, -1000, 1000)
        out.append(f"{n}\n{' '.join(a)}\n{' '.join(b)}")
    return out


def _gen_running(rng):
    out = []
    for _ in range(3):
        n = rng.randint(1, 60)
        out.append(f"{n}\n" + " ".join(_nums(rng, n, -500, 500)))
    return out


def _gen_zscores(rng):
    out = []
    for decimals in (False, True, False):
        n = rng.randint(2, 30)
        vals = _nums(rng, n, -100, 100, decimals)
        while len(set(vals)) == 1:
            vals = _nums(rng, n, -100, 100, decimals)
        out.append(f"{n}\n" + " ".join(vals))
    return out


PROBLEMS = [
    dict(
        id="md-dataset-stats",
        title="Dataset Summary",
        difficulty="beginner",
        category="Math & Data",
        languages=["python"],
        tags=["numpy", "statistics", "mean", "median"],
        inspired_by="Kaggle-style exploratory data analysis (describe())",
        statement="""
Before any data scientist trains a model, they *look* at the numbers. The
quickest look is a three-number summary:

* the **mean** (the average),
* the **median** (the middle value once sorted; for an even count, the average
  of the two middle values),
* the **standard deviation** — how spread out the values are. Use the
  *population* standard deviation:
  σ = √( Σ (xᵢ − mean)² / n ).

NumPy computes all three in one call each. This problem is your excuse to meet
`numpy` arrays.
""",
        input_format="First line: `n` (1 ≤ n ≤ 100). Second line: `n` numbers (integers or decimals, |value| ≤ 1000).",
        output_format="""
Three lines: the mean, the median and the population standard deviation.

Print each value with 6 decimal places, e.g. `print(f"{value:.6f}")`.
Answers within 10⁻⁶ of the expected value are accepted.
""",
        hints=[
            "Turn the input tokens into a NumPy array of floats: `a = np.array(tokens, dtype=float)`.",
            "`np.mean(a)` and `np.median(a)` do exactly what their names say.",
            "`np.std(a)` is the *population* standard deviation by default (`ddof=0`). "
            "`ddof=1` would give the sample version — not what we want here.",
        ],
        samples=["5\n2 4 4 4 5", "4\n1.5 -2 10 3"],
        tests=["1\n7", "2\n-1000 1000", "6\n0 0 0 0 0 0", "7\n3.25 -1.75 8 8 2.5 -100 0.01"],
        gen=_gen_stats,
        checker="float",
        time_limit=5,
        starter_python="""import sys
import numpy as np

data = sys.stdin.read().split()
n = int(data[0])
a = np.array(data[1:n + 1], dtype=float)

# TODO: print the mean, the median and the population standard deviation
""",
        solution_python="""import sys
import numpy as np

data = sys.stdin.read().split()
n = int(data[0])
a = np.array(data[1:n + 1], dtype=float)
for v in (np.mean(a), np.median(a), np.std(a)):
    print(f"{v:.6f}")
""",
    ),
    dict(
        id="md-vector-ops",
        title="Vector Arithmetic",
        difficulty="beginner",
        category="Math & Data",
        languages=["python"],
        tags=["numpy", "vectorisation", "dot-product"],
        inspired_by="MIT 18.06 Linear Algebra, lecture 1 exercise",
        statement="""
NumPy's superpower is **vectorisation**: `a + b` on two arrays adds them
element by element, with no Python loop.

Given two vectors `a` and `b` of the same length, print

1. their element-wise sum `a + b`,
2. their element-wise product `a * b`,
3. their **dot product** a·b = a₁b₁ + a₂b₂ + … + aₙbₙ.
""",
        input_format="""
First line: `n` (1 ≤ n ≤ 100).
Second line: `n` integers — vector `a`.
Third line: `n` integers — vector `b`. All values satisfy |value| ≤ 1000.
""",
        output_format="""
Line 1: the `n` entries of `a + b`, separated by spaces.
Line 2: the `n` entries of `a * b`, separated by spaces.
Line 3: the dot product (one integer).
""",
        hints=[
            "Make integer arrays: `a = np.array(line.split(), dtype=int)`.",
            "With arrays, `a + b` and `a * b` already work element-wise.",
            "`np.dot(a, b)` (or `a @ b`) gives the dot product. "
            "`print(*arr)` prints an array's entries separated by spaces.",
        ],
        samples=["3\n1 2 3\n4 5 6"],
        tests=["1\n-7\n3", "4\n0 0 0 0\n1 2 3 4", "5\n1000 -1000 1000 -1000 1000\n1000 1000 -1000 -1000 1000"],
        gen=_gen_vectors,
        time_limit=5,
        starter_python="""import numpy as np

n = int(input())
a = np.array(input().split(), dtype=int)
b = np.array(input().split(), dtype=int)

# TODO: print a + b, then a * b, then the dot product
""",
        solution_python="""import numpy as np

n = int(input())
a = np.array(input().split(), dtype=int)
b = np.array(input().split(), dtype=int)
print(*(a + b))
print(*(a * b))
print(int(np.dot(a, b)))
""",
    ),
    dict(
        id="md-running-total",
        title="Running Balance",
        difficulty="beginner",
        category="Math & Data",
        languages=["python"],
        tags=["numpy", "cumsum", "argmax"],
        inspired_by="Classic prefix-sum exercise (bank statement)",
        statement="""
Your savings account starts at 0. Each day you deposit (positive number) or
withdraw (negative number) some amount.

Print the **balance at the end of every day**, and then the day on which the
balance was **highest**. Days are numbered from 1; if the highest balance is
reached on several days, report the earliest one.

A running total like this is called a *cumulative sum* (or prefix sum), and
NumPy has a function for it.
""",
        input_format="First line: `n` (1 ≤ n ≤ 200). Second line: `n` integers, the daily changes (|change| ≤ 1000).",
        output_format="""
Line 1: the `n` end-of-day balances, separated by spaces.
Line 2: the (1-based) day with the highest balance.
""",
        hints=[
            "`np.cumsum(a)` returns the running totals of an array.",
            "`np.argmax(arr)` returns the **index** of the largest value — the first one if there are ties.",
            "Indices start at 0 but days start at 1, so add 1.",
        ],
        samples=["5\n10 -3 5 -20 4"],
        tests=["1\n-5", "3\n0 0 0", "4\n-1 -1 -1 -1", "6\n5 -5 5 -5 5 -5"],
        gen=_gen_running,
        time_limit=5,
        starter_python="""import numpy as np

n = int(input())
changes = np.array(input().split(), dtype=int)

# TODO: print the running balances, then the best day
""",
        solution_python="""import numpy as np

n = int(input())
changes = np.array(input().split(), dtype=int)
balance = np.cumsum(changes)
print(*balance)
print(int(np.argmax(balance)) + 1)
""",
    ),
    dict(
        id="md-z-scores",
        title="Normalising Data",
        difficulty="easy",
        category="Math & Data",
        languages=["python"],
        tags=["numpy", "statistics", "normalisation", "broadcasting"],
        inspired_by="Kaggle-style feature scaling (StandardScaler / MinMaxScaler)",
        statement="""
Machine-learning models usually prefer features on a common scale. Two
popular ways to rescale a column of numbers `x`:

* **Standardisation (z-scores):** zᵢ = (xᵢ − mean) / σ, where σ is the
  *population* standard deviation. The result has mean 0 and σ = 1.
* **Min–max scaling:** mᵢ = (xᵢ − min) / (max − min). The result lies in [0, 1].

Compute both for the given data. Subtracting a single number from a whole
array — `x - x.mean()` — is called **broadcasting**.
""",
        input_format="""
First line: `n` (2 ≤ n ≤ 100). Second line: `n` numbers (integers or decimals, |value| ≤ 100).
It is guaranteed that the values are not all equal.
""",
        output_format="""
Line 1: the `n` z-scores, separated by spaces.
Line 2: the `n` min–max scaled values, separated by spaces.

Print every value with 6 decimal places (answers within 10⁻⁶ are accepted).
""",
        hints=[
            "Read the values into a float array: `x = np.array(tokens, dtype=float)`.",
            "`x.mean()`, `x.std()`, `x.min()` and `x.max()` give single numbers; "
            "an expression like `(x - x.mean()) / x.std()` then works on every element at once.",
            "To print: `print(\" \".join(f\"{v:.6f}\" for v in z))`.",
        ],
        samples=["4\n2 4 4 6"],
        tests=["2\n-100 100", "5\n1 1 1 1 2", "6\n3.5 -2.25 0 0 10 7.75"],
        gen=_gen_zscores,
        checker="float",
        time_limit=5,
        starter_python="""import sys
import numpy as np

data = sys.stdin.read().split()
n = int(data[0])
x = np.array(data[1:n + 1], dtype=float)

# TODO: print the z-scores on one line, then the min-max scaled values
""",
        solution_python="""import sys
import numpy as np

data = sys.stdin.read().split()
n = int(data[0])
x = np.array(data[1:n + 1], dtype=float)
z = (x - x.mean()) / x.std()
m = (x - x.min()) / (x.max() - x.min())
print(" ".join(f"{v:.6f}" for v in z))
print(" ".join(f"{v:.6f}" for v in m))
""",
    ),
]
