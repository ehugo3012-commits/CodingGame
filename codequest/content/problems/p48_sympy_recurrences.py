"""Math & Data: solving recurrences in closed form with SymPy's rsolve."""


def _gen_rec(rng):
    out = []
    for _ in range(4):
        r1 = rng.choice([i for i in range(-4, 5) if i])
        r2 = rng.choice([r1, rng.choice([i for i in range(-4, 5) if i])])
        p, q = r1 + r2, -r1 * r2
        d = rng.choice([0, rng.randint(-6, 6)])
        out.append(f"{p} {q} {d}\n{rng.randint(-9, 9)} {rng.randint(-9, 9)}\n{rng.randint(0, 60)}")
    return out


PROBLEMS = [
    dict(
        id="md-recurrence-closed-form",
        title="Closed-Form Recurrence",
        difficulty="hard",
        category="Math & Data",
        languages=["python"],
        tags=["sympy", "recurrences", "rsolve", "closed-form"],
        inspired_by="Concrete Mathematics ch. 7 / Binet's formula for Fibonacci numbers",
        statement="""
A sequence is defined by two starting values and the rule

a(n) = p·a(n−1) + q·a(n−2) + d   for n ≥ 2.

Computing a(1000) by looping is easy, but mathematicians prefer a **closed
form** — a formula in `n` you can evaluate directly. For example
a(n) = 5a(n−1) − 6a(n−2) with a(0) = 1, a(1) = 4 has the closed form
a(n) = 2·3ⁿ − 2ⁿ.

The closed form comes from the roots of the *characteristic equation*
r² = p·r + q. In every test these roots are non-zero **integers** (possibly
equal — then a factor `n` appears, as in n·2ⁿ).

Print the closed form of a(n) (valid for every n ≥ 0) and the exact value
a(N).
""",
        input_format="""
Line 1: three integers `p q d` (|p| ≤ 8, |q| ≤ 16, |d| ≤ 10).
Line 2: `a(0) a(1)` (integers, absolute value ≤ 10).
Line 3: `N` (0 ≤ N ≤ 100).
""",
        output_format="""
Line 1: the closed form as a SymPy expression in `n` — using powers like `3**n` or `(-2)**n` — e.g.
`2*3**n - 2**n`. Any equivalent form is accepted.
Line 2: the exact integer a(N).
""",
        hints=[
            "Declare an unknown sequence with `a = sympy.Function(\"a\")` and the index with `n = sympy.symbols(\"n\")`.",
            "`sympy.rsolve(expr, a(n), {a(0): v0, a(1): v1})` solves the recurrence `expr = 0` with the given "
            "initial values. Here `expr` is `a(n) - p*a(n - 1) - q*a(n - 2) - d`.",
            "The answer for line 2 is `closed.subs(n, N)`; wrap it in `sympy.simplify` / `sympy.Integer` if it "
            "doesn't come out as a plain integer.",
            "Cross-check: the closed form at n = 0 and n = 1 must give back a(0) and a(1).",
        ],
        samples=["5 -6 0\n1 4\n10", "4 -4 0\n1 4\n5"],
        tests=["1 2 0\n0 3\n0", "-1 2 0\n3 -1\n7", "2 -1 1\n0 0\n100", "0 1 0\n5 5\n33", "-6 -9 3\n1 -2\n20"],
        gen=_gen_rec,
        checker="sympy",
        time_limit=8,
        starter_python="""import sympy

n = sympy.symbols("n")
a = sympy.Function("a")
p, q, d = map(int, input().split())
a0, a1 = map(int, input().split())
N = int(input())

# TODO: solve the recurrence with sympy.rsolve, print the closed form and a(N)
""",
        solution_python="""import sympy

n = sympy.symbols("n")
a = sympy.Function("a")
p, q, d = map(int, input().split())
a0, a1 = map(int, input().split())
N = int(input())
closed = sympy.rsolve(a(n) - p * a(n - 1) - q * a(n - 2) - d, a(n), {a(0): a0, a(1): a1})
print(closed)
print(sympy.simplify(closed.subs(n, N)))
""",
    ),
]
