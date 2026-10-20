"""Math & Data, expert tier: Pell equations and absorbing Markov chains (SymPy)."""


def _gen_pell(rng):
    out = []
    for _ in range(3):
        lo = rng.randint(2, 900)
        hi = min(1000, lo + rng.randint(1, 120))
        out.append(f"{lo} {hi}")
    return out


def _gen_chain(rng):
    out = []
    for _ in range(4):
        n = rng.randint(2, 8)
        k = rng.randint(1, n - 1)  # number of absorbing states
        absorbing = set(rng.sample(range(1, n), k))
        transient = [i for i in range(n) if i not in absorbing]
        w = [[0] * n for _ in range(n)]
        for i in range(n):
            if i in absorbing:
                w[i][i] = rng.choice([0, 1, 3])
                continue
            for j in range(n):
                if rng.random() < 0.4:
                    w[i][j] = rng.randint(1, 5)
            # guarantee absorption: each transient state links to the next one, the last to an exit
            pos = transient.index(i)
            target = transient[pos + 1] if pos + 1 < len(transient) else rng.choice(sorted(absorbing))
            w[i][target] = max(w[i][target], 1)
            if rng.random() < 0.5:
                e = rng.choice(sorted(absorbing))
                w[i][e] = max(w[i][e], 1)
        out.append(f"{n}\n" + "\n".join(" ".join(map(str, r)) for r in w))
    return out


PROBLEMS = [
    dict(
        id="md-pell-champion",
        title="Pell's Champion",
        difficulty="expert",
        category="Math & Data",
        languages=["python"],
        tags=["sympy", "diophantine", "pell-equation", "continued-fractions", "number-theory"],
        inspired_by="Project Euler #66 (Diophantine equation)",
        statement="""
For a positive integer `D` that is **not** a perfect square, the Pell equation

x² − D·y² = 1

has infinitely many solutions in positive integers, and the smallest one
(minimal `x`) is called the **fundamental solution**. For D = 13 it is
x = 649, y = 180, since 649² − 13·180² = 1 — but for D = 61 it is the
whopping x = 1766319049, y = 226153980.

For every non-square `D` with `L ≤ D ≤ R`, find the fundamental solution.
Report the `D` whose minimal `x` is the **largest** (the smallest such `D` if
there is a tie), together with that `x` and `y`.

Brute-force search over `y` is hopeless — minimal solutions can have dozens of
digits. The classical method uses the continued fraction of √D, and SymPy
implements it for you.
""",
        input_format="One line: `L R` (2 ≤ L ≤ R ≤ 1000). The range contains at least one non-square.",
        output_format="One line: `D x y`.",
        hints=[
            "`sympy.sqrt(D).is_Integer` (or `math.isqrt(D) ** 2 == D`) tells you whether `D` is a perfect square — "
            "skip those.",
            "`from sympy.solvers.diophantine.diophantine import diop_DN`: `diop_DN(D, N)` solves x² − D·y² = N and "
            "returns a list of fundamental solutions. For N = 1 it is `[(x, y)]`.",
            "Python integers are unbounded, so comparing huge `x` values is no problem; keep the first `D` on ties.",
            "Curious how it works? `sympy.continued_fraction_periodic(0, 1, D)` shows √D's periodic continued "
            "fraction; the fundamental solution is one of its convergents.",
        ],
        samples=["2 7", "13 13"],
        tests=["2 1000", "60 62", "2 3", "990 1000", "8 9"],
        gen=_gen_pell,
        time_limit=8,
        starter_python="""import sympy
from sympy.solvers.diophantine.diophantine import diop_DN

L, R = map(int, input().split())

# TODO: for each non-square D in [L, R], find the fundamental solution of x^2 - D*y^2 = 1
# and print the D with the largest minimal x, followed by x and y
""",
        solution_python="""import math
from sympy.solvers.diophantine.diophantine import diop_DN

L, R = map(int, input().split())
best = None
for D in range(L, R + 1):
    if math.isqrt(D) ** 2 == D:
        continue
    x, y = diop_DN(D, 1)[0]
    if best is None or x > best[1]:
        best = (D, x, y)
print(*best)
""",
    ),
    dict(
        id="md-absorbing-chain",
        title="Escape the Maze",
        difficulty="expert",
        category="Math & Data",
        languages=["python"],
        tags=["sympy", "markov-chain", "linear-algebra", "probability", "rationals"],
        inspired_by="Absorbing Markov chains (Grinstead & Snell, Introduction to Probability, ch. 11)",
        statement="""
A robot wanders through a building with `n` rooms. From room `i` it moves to
room `j` with probability proportional to a weight `w[i][j]` (it may also stay
put if `w[i][i] > 0`). A room whose weights to **every other** room are 0 is an
**exit**: once the robot gets there it stays forever. In every test, an exit
can be reached from every room.

The robot starts in room 1. Compute, **exactly**:

1. the expected number of moves until it reaches an exit;
2. for every exit, the probability that this is where the robot ends up.

This is an *absorbing Markov chain*. Order the rooms so the non-exits
(transient states) come first; the transition matrix splits into blocks `Q`
(transient → transient) and `R` (transient → exit). The **fundamental matrix**
`N = (I − Q)⁻¹` holds the expected number of visits to each transient room,
so the expected time to absorption is `N·1`, and the exit probabilities are
`N·R`.

Floating point is not good enough here: answers must be exact fractions.
""",
        input_format="""
First line: `n` (2 ≤ n ≤ 8). Next `n` lines: `n` non-negative integers each, the weights `w[i][j]` (≤ 9).
Every non-exit room has at least one positive weight to another room.
""",
        output_format="""
Line 1: the expected number of moves from room 1 (0 if room 1 is itself an exit).
Then one line per exit, in increasing room order: the room number and the probability of ending there.
Write every number as an integer or a reduced fraction such as `7/3`.
""",
        hints=[
            "Find the exits first: room `i` is an exit when `w[i][j] == 0` for every `j != i`. "
            "The remaining rooms are transient.",
            "Work with exact numbers: `sympy.Rational(w, row_sum)` builds a fraction, and a `sympy.Matrix` of "
            "Rationals keeps all arithmetic exact.",
            "Extract the blocks with lists of indices: `P.extract(T, T)` is `Q` and `P.extract(T, A)` is `R`, "
            "where `T` and `A` are the transient and exit room indices.",
            "`(sympy.eye(len(T)) - Q).inv()` is `N`. Row 0 of `N * ones` and of `N * R` belongs to room 1 when "
            "room 1 is the first transient index. (Faster: `M.LUsolve(rhs)` solves `M·X = rhs` without inverting.)",
        ],
        samples=["3\n1 1 1\n0 1 0\n0 0 1", "5\n0 1 0 1 0\n1 0 1 0 0\n0 1 0 0 1\n0 0 0 1 0\n0 0 0 0 1"],
        tests=["2\n0 0\n0 0", "2\n3 1\n0 0", "4\n0 1 0 1\n1 0 1 0\n0 1 0 1\n0 0 0 5",
               "4\n1 1 1 1\n1 1 1 1\n0 0 0 0\n0 0 0 0"],
        gen=_gen_chain,
        time_limit=8,
        starter_python="""import sys
import sympy

data = sys.stdin.read().split()
n = int(data[0])
W = [[int(data[1 + i * n + j]) for j in range(n)] for i in range(n)]

# TODO: find the exits, build Q and R exactly, then print the expected number of moves
# and the probability of each exit
""",
        solution_python="""import sys
import sympy

data = sys.stdin.read().split()
n = int(data[0])
W = [[int(data[1 + i * n + j]) for j in range(n)] for i in range(n)]

exits = [i for i in range(n) if all(W[i][j] == 0 for j in range(n) if j != i)]
trans = [i for i in range(n) if i not in exits]

if 0 in exits:
    print(0)
    for e in exits:
        print(e + 1, 1 if e == 0 else 0)
else:
    P = sympy.Matrix(n, n, lambda i, j: sympy.Rational(W[i][j], sum(W[i])) if i in trans else int(i == j))
    Q = P.extract(trans, trans)
    R = P.extract(trans, exits)
    M = sympy.eye(len(trans)) - Q
    rhs = sympy.ones(len(trans), 1).row_join(R)
    X = M.LUsolve(rhs)
    print(X[0, 0])
    for k, e in enumerate(exits):
        print(e + 1, X[0, k + 1])
""",
    ),
]
