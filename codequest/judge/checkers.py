"""Output comparison strategies ("checkers").

A problem chooses one by name; the default is ``tokens``.

* ``tokens``       whitespace-insensitive token comparison (most problems)
* ``exact``        line by line, ignoring trailing spaces / trailing blank lines
                   (use for ASCII-art & formatting problems)
* ``tokens_ci``    like ``tokens`` but case-insensitive (YES / yes)
* ``float``        tokens; numbers equal within 1e-6 absolute or relative
* ``unordered``    lines compared as a multiset (any output order accepted)
* ``sympy``        each line parsed as a SymPy expression and compared
                   symbolically, so ``2*x + 1`` matches ``1 + 2*x``
"""

import math


def _lines(text):
    lines = [ln.rstrip() for ln in text.replace("\r\n", "\n").split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    return lines


def exact(expected, actual):
    return _lines(expected) == _lines(actual)


def tokens(expected, actual):
    return expected.split() == actual.split()


def tokens_ci(expected, actual):
    return expected.lower().split() == actual.lower().split()


def _num(tok):
    try:
        val = float(tok)
    except ValueError:
        return None
    return val if math.isfinite(val) else None


def floats(expected, actual, tol=1e-6):
    exp, act = expected.split(), actual.split()
    if len(exp) != len(act):
        return False
    for e, a in zip(exp, act):
        if e == a:
            continue
        ev, av = _num(e), _num(a)
        if ev is None or av is None:
            return False
        if abs(ev - av) > tol * max(1.0, abs(ev)):
            return False
    return True


def unordered(expected, actual):
    norm = lambda t: sorted(" ".join(ln.split()) for ln in _lines(t) if ln.strip())
    return norm(expected) == norm(actual)


def symbolic(expected, actual):
    exp_lines = [ln for ln in _lines(expected) if ln.strip()]
    act_lines = [ln for ln in _lines(actual) if ln.strip()]
    if len(exp_lines) != len(act_lines):
        return False
    try:
        import sympy
        from sympy.parsing.sympy_parser import (
            parse_expr, standard_transformations, implicit_multiplication_application,
            convert_xor,
        )
    except ImportError:
        return tokens(expected, actual)
    transforms = standard_transformations + (implicit_multiplication_application, convert_xor)
    for e, a in zip(exp_lines, act_lines):
        if e.split() == a.split():
            continue
        try:
            ee = parse_expr(e, transformations=transforms, evaluate=True)
            aa = parse_expr(a, transformations=transforms, evaluate=True)
            if isinstance(ee, (list, tuple, set)) or isinstance(aa, (list, tuple, set)):
                if type(ee) is not type(aa) or len(ee) != len(aa):
                    return False
                pairs = zip(sorted(ee, key=str), sorted(aa, key=str)) if isinstance(ee, set) else zip(ee, aa)
                if not all(sympy.simplify(x - y) == 0 for x, y in pairs):
                    return False
                continue
            if isinstance(ee, sympy.Basic) and ee.is_Relational:
                if not (isinstance(aa, sympy.Basic) and aa.is_Relational):
                    return False
                if sympy.simplify((ee.lhs - ee.rhs) - (aa.lhs - aa.rhs)) != 0:
                    return False
                continue
            if sympy.simplify(ee - aa) != 0:
                return False
        except Exception:
            return False
    return True


CHECKERS = {
    "tokens": tokens,
    "exact": exact,
    "tokens_ci": tokens_ci,
    "float": floats,
    "unordered": unordered,
    "sympy": symbolic,
}


def check(name, expected, actual):
    return CHECKERS.get(name or "tokens", tokens)(expected, actual)
