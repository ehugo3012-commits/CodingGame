"""Hard / expert: fast matrix exponentiation for recurrences and walk counting."""

MOD = 10**9 + 7


def _gen_recurrence(rng):
    tests = []
    for q, nmax in [(1000, 10**18), (200, 100), (100, 10**18)]:
        a0, a1 = rng.randint(0, MOD - 1), rng.randint(0, MOD - 1)
        x, y = rng.randint(0, MOD - 1), rng.randint(0, MOD - 1)
        ns = [rng.randint(0, nmax) for _ in range(q)]
        tests.append(f"{a0} {a1} {x} {y}\n{q}\n" + "\n".join(map(str, ns)))
    # Fibonacci at huge and boundary indices
    tests.append("0 1 1 1\n6\n0\n1\n2\n1000000000000000000\n999999999999999999\n2000000016")
    return tests


def _gen_walks(rng):
    tests = []
    for n, m, k, loops in [(20, 120, 10**18, True), (20, 30, 999999999999999989, False), (15, 225, 123456789, True),
                           (8, 10, 10**17, False), (20, 400, 10**18 - 1, True)]:
        edges = []
        while len(edges) < m:
            a, b = rng.randint(1, n), rng.randint(1, n)
            if a == b and not loops:
                continue
            edges.append((a, b))
        tests.append(f"{n} {m} {k}\n" + "\n".join(f"{a} {b}" for a, b in edges))
    # bipartite-ish graph: only even-length walks exist between 1 and 1, n is on the other side
    n = 6
    edges = [(1, 2), (2, 1), (3, 4), (4, 3), (1, 4), (4, 1), (3, 6), (6, 3), (5, 2), (2, 5)]
    tests.append(f"{n} {len(edges)} 1000000000000000000\n" + "\n".join(f"{a} {b}" for a, b in edges))
    return tests


PROBLEMS = [
    dict(
        id="linear-recurrence-huge-index",
        title="Rabbit Colony Forecast",
        difficulty="hard",
        category="Math",
        tags=["matrix-exponentiation", "linear-recurrence", "fibonacci", "fast-power"],
        inspired_by="Fibonacci via matrix power (CSES 1722 Fibonacci Numbers), generalised",
        statement="""
A biologist models a rabbit colony with the recurrence

```
a(i) = x · a(i − 1) + y · a(i − 2)      (mod 10⁹ + 7)
```

with given starting values `a(0)` and `a(1)` (for `a(0) = 0, a(1) = 1, x = y = 1` this is the Fibonacci sequence).

Answer `q` forecasts: for each `n`, print `a(n) mod 10⁹ + 7`. The indices go up to 10¹⁸, so stepping through
the sequence is out of the question.
""",
        input_format="""
First line: `a0 a1 x y` (0 ≤ each < 10⁹ + 7).
Second line: `q` (1 ≤ q ≤ 1000). Next `q` lines: one index `n` (0 ≤ n ≤ 10¹⁸).
""",
        output_format="For each forecast, one line with `a(n) mod 10⁹ + 7`.",
        hints=[
            "Write one step as a matrix: `[a(i+1), a(i)]ᵀ = M · [a(i), a(i−1)]ᵀ` with `M = [[x, y], [1, 0]]`. "
            "Then `[a(n+1), a(n)]ᵀ = Mⁿ · [a(1), a(0)]ᵀ`.",
            "Compute `Mⁿ` by **binary exponentiation** (square-and-multiply): O(log n) multiplications of 2×2 matrices.",
            "With 1000 queries, precompute the squares `M, M², M⁴, …, M^(2⁵⁹)` once; then for each query multiply the "
            "starting vector by the squares whose bit is set in `n` (all powers of `M` commute, so the order does not matter).",
            "C++: entries are below 10⁹+7, so a product of two fits in `long long`/`unsigned long long` — reduce modulo after "
            "every multiplication. Read `n` as `long long` (10¹⁸ < 9.2·10¹⁸).",
        ],
        samples=["0 1 1 1\n4\n0\n1\n10\n50", "2 3 2 0\n3\n0\n1\n5"],
        tests=["5 7 0 0\n3\n0\n1\n2", "1 1 0 1\n3\n2\n3\n1000000000000000000",
               "1000000006 1000000006 1000000006 1000000006\n2\n3\n1000000000000000000"],
        gen=_gen_recurrence,
        starter_python="""import sys

MOD = 10**9 + 7

def main():
    data = list(map(int, sys.stdin.read().split()))
    a0, a1, x, y = data[0], data[1], data[2], data[3]
    q = data[4]
    out = []
    for n in data[5:5 + q]:
        # TODO: a(n) via powers of the matrix [[x, y], [1, 0]]
        out.append(0)
    print("\\n".join(map(str, out)))

main()
""",
        starter_cpp="""#include <iostream>
#include <array>
using namespace std;

typedef unsigned long long ull;
typedef array<array<ull,2>,2> Mat;
const ull MOD = 1000000007ULL;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    ull a0, a1, x, y;
    int q;
    cin >> a0 >> a1 >> x >> y >> q;
    while (q--) {
        ull n;
        cin >> n;
        // TODO: a(n) via powers of the matrix [[x, y], [1, 0]]
        cout << 0 << "\\n";
    }
    return 0;
}
""",
        solution_python="""import sys

MOD = 10**9 + 7

def mul(A, B):
    return ((A[0] * B[0] + A[1] * B[2]) % MOD, (A[0] * B[1] + A[1] * B[3]) % MOD,
            (A[2] * B[0] + A[3] * B[2]) % MOD, (A[2] * B[1] + A[3] * B[3]) % MOD)

def main():
    data = list(map(int, sys.stdin.read().split()))
    a0, a1, x, y = data[0], data[1], data[2], data[3]
    q = data[4]
    squares = [(x % MOD, y % MOD, 1, 0)]          # M^(2^i), stored row-major as a 4-tuple
    for _ in range(60):
        squares.append(mul(squares[-1], squares[-1]))
    out = []
    for n in data[5:5 + q]:
        u, v = a1, a0                              # vector [a(1), a(0)]
        i = 0
        while n:
            if n & 1:
                A = squares[i]
                u, v = (A[0] * u + A[1] * v) % MOD, (A[2] * u + A[3] * v) % MOD
            n >>= 1
            i += 1
        out.append(v)
    print("\\n".join(map(str, out)))

main()
""",
        solution_cpp="""#include <iostream>
#include <array>
using namespace std;

typedef unsigned long long ull;
typedef array<array<ull,2>,2> Mat;
const ull MOD = 1000000007ULL;

Mat mul(const Mat &A, const Mat &B) {
    Mat C{};
    for (int i = 0; i < 2; i++)
        for (int j = 0; j < 2; j++)
            C[i][j] = (A[i][0] * B[0][j] % MOD + A[i][1] * B[1][j] % MOD) % MOD;
    return C;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    ull a0, a1, x, y;
    int q;
    cin >> a0 >> a1 >> x >> y >> q;
    while (q--) {
        ull n;
        cin >> n;
        Mat R{}; R[0][0] = R[1][1] = 1;            // identity
        Mat M{}; M[0][0] = x; M[0][1] = y; M[1][0] = 1; M[1][1] = 0;
        for (ull e = n; e; e >>= 1) {
            if (e & 1) R = mul(R, M);
            M = mul(M, M);
        }
        // [a(n+1), a(n)] = R * [a1, a0]
        cout << (R[1][0] * a1 % MOD + R[1][1] * a0 % MOD) % MOD << "\\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="walks-of-length-k",
        title="Exactly K Flights",
        difficulty="expert",
        category="Math",
        tags=["matrix-exponentiation", "graphs", "counting", "modulo"],
        inspired_by="CSES 1723 Graph Paths I",
        statement="""
An airline has `n` airports and `m` one-way flights (there may be several flights
between the same pair, and even sightseeing flights that return to the same airport).

A traveller starts at airport `1` and takes **exactly `k` flights**, one after the
other, ending at airport `n`. Airports may be revisited. How many different flight
sequences are possible? Print the answer modulo 10⁹ + 7.

`k` can be as large as 10¹⁸.
""",
        input_format="""
First line: `n m k` (1 ≤ n ≤ 20, 0 ≤ m ≤ 400, 1 ≤ k ≤ 10¹⁸).
Next `m` lines: `a b` — a flight from `a` to `b` (1 ≤ a, b ≤ n).
""",
        output_format="One integer: the number of flight sequences modulo 10⁹ + 7.",
        hints=[
            "Let `A` be the **adjacency matrix**: `A[i][j]` = number of flights from `i` to `j`. "
            "Then `(A²)[i][j]` counts 2-flight sequences from `i` to `j` (sum over the middle airport), and in general "
            "`(Aᵏ)[i][j]` counts `k`-flight sequences.",
            "The answer is `(Aᵏ)[1][n]` — compute the power with **binary exponentiation**: about 60 squarings plus "
            "≤ 60 extra multiplications, each O(n³) = 8000 steps.",
            "Cheaper variant: keep only the row vector `e₁` (start at airport 1) and multiply it by `A^(2^i)` for every set bit of `k`; "
            "vector × matrix is just O(n²).",
            "C++: entries are < 10⁹+7, so one product is < 1.0·10¹⁸ but a sum of 20 products overflows 64 bits — "
            "reduce modulo after **each** addition.",
        ],
        samples=["3 4 2\n1 2\n2 3\n1 3\n3 3", "2 1 3\n1 2"],
        tests=["1 0 1", "1 1 1000000000000000000\n1 1", "2 2 5\n1 2\n2 1", "2 2 6\n1 2\n2 1",
               "3 6 4\n1 2\n1 2\n2 3\n3 1\n2 2\n1 3"],
        gen=_gen_walks,
        starter_python="""import sys

MOD = 10**9 + 7

def main():
    data = list(map(int, sys.stdin.read().split()))
    n, m, k = data[0], data[1], data[2]
    A = [[0] * n for _ in range(n)]
    for i in range(m):
        a, b = data[3 + 2 * i] - 1, data[4 + 2 * i] - 1
        A[a][b] += 1
    # TODO: (A^k)[0][n-1] via binary exponentiation
    print(0)

main()
""",
        starter_cpp="""#include <iostream>
#include <vector>
using namespace std;

typedef unsigned long long ull;
typedef vector<vector<ull>> Mat;
const ull MOD = 1000000007ULL;

int main() {
    int n, m;
    ull k;
    cin >> n >> m >> k;
    Mat A(n, vector<ull>(n, 0));
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        A[a - 1][b - 1]++;
    }
    // TODO: (A^k)[0][n-1] via binary exponentiation
    cout << 0 << "\\n";
    return 0;
}
""",
        solution_python="""import sys

MOD = 10**9 + 7

def mat_mul(X, Y):
    cols = list(zip(*Y))
    return [[sum(a * b for a, b in zip(row, col)) % MOD for col in cols] for row in X]

def main():
    data = list(map(int, sys.stdin.read().split()))
    n, m, k = data[0], data[1], data[2]
    A = [[0] * n for _ in range(n)]
    for i in range(m):
        a, b = data[3 + 2 * i] - 1, data[4 + 2 * i] - 1
        A[a][b] += 1
    vec = [0] * n
    vec[0] = 1                       # row vector: start at airport 1
    P = A
    while k:
        if k & 1:
            vec = [sum(vec[i] * P[i][j] for i in range(n)) % MOD for j in range(n)]
        k >>= 1
        if k:
            P = mat_mul(P, P)
    print(vec[n - 1])

main()
""",
        solution_cpp="""#include <iostream>
#include <vector>
using namespace std;

typedef unsigned long long ull;
typedef vector<vector<ull>> Mat;
const ull MOD = 1000000007ULL;

Mat mul(const Mat &X, const Mat &Y) {
    int n = X.size();
    Mat Z(n, vector<ull>(n, 0));
    for (int i = 0; i < n; i++)
        for (int t = 0; t < n; t++) {
            if (!X[i][t]) continue;
            for (int j = 0; j < n; j++) Z[i][j] = (Z[i][j] + X[i][t] * Y[t][j]) % MOD;
        }
    return Z;
}

int main() {
    int n, m;
    ull k;
    cin >> n >> m >> k;
    Mat A(n, vector<ull>(n, 0));
    for (int i = 0; i < m; i++) {
        int a, b;
        cin >> a >> b;
        A[a - 1][b - 1]++;
    }
    Mat R(n, vector<ull>(n, 0));
    for (int i = 0; i < n; i++) R[i][i] = 1;
    for (; k; k >>= 1) {
        if (k & 1) R = mul(R, A);
        A = mul(A, A);
    }
    cout << R[0][n - 1] << "\\n";
    return 0;
}
""",
    ),
]
