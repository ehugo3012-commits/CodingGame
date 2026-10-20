"""Math & Data: exact linear algebra with SymPy matrices."""


def _gen_rref(rng):
    out = []
    for deficient in (False, True, True, False, True):
        m, n = rng.randint(1, 5), rng.randint(1, 6)
        rows = [[rng.randint(-5, 5) for _ in range(n)] for _ in range(m)]
        if deficient and m >= 2:
            i, j = rng.sample(range(m), 2)
            a, b = rng.randint(-2, 2), rng.randint(-2, 2)
            rows[j] = [a * u + b * v for u, v in zip(rows[i], rows[(i + 1) % m])]
        out.append(f"{m} {n}\n" + "\n".join(" ".join(map(str, r)) for r in rows))
    return out


PROBLEMS = [
    dict(
        id="md-exact-rref",
        title="Row Reduction, Exactly",
        difficulty="hard",
        category="Math & Data",
        languages=["python"],
        tags=["sympy", "linear-algebra", "rref", "rank", "nullspace", "rationals"],
        inspired_by="MIT 18.06 Linear Algebra, lectures 7–8 (Ax = 0, pivot variables, special solutions)",
        statement="""
Gaussian elimination with floating-point numbers leaves you guessing whether
`1e-17` is "really" zero. With **exact rational arithmetic** there is no doubt.

Given an integer matrix `A` (`m` rows, `n` columns), compute:

1. its **rank** — the number of pivots;
2. its **reduced row echelon form** (RREF): every pivot equals 1, is the only
   non-zero entry in its column, and each pivot lies to the right of the pivot
   in the row above; zero rows come last;
3. its **nullity** `n − rank` — the dimension of the null space {x : A·x = 0};
4. the **special solutions** — a basis of the null space. There is one for
   each free (non-pivot) column `j`: set xⱼ = 1, every other free variable to
   0, and solve for the pivot variables. List them by increasing `j`.

For example A = `[[1, 2, 3], [2, 4, 7]]` has RREF `[[1, 2, 0], [0, 0, 1]]`,
rank 2, one free column (column 2) and special solution `(-2, 1, 0)`.
""",
        input_format="""
First line: `m n` (1 ≤ m ≤ 5, 1 ≤ n ≤ 6). Next `m` lines: `n` integers each (|entry| ≤ 20).
""",
        output_format="""
* Line 1: the rank.
* Next `m` lines: the RREF, `n` entries per line.
* Next line: the nullity.
* Then one line per special solution (`n` entries each), in increasing order of the free column.

Write every entry as an integer or a reduced fraction such as `-3/2`.
""",
        hints=[
            "`A = sympy.Matrix(rows)` builds an exact matrix from a list of lists of integers.",
            "`R, pivots = A.rref()` returns the reduced row echelon form and a tuple of pivot column indices — "
            "its length is the rank.",
            "`A.nullspace()` returns a list of column vectors — exactly the special solutions, in free-column order.",
            "Print a row with `print(*R.row(i))` and a column vector `v` with `print(*v)`; "
            "SymPy rationals print like `-3/2`.",
        ],
        samples=["2 3\n1 2 3\n2 4 7", "3 3\n2 1 1\n1 3 2\n1 0 0"],
        tests=["1 1\n0", "1 4\n2 4 -6 8", "3 2\n1 2\n2 4\n3 6", "3 4\n1 2 2 2\n2 4 6 8\n3 6 8 10",
               "2 5\n0 0 3 0 6\n0 0 0 0 0"],
        gen=_gen_rref,
        time_limit=8,
        starter_python="""import sys
import sympy

data = sys.stdin.read().split()
m, n = int(data[0]), int(data[1])
vals = list(map(int, data[2:2 + m * n]))
A = sympy.Matrix(m, n, vals)

# TODO: print the rank, the RREF, the nullity and the special solutions
""",
        solution_python="""import sys
import sympy

data = sys.stdin.read().split()
m, n = int(data[0]), int(data[1])
vals = list(map(int, data[2:2 + m * n]))
A = sympy.Matrix(m, n, vals)
R, pivots = A.rref()
print(len(pivots))
for i in range(m):
    print(*R.row(i))
basis = A.nullspace()
print(len(basis))
for v in basis:
    print(*v)
""",
    ),
]
