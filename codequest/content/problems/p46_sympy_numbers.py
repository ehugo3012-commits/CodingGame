"""Math & Data: number theory helpers in SymPy (primes, factorisation, totient)."""


def _gen_primes(rng):
    out = []
    for hi in (100, 10**6, 10**12):
        vals = [rng.randint(0, hi) for _ in range(rng.randint(3, 8))]
        out.append(f"{len(vals)}\n" + "\n".join(map(str, vals)))
    return out


def _gen_factor(rng):
    out = []
    for hi in (1000, 10**8, 10**12):
        vals = [rng.randint(2, hi) for _ in range(rng.randint(3, 6))]
        out.append(f"{len(vals)}\n" + "\n".join(map(str, vals)))
    return out


PROBLEMS = [
    dict(
        id="md-prime-check",
        title="Prime Time",
        difficulty="beginner",
        category="Math & Data",
        languages=["python"],
        tags=["sympy", "primes", "number-theory"],
        inspired_by="Project Euler #7 (10001st prime) — the SymPy shortcut",
        statement="""
A **prime** is a whole number greater than 1 whose only divisors are 1 and
itself: 2, 3, 5, 7, 11, …

For each given number `n`, say whether it is prime, and print the **next
prime** — the smallest prime strictly greater than `n`.

Numbers go up to 10¹², so trial division by every number below `n` is far too
slow. SymPy ships with fast primality tools — let's use them.
""",
        input_format="First line: `t` (1 ≤ t ≤ 10). Next `t` lines: one integer `n` each (0 ≤ n ≤ 10¹²).",
        output_format="For each `n`, a line with `YES` or `NO` (is `n` prime?) followed by the next prime after `n`.",
        hints=[
            "`from sympy import isprime, nextprime`.",
            "`isprime(n)` returns `True` or `False`; `nextprime(n)` returns the smallest prime greater than `n`.",
            "Remember 0 and 1 are not prime.",
        ],
        samples=["4\n7\n10\n1\n97"],
        tests=["1\n0", "3\n2\n3\n4", "2\n999999999989\n1000000000000", "3\n561\n7919\n1000003"],
        gen=_gen_primes,
        time_limit=5,
        starter_python="""from sympy import isprime, nextprime

t = int(input())
for _ in range(t):
    n = int(input())
    # TODO: print YES/NO and the next prime
""",
        solution_python="""from sympy import isprime, nextprime

t = int(input())
for _ in range(t):
    n = int(input())
    print("YES" if isprime(n) else "NO", nextprime(n))
""",
    ),
    dict(
        id="md-factor-totient",
        title="Prime Factorisation & Totient",
        difficulty="easy",
        category="Math & Data",
        languages=["python"],
        tags=["sympy", "factorization", "totient", "divisors", "number-theory"],
        inspired_by="Project Euler #3 (largest prime factor) and #69 (totient maximum)",
        statement="""
Every integer n ≥ 2 is a product of primes in exactly one way, e.g.
360 = 2³ · 3² · 5. From that factorisation two classic functions follow:

* **Euler's totient** φ(n): how many integers in 1…n share no common factor
  with n. φ(n) = n · Π (1 − 1/p) over the distinct primes p of n.
* **Divisor count** τ(n): if n = p₁^e₁ · … · pₖ^eₖ then τ(n) = (e₁ + 1) · … · (eₖ + 1).

For each `n` print its factorisation, φ(n) and τ(n).
""",
        input_format="First line: `t` (1 ≤ t ≤ 8). Next `t` lines: one integer `n` each (2 ≤ n ≤ 10¹²).",
        output_format="""
For each `n` print two lines:

1. the prime factorisation as tokens `p^e` in increasing order of `p`, always writing the exponent —
   for 360: `2^3 3^2 5^1`;
2. φ(n) and τ(n) separated by a space.
""",
        hints=[
            "`sympy.factorint(n)` returns a dict `{prime: exponent}`, e.g. `{2: 3, 3: 2, 5: 1}` for 360.",
            "Dicts can be sorted: `for p in sorted(f): ...`, and an f-string like `f\"{p}^{e}\"` builds each token.",
            "`sympy.totient(n)` and `sympy.divisor_count(n)` compute φ and τ directly (or derive them from the "
            "factorisation yourself).",
        ],
        samples=["2\n360\n97"],
        tests=["1\n2", "3\n1024\n999999000001\n600851475143", "2\n1000000000000\n720720"],
        gen=_gen_factor,
        time_limit=5,
        starter_python="""import sympy

t = int(input())
for _ in range(t):
    n = int(input())
    # TODO: print the factorisation line, then "phi tau"
""",
        solution_python="""import sympy

t = int(input())
for _ in range(t):
    n = int(input())
    f = sympy.factorint(n)
    print(" ".join(f"{p}^{f[p]}" for p in sorted(f)))
    print(sympy.totient(n), sympy.divisor_count(n))
""",
    ),
]
