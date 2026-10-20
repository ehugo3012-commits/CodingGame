"""Hard / expert combinatorics: factorial tables, modular inverses, the reflection principle."""


def _gen_desk(rng):
    tests = []
    for q, nmax in [(1500, 200000), (300, 30), (200, 200000)]:
        lines = []
        for _ in range(q):
            t = rng.choice("CPM")
            n = rng.randint(1, nmax)
            r = rng.random()
            if r < 0.15:
                k = rng.randint(n, nmax)          # k may exceed n
            elif r < 0.25:
                k = rng.choice([0, n])
            else:
                k = rng.randint(0, n)
            lines.append(f"{t} {n} {k}")
        tests.append(f"{q}\n" + "\n".join(lines))
    return tests


def _gen_ballot(rng):
    tests = []
    for q, nmax in [(1500, 200000), (300, 20)]:
        lines = []
        for _ in range(q):
            n = rng.randint(0, nmax)
            r = rng.random()
            m = rng.randint(0, n) if r < 0.8 else (n if r < 0.9 else rng.randint(0, nmax))
            lines.append(f"{n} {m}")
        tests.append(f"{q}\n" + "\n".join(lines))
    return tests


PROBLEMS = [
    dict(
        id="combinatorics-query-desk",
        title="The Counting Help Desk",
        difficulty="hard",
        category="Math",
        tags=["combinatorics", "modular-inverse", "factorials", "fermat"],
        inspired_by="CSES 1079 Binomial Coefficients",
        statement="""
The counting help desk answers three kinds of questions, all **modulo 10⁹ + 7**:

* `C n k` — in how many ways can you **choose** `k` of `n` different books? (the binomial coefficient)
* `P n k` — in how many ways can you **line up** `k` of `n` different books on a shelf, where order matters?
* `M n k` — in how many ways can you buy `k` scoops of ice cream when there are `n` flavours and
  flavours may repeat? (order does not matter)

For `C` and `P`, the answer is 0 when `k > n`. Answer `q` questions quickly.
""",
        input_format="""
First line: `q` (1 ≤ q ≤ 2000).
Next `q` lines: a letter (`C`, `P` or `M`) and two integers `n k` (1 ≤ n ≤ 2·10⁵, 0 ≤ k ≤ 2·10⁵).
""",
        output_format="For each question, one line with the answer modulo 10⁹ + 7.",
        hints=[
            "All three are factorial formulas: `C(n,k) = n! / (k!(n−k)!)`, `P(n,k) = n! / (n−k)!`, and "
            "\"stars and bars\" gives `M(n,k) = C(n + k − 1, k)`.",
            "Division modulo a prime `p` means multiplying by a **modular inverse**. By Fermat's little theorem "
            "`x⁻¹ ≡ x^(p−2) (mod p)` — Python: `pow(x, p - 2, p)`; C++: write fast exponentiation.",
            "Precompute `fact[i]` for `i` up to the largest value needed (`n + k − 1` can reach 4·10⁵) and "
            "`inv_fact[i]`: compute `inv_fact[top]` with one `pow`, then go down with `inv_fact[i−1] = inv_fact[i] · i`.",
            "Then each question is O(1): e.g. `C = fact[n] · inv_fact[k] · inv_fact[n−k] mod p`. "
            "In C++ reduce after **every** multiplication so the product of two residues stays below 2⁶³.",
        ],
        samples=["4\nC 5 2\nP 5 2\nM 3 2\nC 2 3"],
        tests=[
            "1\nC 1 0",
            "3\nP 1 1\nP 1 2\nM 1 200000",
            "3\nC 200000 100000\nP 200000 200000\nM 200000 200000",
        ],
        gen=_gen_desk,
        starter_python="""import sys

MOD = 10**9 + 7

def main():
    data = sys.stdin.read().split()
    q = int(data[0])
    queries = [(data[1 + 3 * i], int(data[2 + 3 * i]), int(data[3 + 3 * i])) for i in range(q)]
    # TODO: precompute factorials and inverse factorials, answer each query
    print("\\n".join("0" for _ in queries))

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <string>
using namespace std;

const long long MOD = 1000000007LL;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    vector<char> type(q);
    vector<int> N(q), K(q);
    for (int i = 0; i < q; i++) cin >> type[i] >> N[i] >> K[i];
    // TODO: precompute factorials and inverse factorials, answer each query
    for (int i = 0; i < q; i++) cout << 0 << "\\n";
    return 0;
}
""",
        solution_python="""import sys

MOD = 10**9 + 7

def main():
    data = sys.stdin.read().split()
    q = int(data[0])
    queries = [(data[1 + 3 * i], int(data[2 + 3 * i]), int(data[3 + 3 * i])) for i in range(q)]
    top = max(n + k for _, n, k in queries)
    fact = [1] * (top + 1)
    for i in range(1, top + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv = [1] * (top + 1)
    inv[top] = pow(fact[top], MOD - 2, MOD)
    for i in range(top, 0, -1):
        inv[i - 1] = inv[i] * i % MOD

    def C(n, k):
        if k < 0 or k > n:
            return 0
        return fact[n] * inv[k] % MOD * inv[n - k] % MOD

    out = []
    for t, n, k in queries:
        if t == "C":
            out.append(C(n, k))
        elif t == "P":
            out.append(fact[n] * inv[n - k] % MOD if k <= n else 0)
        else:
            out.append(C(n + k - 1, k))
    print("\\n".join(map(str, out)))

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

const long long MOD = 1000000007LL;
vector<long long> fact, inv;

long long power(long long b, long long e) {
    long long r = 1; b %= MOD;
    while (e) { if (e & 1) r = r * b % MOD; b = b * b % MOD; e >>= 1; }
    return r;
}
long long C(long long n, long long k) {
    if (k < 0 || k > n) return 0;
    return fact[n] * inv[k] % MOD * inv[n - k] % MOD;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    vector<char> type(q);
    vector<int> N(q), K(q);
    int top = 1;
    for (int i = 0; i < q; i++) { cin >> type[i] >> N[i] >> K[i]; top = max(top, N[i] + K[i]); }
    fact.assign(top + 1, 1); inv.assign(top + 1, 1);
    for (int i = 1; i <= top; i++) fact[i] = fact[i - 1] * i % MOD;
    inv[top] = power(fact[top], MOD - 2);
    for (int i = top; i > 0; i--) inv[i - 1] = inv[i] * i % MOD;
    for (int i = 0; i < q; i++) {
        long long n = N[i], k = K[i], ans;
        if (type[i] == 'C') ans = C(n, k);
        else if (type[i] == 'P') ans = (k <= n) ? fact[n] * inv[n - k] % MOD : 0;
        else ans = C(n + k - 1, k);
        cout << ans << "\\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="ballot-lattice-paths",
        title="Never Behind in the Vote",
        difficulty="expert",
        category="Math",
        tags=["combinatorics", "reflection-principle", "catalan", "modular-inverse"],
        inspired_by="Project Euler #15 Lattice paths + Bertrand's ballot problem",
        statement="""
An election has two candidates. Alice receives `n` votes and Bob receives `m`
votes, and the votes are counted one by one. In how many counting orders is Alice
**never behind** Bob — at every moment Alice's count is at least Bob's?

Equivalently: count monotone lattice paths from `(0, 0)` to `(n, m)` using steps
`(+1, 0)` (a vote for Alice) and `(0, +1)` (a vote for Bob) that never go above the
diagonal `y = x`. Without the restriction this is the famous Project Euler #15
count `C(n + m, m)`.

Answer `q` elections, each modulo 10⁹ + 7.
""",
        input_format="""
First line: `q` (1 ≤ q ≤ 2000).
Next `q` lines: `n m` (0 ≤ n, m ≤ 2·10⁵).
""",
        output_format="For each election, one line with the number of valid counting orders modulo 10⁹ + 7.",
        hints=[
            "If `m > n` the answer is 0 (Bob ends ahead). Otherwise count **all** orders, `C(n + m, m)`, and subtract the bad ones.",
            "**Reflection principle**: a bad path touches the line `y = x + 1` for a first time. Reflect the part of the path "
            "*before* that touch across the line. This turns bad paths into paths from `(−1, 1)` to `(n, m)`, one-to-one.",
            "Paths from `(−1, 1)` to `(n, m)` use `n + 1` right-steps and `m − 1` up-steps: there are `C(n + m, m − 1)` of them. "
            "So the answer is `C(n + m, m) − C(n + m, m − 1)` (with `C(·, −1) = 0`). For `n = m` you get the Catalan numbers!",
            "Precompute factorials and inverse factorials up to 4·10⁵ once, and after the subtraction add the modulus "
            "before taking `%` so the result is never negative.",
        ],
        samples=["3\n2 1\n3 3\n1 2"],
        tests=["1\n0 0", "2\n5 0\n0 5", "3\n200000 200000\n200000 1\n1 1", "1\n10 10"],
        gen=_gen_ballot,
        starter_python="""import sys

MOD = 10**9 + 7

def main():
    data = list(map(int, sys.stdin.read().split()))
    q = data[0]
    queries = [(data[1 + 2 * i], data[2 + 2 * i]) for i in range(q)]
    # TODO: factorial tables + the reflection-principle formula
    print("\\n".join("0" for _ in queries))

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
using namespace std;

const long long MOD = 1000000007LL;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    vector<int> N(q), M(q);
    for (int i = 0; i < q; i++) cin >> N[i] >> M[i];
    // TODO: factorial tables + the reflection-principle formula
    for (int i = 0; i < q; i++) cout << 0 << "\\n";
    return 0;
}
""",
        solution_python="""import sys

MOD = 10**9 + 7

def main():
    data = list(map(int, sys.stdin.read().split()))
    q = data[0]
    queries = [(data[1 + 2 * i], data[2 + 2 * i]) for i in range(q)]
    top = max(1, max(n + m for n, m in queries))
    fact = [1] * (top + 1)
    for i in range(1, top + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv = [1] * (top + 1)
    inv[top] = pow(fact[top], MOD - 2, MOD)
    for i in range(top, 0, -1):
        inv[i - 1] = inv[i] * i % MOD

    def C(a, b):
        if b < 0 or b > a:
            return 0
        return fact[a] * inv[b] % MOD * inv[a - b] % MOD

    out = []
    for n, m in queries:
        if m > n:
            out.append(0)
        else:
            out.append((C(n + m, m) - C(n + m, m - 1)) % MOD)
    print("\\n".join(map(str, out)))

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

const long long MOD = 1000000007LL;
vector<long long> fact, inv;

long long power(long long b, long long e) {
    long long r = 1; b %= MOD;
    while (e) { if (e & 1) r = r * b % MOD; b = b * b % MOD; e >>= 1; }
    return r;
}
long long C(long long a, long long b) {
    if (b < 0 || b > a) return 0;
    return fact[a] * inv[b] % MOD * inv[a - b] % MOD;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    vector<int> N(q), M(q);
    int top = 1;
    for (int i = 0; i < q; i++) { cin >> N[i] >> M[i]; top = max(top, N[i] + M[i]); }
    fact.assign(top + 1, 1); inv.assign(top + 1, 1);
    for (int i = 1; i <= top; i++) fact[i] = fact[i - 1] * i % MOD;
    inv[top] = power(fact[top], MOD - 2);
    for (int i = top; i > 0; i--) inv[i - 1] = inv[i] * i % MOD;
    for (int i = 0; i < q; i++) {
        long long n = N[i], m = M[i];
        long long ans = (m > n) ? 0 : ((C(n + m, m) - C(n + m, m - 1)) % MOD + MOD) % MOD;
        cout << ans << "\\n";
    }
    return 0;
}
""",
    ),
]
