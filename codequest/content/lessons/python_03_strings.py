"""Python track - Unit 3: Strings."""

LESSONS = [
    dict(
        id="py-string-slicing",
        track="python",
        unit="Strings",
        title="Indexing & Slicing",
        summary="Pick out characters and substrings with s[i] and s[a:b:step].",
        body=r"""
A string is a **sequence** of characters, numbered from `0`:

```text
 s =   P   y   t   h   o   n
       0   1   2   3   4   5
      -6  -5  -4  -3  -2  -1
```

```python
s = "Python"
s[0]     # 'P'
s[-1]    # 'n'  - negative indexes count from the end
len(s)   # 6
```

The last valid index is `len(s) - 1`; `s[6]` raises `IndexError`.

### Slices

`s[a:b]` takes characters from index `a` **up to but not including** `b` -
the same rule as `range`. Leave a side empty to mean "from the start" or
"to the end":

```python
s[0:3]    # 'Pyt'
s[2:]     # 'thon'
s[:-1]    # 'Pytho'  - drop the last char
s[::2]    # 'Pto'    - every second char
s[::-1]   # 'nohtyP' - reversed!
```

Slices are forgiving: `s[2:100]` just stops at the end instead of raising
an error.

### Strings are immutable

You cannot change a string in place: `s[0] = "J"` is a `TypeError`.
Instead build a **new** string: `s = "J" + s[1:]`.

Why immutable? It makes strings safe to share and lets Python use them as
dictionary keys. The price: building a long string by repeated `+=` in a
loop is slow - collect pieces in a list and `"".join` them (next lesson).

A common trick: a word is a palindrome when `w == w[::-1]`.
""",
        examples=[
            dict(title="Indexes",
                 code="""\
s = "Python"
print(s[0], s[1], s[-1], s[-2])
print(len(s), s[len(s) - 1])
""",
                 explain="Index len(s) - 1 and index -1 both mean the last character."),
            dict(title="Slices",
                 code="""\
s = input()
print(s[:3])
print(s[3:])
print(s[::2])
print(s[::-1])
""",
                 stdin="abcdefgh\n",
                 explain="s[:3] + s[3:] always rebuilds the original string."),
            dict(title="Immutable",
                 code="""\
s = "cat"
s = "b" + s[1:]
print(s)
try:
    s[0] = "r"
except TypeError as e:
    print("error:", e)
""",
                 explain="To 'change' a string, build a new one and re-assign the name."),
        ],
        challenge=dict(
            prompt=("Read a single word. Print it reversed on the first line, then `YES` if it "
                    "is a palindrome (reads the same both ways) or `NO` otherwise."),
            starter="w = input()\n# use slicing\n",
            solution="w = input()\nr = w[::-1]\nprint(r)\nprint('YES' if w == r else 'NO')\n",
            samples=["level\n", "python\n"],
            tests=["a\n", "abba\n", "abca\n"],
        ),
    ),
    dict(
        id="py-string-methods",
        track="python",
        unit="Strings",
        title="String Methods",
        summary="upper, strip, find, replace, split and join - the everyday text toolkit.",
        body=r"""
Strings come with dozens of **methods** - functions you call with a dot:

```python
s = "  Hello, World  "
s.strip()           # 'Hello, World'   - trim whitespace at both ends
s.lower()           # '  hello, world  '
s.upper()           # '  HELLO, WORLD  '
s.replace("l", "L") # '  HeLLo, WorLd  '
s.count("l")        # 3
s.find("World")     # 9  (index of first match, -1 if missing)
"World" in s        # True
s.strip().startswith("He")   # True
```

> **Pitfall:** strings are immutable, so methods **return a new string**.
> `s.upper()` on its own line does nothing useful - write `s = s.upper()`.

### split and join

These two are opposites and you will use them in nearly every problem:

```python
words = "red green  blue".split()      # ['red', 'green', 'blue']
"a,b,c".split(",")                     # ['a', 'b', 'c']
"-".join(["red", "green", "blue"])     # 'red-green-blue'
"".join(["a", "b", "c"])               # 'abc'
```

`split()` with **no argument** splits on any run of whitespace and ignores
leading/trailing spaces - usually what you want. `split(" ")` splits on
every single space and leaves empty strings when there are doubles.

`join` is called on the **separator**, and every item must already be a
string: `" ".join(map(str, numbers))` converts numbers first.

Handy checks: `isdigit()`, `isalpha()`, `isupper()`, `islower()`, `isspace()`.

Methods can be chained because each returns a string:
`input().strip().lower().replace(" ", "")`.
""",
        examples=[
            dict(title="Cleaning text",
                 code="""\
s = "  Hello, World  "
print("[" + s.strip() + "]")
print(s.lower(), s.upper(), sep="|")
print(s.replace("l", "L"))
print(s.count("l"), s.find("World"), s.find("xyz"))
""",
                 explain="find returns -1 when the substring is missing."),
            dict(title="split vs split(' ')",
                 code="""\
line = "red green  blue"
print(line.split())
print(line.split(" "))
print("-".join(line.split()))
""",
                 explain="The double space produces an empty string with split(' ')."),
            dict(title="Numbers back to text",
                 code="""\
nums = list(map(int, input().split()))
print(" ".join(map(str, sorted(nums))))
print(", ".join(map(str, nums)))
""",
                 stdin="3 1 4 1 5\n",
                 explain="join only accepts strings, so convert each number with str."),
        ],
        challenge=dict(
            prompt=("Read a line of words that may be separated by several spaces and may use "
                    "any capitalisation. Print the words in lowercase joined by single dashes. "
                    "`Hello   World  PY` -> `hello-world-py`."),
            starter="line = input()\n# split, lower, join\n",
            solution="line = input()\nprint('-'.join(line.lower().split()))\n",
            samples=["Hello   World  PY\n"],
            tests=["one\n", "  Leading and trailing  \n", "MiXeD CaSe wOrDs Here\n"],
            checker="exact",
        ),
    ),
    dict(
        id="py-chars-ord",
        track="python",
        unit="Strings",
        title="Characters, ord & chr",
        summary="Loop over characters and turn letters into numbers and back.",
        body=r"""
Looping over a string gives you one character at a time:

```python
for ch in "Hi 5!":
    if ch.isalpha():
        print(ch, "is a letter")
    elif ch.isdigit():
        print(ch, "is a digit")
```

### Characters are numbers underneath

Every character has a code (its **Unicode code point**). `ord` gives the
number, `chr` goes back:

```python
ord("a")    # 97
ord("b")    # 98
chr(65)     # 'A'
```

Letters are consecutive, so arithmetic on codes is meaningful:

```python
pos = ord(ch) - ord("a")      # 'a' -> 0, 'b' -> 1, ... 'z' -> 25
ch = chr(ord("a") + pos)      # and back again
```

Write `ord("a")` rather than the magic number `97` - it documents your
intent and avoids mistakes.

### Wrapping around with %

To shift a letter by `k` places and wrap from `z` back to `a`, use modulo
26:

```python
new = chr((ord(ch) - ord("a") + k) % 26 + ord("a"))
```

This is the **Caesar cipher**, one of the oldest encryption schemes.

> **Pitfall:** the steps are *subtract `ord('a')`, add, `% 26`, add back*.
> Forgetting to subtract first means `% 26` is applied to 97..122 and the
> result is garbage. Also remember uppercase letters start at `ord("A")`
> (65).

Building the result: append each new character to a list and finish with
`"".join(chars)` - faster and cleaner than repeated `+=`.
""",
        examples=[
            dict(title="Classify characters",
                 code="""\
for ch in "Hi 5!":
    if ch.isalpha():
        kind = "letter"
    elif ch.isdigit():
        kind = "digit"
    else:
        kind = "other"
    print(repr(ch), kind, ord(ch))
""",
                 explain="repr() shows the quotes, so you can see the space character."),
            dict(title="Letter positions",
                 code="""\
word = input()
for c in word:
    print(c, ord(c) - ord("a") + 1)
print(chr(ord("a") + 25), chr(ord("A") + 2))
""",
                 stdin="abcz\n",
                 explain="Subtracting ord('a') maps letters to 0..25 (here +1 for 1..26)."),
            dict(title="ROT13",
                 code="""\
text = "hello world"
out = []
for ch in text:
    if "a" <= ch <= "z":
        ch = chr((ord(ch) - ord("a") + 13) % 26 + ord("a"))
    out.append(ch)
print("".join(out))
""",
                 explain="Shifting by 13 twice brings you back - ROT13 is its own inverse."),
        ],
        challenge=dict(
            prompt=("Caesar cipher. The first line holds a shift `k` (0 <= k <= 100), the second "
                    "a line of text. Shift every **lowercase** letter forward by `k` places, "
                    "wrapping from `z` to `a`; leave all other characters unchanged."),
            starter="k = int(input())\ntext = input()\nout = []\n# for ch in text: ...\nprint(''.join(out))\n",
            solution=("k = int(input())\ntext = input()\nout = []\nfor ch in text:\n"
                      "    if 'a' <= ch <= 'z':\n"
                      "        ch = chr((ord(ch) - ord('a') + k) % 26 + ord('a'))\n"
                      "    out.append(ch)\nprint(''.join(out))\n"),
            samples=["3\nhello, world!\n"],
            tests=["1\nxyz\n", "26\nstay the same\n", "55\nMixed Case 123 zoo\n"],
            checker="exact",
        ),
    ),
]
