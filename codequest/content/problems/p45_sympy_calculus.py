"""Math & Data: calculus with SymPy (derivatives, integrals, series, sums, limits)."""

FUNCS = ["sin(x)", "cos(x)", "exp(x)", "log(x)", "sqrt(x)", "atan(x)", "exp(-x)", "sin(2*x)"]


def _rand_poly(rng, deg):
    terms = []
    for e in range(deg, -1, -1):
        c = rng.randint(-5, 5)
        if c:
            terms.append(f"{c}*x**{e}" if e > 1 else (f"{c}*x" if e == 1 else str(c)))
    return " + ".join(terms).replace("+ -", "- ") or "x"


def _gen_diff(rng):
    out = []
    for _ in range(3):
        exprs = []
        for _ in range(rng.randint(1, 4)):
            kind = rng.randint(0, 3)
            f, g = rng.choice(FUNCS), rng.choice(FUNCS)
            if kind == 0:
                exprs.append(_rand_poly(rng, rng.randint(1, 5)))
            elif kind == 1:
                exprs.append(f"x**{rng.randint(1, 4)}*{f}")
            elif kind == 2:
                exprs.append(f"{f}*{g}")
            else:
                exprs.append(f"{f}/(x**2 + {rng.randint(1, 5)})")
        out.append(f"{len(exprs)}\n" + "\n".join(exprs))
    return out


def _gen_integral(rng):
    out = []
    for _ in range(3):
        qs = []
        for _ in range(rng.randint(1, 3)):
            a = rng.randint(-4, 3)
            b = rng.randint(a + 1, 5)
            qs.append(f"{_rand_poly(rng, rng.randint(0, 4))}\n{a} {b}")
        out.append(f"{len(qs)}\n" + "\n".join(qs))
    return out


PROBLEMS = [
    dict(
        id="md-derivative",
        title="Symbolic Derivative",
        difficulty="beginner",
        category="Math & Data",
        languages=["python"],
        tags=["sympy", "calculus", "derivatives"],
        inspired_by="Calculus I differentiation drills (automated with SymPy)",
        statement="""
**SymPy** is a Python library for *symbolic* mathematics: it manipulates
formulas exactly, the way you would on paper, instead of crunching
approximate numbers.

Your first symbolic task: differentiate. For each given function f(x), print
its derivative f′(x).

The judge compares answers **symbolically**, so any correct equivalent form is
accepted — `2*x + 1`, `1 + 2*x` and `x*2 + 1` are all the same answer.
""",
        input_format="""
First line: `t` (1 ≤ t ≤ 5). Next `t` lines: one function of `x` each, in SymPy syntax
(`*` for multiplication, `**` for powers, functions like `sin`, `cos`, `exp`, `log`, `sqrt`).
""",
        output_format="""
`t` lines: the derivative of each function with respect to `x`, as a SymPy expression,
e.g. `3*x**2 + 2`.
""",
        hints=[
            "`x = sympy.symbols(\"x\")` creates the symbol; `sympy.sympify(text)` parses a formula from a string.",
            "`sympy.diff(expr, x)` differentiates `expr` with respect to `x`.",
            "`print(expr)` prints a SymPy expression in exactly the syntax the judge reads back.",
        ],
        samples=["2\nx**3 + 2*x\nsin(x)*cos(x)"],
        tests=["1\n5", "3\nexp(2*x)\nx*log(x)\n(x**2 + 1)/(x - 1)", "3\nsqrt(x)\nexp(x**2)\ntan(x)",
               "2\nx**x\nlog(sin(x))"],
        gen=_gen_diff,
        checker="sympy",
        time_limit=5,
        starter_python="""import sympy

x = sympy.symbols("x")
t = int(input())
for _ in range(t):
    f = sympy.sympify(input())
    # TODO: print the derivative of f
""",
        solution_python="""import sympy

x = sympy.symbols("x")
t = int(input())
for _ in range(t):
    f = sympy.sympify(input())
    print(sympy.diff(f, x))
""",
    ),
    dict(
        id="md-definite-integral",
        title="Exact Area",
        difficulty="easy",
        category="Math & Data",
        languages=["python"],
        tags=["sympy", "calculus", "integrals"],
        inspired_by="Calculus I definite integrals (Fundamental Theorem of Calculus)",
        statement="""
The definite integral ∫ₐᵇ f(x) dx is the signed area under the curve of f
between x = a and x = b. A numerical method would give 1.718281828…, but
SymPy can give the **exact** answer `E - 1` (where `E` is Euler's number e).

For each query, compute the exact value of the integral. Limits may be
numbers like `0` or `-2`, constants like `pi/2` or `E`, or `oo` (infinity) —
every integral in the tests converges.
""",
        input_format="""
First line: `t` (1 ≤ t ≤ 5). Then `t` queries of two lines each:
the function f(x) in SymPy syntax, and the two limits `a b` separated by a space (a < b).
""",
        output_format="""
`t` lines: the exact value of each integral as a SymPy expression, e.g. `pi/4`, `E - 1` or `log(2)/2`.
Decimal approximations are **not** accepted.
""",
        hints=[
            "Parse each limit with `sympy.sympify` too: it understands `pi`, `E` and `oo`.",
            "`sympy.integrate(f, (x, a, b))` computes a definite integral; `sympy.integrate(f, x)` (no limits) "
            "would give an antiderivative instead.",
            "If an answer looks messy, `sympy.simplify(...)` can tidy it — though the judge accepts any "
            "equivalent exact form.",
        ],
        samples=["3\nx**2\n0 3\nsin(x)\n0 pi\nexp(x)\n0 1"],
        tests=["2\n1/x\n1 E\nx*exp(x)\n0 1", "3\ncos(x)**2\n0 pi\n1/(1 + x**2)\n0 1\nx/(x**2 + 1)\n0 1",
               "2\nexp(-x)\n0 oo\n1/x**2\n1 oo", "2\n1/sqrt(x)\n0 4\nx*sin(x)\n0 pi/2"],
        gen=_gen_integral,
        checker="sympy",
        time_limit=8,
        starter_python="""import sympy

x = sympy.symbols("x")
t = int(input())
for _ in range(t):
    f = sympy.sympify(input())
    a, b = map(sympy.sympify, input().split())
    # TODO: print the exact value of the integral of f from a to b
""",
        solution_python="""import sympy

x = sympy.symbols("x")
t = int(input())
for _ in range(t):
    f = sympy.sympify(input())
    a, b = map(sympy.sympify, input().split())
    print(sympy.simplify(sympy.integrate(f, (x, a, b))))
""",
    ),
    dict(
        id="md-taylor-coefficients",
        title="Taylor Coefficients",
        difficulty="medium",
        category="Math & Data",
        languages=["python"],
        tags=["sympy", "calculus", "series", "taylor"],
        inspired_by="Maclaurin series (Calculus II); 1/(1 − x − x²) is the Fibonacci generating function",
        statement="""
Near x = 0 many functions can be written as a power series (a **Maclaurin
series**):

f(x) = c₀ + c₁x + c₂x² + c₃x³ + …,   where cₖ = f⁽ᵏ⁾(0) / k!

For instance eˣ = 1 + x + x²/2 + x³/6 + …, so its first four coefficients
are `1, 1, 1/2, 1/6`.

Given f and `n`, print the first `n` coefficients c₀ … cₙ₋₁ **exactly**. Every
function in the tests is well-behaved at 0 (or has a removable singularity
there, like sin(x)/x).

A fun one to try: the coefficients of 1/(1 − x − x²) are the Fibonacci numbers.
""",
        input_format="Line 1: the function f(x) in SymPy syntax. Line 2: `n` (1 ≤ n ≤ 8).",
        output_format="`n` lines: c₀, c₁, …, cₙ₋₁, each as an exact number such as `-1/6` (decimals are not accepted).",
        hints=[
            "`sympy.series(f, x, 0, n)` expands f around 0 up to (but not including) xⁿ; it ends with an `O(x**n)` "
            "term which `.removeO()` drops.",
            "`poly_expr.coeff(x, k)` extracts the coefficient of xᵏ (`coeff(x, 0)` gives the constant term).",
            "Remember coefficients can be 0 — e.g. sin(x) has no even powers — and you must still print them.",
        ],
        samples=["exp(x)\n4", "sin(x)\n6"],
        tests=["cos(x)**2\n6", "1/(1 - x - x**2)\n8", "log(1 + x)\n5", "sqrt(1 + x)\n5",
               "sin(x)/x\n5", "exp(x)*sin(x)\n6", "tan(x)\n8", "7\n1"],
        checker="sympy",
        time_limit=8,
        starter_python="""import sympy

x = sympy.symbols("x")
f = sympy.sympify(input())
n = int(input())

# TODO: print the coefficients of x**0 ... x**(n-1) in the Maclaurin series of f
""",
        solution_python="""import sympy

x = sympy.symbols("x")
f = sympy.sympify(input())
n = int(input())
s = sympy.expand(sympy.series(f, x, 0, n).removeO())
for k in range(n):
    print(s.coeff(x, k))
""",
    ),
    dict(
        id="md-sum-of-powers",
        title="Sum of Powers",
        difficulty="medium",
        category="Math & Data",
        languages=["python"],
        tags=["sympy", "summation", "faulhaber", "closed-form"],
        inspired_by="Faulhaber's formula; Project Euler #6 (sum square difference)",
        statement="""
Young Gauss famously found 1 + 2 + … + n = n(n + 1)/2. There is a similar
**closed form** for every power:

1² + 2² + … + n² = n(n + 1)(2n + 1)/6,   1³ + 2³ + … + n³ = (n(n + 1)/2)²,

and in general Σₖ₌₁ⁿ kᵖ is a polynomial in `n` of degree p + 1 (Faulhaber's
formula).

Given `p`, print the closed form of S(n) = 1ᵖ + 2ᵖ + … + nᵖ as a polynomial in
the symbol `n`, and then the exact value S(N) for a given — possibly huge — `N`.
""",
        input_format="One line: two integers `p N` (0 ≤ p ≤ 10, 1 ≤ N ≤ 10¹²).",
        output_format="""
Line 1: the closed form of S(n) in terms of `n`, as a SymPy expression (any equivalent form is accepted,
e.g. `n**2/2 + n/2`).
Line 2: the exact integer S(N).
""",
        hints=[
            "Create both symbols: `k, n = sympy.symbols(\"k n\")`.",
            "`sympy.summation(k**p, (k, 1, n))` evaluates the sum symbolically, returning a formula in `n`.",
            "`formula.subs(n, N)` plugs in a value; SymPy integers are exact, so even N = 10¹² is no problem.",
        ],
        samples=["1 100", "2 10"],
        tests=["0 7", "3 1000000000000", "4 1", "7 12345", "10 999999"],
        gen=lambda rng: [f"{rng.randint(0, 10)} {rng.randint(1, 10**12)}" for _ in range(2)],
        checker="sympy",
        time_limit=8,
        starter_python="""import sympy

k, n = sympy.symbols("k n")
p, N = map(int, input().split())

# TODO: print the closed form of the sum, then its value at n = N
""",
        solution_python="""import sympy

k, n = sympy.symbols("k n")
p, N = map(int, input().split())
S = sympy.expand(sympy.summation(k**p, (k, 1, n)))
print(S)
print(S.subs(n, N))
""",
    ),
    dict(
        id="md-limits",
        title="Limits",
        difficulty="medium",
        category="Math & Data",
        languages=["python"],
        tags=["sympy", "calculus", "limits"],
        inspired_by="Calculus I limit drills (L'Hôpital's rule classics)",
        statement="""
Some limits can't be found by plugging in the point: sin(x)/x at x = 0 gives
the meaningless 0/0, yet the limit is exactly 1. And (1 + 1/x)ˣ as x → ∞
tends to Euler's number e.

For each query compute the exact limit of f(x) as x approaches the given
point. For a finite point `a` the limit is taken **from the right**
(x → a⁺). The limit always exists and is finite.
""",
        input_format="""
First line: `t` (1 ≤ t ≤ 4). Then `t` queries of two lines each: the function f(x) in SymPy syntax,
and the point (a number, a constant such as `pi/2`, or `oo` for +∞).
""",
        output_format="`t` lines: each limit as an exact SymPy expression, e.g. `1/2`, `E` or `log(2)`.",
        hints=[
            "`sympy.sympify(\"oo\")` is SymPy's infinity, `sympy.oo`.",
            "`sympy.limit(f, x, a)` computes the limit; by default it approaches from the right (`dir=\"+\"`).",
        ],
        samples=["2\nsin(x)/x\n0\n(1 + 1/x)**x\noo"],
        tests=["2\n(x**2 - 1)/(x - 1)\n1\n(exp(x) - 1 - x)/x**2\n0",
               "2\nx*log(x)\n0\nsqrt(x**2 + x) - x\noo",
               "3\n(1 - cos(x))/x**2\n0\n(3*x**2 + 1)/(2*x**2 - x)\noo\n(2**x - 1)/x\n0",
               "2\n(1 + 2/x)**x\noo\nsin(3*x)/sin(5*x)\n0",
               "2\n(x - pi/2)*tan(x)\npi/2\nx**(1/x)\noo"],
        checker="sympy",
        time_limit=8,
        starter_python="""import sympy

x = sympy.symbols("x")
t = int(input())
for _ in range(t):
    f = sympy.sympify(input())
    a = sympy.sympify(input())
    # TODO: print the limit of f as x -> a (from the right)
""",
        solution_python="""import sympy

x = sympy.symbols("x")
t = int(input())
for _ in range(t):
    f = sympy.sympify(input())
    a = sympy.sympify(input())
    print(sympy.limit(f, x, a))
""",
    ),
]
