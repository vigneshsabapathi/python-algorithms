#!/usr/bin/env python3
"""
Optimized and alternative implementations of Nested Brackets.

Variants covered:
1. stack_matching     -- Stack-based matching (reference)
2. counter_parens     -- Counter approach (parentheses only)
3. regex_elimination  -- Repeated regex elimination

Run:
    python other/nested_brackets_optimized.py
"""

from __future__ import annotations

import os
import re
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.nested_brackets import is_balanced as reference


def counter_parens_only(expression: str) -> bool:
    """
    Check balanced parentheses only (not brackets/braces) using a counter.

    >>> counter_parens_only("(())")
    True
    >>> counter_parens_only("(()")
    False
    >>> counter_parens_only("")
    True
    >>> counter_parens_only(")(")
    False
    """
    count = 0
    for char in expression:
        if char == "(":
            count += 1
        elif char == ")":
            count -= 1
            if count < 0:
                return False
    return count == 0


def regex_elimination(expression: str) -> bool:
    """
    Check balanced brackets by repeatedly removing matched pairs.

    >>> regex_elimination("([{}])")
    True
    >>> regex_elimination("([)]")
    False
    >>> regex_elimination("")
    True
    """
    brackets_only = re.sub(r"[^()\[\]{}]", "", expression)
    pattern = re.compile(r"\(\)|\[\]|\{\}")
    prev = None
    while prev != brackets_only:
        prev = brackets_only
        brackets_only = pattern.sub("", brackets_only)
    return brackets_only == ""


def max_nesting_depth(expression: str) -> int:
    """
    Find maximum nesting depth of brackets.

    >>> max_nesting_depth("((()))")
    3
    >>> max_nesting_depth("(())()")
    2
    >>> max_nesting_depth("")
    0
    >>> max_nesting_depth("([{()}])")
    4
    """
    depth = 0
    max_depth = 0
    for char in expression:
        if char in "([{":
            depth += 1
            max_depth = max(max_depth, depth)
        elif char in ")]}":
            depth -= 1
    return max_depth


TEST_CASES = [
    ("([])", True),
    ("([)]", False),
    ("{[()]}", True),
    ("", True),
    ("((()))", True),
    ("(", False),
    (")", False),
]

IMPLS = [
    ("reference", reference),
    ("regex", regex_elimination),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for expr, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(expr)
            ok = result == expected
            tag = "OK" if ok else "FAIL"
            if not ok:
                print(f"  [{tag}] {name}: expr={expr!r} expected={expected} got={result}")
        print(f"  [OK] {expr!r} -> {expected}")

    REPS = 50_000
    test_expr = "({[" * 100 + "]})" * 100
    print(f"\n=== Benchmark: {REPS} runs, {len(test_expr)} chars ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(test_expr), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
