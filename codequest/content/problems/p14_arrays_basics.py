"""Arrays, part 1: scanning a list once."""


def _arr(rng, n, lo=-10**9, hi=10**9):
    return [rng.randint(lo, hi) for _ in range(n)]


def _case(a):
    return f"{len(a)}\n" + " ".join(map(str, a))


ARRAY_INPUT = "First line: `n` (1 ≤ n ≤ 1000). Second line: `n` integers `a₁ … aₙ` (−10⁹ ≤ aᵢ ≤ 10⁹)."

PY_READ = r"""n = int(input())
a = list(map(int, input().split()))
"""

CPP_READ = r"""    int n;
    cin >> n;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
"""

CPP_HEAD = r"""#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
"""


PROBLEMS = [
    dict(
        id="array-min-max",
        title="Smallest and Largest",
        difficulty="beginner",
        category="Arrays",
        tags=["arrays", "min-max", "loops"],
        inspired_by="HackerRank 'Mini-Max' theme",
        statement="""
A thermometer logged `n` readings. Report the coldest and the warmest one —
that is, the minimum and the maximum of the list.
""",
        input_format=ARRAY_INPUT,
        output_format="Two integers on one line: the minimum, then the maximum.",
        hints=[
            "Start with `lo = hi = a[0]`, then walk through the rest of the list and update them when you see something smaller or bigger.",
            "Python has built-ins `min(a)` and `max(a)`.",
            "C++: `*min_element(a.begin(), a.end())` and `*max_element(...)` from `<algorithm>` do it in one call.",
        ],
        samples=["5\n3 -1 4 1 5", "1\n42"],
        tests=["3\n7 7 7", "2\n1000000000 -1000000000", "4\n-5 -2 -9 -1",
               _case(list(range(1000, 0, -1)))],
        gen=lambda rng: [_case(_arr(rng, rng.randint(1, 120))) for _ in range(4)],
        starter_python=PY_READ + r"""# TODO: print the minimum and the maximum of a
""",
        starter_cpp=CPP_HEAD + CPP_READ + r"""    // TODO: print the minimum and the maximum of a
    return 0;
}
""",
        solution_python=PY_READ + r"""print(min(a), max(a))
""",
        solution_cpp=CPP_HEAD + CPP_READ + r"""    long long lo = a[0], hi = a[0];
    for (long long x : a) {
        if (x < lo) lo = x;
        if (x > hi) hi = x;
    }
    cout << lo << " " << hi << "\n";
    return 0;
}
""",
    ),
    dict(
        id="running-sum",
        title="Running Sum",
        difficulty="beginner",
        category="Arrays",
        tags=["arrays", "prefix-sums", "overflow"],
        inspired_by="LeetCode #1480 Running Sum of 1d Array",
        statement="""
A shop records the money gained or lost each day. The owner wants to see the
**running total**: after each day, how much has been earned in total so far?

Formally, output `s₁ … sₙ` where `sᵢ = a₁ + a₂ + … + aᵢ`.
""",
        input_format=ARRAY_INPUT,
        output_format="One line with `n` integers `s₁ … sₙ` separated by spaces.",
        hints=[
            "Keep one variable `total`; for every element add it to `total` and record the current value.",
            "Python: collect the results in a list and print with `print(*result)` (the `*` spreads the list into separate arguments).",
            "C++: totals can reach 10¹² — store them in `long long`, not `int`.",
        ],
        samples=["4\n1 2 3 4", "5\n3 -1 -2 5 0"],
        tests=["1\n-7", _case([10**9] * 150), _case([-10**9] * 150), "3\n0 0 0", "4\n5 -5 5 -5"],
        gen=lambda rng: [_case(_arr(rng, rng.randint(1, 120))) for _ in range(4)],
        starter_python=PY_READ + r"""result = []
# TODO: fill result with the running totals
print(*result)
""",
        starter_cpp=CPP_HEAD + CPP_READ + r"""    // TODO: print the running totals, separated by spaces
    return 0;
}
""",
        solution_python=PY_READ + r"""result = []
total = 0
for x in a:
    total += x
    result.append(total)
print(*result)
""",
        solution_cpp=CPP_HEAD + CPP_READ + r"""    long long total = 0;
    for (int i = 0; i < n; i++) {
        total += a[i];
        cout << total << (i + 1 < n ? " " : "\n");
    }
    return 0;
}
""",
    ),
    dict(
        id="sign-counts",
        title="Positive, Negative, Zero",
        difficulty="beginner",
        category="Arrays",
        tags=["arrays", "counting", "conditionals"],
        inspired_by="HackerRank 'Plus Minus' (counting variant)",
        statement="""
Count how many numbers in the list are **positive**, how many are
**negative**, and how many are exactly **zero**.
""",
        input_format=ARRAY_INPUT,
        output_format="Three integers on one line: the number of positive, negative and zero elements, in that order.",
        hints=[
            "Use three counters that all start at 0.",
            "For each element use `if / elif / else` (C++: `if / else if / else`) to decide which counter to increase.",
        ],
        samples=["6\n-4 3 -9 0 4 1"],
        tests=["1\n0", "1\n-1", "1\n1", "5\n0 0 0 0 0", "4\n1000000000 -1000000000 1 -1"],
        gen=lambda rng: [_case(_arr(rng, rng.randint(1, 300), -3, 3)) for _ in range(2)]
        + [_case(_arr(rng, rng.randint(1, 300))) for _ in range(2)],
        starter_python=PY_READ + r"""pos = neg = zero = 0
# TODO: count positives, negatives and zeros
print(pos, neg, zero)
""",
        starter_cpp=CPP_HEAD + CPP_READ + r"""    int pos = 0, neg = 0, zero = 0;
    // TODO: count positives, negatives and zeros
    cout << pos << " " << neg << " " << zero << "\n";
    return 0;
}
""",
        solution_python=PY_READ + r"""pos = sum(1 for x in a if x > 0)
neg = sum(1 for x in a if x < 0)
print(pos, neg, n - pos - neg)
""",
        solution_cpp=CPP_HEAD + CPP_READ + r"""    int pos = 0, neg = 0, zero = 0;
    for (long long x : a) {
        if (x > 0) pos++;
        else if (x < 0) neg++;
        else zero++;
    }
    cout << pos << " " << neg << " " << zero << "\n";
    return 0;
}
""",
    ),
    dict(
        id="second-largest-distinct",
        title="Runner-Up Score",
        difficulty="easy",
        category="Arrays",
        tags=["arrays", "min-max", "duplicates"],
        inspired_by="HackerRank 'Find the Runner-Up Score!'",
        statement="""
Given the scores of a competition, find the **runner-up score**: the largest
value that is strictly smaller than the maximum.

Several players may share the top score, so for `2 3 6 6 5` the answer is `5`,
not `6`. If every score is the same there is no runner-up — print `NONE`.
""",
        input_format=ARRAY_INPUT,
        output_format="The runner-up score, or `NONE` if it does not exist.",
        hints=[
            "Two passes work: first find the maximum, then find the largest element that is not equal to it.",
            "One pass also works: track `best` and `second`. When you see x > best, the old best becomes second; "
            "when best > x > second, x becomes the new second.",
            "Python shortcut: `sorted(set(a))` gives the distinct values in increasing order.",
            "Don't start `second` at 0 or −1 — scores can be negative! Use a flag (or `None`) for \"not found yet\".",
        ],
        samples=["5\n2 3 6 6 5", "3\n4 4 4"],
        tests=["1\n7", "2\n-1000000000 1000000000", "2\n5 5", "4\n-3 -1 -1 -2", "5\n9 9 9 9 8",
               "4\n1 2 3 4"],
        gen=lambda rng: [_case(_arr(rng, rng.randint(2, 300))) for _ in range(2)]
        + [_case(_arr(rng, rng.randint(2, 30), -2, 2)) for _ in range(3)],
        starter_python=PY_READ + r"""# TODO: print the runner-up score, or NONE
""",
        starter_cpp=CPP_HEAD + CPP_READ + r"""    // TODO: print the runner-up score, or NONE
    return 0;
}
""",
        solution_python=PY_READ + r"""vals = sorted(set(a))
print(vals[-2] if len(vals) >= 2 else "NONE")
""",
        solution_cpp=CPP_HEAD + CPP_READ + r"""    long long best = *max_element(a.begin(), a.end());
    bool found = false;
    long long second = 0;
    for (long long x : a) {
        if (x != best && (!found || x > second)) {
            second = x;
            found = true;
        }
    }
    if (found) cout << second << "\n";
    else cout << "NONE\n";
    return 0;
}
""",
    ),
]
