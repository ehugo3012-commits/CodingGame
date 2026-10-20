"""Math & Data: everyday data wrangling with NumPy (masks, bins, windows, fits, distances)."""


def _gen_sensor(rng):
    out = []
    for _ in range(4):
        n = rng.randint(1, 40)
        vals = [rng.choice([-1, rng.randint(-50, -1)]) if rng.random() < 0.3 else rng.randint(0, 100)
                for _ in range(n)]
        if all(v < 0 for v in vals):
            vals[rng.randrange(n)] = rng.randint(0, 100)
        out.append(f"{n} {rng.randint(0, 100)}\n" + " ".join(map(str, vals)))
    return out


def _gen_hist(rng):
    out = []
    for _ in range(3):
        n = rng.randint(1, 80)
        mu = rng.randint(30, 90)
        vals = [min(100, max(0, int(rng.gauss(mu, 15)))) for _ in range(n)]
        out.append(f"{n}\n" + " ".join(map(str, vals)))
    return out


def _gen_window(rng):
    out = []
    for _ in range(3):
        n = rng.randint(1, 60)
        k = rng.randint(1, min(n, 20))
        out.append(f"{n} {k}\n" + " ".join(str(rng.randint(-100, 100)) for _ in range(n)))
    return out


def _gen_fit(rng):
    out = []
    for noise in (0, 2, 10, 30):
        n = rng.randint(2, 25)
        m, c = rng.randint(-5, 5), rng.randint(-20, 20)
        while True:
            xs = [rng.randint(-50, 50) for _ in range(n)]
            ys = [m * x + c + rng.randint(-noise, noise) for x in xs]
            if len(set(xs)) > 1 and len(set(ys)) > 1:
                break
        q = rng.randint(1, 4)
        qs = [rng.randint(-60, 60) for _ in range(q)]
        pts = "\n".join(f"{x} {y}" for x, y in zip(xs, ys))
        out.append(f"{n}\n{pts}\n{q}\n{' '.join(map(str, qs))}")
    return out


def _gen_points(rng):
    out = []
    for d in (1, 2, 3, 4):
        n = rng.randint(2, 30)
        span = rng.choice([3, 20, 100])
        pts = [" ".join(str(rng.randint(-span, span)) for _ in range(d)) for _ in range(n)]
        out.append(f"{n} {d}\n" + "\n".join(pts))
    return out


PROBLEMS = [
    dict(
        id="md-boolean-filter",
        title="Sensor Clean-up",
        difficulty="easy",
        category="Math & Data",
        languages=["python"],
        tags=["numpy", "boolean-mask", "data-cleaning"],
        inspired_by="Kaggle-style missing-value imputation",
        statement="""
A greenhouse humidity sensor logs one integer reading per hour. Unfortunately
it sometimes glitches and logs a **negative** number — those readings are
invalid. Readings ≥ 0 are valid.

Clean up the log:

1. Count the valid readings.
2. Compute the mean of the valid readings.
3. List the valid readings that are **strictly greater** than a threshold `T`,
   in their original order.
4. Produce a repaired log in which every invalid reading is replaced by the
   mean from step 2 (valid readings are kept as they are).

NumPy makes this easy with **boolean masks**: `a >= 0` is an array of
`True`/`False` values that can select elements, `a[a >= 0]`.
""",
        input_format="""
First line: `n T` (1 ≤ n ≤ 100, 0 ≤ T ≤ 100).
Second line: `n` integers, the readings (−100 ≤ reading ≤ 100). At least one reading is valid.
""",
        output_format="""
Line 1: the number of valid readings.
Line 2: their mean.
Line 3: the valid readings greater than `T`, separated by spaces, or `NONE` if there are none.
Line 4: the `n` values of the repaired log, separated by spaces.

Print the mean and every value of the repaired log with 6 decimal places (answers within 10⁻⁶ are accepted).
""",
        hints=[
            "`mask = a >= 0` gives a boolean array; `a[mask]` keeps only the valid readings and "
            "`mask.sum()` counts the `True` values.",
            "Masks combine with `&` (and) / `|` (or): `a[(a >= 0) & (a > T)]` — the parentheses are required.",
            "`np.where(mask, a, value)` picks `a` where the mask is True and `value` elsewhere.",
        ],
        samples=["6 50\n40 -1 70 55 -1 30"],
        tests=["1 0\n0", "3 100\n100 -5 100", "5 10\n-1 -1 -1 -1 7", "4 0\n1 2 3 4"],
        gen=_gen_sensor,
        checker="float",
        time_limit=5,
        starter_python="""import numpy as np

n, T = map(int, input().split())
a = np.array(input().split(), dtype=int)

# TODO: count, mean, readings above T, repaired log
""",
        solution_python="""import numpy as np

n, T = map(int, input().split())
a = np.array(input().split(), dtype=int)
valid = a >= 0
mean = a[valid].mean()
print(int(valid.sum()))
print(f"{mean:.6f}")
above = a[valid & (a > T)]
print(" ".join(map(str, above)) if above.size else "NONE")
fixed = np.where(valid, a, mean)
print(" ".join(f"{v:.6f}" for v in fixed))
""",
    ),
    dict(
        id="md-histogram-bins",
        title="Grade Histogram",
        difficulty="easy",
        category="Math & Data",
        languages=["python"],
        tags=["numpy", "histogram", "bincount"],
        inspired_by="Kaggle-style exploratory data analysis (histograms)",
        statement="""
A teacher wants a quick histogram of exam scores (integers from 0 to 100)
using ten bins:

`0-9`, `10-19`, `20-29`, …, `80-89`, and a last bin `90-100` that also
includes perfect scores of 100.

Print how many scores fall into each bin, and the label of the fullest bin
(if several bins tie, the one with the lowest scores).
""",
        input_format="First line: `n` (1 ≤ n ≤ 200). Second line: `n` integer scores (0 ≤ score ≤ 100).",
        output_format="""
Line 1: ten integers, the counts for the bins in order.
Line 2: the label of the fullest bin, exactly as written above (e.g. `70-79` or `90-100`).
""",
        hints=[
            "Integer division finds the bin: `scores // 10` maps 0–9 to 0, 10–19 to 1, … but 100 lands in bin 10.",
            "`np.minimum(arr, 9)` caps every value at 9, fixing the 100 problem.",
            "`np.bincount(bins, minlength=10)` counts how often each bin number occurs; `np.argmax` finds the fullest.",
        ],
        samples=["8\n55 67 72 78 90 100 34 71"],
        tests=["1\n100", "1\n0", "4\n9 10 19 20", "10\n0 10 20 30 40 50 60 70 80 90"],
        gen=_gen_hist,
        time_limit=5,
        starter_python="""import numpy as np

n = int(input())
scores = np.array(input().split(), dtype=int)

# TODO: count the scores per bin and find the fullest bin
""",
        solution_python="""import numpy as np

n = int(input())
scores = np.array(input().split(), dtype=int)
counts = np.bincount(np.minimum(scores // 10, 9), minlength=10)
print(*counts)
b = int(np.argmax(counts))
print(f"{10 * b}-{10 * b + 9}" if b < 9 else "90-100")
""",
    ),
    dict(
        id="md-moving-average",
        title="Moving Average",
        difficulty="easy",
        category="Math & Data",
        languages=["python"],
        tags=["numpy", "convolution", "time-series", "smoothing"],
        inspired_by="Kaggle-style time-series smoothing (rolling mean)",
        statement="""
Daily step counts are noisy; a **moving average** smooths them out. With a
window of size `k`, the smoothed series has one value per complete window:
the average of values `1..k`, then `2..k+1`, and so on — `n − k + 1` values
in total.

Print the moving averages, and the (1-based) starting position of the window
with the **largest** average (the earliest one if several tie).

A neat NumPy trick: a moving sum is a **convolution** of the data with an
array of `k` ones.
""",
        input_format="""
First line: `n k` (1 ≤ k ≤ n ≤ 200, k ≤ 20).
Second line: `n` integers (|value| ≤ 1000).
""",
        output_format="""
Line 1: the `n − k + 1` moving averages separated by spaces, each with 6 decimal places
(answers within 10⁻⁶ are accepted).
Line 2: the starting position of the best window.
""",
        hints=[
            "`np.convolve(a, np.ones(k), mode=\"valid\")` returns exactly the `n − k + 1` window sums.",
            "Divide the sums by `k` to get the averages.",
            "To find the best window use `np.argmax` on the window **sums** (exact integers) rather than the "
            "divided averages, so that ties are detected reliably. Remember positions are 1-based.",
            "Without convolution: with `c = np.cumsum(...)` padded by a leading 0, window sums are `c[k:] - c[:-k]`.",
        ],
        samples=["7 3\n4 8 6 -1 3 9 9"],
        tests=["1 1\n-5", "5 5\n1 2 3 4 5", "6 2\n3 3 3 3 3 3", "4 1\n-7 2 2 -7"],
        gen=_gen_window,
        checker="float",
        time_limit=5,
        starter_python="""import numpy as np

n, k = map(int, input().split())
a = np.array(input().split(), dtype=int)

# TODO: print the moving averages, then the start of the best window
""",
        solution_python="""import numpy as np

n, k = map(int, input().split())
a = np.array(input().split(), dtype=int)
sums = np.convolve(a, np.ones(k, dtype=int), mode="valid")
print(" ".join(f"{s / k:.6f}" for s in sums))
print(int(np.argmax(sums)) + 1)
""",
    ),
    dict(
        id="md-least-squares-line",
        title="Line of Best Fit",
        difficulty="medium",
        category="Math & Data",
        languages=["python"],
        tags=["numpy", "regression", "least-squares", "polyfit", "statistics"],
        inspired_by="Kaggle-style linear regression / MIT 18.06 least squares lecture",
        statement="""
Given `n` data points (xᵢ, yᵢ), the **least-squares line** `y = m·x + c` is the
one that minimises the sum of squared vertical errors Σ (yᵢ − (m·xᵢ + c))².

Find `m` and `c`, use the line to predict `y` for some new `x` values, and
report how well the line fits with the **coefficient of determination**

R² = 1 − Σ (yᵢ − ŷᵢ)² / Σ (yᵢ − ȳ)²

where ŷᵢ = m·xᵢ + c are the fitted values and ȳ is the mean of the yᵢ.
R² = 1 means a perfect fit.
""",
        input_format="""
First line: `n` (2 ≤ n ≤ 50). Next `n` lines: two integers `x y` (|x|, |y| ≤ 1000).
Then a line with `q` (1 ≤ q ≤ 10) and a line with `q` integers — the `x` values to predict.
The `x` values of the data are not all equal, and neither are the `y` values.
""",
        output_format="""
Line 1: `m c`.
Line 2: the `q` predictions, separated by spaces.
Line 3: R².

Print every number with 6 decimal places (answers within 10⁻⁶ are accepted).
""",
        hints=[
            "`np.polyfit(x, y, 1)` fits a degree-1 polynomial and returns `[m, c]` (highest power first).",
            "`np.polyval([m, c], xs)` evaluates the line at every value in `xs` at once.",
            "For R², compute the fitted values for the data's own x's, then two sums of squares with `np.sum(...)`.",
            "Shortcut worth knowing: for a straight-line fit, R² equals the squared correlation, "
            "`np.corrcoef(x, y)[0, 1] ** 2`.",
        ],
        samples=["4\n0 1\n1 3\n2 5\n3 7\n2\n4 -1", "3\n0 0\n1 1\n2 1\n1\n3"],
        tests=["2\n-5 10\n5 -10\n1\n0", "5\n1 2\n2 1\n3 4\n4 3\n5 5\n3\n0 6 100"],
        gen=_gen_fit,
        checker="float",
        time_limit=5,
        starter_python="""import sys
import numpy as np

data = sys.stdin.read().split()
n = int(data[0])
pts = np.array(data[1:1 + 2 * n], dtype=float).reshape(n, 2)
x, y = pts[:, 0], pts[:, 1]
q = int(data[1 + 2 * n])
queries = np.array(data[2 + 2 * n:2 + 2 * n + q], dtype=float)

# TODO: fit the line, print m c, the predictions, and R^2
""",
        solution_python="""import sys
import numpy as np

data = sys.stdin.read().split()
n = int(data[0])
pts = np.array(data[1:1 + 2 * n], dtype=float).reshape(n, 2)
x, y = pts[:, 0], pts[:, 1]
q = int(data[1 + 2 * n])
queries = np.array(data[2 + 2 * n:2 + 2 * n + q], dtype=float)

m, c = np.polyfit(x, y, 1)
pred = np.polyval([m, c], queries)
fitted = m * x + c
r2 = 1 - np.sum((y - fitted) ** 2) / np.sum((y - y.mean()) ** 2)
print(f"{m:.6f} {c:.6f}")
print(" ".join(f"{v:.6f}" for v in pred))
print(f"{r2:.6f}")
""",
    ),
    dict(
        id="md-pairwise-distances",
        title="Nearest Neighbours",
        difficulty="medium",
        category="Math & Data",
        languages=["python"],
        tags=["numpy", "broadcasting", "distances", "nearest-neighbour"],
        inspired_by="k-nearest-neighbours classifier (Kaggle-style), vectorised distance matrix",
        statement="""
The k-nearest-neighbours algorithm classifies a point by looking at the
points closest to it. Its core is the **distance matrix**: the Euclidean
distance between every pair of points,

dist(p, q) = √( Σⱼ (pⱼ − qⱼ)² ).

For each of the `n` points (in `d` dimensions), find its nearest **other**
point. If several points are equally close, choose the one with the smallest
index.

Try to do it without any Python loop over pairs — with **broadcasting**, an
`(n, 1, d)` array minus a `(1, n, d)` array gives all `n × n` differences at
once.
""",
        input_format="""
First line: `n d` (2 ≤ n ≤ 40, 1 ≤ d ≤ 4).
Next `n` lines: `d` integers each, the coordinates of a point (|coordinate| ≤ 100).
Points may coincide.
""",
        output_format="""
`n` lines; line `i` contains the 1-based index of the nearest other point to point `i`
and the distance to it, printed with 6 decimal places (answers within 10⁻⁶ are accepted).
""",
        hints=[
            "With `P` of shape `(n, d)`, `diff = P[:, None, :] - P[None, :, :]` has shape `(n, n, d)`.",
            "Square, sum over the last axis (`axis=2`) and take `np.sqrt` to get the `n × n` distance matrix.",
            "A point is always at distance 0 from itself — overwrite the diagonal first: "
            "`np.fill_diagonal(D, np.inf)`. Then `D.argmin(axis=1)` gives each row's nearest index "
            "(the first one on ties).",
        ],
        samples=["4 2\n0 0\n3 4\n1 1\n10 10"],
        tests=["2 1\n5\n-5", "3 2\n1 1\n1 1\n2 2", "3 3\n0 0 0\n1 0 0\n0 1 0"],
        gen=_gen_points,
        checker="float",
        time_limit=5,
        starter_python="""import sys
import numpy as np

data = sys.stdin.read().split()
n, d = int(data[0]), int(data[1])
P = np.array(data[2:2 + n * d], dtype=float).reshape(n, d)

# TODO: build the distance matrix and report each point's nearest neighbour
""",
        solution_python="""import sys
import numpy as np

data = sys.stdin.read().split()
n, d = int(data[0]), int(data[1])
P = np.array(data[2:2 + n * d], dtype=np.int64).reshape(n, d)
sq = ((P[:, None, :] - P[None, :, :]) ** 2).sum(axis=2)  # exact integers
best = np.where(np.eye(n, dtype=bool), np.iinfo(np.int64).max, sq).argmin(axis=1)
for i, j in enumerate(best):
    print(int(j) + 1, f"{np.sqrt(sq[i, j]):.6f}")
""",
    ),
]
