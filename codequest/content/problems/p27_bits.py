"""Bit Manipulation: popcounts, XOR tricks, powers of two, Gray codes."""


def _arr(xs):
    return " ".join(map(str, xs))


def _bits_gen(rng):
    qs = [rng.randint(1, 10**15) for _ in range(30)] + [rng.randint(1, 1000) for _ in range(20)]
    qs += [(1 << k) - 1 for k in range(1, 50, 7)] + [1 << k for k in range(0, 50, 9)]
    return [f"{len(qs)}\n" + "\n".join(map(str, qs))]


def _triples_case(rng, m, lim):
    vals = rng.sample(range(0, lim + 1), m + 1)
    single = vals[0]
    arr = [single] + [v for v in vals[1:] for _ in range(3)]
    rng.shuffle(arr)
    return f"{len(arr)}\n{_arr(arr)}"


def _triples_gen(rng):
    return [_triples_case(rng, 0, 10), _triples_case(rng, 3, 10), _triples_case(rng, 50, 1000),
            _triples_case(rng, 1300, 10**4), _triples_case(rng, 600, 2**31 - 1)]


def _pow2_gen(rng):
    qs = []
    for _ in range(40):
        k = rng.randint(0, 59)
        r = rng.random()
        if r < 0.4:
            qs.append(1 << k)
        elif r < 0.6:
            qs.append((1 << k) + rng.choice((-1, 1)))
        elif r < 0.8:
            qs.append(rng.randint(-10**18, 10**18))
        else:
            qs.append(-(1 << k))
    qs = [q for q in qs if abs(q) <= 10**18]
    return [f"{len(qs)}\n" + "\n".join(map(str, qs))]


PROBLEMS = [
    dict(
        id="total-set-bits-1-to-n",
        title="Total Set Bits from 1 to n",
        difficulty="medium",
        category="Bit Manipulation",
        tags=["bits", "popcount", "math", "counting"],
        inspired_by="LeetCode #338 Counting Bits; CSES Counting Bits",
        statement="""
Write the numbers `1, 2, 3, …, n` in binary and count **all** the `1` digits.

For `n = 5`: `1, 10, 11, 100, 101` contain `1 + 1 + 2 + 1 + 2 = 7` ones.

`n` can be as large as 10¹⁵, so looping over every number is far too slow —
count the ones **column by column** instead.
""",
        input_format="First line: `t` (1 ≤ t ≤ 100). Next `t` lines: `n` (1 ≤ n ≤ 10¹⁵).",
        output_format="For each `n`, the total number of `1` bits in the binary forms of 1 … n.",
        hints=[
            "Look at a single bit position `b` (value `2ᵇ`) over 0, 1, 2, …: it is `0` for 2ᵇ numbers, then `1` for 2ᵇ "
            "numbers, repeating with period `2ᵇ⁺¹`.",
            "Among `0 … n` (that's `n + 1` numbers) there are `(n + 1) // 2ᵇ⁺¹` full periods, each contributing `2ᵇ` "
            "ones, plus a partial period contributing `max(0, (n + 1) % 2ᵇ⁺¹ − 2ᵇ)`.",
            "Sum that over `b = 0 … 50`. In C++ use `long long` and shifts like `1LL << b` "
            "(plain `1 << 40` overflows an `int`).",
        ],
        samples=["3\n5\n1\n7"],
        tests=["1\n2", "4\n3\n4\n8\n16", "1\n1000000000000000", "2\n562949953421311\n999999999999999"],
        gen=_bits_gen,
        starter_python="""t = int(input())
for _ in range(t):
    n = int(input())
    total = 0
    # TODO: add the contribution of every bit position b
    print(total)
""",
        starter_cpp="""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long n, total = 0;
        cin >> n;
        // TODO: add the contribution of every bit position b (use 1LL << b)
        cout << total << "\\n";
    }
    return 0;
}
""",
        solution_python=r"""t = int(input())
out = []
for _ in range(t):
    n = int(input())
    total = 0
    b = 0
    while (1 << b) <= n:
        period = 1 << (b + 1)
        half = 1 << b
        total += (n + 1) // period * half + max(0, (n + 1) % period - half)
        b += 1
    out.append(total)
print("\n".join(map(str, out)))
""",
        solution_cpp=r"""#include <iostream>
#include <algorithm>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long n, total = 0;
        cin >> n;
        for (int b = 0; (1LL << b) <= n; b++) {
            long long period = 1LL << (b + 1), half = 1LL << b;
            total += (n + 1) / period * half + max(0LL, (n + 1) % period - half);
        }
        cout << total << "\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="single-among-triples",
        title="Single Among Triples",
        difficulty="medium",
        category="Bit Manipulation",
        tags=["bits", "xor", "counting"],
        inspired_by="LeetCode #136 / #137 Single Number (I & II)",
        statement="""
A list contains `3m + 1` non-negative integers: every value appears **exactly
three times**, except one value that appears **once**. Find that lonely value.

(Warm-up idea: if everything appeared *twice*, XOR-ing all numbers would
cancel the pairs. With triples XOR alone doesn't work — but thinking about
each bit separately does.)

A hash map solves it too, but try for **O(1) extra memory**: a few integer
variables only.
""",
        input_format="""First line: `N = 3m + 1` (1 ≤ N ≤ 4000).
Second line: `N` integers (0 ≤ aᵢ < 2³¹).""",
        output_format="One integer: the value that appears once.",
        hints=[
            "Fix a bit position `b`. Count how many numbers have that bit set: `(x >> b) & 1`.",
            "Values that appear three times add a multiple of 3 to that count. So `count % 3` is exactly the bit `b` of "
            "the lonely value.",
            "Do this for `b = 0 … 30` and rebuild the answer with `ans |= 1 << b`. (The famous `ones`/`twos` "
            "two-variable trick does the same in a single pass — look it up after you solve it!)",
        ],
        samples=["4\n2 2 3 2", "7\n0 1 0 1 0 1 99"],
        tests=["1\n0", "1\n2147483647", "4\n5 5 5 0", "7\n2147483647 1 2147483647 1 2147483647 1 1073741824"],
        gen=_triples_gen,
        starter_python="""n = int(input())
a = list(map(int, input().split()))
ans = 0
for b in range(31):
    # TODO: count numbers with bit b set; use the count modulo 3
    pass
print(ans)
""",
        starter_cpp="""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    long long ans = 0;
    for (int b = 0; b < 31; b++) {
        // TODO: count numbers with bit b set; use the count modulo 3
    }
    cout << ans << "\\n";
    return 0;
}
""",
        solution_python=r"""n = int(input())
a = list(map(int, input().split()))
ans = 0
for b in range(31):
    c = sum((x >> b) & 1 for x in a)
    if c % 3:
        ans |= 1 << b
print(ans)
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    long long ones = 0, twos = 0;  // bits seen 1 (mod 3) times, 2 (mod 3) times
    for (long long x : a) {
        ones = (ones ^ x) & ~twos;
        twos = (twos ^ x) & ~ones;
    }
    cout << ones << "\n";
    return 0;
}
""",
    ),
    dict(
        id="is-it-a-power-of-two",
        title="Is It a Power of Two?",
        difficulty="easy",
        category="Bit Manipulation",
        tags=["bits", "powers-of-two"],
        inspired_by="LeetCode #231 Power of Two",
        statement="""
For each integer `x`, decide whether it is a power of two: `1, 2, 4, 8, …`
(that is, `x = 2ᵏ` for some `k ≥ 0`).

Zero and negative numbers are never powers of two.

You can solve this without any loop: a power of two has exactly **one** `1`
bit, and there's a famous one-line test for that.
""",
        input_format="First line: `t` (1 ≤ t ≤ 100). Next `t` lines: `x` (−10¹⁸ ≤ x ≤ 10¹⁸).",
        output_format="For each `x`, print `YES` or `NO` on its own line.",
        hints=[
            "Write a power of two and the number just below it in binary: `1000` and `0111`. What do they have in common?",
            "Subtracting 1 flips the lowest `1` bit and all zeros below it. So `x & (x − 1)` clears the lowest set bit.",
            "`x` is a power of two exactly when `x > 0` and `x & (x − 1) == 0`. In C++ read `x` as `long long`.",
        ],
        samples=["5\n1\n6\n16\n0\n-8"],
        tests=["1\n2", "3\n1000000000000000000\n576460752303423488\n-1000000000000000000", "2\n3\n1024"],
        gen=_pow2_gen,
        starter_python="""t = int(input())
for _ in range(t):
    x = int(input())
    # TODO: decide if x is a power of two
    print("NO")
""",
        starter_cpp="""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long x;
        cin >> x;
        bool power = false;  // TODO
        cout << (power ? "YES" : "NO") << "\\n";
    }
    return 0;
}
""",
        solution_python=r"""t = int(input())
out = []
for _ in range(t):
    x = int(input())
    out.append("YES" if x > 0 and x & (x - 1) == 0 else "NO")
print("\n".join(out))
""",
        solution_cpp=r"""#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long x;
        cin >> x;
        bool power = x > 0 && (x & (x - 1)) == 0;
        cout << (power ? "YES" : "NO") << "\n";
    }
    return 0;
}
""",
    ),
    dict(
        id="reflected-gray-sequence",
        title="Reflected Gray Code",
        difficulty="medium",
        category="Bit Manipulation",
        tags=["bits", "xor", "gray-code"],
        inspired_by="LeetCode #89 Gray Code; CSES Gray Code",
        statement="""
A **Gray code** lists all `2ⁿ` bit strings of length `n` so that neighbouring
strings differ in **exactly one bit**. They are used in rotary encoders, where
reading two bits changing at once would cause glitches.

Print the **binary-reflected** Gray code of length `n`. It is built like this:
start with `0` and `1` for `n = 1`; to go from `n − 1` to `n`, write the list
with a `0` in front, then the list **reversed** with a `1` in front.

```
n = 1: 0 1
n = 2: 00 01 11 10
n = 3: 000 001 011 010 110 111 101 100
```
""",
        input_format="One integer `n` (1 ≤ n ≤ 10).",
        output_format="`2ⁿ` lines: the reflected Gray code, each as an `n`-character bit string.",
        hints=[
            "You can follow the construction literally: keep a list, and for each new bit build "
            "`['0' + s for s in lst] + ['1' + s for s in reversed(lst)]`.",
            "There's also a closed formula: the `i`-th code word is `i ^ (i >> 1)`.",
            "Printing with exactly `n` digits: Python `format(g, f'0{n}b')`; C++ `bitset<10>(g).to_string().substr(10 - n)` "
            "(header `<bitset>`), or build the string bit by bit.",
        ],
        samples=["2", "3"],
        tests=["1", "4", "5", "8", "10"],
        starter_python="""n = int(input())
codes = []
# TODO: build the reflected Gray code of length n
print("\\n".join(codes))
""",
        starter_cpp="""#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<string> codes;
    // TODO: build the reflected Gray code of length n
    for (auto &s : codes) cout << s << "\\n";
    return 0;
}
""",
        solution_python=r"""n = int(input())
codes = ["0", "1"]
for _ in range(n - 1):
    codes = ["0" + s for s in codes] + ["1" + s for s in reversed(codes)]
print("\n".join(codes))
""",
        solution_cpp=r"""#include <iostream>
#include <string>
using namespace std;

int main() {
    int n;
    cin >> n;
    for (int i = 0; i < (1 << n); i++) {
        int g = i ^ (i >> 1);
        string s(n, '0');
        for (int b = 0; b < n; b++)
            if (g >> b & 1) s[n - 1 - b] = '1';
        cout << s << "\n";
    }
    return 0;
}
""",
    ),
]
