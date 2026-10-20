"""Number theory: primes, divisors, gcd, Collatz, factorials."""


def _lines(t, make):
    return f"{t}\n" + "\n".join(make() for _ in range(t))


def _is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def _prime_near(rng, hi):
    n = rng.randint(2, hi)
    while not _is_prime(n):
        n -= 1 if n > 2 else -1
    return n


def _prime_query(rng):
    k = rng.randrange(4)
    if k == 0:
        return str(_prime_near(rng, 10**9))
    if k == 1:
        p = _prime_near(rng, 31622)
        return str(p * p)
    if k == 2:
        return str(_prime_near(rng, 40000) * _prime_near(rng, 25000))
    return str(rng.randint(1, 10**9))


def _gcd_query(rng):
    if rng.random() < 0.5:
        g = rng.randint(1, 10**5)
        return f"{g * rng.randint(1, 10**4)} {g * rng.randint(1, 10**4)}"
    return f"{rng.randint(1, 10**9)} {rng.randint(1, 10**9)}"


PROBLEMS = [
    dict(
        id="prime-check",
        title="Is It Prime?",
        difficulty="easy",
        category="Number Theory",
        tags=["primes", "trial-division", "sqrt"],
        inspired_by="Classic primality test (HackerRank 'Running Time and Complexity')",
        statement="""
A **prime** is an integer greater than 1 whose only positive divisors are 1
and itself. Decide for each number whether it is prime.

The numbers go up to 10⁹, so trying every divisor up to `n` is too slow.
""",
        input_format="First line: `t` (1 ≤ t ≤ 50). Then `t` lines, each with one integer `n` (1 ≤ n ≤ 10⁹).",
        output_format="For each `n` print `PRIME` or `NOT PRIME` on its own line.",
        hints=[
            "1 is not prime. 2 is the only even prime.",
            "If n = a · b with a ≤ b, then a ≤ √n. So you only need to try divisors d while `d * d <= n`.",
            "Watch the boundary: for n = 49 you must still test d = 7 — use `<=`, not `<`. "
            "In C++ compute `d * d` in `long long` to be safe.",
        ],
        samples=["5\n1\n2\n15\n17\n97"],
        tests=["1\n999999937", "1\n999002449", "1\n1000000000", "4\n3\n4\n9\n25", "1\n999999929"],
        gen=lambda rng: [_lines(20, lambda: _prime_query(rng)) for _ in range(2)],
        starter_python=r"""t = int(input())
for _ in range(t):
    n = int(input())
    # TODO: print PRIME or NOT PRIME
""",
        starter_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long n;
        cin >> n;
        // TODO: print PRIME or NOT PRIME
    }
    return 0;
}
""",
        solution_python=r"""def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True

t = int(input())
for _ in range(t):
    print("PRIME" if is_prime(int(input())) else "NOT PRIME")
""",
        solution_cpp=r"""#include <iostream>
using namespace std;

bool isPrime(long long n) {
    if (n < 2) return false;
    if (n % 2 == 0) return n == 2;
    for (long long d = 3; d * d <= n; d += 2)
        if (n % d == 0) return false;
    return true;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long n;
        cin >> n;
        cout << (isPrime(n) ? "PRIME" : "NOT PRIME") << "\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="gcd-and-lcm",
        title="GCD and LCM",
        difficulty="easy",
        category="Number Theory",
        tags=["gcd", "lcm", "euclid", "overflow"],
        inspired_by="Classic Euclidean algorithm exercise",
        statement="""
For two positive integers find

* their **greatest common divisor** (the largest number dividing both), and
* their **least common multiple** (the smallest positive number divisible by both).

For `12` and `18`: gcd = 6, lcm = 36.
""",
        input_format="First line: `t` (1 ≤ t ≤ 100). Then `t` lines, each with two integers `a b` (1 ≤ a, b ≤ 10⁹).",
        output_format="For each pair print `gcd lcm` on its own line.",
        hints=[
            "Euclid's algorithm: gcd(a, b) = gcd(b, a mod b), and gcd(a, 0) = a. It needs only a handful of steps.",
            "Once you know g = gcd(a, b), the lcm is a · b / g.",
            "C++: a · b can be 10¹⁸ — use `long long`, and compute `a / g * b` (divide first) to stay safe. "
            "Python has `math.gcd`; C++17 has `std::gcd` in `<numeric>`, but try writing it yourself.",
        ],
        samples=["3\n12 18\n7 5\n10 10"],
        tests=["1\n1 1", "1\n1000000000 999999999", "1\n1000000000 1000000000", "2\n1 1000000000\n999999937 999999929",
               "2\n48 180\n17 51"],
        gen=lambda rng: [_lines(30, lambda: _gcd_query(rng)) for _ in range(2)],
        starter_python=r"""t = int(input())
for _ in range(t):
    a, b = map(int, input().split())
    # TODO: compute gcd and lcm of a and b, print them
""",
        starter_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long a, b;
        cin >> a >> b;
        // TODO: compute gcd and lcm of a and b, print them
    }
    return 0;
}
""",
        solution_python=r"""def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

t = int(input())
for _ in range(t):
    a, b = map(int, input().split())
    g = gcd(a, b)
    print(g, a // g * b)
""",
        solution_cpp=r"""#include <iostream>
using namespace std;

long long gcd_ll(long long a, long long b) {
    while (b != 0) {
        long long r = a % b;
        a = b;
        b = r;
    }
    return a;
}

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long a, b;
        cin >> a >> b;
        long long g = gcd_ll(a, b);
        cout << g << " " << a / g * b << "\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="collatz-steps",
        title="Collatz Steps",
        difficulty="easy",
        category="Number Theory",
        tags=["loops", "simulation", "overflow"],
        inspired_by="Project Euler #14 (Longest Collatz sequence) / Kattis 'Collatz'",
        statement="""
Start with a positive integer `n` and repeat:

* if `n` is even, replace it with `n / 2`;
* if `n` is odd, replace it with `3·n + 1`.

It is believed that you always reach `1` eventually. Count the number of
steps needed. For `n = 6`: 6 → 3 → 10 → 5 → 16 → 8 → 4 → 2 → 1, which is
**8 steps**. For `n = 1` no steps are needed.
""",
        input_format="First line: `t` (1 ≤ t ≤ 50). Then `t` lines, each with an integer `n` (1 ≤ n ≤ 10⁶).",
        output_format="For each `n` print the number of steps to reach 1.",
        hints=[
            "A `while n != 1:` loop with a step counter is all you need.",
            "C++ trap: the values in between can grow much larger than n — for some n below 10⁶ they exceed "
            "5·10¹⁰, which overflows `int`. Store n in a `long long`.",
        ],
        samples=["3\n6\n1\n27"],
        tests=["1\n2", "1\n837799", "1\n1000000", "3\n3\n7\n9", "1\n704511"],
        gen=lambda rng: [_lines(25, lambda: str(rng.randint(1, 10**6))) for _ in range(2)],
        starter_python=r"""t = int(input())
for _ in range(t):
    n = int(input())
    steps = 0
    # TODO: apply the Collatz rule until n becomes 1, counting the steps
    print(steps)
""",
        starter_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long n;
        cin >> n;
        int steps = 0;
        // TODO: apply the Collatz rule until n becomes 1, counting the steps
        cout << steps << "\n";
    }
    return 0;
}
""",
        solution_python=r"""t = int(input())
for _ in range(t):
    n = int(input())
    steps = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        steps += 1
    print(steps)
""",
        solution_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long n;
        cin >> n;
        int steps = 0;
        while (n != 1) {
            n = (n % 2 == 0) ? n / 2 : 3 * n + 1;
            steps++;
        }
        cout << steps << "\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="factorial-trailing-zeros",
        title="Zeros at the End of n!",
        difficulty="easy",
        category="Number Theory",
        tags=["factorial", "legendre", "math"],
        inspired_by="LeetCode #172 Factorial Trailing Zeroes / SPOJ FCTRL",
        statement="""
`n!` (n factorial) is `1 · 2 · 3 · … · n`, and `0! = 1`. How many zeros does
`n!` end with?

`10! = 3628800` ends with **2** zeros. Here `n` can be up to 10¹⁸, so
computing `n!` itself is hopeless — think about where the zeros come from.
""",
        input_format="First line: `t` (1 ≤ t ≤ 100). Then `t` lines, each with an integer `n` (0 ≤ n ≤ 10¹⁸).",
        output_format="For each `n` print the number of trailing zeros of `n!`.",
        hints=[
            "Each trailing zero comes from a factor 10 = 2 · 5. There are always more 2s than 5s, so count the factors of 5.",
            "Multiples of 5 contribute one 5 each, multiples of 25 one more, multiples of 125 yet another, …",
            "So the answer is ⌊n/5⌋ + ⌊n/25⌋ + ⌊n/125⌋ + … . In code: repeatedly do `n //= 5` and add n to the answer "
            "until n becomes 0 (this also avoids overflowing a growing power of 5 in C++).",
        ],
        samples=["3\n5\n10\n0"],
        tests=["1\n1000000000000000000", "3\n4\n24\n25", "2\n100\n125", "1\n999999999999999999"],
        gen=lambda rng: [_lines(30, lambda: str(rng.randint(0, 10 ** rng.randint(1, 18)))) for _ in range(2)],
        starter_python=r"""t = int(input())
for _ in range(t):
    n = int(input())
    zeros = 0
    # TODO: count the trailing zeros of n!
    print(zeros)
""",
        starter_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long n;
        cin >> n;
        long long zeros = 0;
        // TODO: count the trailing zeros of n!
        cout << zeros << "\n";
    }
    return 0;
}
""",
        solution_python=r"""t = int(input())
for _ in range(t):
    n = int(input())
    zeros = 0
    while n:
        n //= 5
        zeros += n
    print(zeros)
""",
        solution_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long n;
        cin >> n;
        long long zeros = 0;
        while (n > 0) {
            n /= 5;
            zeros += n;
        }
        cout << zeros << "\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="perfect-number-class",
        title="Perfect, Abundant or Deficient",
        difficulty="easy",
        category="Number Theory",
        tags=["divisors", "sqrt", "classification"],
        inspired_by="Project Euler #23 (abundant numbers) / classic perfect-number check",
        statement="""
The **proper divisors** of `n` are its positive divisors smaller than `n`
(for 12: 1, 2, 3, 4, 6). Let `s` be their sum. Then `n` is

* `PERFECT` if `s = n` (e.g. 6 = 1 + 2 + 3, or 28),
* `ABUNDANT` if `s > n` (e.g. 12, since 1 + 2 + 3 + 4 + 6 = 16),
* `DEFICIENT` if `s < n` (e.g. 8, or any prime, or 1 whose sum is 0).
""",
        input_format="First line: `t` (1 ≤ t ≤ 50). Then `t` lines, each with an integer `n` (1 ≤ n ≤ 10⁸).",
        output_format="For each `n` print `PERFECT`, `ABUNDANT` or `DEFICIENT` on its own line.",
        hints=[
            "Looping d from 1 to n − 1 costs up to 10⁸ steps per number — too slow. Divisors come in pairs: "
            "if d divides n, so does n / d.",
            "So loop d while `d * d <= n`; for each divisor d add both d and n / d — but only once when d == n / d.",
            "That sum includes n itself (from the pair 1 · n): subtract it at the end. Remember 1 has no proper divisors.",
        ],
        samples=["4\n6\n12\n8\n1"],
        tests=["1\n33550336", "1\n8128", "1\n99999989", "1\n100000000", "4\n2\n28\n945\n496",
               "3\n49\n36\n99999999"],
        gen=lambda rng: [_lines(20, lambda: str(rng.randint(1, 10**8))) for _ in range(2)]
        + [_lines(30, lambda: str(rng.randint(1, 1000)))],
        starter_python=r"""t = int(input())
for _ in range(t):
    n = int(input())
    s = 0
    # TODO: compute s = sum of the proper divisors of n, then classify n
""",
        starter_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long n;
        cin >> n;
        long long s = 0;
        // TODO: compute s = sum of the proper divisors of n, then classify n
    }
    return 0;
}
""",
        solution_python=r"""t = int(input())
for _ in range(t):
    n = int(input())
    s = 0
    d = 1
    while d * d <= n:
        if n % d == 0:
            s += d
            if d != n // d:
                s += n // d
        d += 1
    s -= n
    print("PERFECT" if s == n else "ABUNDANT" if s > n else "DEFICIENT")
""",
        solution_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long n;
        cin >> n;
        long long s = 0;
        for (long long d = 1; d * d <= n; d++) {
            if (n % d == 0) {
                s += d;
                if (d != n / d) s += n / d;
            }
        }
        s -= n;
        if (s == n) cout << "PERFECT\n";
        else if (s > n) cout << "ABUNDANT\n";
        else cout << "DEFICIENT\n";
    }
    return 0;
}
""",
    ),
]
