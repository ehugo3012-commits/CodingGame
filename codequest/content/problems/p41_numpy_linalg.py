"""Math & Data: linear algebra with numpy.linalg."""

from fractions import Fraction


def _det(rows):
    """Exact determinant (Fraction Gaussian elimination) - used by generators only."""
    m = [[Fraction(v) for v in r] for r in rows]
    n, det = len(m), Fraction(1)
    for c in range(n):
        p = next((r for r in range(c, n) if m[r][c] != 0), None)
        if p is None:
            return Fraction(0)
        if p != c:
            m[c], m[p] = m[p], m[c]
            det = -det
        det *= m[c][c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            for k in range(c, n):
                m[r][k] -= f * m[c][k]
    return det


def _fmt(rows):
    return "\n".join(" ".join(map(str, r)) for r in rows)


def _gen_matmul(rng):
    out = []
    for _ in range(3):
        n, m, p = rng.randint(1, 6), rng.randint(1, 6), rng.randint(1, 6)
        a = [[rng.randint(-20, 20) for _ in range(m)] for _ in range(n)]
        b = [[rng.randint(-20, 20) for _ in range(p)] for _ in range(m)]
        out.append(f"{n} {m} {p}\n{_fmt(a)}\n{_fmt(b)}")
    return out


def _gen_linsys(rng):
    out = []
    for singular in (False, False, True, False):
        n = rng.randint(2, 5)
        while True:
            a = [[rng.randint(-9, 9) for _ in range(n)] for _ in range(n)]
            if singular:  # make one row a combination of others
                if n == 2:
                    a[1] = [2 * x for x in a[0]]
                else:
                    r1, r2, r3 = rng.sample(range(n), 3)
                    a[r3] = [x - y for x, y in zip(a[r1], a[r2])]
            if (_det(a) == 0) == singular:
                break
        b = [rng.randint(-50, 50) for _ in range(n)]
        out.append(f"{n}\n" + "\n".join(" ".join(map(str, r + [v])) for r, v in zip(a, b)))
    return out


def _gen_eig(rng):
    out = []
    for kind in ("any", "pd", "any", "pd"):
        n = rng.randint(2, 6)
        while True:
            if kind == "pd":
                m = [[rng.randint(-3, 3) for _ in range(n)] for _ in range(n)]
                a = [[sum(m[k][i] * m[k][j] for k in range(n)) + (i == j) for j in range(n)]
                     for i in range(n)]
            else:
                a = [[0] * n for _ in range(n)]
                for i in range(n):
                    for j in range(i, n):
                        a[i][j] = a[j][i] = rng.randint(-9, 9)
            if _det(a) != 0:
                break
        out.append(f"{n}\n{_fmt(a)}")
    return out


def _gen_markov(rng):
    out = []
    for k in (1, rng.randint(2, 20), rng.randint(10**5, 10**9), rng.randint(0, 3)):
        n = rng.randint(2, 6)
        w = [[rng.choice([0, 0, rng.randint(1, 9)]) for _ in range(n)] for _ in range(n)]
        for i in range(n):  # a cycle plus self-loops keeps the chain ergodic
            w[i][(i + 1) % n] = max(w[i][(i + 1) % n], 1)
            w[i][i] = max(w[i][i], 1)
        out.append(f"{n} {k}\n{_fmt(w)}")
    return out


PROBLEMS = [
    dict(
        id="md-matrix-multiply",
        title="Matrix Multiplication",
        difficulty="easy",
        category="Math & Data",
        languages=["python"],
        tags=["numpy", "matrices", "linear-algebra"],
        inspired_by="MIT 18.06 Linear Algebra, lecture 3 (multiplication)",
        statement="""
The product `C = A·B` of an `n×m` matrix `A` and an `m×p` matrix `B` is the
`n×p` matrix whose entry in row `i`, column `j` is the dot product of row `i`
of `A` with column `j` of `B`:

C[i][j] = Σₖ A[i][k] · B[k][j]

Writing three nested loops is a classic exercise — but in NumPy it is a single
operator. Compute `A·B`.

Careful: `A * B` in NumPy multiplies **element-wise**, which is *not* the
matrix product.
""",
        input_format="""
First line: `n m p` (1 ≤ n, m, p ≤ 8).
Next `n` lines: `m` integers each — matrix `A`.
Next `m` lines: `p` integers each — matrix `B`. All entries satisfy |value| ≤ 100.
""",
        output_format="`n` lines with `p` integers each: the matrix `A·B`.",
        hints=[
            "Read all numbers at once (`sys.stdin.read().split()`), then build `A` with "
            "`np.array(tokens, dtype=int).reshape(n, m)`.",
            "The matrix product is `A @ B` (or `np.matmul(A, B)` / `np.dot(A, B)`).",
            "Print each row with `print(*row)`.",
        ],
        samples=["2 3 2\n1 2 3\n4 5 6\n7 8\n9 10\n11 12"],
        tests=["1 1 1\n-5\n7", "1 3 1\n1 2 3\n4\n5\n6", "3 1 3\n1\n2\n3\n4 5 6",
               "2 2 2\n1 0\n0 1\n100 -100\n-100 100"],
        gen=_gen_matmul,
        time_limit=5,
        starter_python="""import sys
import numpy as np

data = sys.stdin.read().split()
n, m, p = map(int, data[:3])
nums = np.array(data[3:], dtype=int)
A = nums[:n * m].reshape(n, m)
B = nums[n * m:].reshape(m, p)

# TODO: print the matrix product, one row per line
""",
        solution_python="""import sys
import numpy as np

data = sys.stdin.read().split()
n, m, p = map(int, data[:3])
nums = np.array(data[3:], dtype=int)
A = nums[:n * m].reshape(n, m)
B = nums[n * m:].reshape(m, p)
for row in A @ B:
    print(*row)
""",
    ),
    dict(
        id="md-linear-system",
        title="Solve the System",
        difficulty="medium",
        category="Math & Data",
        languages=["python"],
        tags=["numpy", "linear-algebra", "linalg-solve", "rank"],
        inspired_by="MIT 18.06 Linear Algebra, elimination exercises",
        statement="""
A shop sells apples, bananas and cherries. Three customers' receipts give
three equations in three unknown prices — a **system of linear equations**,
which we write as `A·x = b`.

Given an `n×n` coefficient matrix `A` and right-hand side `b`, find `x`.

Not every system has a single answer: if `A` is **singular** (its rows are
linearly dependent, i.e. its rank is less than `n`), there are either no
solutions or infinitely many. In that case print `SINGULAR`.
""",
        input_format="""
First line: `n` (1 ≤ n ≤ 6).
Next `n` lines: `n + 1` integers each — a row of `A` followed by the matching entry of `b`.
All values satisfy |value| ≤ 50.
""",
        output_format="""
If `A` is singular, print `SINGULAR`. Otherwise print `n` lines: `x₁ … xₙ`,
one per line, each with 6 decimal places (answers within 10⁻⁶ are accepted).
""",
        hints=[
            "Load the numbers into an `n×(n+1)` array `M`; then `A = M[:, :n]` and `b = M[:, n]`.",
            "`np.linalg.matrix_rank(A)` tells you the rank; the system has a unique solution exactly when it equals `n`.",
            "`np.linalg.solve(A, b)` returns `x` with `A @ x == b` — much more accurate than computing an inverse first.",
            "Don't rely on `solve` raising an error for singular matrices: rounding can make a singular matrix look "
            "*almost* fine. Check the rank first.",
        ],
        samples=["3\n2 1 -1 8\n-3 -1 2 -11\n-2 1 2 -3", "2\n1 2 3\n2 4 7"],
        tests=["1\n4 10", "1\n0 5", "2\n0 1 3\n1 0 -2", "3\n1 2 3 1\n4 5 6 2\n7 8 9 3",
               "4\n2 0 0 0 1\n0 3 0 0 1\n0 0 -5 0 1\n0 0 0 7 1"],
        gen=_gen_linsys,
        checker="float",
        time_limit=5,
        starter_python="""import sys
import numpy as np

data = sys.stdin.read().split()
n = int(data[0])
M = np.array(data[1:], dtype=float).reshape(n, n + 1)
A, b = M[:, :n], M[:, n]

# TODO: print SINGULAR, or the solution x one value per line
""",
        solution_python="""import sys
import numpy as np

data = sys.stdin.read().split()
n = int(data[0])
M = np.array(data[1:], dtype=float).reshape(n, n + 1)
A, b = M[:, :n], M[:, n]
if np.linalg.matrix_rank(A) < n:
    print("SINGULAR")
else:
    for v in np.linalg.solve(A, b):
        print(f"{v:.6f}")
""",
    ),
    dict(
        id="md-eigenvalues",
        title="Eigenvalues of a Symmetric Matrix",
        difficulty="medium",
        category="Math & Data",
        languages=["python"],
        tags=["numpy", "linear-algebra", "eigenvalues"],
        inspired_by="MIT 18.06 Linear Algebra, symmetric matrices & positive definiteness",
        statement="""
An **eigenvalue** λ of a square matrix `A` is a number for which some non-zero
vector `v` satisfies `A·v = λ·v` — the matrix merely stretches `v`.

When `A` is **symmetric** (`A = Aᵀ`) all of its eigenvalues are real. Such a
matrix is called **positive definite** when every eigenvalue is strictly
positive; positive-definite matrices appear everywhere from physics (energy)
to statistics (covariance matrices).

Print the eigenvalues of the given symmetric matrix in ascending order (each
repeated according to its multiplicity), and say whether the matrix is
positive definite.
""",
        input_format="""
First line: `n` (1 ≤ n ≤ 6). Next `n` lines: `n` integers each, a symmetric matrix
(|entry| ≤ 100). The matrix is guaranteed to be invertible (no eigenvalue is 0).
""",
        output_format="""
Line 1: the `n` eigenvalues in ascending order, separated by spaces, each with 6 decimal
places (answers within 10⁻⁶ are accepted).
Line 2: `YES` if the matrix is positive definite, otherwise `NO`.
""",
        hints=[
            "`np.linalg.eigvals` works for any square matrix, but for symmetric ones prefer "
            "`np.linalg.eigvalsh` — it is faster, more accurate and always returns real numbers.",
            "`eigvalsh` already returns the eigenvalues in ascending order.",
            "Positive definite ⇔ the smallest eigenvalue is > 0.",
        ],
        samples=["2\n2 1\n1 2", "2\n1 2\n2 1"],
        tests=["1\n-4", "1\n9", "3\n4 0 0\n0 -1 0\n0 0 2", "3\n2 -1 0\n-1 2 -1\n0 -1 2"],
        gen=_gen_eig,
        checker="float",
        time_limit=5,
        starter_python="""import sys
import numpy as np

data = sys.stdin.read().split()
n = int(data[0])
A = np.array(data[1:], dtype=float).reshape(n, n)

# TODO: print the sorted eigenvalues, then YES or NO
""",
        solution_python="""import sys
import numpy as np

data = sys.stdin.read().split()
n = int(data[0])
A = np.array(data[1:], dtype=float).reshape(n, n)
ev = np.linalg.eigvalsh(A)
print(" ".join(f"{v:.6f}" for v in ev))
print("YES" if ev[0] > 0 else "NO")
""",
    ),
    dict(
        id="md-markov-steady-state",
        title="Weather Machine",
        difficulty="hard",
        category="Math & Data",
        languages=["python"],
        tags=["numpy", "markov-chain", "matrix-power", "linear-algebra"],
        inspired_by="Markov chains (Rosalind / MIT 18.06 Markov matrices lecture)",
        statement="""
A toy weather model has `n` states (sunny, cloudy, rainy, …). Each day the
weather moves from state `i` to state `j` with a probability proportional to a
given weight `w[i][j]`:

P[i][j] = w[i][j] / (w[i][0] + w[i][1] + … + w[i][n−1])

`P` is a **Markov (stochastic) matrix**: every row sums to 1. If today's
weather is described by a row vector of probabilities `p`, tomorrow's is
`p·P`, and in `k` days it is `p·Pᵏ`.

Today the weather is in state 1 with certainty. Print

1. the probability of each state exactly `k` days from now, and
2. the **steady-state distribution** π — the unique probability vector with
   π·P = π. (The chain in every test is irreducible and aperiodic, so it
   exists, is unique, and `p·Pᵏ` converges to it.)

`k` can be as large as 10⁹, so simulating day by day is too slow.
""",
        input_format="""
First line: `n k` (2 ≤ n ≤ 6, 0 ≤ k ≤ 10⁹).
Next `n` lines: `n` non-negative integers each — the weights `w[i][j]` (≤ 9). Every row has a positive sum.
""",
        output_format="""
Line 1: the `n` probabilities after `k` days.
Line 2: the `n` steady-state probabilities.
Separate values by spaces and print each with 6 decimal places (answers within 10⁻⁶ are accepted).
""",
        hints=[
            "Normalise the rows: `P = W / W.sum(axis=1, keepdims=True)` (broadcasting divides each row by its own sum).",
            "`np.linalg.matrix_power(P, k)` uses repeated squaring, so even k = 10⁹ needs only ~60 multiplications. "
            "Starting in state 1 means the answer to part 1 is simply row 0 of Pᵏ.",
            "π·P = π is the same as (Pᵀ − I)·πᵀ = 0. That system alone has infinitely many solutions; "
            "replace one of its equations with π₁ + … + πₙ = 1 and use `np.linalg.solve`.",
            "Alternative for part 2: π is the eigenvector of `P.T` for eigenvalue 1 (`np.linalg.eig`), "
            "rescaled so its entries sum to 1.",
        ],
        samples=["2 1\n9 1\n5 5", "3 0\n1 1 0\n0 1 1\n1 0 1"],
        tests=["2 1000000000\n1 1\n1 1", "3 5\n2 1 1\n1 2 1\n1 1 2", "4 3\n1 3 0 0\n0 1 3 0\n0 0 1 3\n3 0 0 1"],
        gen=_gen_markov,
        checker="float",
        time_limit=5,
        starter_python="""import sys
import numpy as np

data = sys.stdin.read().split()
n, k = int(data[0]), int(data[1])
W = np.array(data[2:], dtype=float).reshape(n, n)

# TODO: build the transition matrix P, then print the distribution after k days
# and the steady-state distribution
""",
        solution_python="""import sys
import numpy as np

data = sys.stdin.read().split()
n, k = int(data[0]), int(data[1])
W = np.array(data[2:], dtype=float).reshape(n, n)
P = W / W.sum(axis=1, keepdims=True)

after = np.linalg.matrix_power(P, k)[0]

A = P.T - np.eye(n)
A[-1, :] = 1.0
rhs = np.zeros(n)
rhs[-1] = 1.0
pi = np.linalg.solve(A, rhs)

print(" ".join(f"{v:.6f}" for v in after))
print(" ".join(f"{v:.6f}" for v in pi))
""",
    ),
]
