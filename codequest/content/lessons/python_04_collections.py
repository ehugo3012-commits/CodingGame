"""Python track - Unit 4: Collections (lists, tuples, sets, dicts)."""

LESSONS = [
    dict(
        id="py-lists",
        track="python",
        unit="Collections",
        title="Lists",
        summary="Ordered, changeable sequences: append, pop, len, slicing and sorting.",
        body=r"""
A **list** holds many values in order, inside square brackets:

```python
nums = [5, 3, 8]
nums.append(1)      # [5, 3, 8, 1]   add at the end
nums[0] = 7         # [7, 3, 8, 1]   lists ARE mutable
last = nums.pop()   # removes and returns 1
nums.insert(0, 9)   # [9, 7, 3, 8]
len(nums)           # 4
8 in nums           # True
```

Indexing and slicing work exactly like strings: `nums[-1]`, `nums[1:3]`,
`nums[::-1]`. Useful built-ins: `sum`, `min`, `max`, `sorted`.

### Reading a list from input

```python
nums = list(map(int, input().split()))
```

### Sorting: sort() vs sorted()

- `nums.sort()` sorts **in place** and returns `None`.
- `sorted(nums)` returns a **new** sorted list and leaves `nums` alone.

Both accept `reverse=True`.

> **Pitfall:** `nums = nums.sort()` sets `nums` to `None`!

### Aliasing

Assignment never copies a list - it gives the *same* list a second name:

```python
a = [1, 2, 3]
b = a          # same list
b.append(4)
print(a)       # [1, 2, 3, 4]  - surprise!
c = a.copy()   # or a[:] - a real copy
```

> **Pitfall:** `[[0] * 3] * 3` makes three references to *one* inner list.
> Build grids with `[[0] * 3 for _ in range(3)]` instead.

`pop()` from the end is fast; `pop(0)` from the front has to shift every
element, so it is slow for big lists (see `deque` later).
""",
        examples=[
            dict(title="Changing a list",
                 code="""\
nums = [5, 3, 8]
nums.append(1)
nums[0] = 7
print(nums, len(nums))
print("popped", nums.pop(), "->", nums)
nums.insert(0, 9)
print(nums, nums[1:3], sum(nums), max(nums))
""",
                 explain="append/pop work at the end; insert puts an item at a given index."),
            dict(title="sort vs sorted",
                 code="""\
nums = list(map(int, input().split()))
print(sorted(nums), nums)
nums.sort(reverse=True)
print(nums)
print(nums.sort())
""",
                 stdin="4 1 3 9 2\n",
                 explain="sorted() returns a copy; .sort() changes the list and returns None."),
            dict(title="Aliasing trap",
                 code="""\
a = [1, 2, 3]
b = a
c = a.copy()
b.append(4)
print(a, b, c)
print(a is b, a is c)
""",
                 explain="b is another name for the same list; c is an independent copy."),
        ],
        challenge=dict(
            prompt=("Read a line of integers. Print them sorted ascending on one line (space "
                    "separated), and on the second line print the largest minus the smallest."),
            starter="nums = list(map(int, input().split()))\n# sorted, max, min\n",
            solution=("nums = list(map(int, input().split()))\n"
                      "print(' '.join(map(str, sorted(nums))))\nprint(max(nums) - min(nums))\n"),
            samples=["4 1 3 9 2\n"],
            tests=["7\n", "-5 10 -5 3\n", "2 2 2\n"],
        ),
    ),
    dict(
        id="py-tuples",
        track="python",
        unit="Collections",
        title="Tuples & Unpacking",
        summary="Fixed groups of values, multiple assignment and the a, b = b, a swap.",
        body=r"""
A **tuple** is like a list that cannot change. Write it with parentheses
(or just commas):

```python
point = (3, 4)
rgb = 255, 128, 0     # parentheses optional
point[0]              # 3
```

Use a tuple for a fixed bundle of related values: a coordinate, a
`(name, score)` pair, a date. Being immutable, tuples can be dictionary keys
and set members - lists cannot.

> **Pitfall:** a one-item tuple needs a trailing comma: `(5,)`. Plain
> `(5)` is just the number 5 in brackets.

### Unpacking

Assign a sequence to several names at once:

```python
x, y = point                 # x = 3, y = 4
name, score = "Ada", 91
first, *rest = [1, 2, 3, 4]  # first = 1, rest = [2, 3, 4]
```

The counts must match (except for the starred name), otherwise you get
`ValueError: too many values to unpack`. That is also why
`a, b = map(int, input().split())` crashes when the line has three numbers.

Swapping needs no temporary variable:

```python
a, b = b, a
```

The right side builds a tuple *first*, then unpacks it.

### Comparing tuples

Tuples compare **element by element**, left to right, like words in a
dictionary: `(2, "b") < (2, "c") < (3, "a")`. This makes them perfect for
"sort by score, then by name". A trick for "highest score, ties by smallest
name": take `min` of `(-score, name)`.

Functions can return several values - they are really returning one tuple:
`return lo, hi`.
""",
        examples=[
            dict(title="Pack and unpack",
                 code="""\
point = (3, 4)
x, y = point
print(x, y, type(point))
first, *rest = [1, 2, 3, 4]
print(first, rest)
print(type((5)), type((5,)))
""",
                 explain="The trailing comma, not the parentheses, makes a tuple."),
            dict(title="Swap",
                 code="""\
a, b = map(int, input().split())
a, b = b, a
print(a, b)
""",
                 stdin="1 2\n"),
            dict(title="Tuples compare in order",
                 code="""\
people = [(91, "Bob"), (85, "Ada"), (91, "Al")]
print(sorted(people))
negated = [(-91, "Bob"), (-85, "Ada"), (-91, "Al")]
print(min(negated))   # highest score, ties -> smallest name
print((2, "b") < (2, "c") < (3, "a"))
""",
                 explain="The first element decides; ties fall through to the next element."),
        ],
        challenge=dict(
            prompt=("The first line holds `n`. Each of the next `n` lines has `name score`. Print "
                    "the name with the highest score; if several share it, print the "
                    "alphabetically smallest name."),
            starter="n = int(input())\nbest = None\nfor _ in range(n):\n    name, score = input().split()\n    # compare tuples\n",
            solution=("n = int(input())\nbest = None\nfor _ in range(n):\n"
                      "    name, score = input().split()\n    key = (-int(score), name)\n"
                      "    if best is None or key < best:\n        best = key\nprint(best[1])\n"),
            samples=["3\nBob 91\nAda 85\nAl 91\n"],
            tests=["1\nZed 0\n", "4\ncara 50\nbea 70\nanna 70\ndan 69\n", "2\nx 5\ny 10\n"],
        ),
    ),
    dict(
        id="py-sets",
        track="python",
        unit="Collections",
        title="Sets",
        summary="Unordered collections of unique items with lightning-fast membership tests.",
        body=r"""
A **set** stores each value **at most once**, with no particular order:

```python
s = {3, 1, 3, 2}       # {1, 2, 3}
s.add(5)
s.discard(1)           # remove if present (no error if missing)
len(s)                 # 3
2 in s                 # True - and very fast
```

`set(some_list)` removes duplicates in one step, so
`len(set(words))` counts distinct words.

### Why sets are fast

`x in my_list` checks items one by one - slow for big lists. A set uses
**hashing** to jump straight to where `x` would be, so `x in my_set` takes
about the same time whether the set has 10 or 10 million items. If your
code does many `in` checks, convert to a set first.

### Set algebra

```python
a = {1, 2, 3, 4}
b = {3, 4, 5}
a | b     # union         {1, 2, 3, 4, 5}
a & b     # intersection  {3, 4}
a - b     # difference    {1, 2}
a ^ b     # in exactly one {1, 2, 5}
```

> **Pitfall:** `{}` is an empty **dict**, not a set. Write `set()`.

> **Pitfall:** sets have no order and no indexes - `s[0]` is an error, and
> printing a set may show items in any order. When output order matters,
> use `sorted(s)`.

Only immutable values can go in a set: numbers, strings, tuples - but not
lists. Sets themselves are mutable; `frozenset` is the immutable version.
""",
        examples=[
            dict(title="Unique values",
                 code="""\
words = input().split()
uniq = set(words)
print(len(words), "words,", len(uniq), "distinct")
print(sorted(uniq))
""",
                 stdin="the cat and the hat and the bat\n",
                 explain="sorted() turns the set into a list with a predictable order."),
            dict(title="Set algebra",
                 code="""\
a = {1, 2, 3, 4}
b = {3, 4, 5}
print(sorted(a | b), sorted(a & b), sorted(a - b), sorted(a ^ b))
print(type({}), type(set()))
""",
                 explain="{} is a dict - use set() for an empty set."),
            dict(title="Seen-before check",
                 code="""\
seen = set()
for x in [4, 7, 1, 7, 3, 4]:
    if x in seen:
        print("repeat:", x)
    seen.add(x)
""",
                 explain="A classic pattern: remember what you've seen in a set."),
        ],
        challenge=dict(
            prompt=("Read two lines of words. Print the words that appear in **both** lines, "
                    "each once, sorted alphabetically and separated by spaces. If there are none, "
                    "print `NONE`."),
            starter="a = set(input().split())\nb = set(input().split())\n# intersection\n",
            solution=("a = set(input().split())\nb = set(input().split())\ncommon = sorted(a & b)\n"
                      "print(' '.join(common) if common else 'NONE')\n"),
            samples=["red green blue green\nblue yellow red\n"],
            tests=["a b c\nd e f\n", "x x x\nx\n", "pear apple fig\nfig apple pear kiwi\n"],
        ),
    ),
    dict(
        id="py-dicts",
        track="python",
        unit="Collections",
        title="Dictionaries",
        summary="Map keys to values: lookup, .get, counting and looping with items().",
        body=r"""
A **dictionary** maps **keys** to **values**, like a phone book:

```python
ages = {"Ada": 36, "Linus": 28}
ages["Grace"] = 45        # add or overwrite
print(ages["Ada"])        # 36
"Linus" in ages           # True - checks KEYS, not values
del ages["Linus"]
len(ages)                 # 2
```

Like sets, dicts use hashing, so lookups are fast no matter how big the
dict is. Keys must be immutable (str, int, tuple); values can be anything.

> **Pitfall:** `ages["Bob"]` for a missing key raises `KeyError`. Use
> `ages.get("Bob")` (gives `None`) or `ages.get("Bob", 0)` for a default.

### Counting

The most common dict job of all:

```python
counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1
```

`get(w, 0)` returns 0 the first time a word is seen, so no special case is
needed.

### Looping

```python
for name in ages:                  # keys
for age in ages.values():          # values
for name, age in ages.items():     # both - the usual choice
```

Since Python 3.7 a dict remembers **insertion order**, so loops visit keys
in the order they were first added. To loop in another order, sort:
`for k in sorted(d)` (by key) or
`sorted(d.items(), key=lambda kv: kv[1])` (by value - see the lambda
lesson).

> **Pitfall:** don't add or remove keys while looping over the same dict -
> loop over `list(d)` if you must.
""",
        examples=[
            dict(title="Basics",
                 code="""\
ages = {"Ada": 36, "Linus": 28}
ages["Grace"] = 45
print(ages["Ada"], "Linus" in ages, 36 in ages)
print(ages.get("Bob"), ages.get("Bob", 0))
for name, age in ages.items():
    print(name, age)
""",
                 explain="`in` looks at keys; .get avoids a KeyError for missing keys."),
            dict(title="Counting letters",
                 code="""\
counts = {}
for ch in input():
    counts[ch] = counts.get(ch, 0) + 1
for ch in sorted(counts):
    print(ch, counts[ch])
""",
                 stdin="banana\n",
                 explain="get(ch, 0) handles the first time each letter appears."),
            dict(title="KeyError",
                 code="""\
d = {"a": 1}
try:
    print(d["z"])
except KeyError as e:
    print("missing key:", e)
""",
                 explain="Square brackets demand the key exists."),
        ],
        challenge=dict(
            prompt=("Read a line of words. For each distinct word, in order of **first "
                    "appearance**, print the word and how many times it occurs, one per line "
                    "(`word count`)."),
            starter="words = input().split()\ncounts = {}\n# count, then loop over counts.items()\n",
            solution=("words = input().split()\ncounts = {}\nfor w in words:\n"
                      "    counts[w] = counts.get(w, 0) + 1\nfor w, c in counts.items():\n"
                      "    print(w, c)\n"),
            samples=["to be or not to be\n"],
            tests=["hello\n", "b a b a c b\n", "x y z\n"],
            checker="exact",
        ),
    ),
]
