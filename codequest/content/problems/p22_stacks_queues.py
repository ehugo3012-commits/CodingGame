"""Stacks & Queues: monotonic stacks, expression evaluation, min-stack, monotonic deque."""


def _arr(xs):
    return " ".join(map(str, xs))


def _nge_gen(rng):
    out = []
    for n, lim in ((1, 9), (8, 5), (100, 1000), (3000, 10**4)):
        out.append(f"{n}\n{_arr(rng.randint(1, lim) for _ in range(n))}")
    n = 2000
    out.append(f"{n}\n{_arr(range(n, 0, -1))}")  # strictly decreasing: all -1
    return out


def _temps_gen(rng):
    out = []
    for n in (1, 7, 300, 3500):
        out.append(f"{n}\n{_arr(rng.randint(30, 100) for _ in range(n))}")
    return out


def _tdiv(a, b):
    q = abs(a) // abs(b)
    return -q if (a < 0) != (b < 0) else q


_LIM = 10**12


def _apply(op, a, b):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    return _tdiv(a, b)


def _rpn_build(rng, leaves, leafmax):
    """Return (tokens, value) of a random valid expression with `leaves` operands."""
    if leaves == 1:
        v = rng.randint(-leafmax, leafmax)
        return [str(v)], v
    k = rng.randint(1, leaves - 1)
    lt, lv = _rpn_build(rng, k, leafmax)
    rt, rv = _rpn_build(rng, leaves - k, leafmax)
    for op in (rng.choice("+-*/"), "+", "-"):
        if op == "/" and rv == 0:
            continue
        v = _apply(op, lv, rv)
        if abs(v) <= _LIM:
            return lt + rt + [op], v
    raise AssertionError("unreachable")


def _rpn_case(rng, leaves, leafmax):
    toks, _ = _rpn_build(rng, leaves, leafmax)
    return f"{len(toks)}\n{' '.join(toks)}"


def _rpn_gen(rng):
    return [_rpn_case(rng, 1, 1000), _rpn_case(rng, 3, 9), _rpn_case(rng, 8, 20),
            _rpn_case(rng, 40, 50), _rpn_case(rng, 400, 100), _rpn_case(rng, 1500, 10**6)]


def _minstack_case(rng, q, lim):
    ops, size = [], 0
    for _ in range(q - 1):
        r = rng.random()
        if size == 0 or r < 0.45:
            ops.append(f"push {rng.randint(-lim, lim)}")
            size += 1
        elif r < 0.65:
            ops.append("pop")
            size -= 1
        else:
            ops.append("top" if r < 0.8 else "min")
    if size == 0:
        ops.append(f"push {rng.randint(-lim, lim)}")
    ops.append("min")  # always end with a query that prints something
    return f"{len(ops)}\n" + "\n".join(ops)


def _minstack_gen(rng):
    return [_minstack_case(rng, 5, 10), _minstack_case(rng, 30, 5), _minstack_case(rng, 400, 1000),
            _minstack_case(rng, 2500, 10**4)]


def _win_gen(rng):
    out = []
    for n, k in ((1, 1), (6, 6), (10, 1), (200, 7), (3000, 1000), (3000, 40)):
        out.append(f"{n} {k}\n{_arr(rng.randint(-999, 999) for _ in range(n))}")
    return out


PROBLEMS = [
    dict(
        id="next-taller-to-the-right",
        title="Next Taller to the Right",
        difficulty="medium",
        category="Stacks & Queues",
        tags=["stack", "monotonic-stack"],
        inspired_by="LeetCode #496 / #503 Next Greater Element; CSES Nearest Smaller Values",
        statement="""
`n` people stand in a line facing right. For each person, find the height of
the **first person to their right who is strictly taller**. If nobody to the
right is taller, print `-1` for that person.

For heights `2 1 2 4 3` the answers are `4 2 4 -1 -1`.

A double loop is O(n²). A *monotonic stack* solves it in O(n): every person
is pushed and popped at most once.
""",
        input_format="First line: `n` (1 ≤ n ≤ 3000). Second line: `n` heights (1 ≤ hᵢ ≤ 10⁴).",
        output_format="One line with `n` integers: the next taller height for each person, or `-1`.",
        hints=[
            "Scan from left to right and keep a stack of *indices* of people who are still waiting for a taller "
            "person.",
            "When person `i` arrives, everyone on the stack shorter than `h[i]` has found their answer: pop them and "
            "set `ans[popped] = h[i]`. Then push `i`.",
            "The heights of the waiting indices on the stack are non-increasing from bottom to top — that's why "
            "popping from the top is enough. Python: a list with `.append` / `.pop()`; C++: `vector<int>` or `stack<int>`.",
        ],
        samples=["5\n2 1 2 4 3", "4\n1 3 2 4"],
        tests=["1\n7", "4\n5 5 5 5", "5\n1 2 3 4 5", "5\n5 4 3 2 1"],
        gen=_nge_gen,
        starter_python="""n = int(input())
h = list(map(int, input().split()))
ans = [-1] * n
stack = []  # indices still waiting for a taller person
for i in range(n):
    # TODO: pop everyone shorter than h[i], then push i
    pass
print(*ans)
""",
        starter_cpp="""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> h(n), ans(n, -1), st;
    for (auto &x : h) cin >> x;
    for (int i = 0; i < n; i++) {
        // TODO: pop shorter people, then push i
    }
    for (int i = 0; i < n; i++) cout << ans[i] << (i + 1 < n ? ' ' : '\\n');
    return 0;
}
""",
        solution_python=r"""n = int(input())
h = list(map(int, input().split()))
ans = [-1] * n
stack = []
for i in range(n):
    while stack and h[stack[-1]] < h[i]:
        ans[stack.pop()] = h[i]
    stack.append(i)
print(*ans)
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> h(n), ans(n, -1), st;
    for (auto &x : h) cin >> x;
    for (int i = 0; i < n; i++) {
        while (!st.empty() && h[st.back()] < h[i]) {
            ans[st.back()] = h[i];
            st.pop_back();
        }
        st.push_back(i);
    }
    for (int i = 0; i < n; i++) cout << ans[i] << (i + 1 < n ? ' ' : '\n');
    return 0;
}
""",
    ),
    dict(
        id="days-until-warmer",
        title="Days Until Warmer",
        difficulty="medium",
        category="Stacks & Queues",
        tags=["stack", "monotonic-stack"],
        inspired_by="LeetCode #739 Daily Temperatures",
        statement="""
You have a forecast of daily temperatures for `n` days. For each day, how many
days do you have to wait until a **strictly warmer** day? If no warmer day
follows, the answer for that day is `0`.

For `73 74 75 71 69 72 76 73` the answers are `1 1 4 2 1 1 0 0`.
""",
        input_format="First line: `n` (1 ≤ n ≤ 3500). Second line: `n` temperatures (30 ≤ tᵢ ≤ 100).",
        output_format="One line with `n` integers: the waiting time for each day.",
        hints=[
            "This is a 'next greater element' question, but the answer is a *distance*, so store indices.",
            "Keep a stack of indices of days that haven't seen a warmer day yet. When day `i` is warmer than the day "
            "on top, that day's answer is `i − top`; pop it and repeat.",
            "Every index is pushed once and popped at most once, so the whole scan is O(n).",
        ],
        samples=["8\n73 74 75 71 69 72 76 73", "3\n30 60 90"],
        tests=["1\n50", "4\n90 80 70 60", "5\n50 50 50 50 51"],
        gen=_temps_gen,
        starter_python="""n = int(input())
t = list(map(int, input().split()))
wait = [0] * n
stack = []
# TODO: monotonic stack of indices
print(*wait)
""",
        starter_cpp="""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> t(n), wait(n, 0), st;
    for (auto &x : t) cin >> x;
    // TODO: monotonic stack of indices
    for (int i = 0; i < n; i++) cout << wait[i] << (i + 1 < n ? ' ' : '\\n');
    return 0;
}
""",
        solution_python=r"""n = int(input())
t = list(map(int, input().split()))
wait = [0] * n
stack = []
for i, x in enumerate(t):
    while stack and t[stack[-1]] < x:
        j = stack.pop()
        wait[j] = i - j
    stack.append(i)
print(*wait)
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> t(n), wait(n, 0), st;
    for (auto &x : t) cin >> x;
    for (int i = 0; i < n; i++) {
        while (!st.empty() && t[st.back()] < t[i]) {
            wait[st.back()] = i - st.back();
            st.pop_back();
        }
        st.push_back(i);
    }
    for (int i = 0; i < n; i++) cout << wait[i] << (i + 1 < n ? ' ' : '\n');
    return 0;
}
""",
    ),
    dict(
        id="postfix-calculator",
        title="Postfix Calculator",
        difficulty="medium",
        category="Stacks & Queues",
        tags=["stack", "parsing", "expressions"],
        inspired_by="LeetCode #150 Evaluate Reverse Polish Notation",
        statement="""
In **postfix** (Reverse Polish) notation the operator comes *after* its two
operands, so no parentheses are ever needed:

| infix | postfix |
|---|---|
| `(2 + 1) * 3` | `2 1 + 3 *` |
| `4 + 13 / 5` | `4 13 5 / +` |

Evaluate a postfix expression made of integers and the operators `+ - * /`.

* Division is **integer division truncating toward zero**: `7 / -2 = -3`,
  `-7 / 2 = -3`.
* Operands can be negative, e.g. the token `-5` is a number, not an operator.
* The expression is always valid, never divides by zero, and every
  intermediate result satisfies |v| ≤ 10¹².
""",
        input_format="""First line: `m`, the number of tokens (1 ≤ m ≤ 3000).
Second line: the `m` tokens separated by spaces.""",
        output_format="One integer: the value of the expression.",
        hints=[
            "Use a stack. A number token is pushed. An operator pops the top two values — careful, the first one "
            "popped is the **right** operand — and pushes the result.",
            "A token is an operator only if it is exactly one of `+ - * /`; `-5` is a number. "
            "In Python, `int('-5')` handles the sign for you.",
            "Python's `//` rounds toward −∞ (`-7 // 2 == -4`). For truncation use `int(a / b)` only if values are small; "
            "safer: `q = abs(a) // abs(b)` and flip the sign when `a` and `b` have opposite signs. "
            "C++'s `/` on integers already truncates toward zero — use `long long`.",
        ],
        samples=["5\n2 1 + 3 *", "5\n4 13 5 / +", "13\n10 6 9 3 + -11 * / * 17 + 5 +"],
        tests=["1\n42", "1\n-7", "3\n7 -2 /", "3\n-7 2 /", "3\n-6 3 /", "3\n1000000 1000000 *",
               "5\n3 4 - 5 -"],
        gen=_rpn_gen,
        starter_python="""m = int(input())
tokens = input().split()
stack = []
for tok in tokens:
    if tok in ("+", "-", "*", "/"):
        b = stack.pop()
        a = stack.pop()
        result = 0  # TODO: compute a <tok> b
        stack.append(result)
    else:
        stack.append(int(tok))
print(stack[-1])
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    int m;
    cin >> m;
    vector<long long> st;
    for (int i = 0; i < m; i++) {
        string tok;
        cin >> tok;
        if (tok == "+" || tok == "-" || tok == "*" || tok == "/") {
            long long b = st.back(); st.pop_back();
            long long a = st.back(); st.pop_back();
            long long result = 0;  // TODO: compute a <tok> b
            st.push_back(result);
        } else {
            st.push_back(stoll(tok));
        }
    }
    cout << st.back() << "\\n";
    return 0;
}
""",
        solution_python=r"""m = int(input())
tokens = input().split()
stack = []
for tok in tokens:
    if tok in ("+", "-", "*", "/"):
        b = stack.pop()
        a = stack.pop()
        if tok == "+":
            stack.append(a + b)
        elif tok == "-":
            stack.append(a - b)
        elif tok == "*":
            stack.append(a * b)
        else:
            q = abs(a) // abs(b)
            stack.append(-q if (a < 0) != (b < 0) else q)
    else:
        stack.append(int(tok))
print(stack[-1])
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    int m;
    cin >> m;
    vector<long long> st;
    for (int i = 0; i < m; i++) {
        string tok;
        cin >> tok;
        if (tok == "+" || tok == "-" || tok == "*" || tok == "/") {
            long long b = st.back(); st.pop_back();
            long long a = st.back(); st.pop_back();
            long long r;
            if (tok == "+") r = a + b;
            else if (tok == "-") r = a - b;
            else if (tok == "*") r = a * b;
            else r = a / b;
            st.push_back(r);
        } else {
            st.push_back(stoll(tok));
        }
    }
    cout << st.back() << "\n";
    return 0;
}
""",
    ),
    dict(
        id="min-stack-console",
        title="Min-Stack Console",
        difficulty="medium",
        category="Stacks & Queues",
        tags=["stack", "design", "simulation"],
        inspired_by="LeetCode #155 Min Stack",
        statement="""
Simulate a stack that also reports its **minimum** instantly. Process `q`
commands:

* `push x` — push integer `x`,
* `pop` — remove the top element,
* `top` — print the top element,
* `min` — print the smallest element currently in the stack.

Every operation should take **O(1)** time — scanning the whole stack for each
`min` is the slow way. `pop`, `top` and `min` are only issued when the stack
is non-empty.
""",
        input_format="First line: `q` (1 ≤ q ≤ 3000). Next `q` lines: one command each (|x| ≤ 10⁴).",
        output_format="For every `top` and `min` command, print the answer on its own line.",
        hints=[
            "Keep a second stack (or store pairs): next to every pushed value remember the minimum of the stack "
            "*at that moment*.",
            "On `push x` the new minimum is `min(x, previous minimum)`; on `pop` both disappear together, so the "
            "previous minimum is restored automatically.",
            "Python: `stack.append((x, m))`, `stack[-1][1]`. C++: `vector<pair<int,int>>` with `push_back` / `back()` / "
            "`pop_back()`. Read commands as strings: `cin >> cmd; if (cmd == \"push\") cin >> x;`.",
        ],
        samples=["8\npush 5\npush 3\nmin\npush 7\ntop\npop\npop\nmin"],
        tests=["2\npush -4\nmin", "6\npush 2\npush 2\npush 1\npop\nmin\ntop",
               "7\npush 3\npush 1\npush 1\npop\nmin\npop\nmin"],
        gen=_minstack_gen,
        starter_python="""import sys

lines = sys.stdin.read().split("\\n")
q = int(lines[0])
stack = []
out = []
for line in lines[1:q + 1]:
    parts = line.split()
    cmd = parts[0]
    # TODO: handle push / pop / top / min
print("\\n".join(out))
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <string>
using namespace std;

int main() {
    int q;
    cin >> q;
    vector<pair<int, int>> st;  // (value, minimum so far)
    while (q--) {
        string cmd;
        cin >> cmd;
        if (cmd == "push") {
            int x;
            cin >> x;
            // TODO
        }
        // TODO: pop / top / min
    }
    return 0;
}
""",
        solution_python=r"""import sys

lines = sys.stdin.read().split("\n")
q = int(lines[0])
stack = []
out = []
for line in lines[1:q + 1]:
    parts = line.split()
    cmd = parts[0]
    if cmd == "push":
        x = int(parts[1])
        m = min(x, stack[-1][1]) if stack else x
        stack.append((x, m))
    elif cmd == "pop":
        stack.pop()
    elif cmd == "top":
        out.append(str(stack[-1][0]))
    else:
        out.append(str(stack[-1][1]))
print("\n".join(out))
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    vector<pair<int, int>> st;
    while (q--) {
        string cmd;
        cin >> cmd;
        if (cmd == "push") {
            int x;
            cin >> x;
            int m = st.empty() ? x : min(x, st.back().second);
            st.push_back({x, m});
        } else if (cmd == "pop") {
            st.pop_back();
        } else if (cmd == "top") {
            cout << st.back().first << "\n";
        } else {
            cout << st.back().second << "\n";
        }
    }
    return 0;
}
""",
    ),
    dict(
        id="sliding-window-peaks",
        title="Sliding Window Peaks",
        difficulty="medium",
        category="Stacks & Queues",
        tags=["deque", "monotonic-queue", "sliding-window"],
        inspired_by="LeetCode #239 Sliding Window Maximum; CSES Sliding Window Maximum",
        statement="""
A window of width `k` slides over an array of `n` integers, one position at a
time, from the left end to the right end. Print the **maximum** inside the
window for each of its `n − k + 1` positions.

For `1 3 -1 -3 5 3 6 7` and `k = 3` the maxima are `3 3 5 5 6 7`.

Recomputing each maximum costs O(k), so O(n·k) overall. A **monotonic deque**
brings it down to O(n).
""",
        input_format="""First line: `n k` (1 ≤ k ≤ n ≤ 3000).
Second line: `n` integers (|aᵢ| < 1000).""",
        output_format="One line with `n − k + 1` integers: the window maxima.",
        hints=[
            "Keep a deque of *indices* whose values are in decreasing order from front to back. The front is always "
            "the maximum of the current window.",
            "When adding index `i`: pop from the **back** while `a[back] <= a[i]` (they can never be a maximum again), "
            "then push `i`. Pop from the **front** if it has slid out of the window (`front <= i − k`).",
            "Python: `from collections import deque` with `append`, `pop`, `popleft`, `dq[0]`, `dq[-1]`. "
            "C++: `#include <deque>` with `push_back`, `pop_back`, `pop_front`, `front()`, `back()`.",
        ],
        samples=["8 3\n1 3 -1 -3 5 3 6 7", "3 1\n4 -2 9"],
        tests=["1 1\n-5", "5 5\n2 9 1 9 3", "6 2\n5 4 3 2 1 0", "6 3\n1 1 1 1 1 1"],
        gen=_win_gen,
        starter_python="""from collections import deque

n, k = map(int, input().split())
a = list(map(int, input().split()))
dq = deque()   # indices, values decreasing from front to back
out = []
for i in range(n):
    # TODO: maintain the deque, record the max once i >= k - 1
    pass
print(*out)
""",
        starter_cpp="""#include <iostream>
#include <vector>
#include <deque>
using namespace std;

int main() {
    int n, k;
    cin >> n >> k;
    vector<int> a(n), out;
    for (auto &x : a) cin >> x;
    deque<int> dq;  // indices
    for (int i = 0; i < n; i++) {
        // TODO: maintain the deque, record the max once i >= k - 1
    }
    for (size_t i = 0; i < out.size(); i++) cout << out[i] << (i + 1 < out.size() ? ' ' : '\\n');
    return 0;
}
""",
        solution_python=r"""from collections import deque

n, k = map(int, input().split())
a = list(map(int, input().split()))
dq = deque()
out = []
for i in range(n):
    while dq and a[dq[-1]] <= a[i]:
        dq.pop()
    dq.append(i)
    if dq[0] <= i - k:
        dq.popleft()
    if i >= k - 1:
        out.append(a[dq[0]])
print(*out)
""",
        solution_cpp=r"""#include <iostream>
#include <vector>
#include <deque>
using namespace std;

int main() {
    int n, k;
    cin >> n >> k;
    vector<int> a(n), out;
    for (auto &x : a) cin >> x;
    deque<int> dq;
    for (int i = 0; i < n; i++) {
        while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back();
        dq.push_back(i);
        if (dq.front() <= i - k) dq.pop_front();
        if (i >= k - 1) out.push_back(a[dq.front()]);
    }
    for (size_t i = 0; i < out.size(); i++) cout << out[i] << (i + 1 < out.size() ? ' ' : '\n');
    return 0;
}
""",
    ),
]
