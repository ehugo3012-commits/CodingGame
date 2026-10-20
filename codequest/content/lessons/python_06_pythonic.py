"""Python track - Unit 6: Pythonic Tools (comprehensions, iteration helpers, stdlib)."""

LESSONS = [
    dict(
        id="py-comprehensions",
        track="python",
        unit="Pythonic Tools",
        title="Comprehensions",
        summary="Build lists, sets and dicts in one readable line.",
        body=r"""
You have written this loop many times:

```python
squares = []
for x in range(10):
    if x % 2 == 0:
        squares.append(x * x)
```

A **list comprehension** says the same in one line:

```python
squares = [x * x for x in range(10) if x % 2 == 0]
```

Read it left to right as "**x squared, for each x in range(10), if x is
even**". The pattern is `[expression for item in iterable if condition]`;
the `if` part is optional.

### Other flavours

```python
lengths = {w: len(w) for w in words}       # dict comprehension
first_letters = {w[0] for w in words}      # set comprehension
total = sum(x * x for x in nums)           # generator expression
```

A **generator expression** (round brackets, or none inside a function
call) produces values one at a time without building a list - ideal for
`sum`, `max`, `any`, `all`.

```python
any(n < 0 for n in nums)    # is there a negative?
all(c.isdigit() for c in s) # is s all digits?
```

### if/else inside

A filter `if` goes at the **end**. To *transform* with a choice, put a
conditional expression at the **front**:

```python
["even" if x % 2 == 0 else "odd" for x in nums]
```

Nested loops read in the same order as normal loops:
`[(r, c) for r in range(3) for c in range(3)]`.

> **Pitfall:** comprehensions are for *building* collections. If you only
> want side effects (printing), use a plain `for` loop. And if a
> comprehension needs two lines to read, a loop is probably clearer.
""",
        examples=[
            dict(title="Loop vs comprehension",
                 code="""\
squares = []
for x in range(10):
    if x % 2 == 0:
        squares.append(x * x)
print(squares)
print([x * x for x in range(10) if x % 2 == 0])
""",
                 explain="Both produce the same list; the comprehension is shorter and idiomatic."),
            dict(title="dict, set, generator",
                 code="""\
words = input().split()
print({w: len(w) for w in words})
print(sorted({w[0] for w in words}))
print(sum(len(w) for w in words), any(len(w) > 5 for w in words))
""",
                 stdin="apple avocado banana cherry\n"),
            dict(title="Transform with if/else",
                 code="""\
nums = [3, 8, -1, 0, 5]
print(["even" if x % 2 == 0 else "odd" for x in nums])
print([x for x in nums if x > 0])
print([(r, c) for r in range(2) for c in range(3)])
""",
                 explain="if/else at the front chooses a value; if at the end filters items."),
        ],
        challenge=dict(
            prompt=("Read a line of integers. Using a list comprehension, print the squares of "
                    "the **even** numbers, in their original order, on one line. If there are "
                    "none, print an empty line."),
            starter="nums = list(map(int, input().split()))\nresult = []  # replace with a comprehension\nprint(' '.join(map(str, result)))\n",
            solution=("nums = list(map(int, input().split()))\nresult = [x * x for x in nums if x % 2 == 0]\n"
                      "print(' '.join(map(str, result)))\n"),
            samples=["1 2 3 4 5 6\n"],
            tests=["-2 7 0\n", "10\n", "8 6 4 2\n"],
        ),
    ),
    dict(
        id="py-enumerate-zip",
        track="python",
        unit="Pythonic Tools",
        title="enumerate & zip",
        summary="Loop with an index, or over several sequences side by side.",
        body=r"""
Beginners often write `for i in range(len(names)):` and then use
`names[i]`. Python has two helpers that make such loops cleaner and less
error-prone.

### enumerate - index and item together

```python
for i, name in enumerate(names):
    print(i, name)
```

Need numbering from 1 (for rankings, line numbers)? Pass `start=1`:
`enumerate(names, start=1)`.

### zip - walk sequences in parallel

```python
names = ["Ada", "Bo", "Cy"]
scores = [91, 78, 85]
for name, score in zip(names, scores):
    print(name, score)
```

`zip` pairs the first items, then the second items, and so on. Useful
tricks:

```python
dict(zip(names, scores))          # {'Ada': 91, 'Bo': 78, 'Cy': 85}
for a, b in zip(nums, nums[1:]):  # neighbouring pairs
    ...
```

> **Pitfall:** `zip` stops at the **shortest** input and silently drops the
> rest. If the lengths should match, `zip(a, b, strict=True)` (Python 3.10+)
> raises an error when they don't.

Both `enumerate` and `zip` are **lazy**: they produce pairs on demand
instead of building a list. Wrap them in `list()` if you want to print or
reuse the pairs.

Combining them is common: `for i, (a, b) in enumerate(zip(xs, ys)):` -
note the parentheses that unpack the inner pair.
""",
        examples=[
            dict(title="enumerate",
                 code="""\
names = ["Ada", "Bo", "Cy"]
for i, name in enumerate(names):
    print(i, name)
for rank, name in enumerate(names, start=1):
    print(f"#{rank} {name}")
""",
                 explain="No range(len(...)) needed; start=1 shifts the numbering."),
            dict(title="zip",
                 code="""\
names = ["Ada", "Bo", "Cy", "Dee"]
scores = [91, 78, 85]
print(list(zip(names, scores)))
print(dict(zip(names, scores)))
""",
                 explain="Dee is dropped: zip stops at the shorter list."),
            dict(title="Neighbouring pairs",
                 code="""\
temps = list(map(int, input().split()))
for a, b in zip(temps, temps[1:]):
    print(b - a, end=" ")
print()
""",
                 stdin="12 15 11 11 18\n",
                 explain="zip(xs, xs[1:]) gives each element with the one after it."),
        ],
        challenge=dict(
            prompt=("The first line has names, the second line has the same number of scores. "
                    "Print a numbered list, one line per person, in the form `1. Ada 91`, using "
                    "`enumerate` and `zip`."),
            starter="names = input().split()\nscores = input().split()\n# for i, (name, score) in enumerate(zip(...), start=1):\n",
            solution=("names = input().split()\nscores = input().split()\n"
                      "for i, (name, score) in enumerate(zip(names, scores), start=1):\n"
                      "    print(f\"{i}. {name} {score}\")\n"),
            samples=["Ada Bo Cy\n91 78 85\n"],
            tests=["Solo\n100\n", "a b c d\n1 2 3 4\n"],
            checker="exact",
        ),
    ),
    dict(
        id="py-collections-module",
        track="python",
        unit="Pythonic Tools",
        title="Counter, defaultdict & deque",
        summary="Three power tools from the collections module.",
        body=r"""
The standard library's `collections` module has ready-made containers
for jobs you would otherwise code by hand.

### Counter - counting made trivial

```python
from collections import Counter
c = Counter("mississippi")
c["s"]              # 4
c["z"]              # 0 - missing keys count as zero, no KeyError
c.most_common(2)    # [('i', 4), ('s', 4)]
```

`Counter(words)` replaces the whole `counts.get(w, 0) + 1` loop.
`most_common` sorts by count; ties keep the order in which items were first
seen.

### defaultdict - dicts with automatic defaults

```python
from collections import defaultdict
groups = defaultdict(list)
for w in words:
    groups[w[0]].append(w)     # no "if key not in groups" needed
```

`defaultdict(list)` creates an empty list the first time a key is used;
`defaultdict(int)` starts at 0. You pass the *function* (`list`, `int`),
not a value.

### deque - a fast double-ended queue

```python
from collections import deque
q = deque([1, 2, 3])
q.append(4)        # right end
q.appendleft(0)    # left end
q.popleft()        # 0  - fast!
```

> **Pitfall:** `list.pop(0)` shifts every remaining element, so a queue
> built on a list gets slow with many items. `deque.popleft()` is
> constant-time - use it for queues and breadth-first search.

`deque(maxlen=3)` keeps only the last 3 items - perfect for "recent
history" windows.
""",
        examples=[
            dict(title="Counter",
                 code="""\
from collections import Counter
c = Counter("mississippi")
print(c)
print(c["s"], c["z"])
print(c.most_common(2))
""",
                 explain="Missing keys report 0 instead of raising KeyError."),
            dict(title="defaultdict(list)",
                 code="""\
from collections import defaultdict
groups = defaultdict(list)
for w in input().split():
    groups[len(w)].append(w)
for length in sorted(groups):
    print(length, groups[length])
""",
                 stdin="a to be cat or dog fish\n",
                 explain="Each new key starts with an empty list automatically."),
            dict(title="deque",
                 code="""\
from collections import deque
q = deque([1, 2, 3])
q.append(4)
q.appendleft(0)
print(q.popleft(), q.pop(), q)
recent = deque(maxlen=3)
for x in range(6):
    recent.append(x)
print(list(recent))
""",
                 explain="maxlen discards the oldest items as new ones arrive."),
        ],
        challenge=dict(
            prompt=("Read a line of words. Print the most common word and its count, separated by "
                    "a space. If several words tie, choose the one that appears **first** in the "
                    "line."),
            starter="from collections import Counter\nwords = input().split()\n# Counter(...).most_common(1)\n",
            solution=("from collections import Counter\nwords = input().split()\n"
                      "word, count = Counter(words).most_common(1)[0]\nprint(word, count)\n"),
            samples=["the cat saw the dog and the cat\n"],
            tests=["solo\n", "b a a b\n", "x y z y z z\n"],
        ),
    ),
    dict(
        id="py-itertools-math",
        track="python",
        unit="Pythonic Tools",
        title="math & itertools",
        summary="Ready-made maths functions and combinatorics generators.",
        body=r"""
### The math module

```python
import math
math.sqrt(2)         # 1.4142...
math.isqrt(17)       # 4 - exact integer square root
math.gcd(12, 18)     # 6
math.lcm(4, 6)       # 12
math.factorial(5)    # 120
math.comb(5, 2)      # 10 - ways to choose 2 of 5
math.floor(2.7), math.ceil(2.1)   # 2, 3
math.pi, math.inf
```

> **Pitfall:** `int(math.sqrt(n))` can be off by one for huge `n` because
> of float rounding. Use `math.isqrt(n)` for exact integer roots.

### itertools - loops you don't have to write

```python
from itertools import combinations, permutations, product, accumulate

list(combinations("ABC", 2))   # [('A','B'), ('A','C'), ('B','C')]
list(permutations("AB"))       # [('A','B'), ('B','A')]
list(product([0, 1], repeat=2))  # (0,0) (0,1) (1,0) (1,1)
list(accumulate([1, 2, 3, 4]))   # [1, 3, 6, 10] - running totals
```

- `combinations(items, k)` - order doesn't matter, no repeats.
- `permutations(items, k)` - order matters.
- `product(a, b)` - every pairing, like nested loops.

These are **lazy** iterators and their output grows explosively:
`permutations(range(10))` has 3 628 800 items. They are perfect for small
brute-force searches, but check the count first (`math.comb`,
`math.factorial`) before looping.

Both modules are written in C, so they are much faster than equivalent
hand-written Python loops.
""",
        examples=[
            dict(title="math",
                 code="""\
import math
print(math.sqrt(2), math.isqrt(17))
print(math.gcd(12, 18), math.lcm(4, 6))
print(math.factorial(5), math.comb(5, 2))
print(math.floor(2.7), math.ceil(2.1), round(math.pi, 4))
""",
                 explain="isqrt gives an exact integer; comb counts combinations."),
            dict(title="itertools",
                 code="""\
from itertools import combinations, permutations, product, accumulate
print(list(combinations("ABC", 2)))
print(["".join(p) for p in permutations("abc")])
print(list(product([0, 1], repeat=2)))
print(list(accumulate([1, 2, 3, 4])))
""",
                 explain="Each tuple is one arrangement; join turns letter tuples back into strings."),
            dict(title="Brute-force pairs",
                 code="""\
from itertools import combinations
nums = list(map(int, input().split()))
target = 10
for a, b in combinations(nums, 2):
    if a + b == target:
        print(a, "+", b)
""",
                 stdin="3 7 5 5 2 8\n",
                 explain="combinations replaces a double loop over i < j."),
        ],
        challenge=dict(
            prompt=("The first line has `n` and `k`; the second line has `n` integers "
                    "(n <= 15). Print how many ways there are to choose `k` of the numbers "
                    "(by position) so that their sum is **even**."),
            starter="from itertools import combinations\nn, k = map(int, input().split())\nnums = list(map(int, input().split()))\n# count combinations with even sum\n",
            solution=("from itertools import combinations\nn, k = map(int, input().split())\n"
                      "nums = list(map(int, input().split()))\n"
                      "print(sum(1 for c in combinations(nums, k) if sum(c) % 2 == 0))\n"),
            samples=["4 2\n1 2 3 4\n"],
            tests=["1 1\n7\n", "5 3\n2 4 6 8 10\n", "15 7\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15\n"],
        ),
    ),
    dict(
        id="py-heapq",
        track="python",
        unit="Pythonic Tools",
        title="Heaps with heapq",
        summary="Always grab the smallest item fast: priority queues in Python.",
        body=r"""
Sometimes you repeatedly need **the smallest item** of a changing
collection - the next event, the cheapest task, the closest node. Sorting
after every change is slow. A **heap** keeps a list arranged so the
smallest item is always at index 0 and both inserting and removing take
only `O(log n)` steps.

```python
import heapq
h = []
heapq.heappush(h, 5)
heapq.heappush(h, 1)
heapq.heappush(h, 3)
h[0]                  # 1 - peek at the smallest
heapq.heappop(h)      # 1 - remove the smallest
```

`heapq.heapify(lst)` turns an existing list into a heap in place, in
linear time.

> **Pitfall:** the list is *heap-ordered*, not sorted. `print(h)` may show
> `[1, 5, 3]`. Only `h[0]` is guaranteed to be the minimum.

### Max-heaps

`heapq` only does **min**-heaps. For the largest first, push negated
values: `heappush(h, -x)` and negate again when you pop.

### Priorities

Push tuples `(priority, item)`: tuples compare by the first element, so the
smallest priority comes out first.

```python
heapq.heappush(tasks, (2, "write"))
heapq.heappush(tasks, (1, "plan"))
heapq.heappop(tasks)   # (1, 'plan')
```

For a one-off "top k", `heapq.nsmallest(k, data)` and
`heapq.nlargest(k, data)` are simpler than writing the loop.

Heaps power Dijkstra's shortest paths, event simulations and greedy
algorithms like "always merge the two smallest".
""",
        examples=[
            dict(title="Push and pop",
                 code="""\
import heapq
h = []
for x in [5, 1, 8, 3, 2]:
    heapq.heappush(h, x)
print("heap list:", h)
print([heapq.heappop(h) for _ in range(5)])
""",
                 explain="The internal list isn't sorted, but pops come out in order."),
            dict(title="Max-heap and top-k",
                 code="""\
import heapq
nums = list(map(int, input().split()))
h = [-x for x in nums]
heapq.heapify(h)
print("largest:", -heapq.heappop(h))
print(heapq.nsmallest(3, nums), heapq.nlargest(2, nums))
""",
                 stdin="4 9 1 7 3\n",
                 explain="Negating turns a min-heap into a max-heap."),
            dict(title="Priority queue",
                 code="""\
import heapq
tasks = []
heapq.heappush(tasks, (2, "write code"))
heapq.heappush(tasks, (1, "plan"))
heapq.heappush(tasks, (3, "test"))
while tasks:
    prio, name = heapq.heappop(tasks)
    print(prio, name)
""",
                 explain="Tuples are compared by priority first."),
        ],
        challenge=dict(
            prompt=("Ropes. The input is a line of positive integer rope lengths. Joining two ropes "
                    "of lengths `a` and `b` costs `a + b` and produces one rope of that length. "
                    "Join all ropes into one with the **minimum total cost** (always join the two "
                    "shortest) and print that cost. A single rope costs `0`."),
            starter="import heapq\nh = list(map(int, input().split()))\nheapq.heapify(h)\ncost = 0\n# while len(h) > 1: ...\nprint(cost)\n",
            solution=("import heapq\nh = list(map(int, input().split()))\nheapq.heapify(h)\ncost = 0\n"
                      "while len(h) > 1:\n    a = heapq.heappop(h)\n    b = heapq.heappop(h)\n"
                      "    cost += a + b\n    heapq.heappush(h, a + b)\nprint(cost)\n"),
            samples=["4 3 2 6\n"],
            tests=["10\n", "1 1 1 1\n", "5 2 9 1 7 3\n"],
        ),
    ),
]
