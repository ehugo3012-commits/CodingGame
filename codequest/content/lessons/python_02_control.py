"""Python track - Unit 2: Control Flow (decisions and loops)."""

LESSONS = [
    dict(
        id="py-if-else",
        track="python",
        unit="Control Flow",
        title="if, elif, else",
        summary="Make decisions with comparisons and boolean logic.",
        body=r"""
`if` runs a block only when a condition is `True`. The block is everything
**indented** under the line ending in `:` (use 4 spaces):

```python
temp = int(input())
if temp > 25:
    print("hot")
elif temp > 10:
    print("mild")
else:
    print("cold")
```

Python checks the conditions **top to bottom and stops at the first true
one**, so order matters: if the `> 10` test came first, 30 degrees would be
"mild".

### Comparisons

`==` equal, `!=` not equal, `<`, `<=`, `>`, `>=`. They produce a `bool`.
Python allows chaining: `0 <= x < 10` means `0 <= x and x < 10`.

> **Pitfall:** `=` assigns, `==` compares. `if x = 5:` is a syntax error.

### Combining conditions

`and` (both true), `or` (at least one), `not` (flip):

```python
if age >= 13 and age <= 19:
    print("teen")
if not done:
    print("keep going")
```

`and`/`or` are *short-circuit*: in `x != 0 and 10 / x > 2` the division
never runs when `x` is 0.

Empty things are "falsy": `0`, `0.0`, `""`, `[]`, `None`. So `if name:`
means "if name is not empty".

> **Pitfall:** `if x == 1 or 2:` is always true (it reads as
> `(x == 1) or 2`). Write `if x == 1 or x == 2:` or `if x in (1, 2):`.
""",
        examples=[
            dict(title="Order of elif",
                 code="""\
temp = int(input())
if temp > 25:
    print("hot")
elif temp > 10:
    print("mild")
else:
    print("cold")
""",
                 stdin="18\n",
                 explain="Only the first matching branch runs."),
            dict(title="Boolean logic",
                 code="""\
x = 7
print(x > 5 and x < 10)
print(0 < x < 5)
print(not x == 7)
print(x == 1 or 2)       # surprise!
print(x in (1, 2))
""",
                 explain="`x == 1 or 2` evaluates to 2 (truthy) - a classic bug."),
            dict(title="Even or odd",
                 code="""\
n = int(input())
if n % 2 == 0:
    print(n, "is even")
else:
    print(n, "is odd")
""",
                 stdin="-3\n"),
        ],
        challenge=dict(
            prompt=("Read an exam score from 0 to 100 and print its grade: `A` for 90 and above, "
                    "`B` for 80-89, `C` for 70-79, `D` for 60-69 and `F` below 60."),
            starter="score = int(input())\n# if / elif / else\n",
            solution=("score = int(input())\n"
                      "if score >= 90:\n    print('A')\n"
                      "elif score >= 80:\n    print('B')\n"
                      "elif score >= 70:\n    print('C')\n"
                      "elif score >= 60:\n    print('D')\n"
                      "else:\n    print('F')\n"),
            samples=["85\n"],
            tests=["90\n", "89\n", "0\n", "60\n"],
        ),
    ),
    dict(
        id="py-while",
        track="python",
        unit="Control Flow",
        title="while Loops",
        summary="Repeat code as long as a condition stays true.",
        body=r"""
A `while` loop repeats its block **while** a condition is true. It checks the
condition before every round:

```python
n = 3
while n > 0:
    print(n)
    n -= 1
print("go!")
```

Use `while` when you **don't know in advance** how many repetitions you
need - "keep halving until it reaches 1", "keep reading until the input is
0", "keep guessing until correct".

Every `while` loop needs three things:

1. a variable the condition depends on, set up **before** the loop,
2. the condition itself,
3. a line **inside** the loop that changes that variable.

> **Pitfall:** forget step 3 and the condition never becomes false - an
> **infinite loop**. In CodeQuest that shows up as "time limit exceeded".

A classic `while` example is the *Collatz* process: if `n` is even halve
it, otherwise make it `3n + 1`. Nobody has proven it always reaches 1, but
it does for every number ever tried:

```python
steps = 0
while n != 1:
    if n % 2 == 0:
        n //= 2
    else:
        n = 3 * n + 1
    steps += 1
```

Another common pattern is peeling digits off a number with `% 10` and
`// 10` until nothing is left (`while n > 0`).
""",
        examples=[
            dict(title="Countdown",
                 code="""\
n = 3
while n > 0:
    print(n)
    n -= 1
print("go!")
""",
                 explain="The condition is re-checked before each round; n -= 1 guarantees it ends."),
            dict(title="Digit sum",
                 code="""\
n = int(input())
total = 0
while n > 0:
    total += n % 10
    n //= 10
print(total)
""",
                 stdin="9045\n",
                 explain="Each round removes the last digit, so the loop stops when n hits 0."),
            dict(title="Doubling until big",
                 code="""\
money = 1
days = 0
while money < 1000:
    money *= 2
    days += 1
print(days, "days ->", money)
""",
                 explain="We don't know the number of rounds up front - perfect for while."),
        ],
        challenge=dict(
            prompt=("Read a positive integer `n`. Apply the Collatz rule (even: `n // 2`, odd: "
                    "`3n + 1`) until `n` becomes 1 and print how many steps it took. For `6` the "
                    "answer is `8` (6, 3, 10, 5, 16, 8, 4, 2, 1)."),
            starter="n = int(input())\nsteps = 0\n# while n != 1: ...\nprint(steps)\n",
            solution=("n = int(input())\nsteps = 0\nwhile n != 1:\n"
                      "    if n % 2 == 0:\n        n //= 2\n    else:\n        n = 3 * n + 1\n"
                      "    steps += 1\nprint(steps)\n"),
            samples=["6\n"],
            tests=["1\n", "27\n", "1024\n", "97\n"],
        ),
    ),
    dict(
        id="py-for-range",
        track="python",
        unit="Control Flow",
        title="for Loops & range",
        summary="Loop over sequences and count with range(start, stop, step).",
        body=r"""
A `for` loop visits each item of a sequence in turn:

```python
for fruit in ["apple", "kiwi", "fig"]:
    print(fruit)
```

To repeat something a fixed number of times, loop over `range`:

```python
for i in range(5):        # 0 1 2 3 4
    print(i)
```

`range` has three forms:

- `range(stop)` - 0 up to **but not including** `stop`
- `range(start, stop)` - `start` up to `stop - 1`
- `range(start, stop, step)` - jumps by `step`; a negative step counts down

```python
range(1, 11)        # 1..10
range(0, 20, 5)     # 0 5 10 15
range(10, 0, -1)    # 10 9 ... 1
```

> **Pitfall (off-by-one):** the stop value is **excluded**. To include `n`
> write `range(1, n + 1)`. To count down to 1, the stop must be `0`.

Why exclude the end? Because `range(n)` then has exactly `n` items, and
`range(len(lst))` gives exactly the valid indexes of a list.

### Accumulators

Most loops build up an answer in a variable created *before* the loop:

```python
total = 0
for i in range(1, n + 1):
    total += i
```

Use `for` when you know what to iterate over; use `while` when you only
know when to stop.
""",
        examples=[
            dict(title="range forms",
                 code="""\
print(list(range(5)))
print(list(range(2, 6)))
print(list(range(0, 20, 5)))
print(list(range(5, 0, -1)))
""",
                 explain="list(range(...)) is a quick way to see which numbers a range produces."),
            dict(title="Sum 1..n",
                 code="""\
n = int(input())
total = 0
for i in range(1, n + 1):
    total += i
print(total)
""",
                 stdin="100\n",
                 explain="range(1, n + 1) includes n; range(1, n) would miss it."),
            dict(title="Loop over a string",
                 code="""\
vowels = 0
for ch in "programming":
    if ch in "aeiou":
        vowels += 1
print(vowels)
""",
                 explain="Strings are sequences too, so for visits each character."),
        ],
        challenge=dict(
            prompt=("Read `n` (1 <= n <= 50). Print a countdown from `n` down to `1`, one number "
                    "per line, and then print `Liftoff!`."),
            starter="n = int(input())\n# for i in range(...):\n",
            solution="n = int(input())\nfor i in range(n, 0, -1):\n    print(i)\nprint('Liftoff!')\n",
            samples=["3\n"],
            tests=["1\n", "10\n"],
            checker="exact",
        ),
    ),
    dict(
        id="py-break-continue",
        track="python",
        unit="Control Flow",
        title="break & continue",
        summary="Leave a loop early or skip to the next round.",
        body=r"""
Two keywords change how a loop flows:

- `break` - exit the loop **immediately**.
- `continue` - skip the rest of this round and jump to the **next** one.

```python
for n in range(1, 10):
    if n % 2 == 0:
        continue      # skip even numbers
    if n > 7:
        break         # stop completely
    print(n)          # 1 3 5 7
```

### The "loop until a sentinel" pattern

Often input ends with a special value such as `0`. Combine `while True`
with `break`:

```python
while True:
    x = int(input())
    if x == 0:
        break
    print(x * 2)
```

`while True` would run forever on its own; the `break` is the exit door.
This keeps the "read" and the "check" next to each other, instead of
duplicating `input()` before and inside the loop.

### for ... else

A loop can have an `else` block that runs only if the loop finished
**without** hitting `break`. It is handy for searches:

```python
for d in range(2, n):
    if n % d == 0:
        print("not prime")
        break
else:
    print("prime")
```

> **Pitfall:** `break` only leaves the **innermost** loop. To escape nested
> loops, use a flag variable or put the loops in a function and `return`.

Use these sparingly - a loop with many `break`s is hard to follow. But for
"stop at the first match" they make code shorter and faster.
""",
        examples=[
            dict(title="Skip and stop",
                 code="""\
for n in range(1, 10):
    if n % 2 == 0:
        continue
    if n > 7:
        break
    print(n)
""",
                 explain="Evens are skipped by continue; break ends the loop when n reaches 9."),
            dict(title="Read until 0",
                 code="""\
count = 0
while True:
    x = int(input())
    if x == 0:
        break
    count += 1
print("read", count, "numbers")
""",
                 stdin="4\n8\n15\n0\n",
                 explain="The sentinel 0 is not counted."),
            dict(title="for-else prime test",
                 code="""\
n = int(input())
for d in range(2, n):
    if n % d == 0:
        print(n, "is divisible by", d)
        break
else:
    print(n, "is prime")
""",
                 stdin="97\n"),
        ],
        challenge=dict(
            prompt=("Integers arrive one per line, ending with a line containing `0`. Print the "
                    "sum of the **positive** numbers that appear before the `0`. Skip negative "
                    "numbers with `continue`; ignore anything after the `0`."),
            starter="total = 0\nwhile True:\n    x = int(input())\n    # break on 0, continue on negatives\n\nprint(total)\n",
            solution=("total = 0\nwhile True:\n    x = int(input())\n    if x == 0:\n        break\n"
                      "    if x < 0:\n        continue\n    total += x\nprint(total)\n"),
            samples=["5\n-2\n3\n0\n7\n"],
            tests=["0\n", "-1\n-2\n0\n", "10\n20\n30\n0\n"],
        ),
    ),
]
