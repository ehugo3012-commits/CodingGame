"""Math & Data: polynomial algebra with SymPy (expand, roots, partial fractions)."""


def _pmul(p, q):
    """Multiply coefficient lists (highest power first)."""
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def _peval(p, v):
    r = 0
    for c in p:
        r = r * v + c
    return r


def _poly_str(p):
    """Coefficient list -> SymPy-readable expression string in x."""
    d = len(p) - 1
    parts = []
    for i, c in enumerate(p):
        e = d - i
        if c == 0:
            continue
        mono = "" if e == 0 else ("x" if e == 1 else f"x**{e}")
        if mono and abs(c) == 1:
            term = mono
        else:
            term = f"{abs(c)}*{mono}" if mono else str(abs(c))
        parts.append(("- " if c < 0 else "+ ") + term)
    if not parts:
        return "0"
    s = " ".join(parts)
    return s[2:] if s.startswith("+ ") else "-" + s[2:]


def _lin(a, b):
    """String for (a*x + b)."""
    ax = "x" if a == 1 else f"{a}*x"
    return f"({ax} {'+' if b >= 0 else '-'} {abs(b)})"


def _gen_expand(rng):
    out = []
    for _ in range(4):
        factors = []
        for _ in range(rng.randint(1, 3)):
            a, b = rng.randint(1, 3), rng.choice([i for i in range(-5, 6) if i])
            e = rng.choice([1, 1, 2, 3])
            factors.append(_lin(a, b) + (f"**{e}" if e > 1 else ""))
        expr = "*".join(factors)
        if rng.random() < 0.5:
            expr += f" {rng.choice('+-')} {rng.randint(1, 4)}*x**{rng.randint(1, 3)}"
        out.append(expr)
    return out


QUADS = [[1, 0, 1], [1, 0, -2], [1, 1, 1], [1, 0, 3], [2, 0, -3], [1, -1, -1]]


def _gen_roots(rng):
    out = []
    for _ in range(4):
        p = [rng.choice([1, -1, 2, 3])]
        for _ in range(rng.randint(0, 3)):
            a = rng.randint(1, 3)
            b = rng.randint(-4, 4)
            p = _pmul(p, [a, -b])
            if rng.random() < 0.3:
                p = _pmul(p, [a, -b])
        for _ in range(rng.randint(0, 2)):
            p = _pmul(p, rng.choice(QUADS))
        if len(p) == 1:
            p = _pmul(p, rng.choice(QUADS))
        out.append(f"{len(p) - 1}\n{' '.join(map(str, p))}")
    return out


def _gen_apart(rng):
    out = []
    for _ in range(4):
        rs = rng.sample(range(-4, 5), rng.randint(1, 3))
        q = [1]
        for r in rs:
            for _ in range(rng.choice([1, 1, 2])):
                q = _pmul(q, [1, -r])
        while True:
            p = [rng.randint(-6, 6) for _ in range(rng.randint(1, len(q) + 1))]
            if p[0] != 0 and all(_peval(p, r) != 0 for r in rs):
                break
        out.append(f"{_poly_str(p)}\n{_poly_str(q)}")
    return out


PROBLEMS = [
    dict(
        id="md-expand-coefficients",
        title="Expand the Polynomial",
        difficulty="easy",
        category="Math & Data",
        languages=["python"],
        tags=["sympy", "polynomials", "expand"],
        inspired_by="High-school algebra drill, automated with a computer algebra system",
        statement="""
Multiplying out `(x + 1)**3*(2*x - 3)` by hand is tedious and error-prone —
exactly the kind of job a **computer algebra system** does perfectly.

Given a polynomial in `x` written in any form (products, powers, sums),
expand it and print its **degree** and its **coefficients**, from the highest
power of `x` down to the constant term (including zero coefficients).

For example `(x + 1)**3*(2*x - 3)` expands to `2*x**4 + 3*x**3 - 3*x**2 - 7*x - 3`,
so the degree is 4 and the coefficients are `2 3 -3 -7 -3`.
""",
        input_format="""
One line: a polynomial in `x` with integer coefficients, in Python/SymPy syntax
(`*` for multiplication, `**` for powers). Its degree is at most 12 and it is not the zero polynomial.
""",
        output_format="""
Line 1: the degree.
Line 2: the coefficients from the highest power down to the constant term, separated by spaces.
""",
        hints=[
            "`sympy.sympify(text)` turns the input string into a SymPy expression (the name `x` becomes a symbol).",
            "`sympy.expand(expr)` multiplies everything out. `sympy.Poly(expr, x)` goes further and gives you a "
            "polynomial object.",
            "A `Poly` has `.degree()` and `.all_coeffs()` — the latter lists every coefficient, highest power first, "
            "zeros included.",
        ],
        samples=["(x + 1)**3*(2*x - 3)", "(x - 2)*(x + 2) + x**3"],
        tests=["7", "(x + 1)**2 - x**2 - 2*x", "x**5", "(x - 1)*(x**2 + x + 1)", "(2*x - 1)**6"],
        gen=_gen_expand,
        time_limit=5,
        starter_python="""import sympy

x = sympy.symbols("x")
expr = sympy.sympify(input())

# TODO: expand the polynomial, then print its degree and all its coefficients
""",
        solution_python="""import sympy

x = sympy.symbols("x")
expr = sympy.sympify(input())
p = sympy.Poly(expr, x)
print(p.degree())
print(*p.all_coeffs())
""",
    ),
    dict(
        id="md-rational-roots",
        title="Rational Roots",
        difficulty="medium",
        category="Math & Data",
        languages=["python"],
        tags=["sympy", "polynomials", "roots", "rationals"],
        inspired_by="The Rational Root Theorem (classic algebra), checked with SymPy",
        statement="""
Find every **rational** root of a polynomial with integer coefficients, together
with its **multiplicity** (how many times the factor appears: `(x − 2)³` gives
the root 2 with multiplicity 3).

Irrational roots (like √2) and complex roots (like `i`) must be ignored.

For example 4x³ − 4x² − 3x = x·(2x + 1)·(2x − 3) has the rational roots −1/2,
0 and 3/2, each with multiplicity 1, while x² − 2 has none at all: its roots
±√2 are irrational.
""",
        input_format="""
Line 1: the degree `d` (1 ≤ d ≤ 10).
Line 2: `d + 1` integers, the coefficients from xᵈ down to the constant term (the first is not 0).
""",
        output_format="""
For each distinct rational root, in **ascending** order, print a line `r k`: the root and its multiplicity.
Write the root as an integer or a reduced fraction such as `-3/2`.
If there is no rational root, print `NONE`.
""",
        hints=[
            "`sympy.Poly(coeffs, x)` builds a polynomial straight from a list of coefficients (highest power first).",
            "`sympy.roots(poly)` returns a dict `{root: multiplicity}`. Passing `filter=\"Q\"` keeps only the "
            "rational roots.",
            "Alternatively, `sympy.factor_list(poly)` gives the irreducible factors with their multiplicities; "
            "the linear ones are the rational roots.",
            "SymPy rationals print as `-3/2` with `str(...)`, and they sort correctly with `sorted(...)`.",
        ],
        samples=["3\n4 -4 -3 0", "2\n1 0 -2"],
        tests=["1\n2 -5", "4\n1 -4 6 -4 1", "4\n1 0 0 0 1", "5\n1 2 -1 -4 -2 0", "6\n8 -12 6 -1 0 0 0"],
        gen=_gen_roots,
        time_limit=5,
        starter_python="""import sympy

x = sympy.symbols("x")
d = int(input())
coeffs = list(map(int, input().split()))

# TODO: find the rational roots and their multiplicities
""",
        solution_python="""import sympy

x = sympy.symbols("x")
d = int(input())
coeffs = list(map(int, input().split()))
rs = sympy.roots(sympy.Poly(coeffs, x), filter="Q")
if not rs:
    print("NONE")
for r in sorted(rs):
    print(r, rs[r])
""",
    ),
    dict(
        id="md-partial-fractions",
        title="Partial Fractions",
        difficulty="hard",
        category="Math & Data",
        languages=["python"],
        tags=["sympy", "partial-fractions", "apart", "rational-functions"],
        inspired_by="Partial fraction decomposition (calculus integration technique)",
        statement="""
To integrate a rational function such as (3x³ + 2) / (x³ − 3x² + 4), calculus
students first split it into **partial fractions**:

(3x³ + 2) / ((x + 1)(x − 2)²) = 3 − 1/(9(x + 1)) + 82/(9(x − 2)) + 26/(3(x − 2)²)

In general the result is a **polynomial part** plus terms of the form
A / (x − r)ᵏ. In this problem the denominator always factors into linear
factors (x − r) with **integer** roots `r`.

Print the decomposition one piece per line, in a fixed order:

1. the polynomial part (print `0` if there is none);
2. then each fraction term A/(x − r)ᵏ with A ≠ 0, sorted by `r` ascending and,
   for equal `r`, by the power `k` ascending.

Each line is compared **symbolically**, so `26/(3*(x - 2)**2)` and
`(26/3)/(x-2)**2` are both fine — but the pieces must be on separate lines in
the right order.
""",
        input_format="""
Line 1: the numerator, a polynomial in `x` with integer coefficients.
Line 2: the denominator, a monic polynomial in `x` (degree 1–6) whose roots are distinct-or-repeated
integers; it shares no root with the numerator.
Both are written in SymPy syntax (`*` and `**`).
""",
        output_format="""
The polynomial part on the first line, then one fraction term per line in the order described.
Use SymPy syntax, e.g. `-1/(9*(x + 1))`.
""",
        hints=[
            "`sympy.apart(expr, x)` computes the whole decomposition as one sum.",
            "`sympy.Add.make_args(sum_expr)` splits a sum into its individual terms. A term `t` belongs to the "
            "polynomial part when `t.is_polynomial(x)` is True — there may be several such terms to add up.",
            "For a fraction term, `num, den = t.as_numer_denom()` gives its denominator; `sympy.roots(den, x)` "
            "returns `{r: k}`, exactly the key you need for sorting.",
        ],
        samples=["3*x**3 + 2\nx**3 - 3*x**2 + 4", "1\nx**2 - 1"],
        tests=["x\nx - 5", "x**4 + 1\nx**2", "2*x + 3\nx**3 - x", "x**5 + 1\nx**2 - 4*x + 4",
               "-7\nx**3 + 3*x**2 + 3*x + 1"],
        gen=_gen_apart,
        checker="sympy",
        time_limit=8,
        starter_python="""import sympy

x = sympy.symbols("x")
num = sympy.sympify(input())
den = sympy.sympify(input())
f = num / den

# TODO: decompose f, print the polynomial part, then the sorted fraction terms
""",
        solution_python="""import sympy

x = sympy.symbols("x")
num = sympy.sympify(input())
den = sympy.sympify(input())
f = sympy.apart(num / den, x)

poly_part = sympy.Integer(0)
terms = []
for t in sympy.Add.make_args(f):
    if t.is_polynomial(x):
        poly_part += t
    else:
        _, d = t.as_numer_denom()
        (r, k), = sympy.roots(sympy.Poly(d, x)).items()
        terms.append((r, k, t))
print(poly_part)
for r, k, t in sorted(terms, key=lambda e: (e[0], e[1])):
    print(t)
""",
    ),
]
