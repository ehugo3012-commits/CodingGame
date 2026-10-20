"""Python track - Unit 0. Also the style reference for lesson authors."""

LESSONS = [
    dict(
        id="py-hello",
        track="python",
        unit="Getting Started",
        title="Hello, Python",
        summary="Your first program: print() and how CodeQuest runs your code.",
        body="""
Python runs your file **top to bottom**, one line at a time. The built-in
`print()` function writes text to the screen (standard output):

```python
print("Hello, world!")
print("2 + 3 =", 2 + 3)
```

`print` accepts several values separated by commas and puts a space between
them. Text must be wrapped in quotes — `"double"` or `'single'`, both work.

**Comments** start with `#` and are ignored by Python. Use them to explain
*why* your code does something.

> In CodeQuest every program talks to the judge through standard input and
> standard output, exactly like on competitive-programming sites.
""",
        examples=[
            dict(title="Printing", code='print("Hello, world!")\nprint("2 + 3 =", 2 + 3)\n'),
            dict(title="sep and end",
                 code='print("a", "b", "c", sep="-")\nprint("no newline", end="!")\nprint()\n',
                 explain="`sep` changes the separator, `end` changes what is printed at the end."),
        ],
        challenge=dict(
            prompt="Print exactly `I am learning Python!` (no input).",
            starter='# print the sentence below\n',
            solution='print("I am learning Python!")\n',
            samples=[""],
            checker="exact",
        ),
    ),
    dict(
        id="py-input",
        track="python",
        unit="Getting Started",
        title="Reading Input",
        summary="input(), int() and split(): getting data into your program.",
        body="""
`input()` reads **one line** of text from standard input and returns it as a
string (without the trailing newline).

```python
name = input()
print("Hi", name)
```

Input is always text. To do maths, convert it:

```python
age = int(input())      # whole numbers
price = float(input())  # decimals
```

Several values on one line? `split()` cuts a string at whitespace, and `map`
applies a function to every piece:

```python
a, b = map(int, input().split())
```

For big inputs, read everything at once: `import sys; data = sys.stdin.read().split()`.
""",
        examples=[
            dict(title="Greeting", code='name = input()\nprint("Hi", name)\n', stdin="Ada\n"),
            dict(title="Two numbers", code="a, b = map(int, input().split())\nprint(a * b)\n",
                 stdin="6 7\n"),
            dict(title="Read everything",
                 code="import sys\nnums = list(map(int, sys.stdin.read().split()))\nprint(len(nums), sum(nums))\n",
                 stdin="3\n1 2 3\n", explain="Handy when you don't care about line breaks."),
        ],
        challenge=dict(
            prompt="Read a name on the first line and a year on the second. Print `<name> is <age> in 2030`.",
            starter="name = input()\nyear = int(input())\n# print the sentence\n",
            solution='name = input()\nyear = int(input())\nprint(name, "is", 2030 - year, "in 2030")\n',
            samples=["Ada\n1990\n"],
            tests=["Linus\n2001\n", "Grace\n2030\n"],
            checker="exact",
        ),
    ),
]
