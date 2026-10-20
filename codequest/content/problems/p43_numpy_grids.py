"""Math & Data: 2-D grid filters and matrix exponentiation with NumPy."""


def _grid(rng, h, w, lo, hi):
    return "\n".join(" ".join(str(rng.randint(lo, hi)) for _ in range(w)) for _ in range(h))


def _gen_conv(rng):
    out = []
    for _ in range(4):
        h, w = rng.randint(1, 10), rng.randint(1, 10)
        out.append(f"{h} {w}\n{_grid(rng, h, w, 0, 9)}\n{_grid(rng, 3, 3, -2, 2)}")
    return out


def _gen_recur(rng):
    out = []
    for k in (1, 2, 3, 4):
        m = rng.choice([2, 10, 1000, 10**9 + 7, rng.randint(2, 10**9)])
        cs = [rng.randrange(m) for _ in range(k)]
        a0 = [rng.randrange(m) for _ in range(k)]
        qs = [rng.choice([rng.randint(0, 20), rng.randint(0, 10**18)]) for _ in range(rng.randint(1, 5))]
        out.append(f"{k} {m}\n{' '.join(map(str, cs))}\n{' '.join(map(str, a0))}\n{len(qs)}\n"
                   + "\n".join(map(str, qs)))
    return out


PROBLEMS = [
    dict(
        id="md-grid-convolution",
        title="Image Filter",
        difficulty="medium",
        category="Math & Data",
        languages=["python"],
        tags=["numpy", "convolution", "image-processing", "slicing"],
        inspired_by="Image kernels in computer vision (box blur, edge detection, sharpen)",
        statement="""
A grayscale image is just a 2-D grid of numbers. Many image effects — blur,
sharpen, edge detection — are computed by sliding a small **kernel** over the
image: each output pixel is the weighted sum of the 3×3 neighbourhood around
the corresponding input pixel.

out[i][j] = Σ K[a][b] · G[i + a − 1][j + b − 1]   for a, b ∈ {0, 1, 2}

Pixels outside the image count as 0 (**zero padding**), so the output has
the same size as the input. (The kernel is *not* flipped — this is what image
libraries usually call "filtering"; mathematicians call it cross-correlation.)

For example the kernel `0 -1 0 / -1 4 -1 / 0 -1 0` highlights edges: it is 0
wherever the image is flat.
""",
        input_format="""
First line: `H W` (1 ≤ H, W ≤ 12).
Next `H` lines: `W` integers each, the image (0 ≤ pixel ≤ 9).
Next 3 lines: 3 integers each, the kernel `K` (|entry| ≤ 5).
""",
        output_format="`H` lines with `W` integers each: the filtered image.",
        hints=[
            "`np.pad(G, 1)` surrounds the grid with a border of zeros, giving shape `(H + 2, W + 2)`.",
            "In the padded grid `P`, the slice `P[a:a + H, b:b + W]` lines up every pixel with its neighbour at "
            "offset (a − 1, b − 1).",
            "So the whole filter is the sum over the 9 kernel cells of `K[a, b] * P[a:a + H, b:b + W]` — "
            "only 9 array operations, no per-pixel loop.",
        ],
        samples=["3 3\n0 0 0\n0 9 0\n0 0 0\n1 1 1\n1 1 1\n1 1 1",
                 "3 4\n1 1 1 1\n1 5 5 1\n1 1 1 1\n0 -1 0\n-1 4 -1\n0 -1 0"],
        tests=["1 1\n7\n1 2 3\n4 5 6\n7 8 9", "2 2\n1 2\n3 4\n0 0 0\n0 0 1\n0 0 0",
               "1 5\n1 2 3 4 5\n0 0 0\n-1 0 1\n0 0 0"],
        gen=_gen_conv,
        time_limit=5,
        starter_python="""import sys
import numpy as np

data = sys.stdin.read().split()
H, W = int(data[0]), int(data[1])
G = np.array(data[2:2 + H * W], dtype=int).reshape(H, W)
K = np.array(data[2 + H * W:2 + H * W + 9], dtype=int).reshape(3, 3)

# TODO: apply the kernel with zero padding and print the result
""",
        solution_python="""import sys
import numpy as np

data = sys.stdin.read().split()
H, W = int(data[0]), int(data[1])
G = np.array(data[2:2 + H * W], dtype=int).reshape(H, W)
K = np.array(data[2 + H * W:2 + H * W + 9], dtype=int).reshape(3, 3)
P = np.pad(G, 1)
out = np.zeros((H, W), dtype=int)
for a in range(3):
    for b in range(3):
        out += K[a, b] * P[a:a + H, b:b + W]
for row in out:
    print(*row)
""",
    ),
    dict(
        id="md-matrix-recurrence-mod",
        title="Recurrences at Warp Speed",
        difficulty="hard",
        category="Math & Data",
        languages=["python"],
        tags=["numpy", "matrix-power", "linear-recurrence", "modular-arithmetic"],
        inspired_by="Fibonacci via matrix exponentiation (Project Euler / competitive-programming classic)",
        statement="""
A **linear recurrence** of order `k` defines each term from the previous `k`:

aₙ = c₁·aₙ₋₁ + c₂·aₙ₋₂ + … + cₖ·aₙ₋ₖ

Fibonacci is the case `k = 2`, `c = (1, 1)`. Given the coefficients, the first
`k` terms a₀ … aₖ₋₁ and a modulus `m`, answer queries "what is aₙ mod m?" for
`n` up to 10¹⁸.

The trick: the vector of the last `k` terms is multiplied by a fixed `k×k`
**companion matrix** at every step, so jumping `n` steps means raising that
matrix to the `n`-th power — which repeated squaring does in about log₂ n
multiplications.
""",
        input_format="""
Line 1: `k m` (1 ≤ k ≤ 4, 2 ≤ m ≤ 1.1·10⁹).
Line 2: `k` integers `c₁ … cₖ` (0 ≤ cᵢ < m).
Line 3: `k` integers `a₀ … aₖ₋₁` (0 ≤ aᵢ < m).
Line 4: `q` (1 ≤ q ≤ 10). Next `q` lines: one integer `n` each (0 ≤ n ≤ 10¹⁸).
""",
        output_format="For each query print aₙ mod m on its own line.",
        hints=[
            "Companion matrix: with state `v = [aₙ₊ₖ₋₁, …, aₙ₊₁, aₙ]`, the next state is `M @ v`, where the first row "
            "of `M` is `c₁ … cₖ` and below it sits a shifted identity (`M[i, i − 1] = 1`).",
            "`np.linalg.matrix_power` can't reduce modulo `m`, and NumPy's `int64` silently **wraps around** on "
            "overflow. Write your own square-and-multiply loop and apply `% m` after every product.",
            "Entries stay below m < 2³¹, so each product is < 2⁶², and a row·column sum of k ≤ 4 such products still "
            "fits in `int64` (< 9.2·10¹⁸). (Using `dtype=object` — Python integers — avoids the worry entirely.)",
            "Then aₙ is the **last** entry of `Mⁿ @ [aₖ₋₁, …, a₁, a₀]`.",
        ],
        samples=["2 1000000007\n1 1\n0 1\n3\n10\n50\n1000000000000000000"],
        tests=["1 7\n3\n2\n4\n0\n1\n2\n100", "4 2\n1 1 1 1\n1 0 0 0\n3\n0\n4\n123456789",
               "3 1000\n0 0 0\n5 6 7\n4\n0\n2\n3\n999999999999999999"],
        gen=_gen_recur,
        time_limit=5,
        starter_python="""import sys
import numpy as np

data = sys.stdin.read().split()
k, m = int(data[0]), int(data[1])
c = [int(v) for v in data[2:2 + k]]
a = [int(v) for v in data[2 + k:2 + 2 * k]]
q = int(data[2 + 2 * k])
queries = [int(v) for v in data[3 + 2 * k:3 + 2 * k + q]]

# TODO: build the companion matrix and answer each query with fast matrix powers mod m
""",
        solution_python="""import sys
import numpy as np

data = sys.stdin.read().split()
k, m = int(data[0]), int(data[1])
c = [int(v) for v in data[2:2 + k]]
a = [int(v) for v in data[2 + k:2 + 2 * k]]
q = int(data[2 + 2 * k])
queries = [int(v) for v in data[3 + 2 * k:3 + 2 * k + q]]

M = np.zeros((k, k), dtype=np.int64)
M[0, :] = c
for i in range(1, k):
    M[i, i - 1] = 1
v0 = np.array(a[::-1], dtype=np.int64)


def mat_pow(A, e):
    R = np.eye(k, dtype=np.int64)
    while e:
        if e & 1:
            R = (R @ A) % m
        A = (A @ A) % m
        e >>= 1
    return R


for n in queries:
    print(int(((mat_pow(M, n) @ v0) % m)[-1]))
""",
    ),
]
