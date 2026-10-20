"""Python track - Unit 1: Basics (variables, arithmetic, formatting)."""

LESSONS = [
    dict(
        id="py-variables",
        track="python",
        unit="Basics",
        title="Variables & Types",
        summary="Store values in names and learn the four basic types: int, float, str, bool.",
        body=r"""
A **variable** is a name that points at a value. You create one with `=`
(read it as "becomes", not "equals"):

```python
score = 10        # int   - whole number
price = 4.99      # float - number with a decimal point
name = "Ada"      # str   - text
done = False      # bool  - True or False
```

Python figures out the type from the value. Ask for it with `type()`:

```python
print(type(score))   # <class 'int'>
```

A variable can be re-assigned at any time, even to a different type, and the
right-hand side is evaluated **first**, so `score = score + 1` means "take
the old score, add one, store it back".

### Converting between types

`int("42")`, `float("3.5")`, `str(7)` and `bool(0)` convert values. You need
this constantly, because **`input()` always returns a `str`**:

```python
a = input()        # the user types 12
print(a + a)       # 1212  - string concatenation!
print(int(a) + int(a))   # 24
```

> **Pitfall:** `"5" + 5` is a `TypeError`. Python never guesses whether you
> meant text or maths - convert explicitly.

Names are case-sensitive (`Score` and `score` differ), may contain letters,
digits and `_`, and cannot start with a digit. Prefer clear names like
`total_price` over `tp`.
""",
        examples=[
            dict(title="Four types",
                 code="""\
score = 10
price = 4.99
name = "Ada"
done = False
print(type(score), type(price), type(name), type(done))
""",
                 explain="`type()` tells you what kind of value a variable holds."),
            dict(title="input() gives text",
                 code="""\
a = input()
print(a + a)
print(int(a) + int(a))
""",
                 stdin="12\n",
                 explain="Adding two strings glues them together; convert with int() to do maths."),
            dict(title="Conversions",
                 code="""\
print(int("42") + 1)
print(float("2.5") * 2)
print(str(7) + "!")
print(int(3.99))    # truncates, does not round
print(bool(0), bool(5), bool(""), bool("hi"))
""",
                 explain="int() on a float chops off the decimals; 0 and empty strings are falsy."),
        ],
        challenge=dict(
            prompt=("Read two lines, each containing a whole number. Print the two lines glued "
                    "together as text on the first output line, and their numeric sum on the "
                    "second line. For `12` and `34` print `1234` then `46`."),
            starter="a = input()\nb = input()\n# print the text version, then the numeric sum\n",
            solution="a = input()\nb = input()\nprint(a + b)\nprint(int(a) + int(b))\n",
            samples=["12\n34\n"],
            tests=["7\n8\n", "100\n0\n", "-5\n20\n"],
        ),
    ),
    dict(
        id="py-arithmetic",
        track="python",
        unit="Basics",
        title="Arithmetic Operators",
        summary="+ - * / plus the three you will use all the time: //, % and **.",
        body=r"""
Python has the usual operators, plus a few that are gold for programming
puzzles:

| Operator | Meaning | Example | Result |
|---|---|---|---|
| `/` | true division | `7 / 2` | `3.5` |
| `//` | floor division | `7 // 2` | `3` |
| `%` | remainder (modulo) | `7 % 2` | `1` |
| `**` | power | `2 ** 10` | `1024` |

> **Pitfall:** `/` **always** gives a float, even `6 / 3` is `2.0`. When you
> need a whole number (an index, a count) use `//`.

`//` and `%` are a pair: for any `a` and positive `b`,
`a == (a // b) * b + a % b`. That makes them perfect for splitting numbers:

```python
n = 1234
last_digit = n % 10      # 4
rest = n // 10           # 123
minutes, seconds = divmod(200, 60)   # 3, 20
```

`x % 2 == 0` tests "is x even?". `//` rounds **down** (towards minus
infinity), so `-7 // 2` is `-4`, not `-3`.

Precedence follows maths: `**` first, then `* / // %`, then `+ -`. Use
parentheses when in doubt: `(a + b) / 2`.

Python integers have **no size limit**: `2 ** 200` just works. Floats, on
the other hand, are approximations: `0.1 + 0.2` prints
`0.30000000000000004`. Never compare floats with `==`; check that the
difference is tiny instead.

Shortcut operators update a variable in place: `x += 3`, `x *= 2`, `x //= 10`.
""",
        examples=[
            dict(title="Division family",
                 code="""\
print(7 / 2, 7 // 2, 7 % 2)
print(6 / 3)
print(-7 // 2, -7 % 2)
print(divmod(200, 60))
""",
                 explain="`/` is always float; `//` floors toward minus infinity; divmod gives both at once."),
            dict(title="Digits of a number",
                 code="""\
n = int(input())
print("last digit:", n % 10)
print("without it:", n // 10)
print("squared:", n ** 2)
""",
                 stdin="1234\n"),
            dict(title="Big ints, fuzzy floats",
                 code="""\
print(2 ** 100)
print(0.1 + 0.2)
print(abs(0.1 + 0.2 - 0.3) < 1e-9)
""",
                 explain="Integers are exact and unbounded; floats carry tiny rounding errors."),
        ],
        challenge=dict(
            prompt=("Read a number of seconds `s` (0 <= s < 10^9). Print how many whole hours, "
                    "minutes and seconds that is, separated by spaces. `3725` -> `1 2 5`."),
            starter="s = int(input())\n# use // and %\n",
            solution="s = int(input())\nh = s // 3600\nm = s % 3600 // 60\nprint(h, m, s % 60)\n",
            samples=["3725\n"],
            tests=["0\n", "59\n", "86399\n", "360000\n"],
        ),
    ),
    dict(
        id="py-fstrings",
        track="python",
        unit="Basics",
        title="f-strings & Formatting",
        summary="Build output text with f-strings, round numbers and control decimals.",
        body=r"""
Gluing text with `+` and `str()` gets messy fast. An **f-string** (a string
with an `f` in front) lets you drop any expression straight into `{}`:

```python
name, age = "Ada", 36
print(f"{name} is {age} years old")
print(f"Next year: {age + 1}")
```

### Format specs

After a colon inside the braces you can say *how* to show the value:

```python
pi = 3.14159265
print(f"{pi:.2f}")      # 3.14     - 2 decimals
print(f"{42:5}|")       #    42|   - width 5, numbers right-aligned
print(f"{'ab':>5}|")    #    ab|   - right-align text
print(f"{1234567:,}")   # 1,234,567
print(f"{0.25:.0%}")    # 25%
```

`:.2f` is the one you will use most - many judges ask for "exactly two
decimal places".

### round()

`round(x, 2)` returns a *number* rounded to 2 places, while `f"{x:.2f}"`
returns *text* that always has 2 decimals. Note `round(2.5)` is `2`:
Python rounds halves to the nearest **even** number ("banker's rounding").
And `round(1.50, 2)` prints as `1.5` - if the output format matters, use an
f-string.

> **Pitfall:** forgetting the `f` prints the braces literally:
> `"{name}"` stays `{name}`.
""",
        examples=[
            dict(title="Basic f-string",
                 code="""\
name, age = "Ada", 36
print(f"{name} is {age} years old")
print(f"In ten years: {age + 10}")
print("{name} without the f")
""",
                 explain="Anything inside {} is evaluated; without the f nothing happens."),
            dict(title="Decimals and alignment",
                 code="""\
price = float(input())
print(f"Price: {price:.2f}")
print(f"[{price:8.1f}]")
print(f"[{'left':<8}][{'right':>8}]")
""",
                 stdin="3.14159\n",
                 explain="`8.1f` means width 8 with 1 decimal; `<` and `>` choose alignment."),
            dict(title="round() vs :.2f",
                 code="""\
print(round(2.5), round(3.5))
print(round(1.5, 2), f"{1.5:.2f}")
print(round(2.675, 2))
""",
                 explain="round() returns a number (and floats are approximate); :.2f always shows two decimals."),
        ],
        challenge=dict(
            prompt=("Read one line `name price quantity` (for example `apple 0.5 3`). Print "
                    "`<quantity> x <name> = <total>` where total is price times quantity with "
                    "exactly two decimals: `3 x apple = 1.50`."),
            starter="name, price, qty = input().split()\n# convert and print with an f-string\n",
            solution=("name, price, qty = input().split()\n"
                      "total = float(price) * int(qty)\n"
                      "print(f\"{qty} x {name} = {total:.2f}\")\n"),
            samples=["apple 0.5 3\n"],
            tests=["coffee 2.75 4\n", "pen 1 1\n", "melon 3.333 3\n"],
            checker="exact",
        ),
    ),
]
