"""Number Theory: the sieve of Eratosthenes and fast modular exponentiation."""


def _sieve_gen(rng):
    qs = [rng.randint(1, 3 * 10**6) for _ in range(15)] + [rng.randint(1, 1000) for _ in range(15)]
    return [f"{len(qs)}\n" + "\n".join(map(str, qs)), "1\n3000000"]


def _modpow_gen(rng):
    lines = []
    for _ in range(60):
        a = rng.choice((rng.randint(0, 10), rng.randint(0, 10**9), rng.randint(0, 10**18)))
        b = rng.choice((rng.randint(0, 20), rng.randint(0, 10**18)))
        m = rng.choice((rng.randint(1, 100), rng.randint(1, 10**9), 10**9 + 7, 998244353))
        lines.append(f"{a} {b} {m}")
    return [f"{len(lines)}\n" + "\n".join(lines)]


PROBLEMS = [
    dict(
        id="prime-count-sieve",
        title="Prime Count with a Sieve",
        difficulty="medium",
        category="Number Theory",
        tags=["primes", "sieve", "prefix-sums"],
        inspired_by="LeetCode #204 Count Primes; the Sieve of Eratosthenes",
        statement="""
For each query `n`, print how many **prime numbers** are `≤ n`.

For `n = 10` the primes are 2, 3, 5, 7, so the answer is 4.

Testing each number for primality separately is too slow for millions of
numbers. Over 2000 years ago Eratosthenes found a better way: cross out the
multiples of every prime, and whatever survives is prime.
""",
        input_format="First line: `t` (1 ≤ t ≤ 50). Next `t` lines: `n` (1 ≤ n ≤ 3·10⁶).",
        output_format="For each query, the number of primes ≤ n on its own line.",
        hints=[
            "Make a boolean array `is_prime[0..N]` for the largest `N` asked, all `True` except 0 and 1. For each `p` "
            "from 2 while `p·p <= N`: if `is_prime[p]`, mark `p·p, p·p + p, …` as not prime.",
            "Starting at `p·p` is enough — smaller multiples already have a smaller prime factor. "
            "Python speed trick: `sieve[p*p::p] = bytes(len(range(p*p, N + 1, p)))` on a `bytearray`.",
            "To answer many queries, build a prefix count `cnt[i]` = primes ≤ i once (C++: `vector<int>`), or in Python "
            "use `sieve[:n + 1].count(1)` per query.",
        ],
        samples=["3\n10\n1\n100"],
        tests=["1\n2", "4\n3\n4\n5\n6", "2\n1000000\n999983"],
        gen=_sieve_gen,
        starter_python="""t = int(input())
qs = [int(input()) for _ in range(t)]
N = max(qs)
sieve = bytearray([1]) * (N + 1)
sieve[0] = 0
if N >= 1:
    sieve[1] = 0
# TODO: cross out multiples of each prime p with p*p <= N
for n in qs:
    print(sieve[:n + 1].count(1))
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int t;
    cin >> t;
    vector<int> qs(t);
    for (auto &q : qs) cin >> q;
    int N = *max_element(qs.begin(), qs.end());
    vector<char> isPrime(N + 1, 1);
    isPrime[0] = 0;
    if (N >= 1) isPrime[1] = 0;
    // TODO: sieve, then build prefix counts
    for (int n : qs) cout << 0 << "\\n";
    return 0;
}
""",
        solution_python=r"""t = int(input())
qs = [int(input()) for _ in range(t)]
N = max(qs)
sieve = bytearray([1]) * (N + 1)
sieve[0] = 0
if N >= 1:
    sieve[1] = 0
p = 2
while p * p <= N:
    if sieve[p]:
        sieve[p * p::p] = bytes(len(range(p * p, N + 1, p)))
    p += 1
print("\n".join(str(sieve[:n + 1].count(1)) for n in qs))
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int t;
    cin >> t;
    vector<int> qs(t);
    for (auto &q : qs) cin >> q;
    int N = *max_element(qs.begin(), qs.end());
    vector<char> isPrime(N + 1, 1);
    isPrime[0] = 0;
    if (N >= 1) isPrime[1] = 0;
    for (long long p = 2; p * p <= N; p++)
        if (isPrime[p])
            for (long long q = p * p; q <= N; q += p) isPrime[q] = 0;
    vector<int> cnt(N + 1, 0);
    for (int i = 1; i <= N; i++) cnt[i] = cnt[i - 1] + isPrime[i];
    for (int n : qs) cout << cnt[n] << "\n";
    return 0;
}
""",
    ),
    dict(
        id="modular-power-fast",
        title="Fast Modular Power",
        difficulty="medium",
        category="Number Theory",
        tags=["modular-arithmetic", "exponentiation-by-squaring", "math"],
        inspired_by="CSES Exponentiation; the classic binary exponentiation",
        statement="""
Compute `aᵇ mod m` for several triples.

The exponent can be as big as 10¹⁸ — multiplying `a` by itself `b` times would
take millions of years. **Exponentiation by squaring** needs only about
`2·log₂ b` multiplications: `a¹³ = a⁸ · a⁴ · a¹` because `13 = 1101₂`.

By convention `a⁰ = 1` (also for `a = 0`), and the result is always reduced
modulo `m`, so with `m = 1` every answer is 0.
""",
        input_format="""First line: `t` (1 ≤ t ≤ 100).
Next `t` lines: `a b m` (0 ≤ a, b ≤ 10¹⁸, 1 ≤ m ≤ 10⁹).""",
        output_format="For each triple, `aᵇ mod m` on its own line.",
        hints=[
            "Keep `result = 1 % m` and `base = a % m`. Look at the bits of `b` from the lowest: if the bit is 1, "
            "`result = result * base % m`; then square `base = base * base % m` and shift `b >>= 1`.",
            "Reduce `a % m` **first**: with `m ≤ 10⁹`, every product of two reduced numbers is below 10¹⁸ and fits in "
            "a C++ `long long`.",
            "Python has this built in as `pow(a, b, m)` — but write the loop once yourself; it's the same trick used in "
            "RSA cryptography.",
        ],
        samples=["3\n2 10 1000\n3 13 7\n5 0 3"],
        tests=["1\n0 0 1", "2\n0 0 5\n0 7 5", "1\n1000000000000000000 1000000000000000000 1000000000",
               "1\n2 1000000000000000000 1000000007", "1\n123456789 987654321 1"],
        gen=_modpow_gen,
        starter_python="""t = int(input())
for _ in range(t):
    a, b, m = map(int, input().split())
    result = 1 % m
    base = a % m
    # TODO: exponentiation by squaring
    print(result)
""",
        starter_cpp="""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long a, b, m;
        cin >> a >> b >> m;
        long long result = 1 % m, base = a % m;
        // TODO: exponentiation by squaring
        cout << result << "\\n";
    }
    return 0;
}
""",
        solution_python=r"""t = int(input())
out = []
for _ in range(t):
    a, b, m = map(int, input().split())
    result = 1 % m
    base = a % m
    while b:
        if b & 1:
            result = result * base % m
        base = base * base % m
        b >>= 1
    out.append(result)
print("\n".join(map(str, out)))
""",
        solution_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long a, b, m;
        cin >> a >> b >> m;
        long long result = 1 % m, base = a % m;
        while (b > 0) {
            if (b & 1) result = result * base % m;
            base = base * base % m;
            b >>= 1;
        }
        cout << result << "\n";
    }
    return 0;
}
""",
    ),
]
