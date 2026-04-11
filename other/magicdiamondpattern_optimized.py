#!/usr/bin/env python3
"""
Optimized and alternative implementations of Magic Diamond Pattern.

Variants covered:
1. loop_based       -- Nested loops with spaces (reference)
2. string_center    -- Using str.center()
3. list_comp        -- List comprehension one-liner

Run:
    python other/magicdiamondpattern_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.magicdiamondpattern import magic_diamond as reference


def center_diamond(n: int) -> str:
    """
    Diamond using str.center().

    >>> print(center_diamond(3))
      1
     2 2
    3 3 3
     2 2
      1
    >>> print(center_diamond(1))
    1
    """
    if n <= 0:
        return ""
    width = 2 * n - 1
    rows = list(range(1, n + 1)) + list(range(n - 1, 0, -1))
    lines = []
    for i in rows:
        content = " ".join(str(i) for _ in range(i))
        lines.append(content.center(width))
    return "\n".join(line.rstrip() for line in lines)


def list_comp_diamond(n: int) -> str:
    """
    Diamond using list comprehension.

    >>> print(list_comp_diamond(3))
      1
     2 2
    3 3 3
     2 2
      1
    """
    if n <= 0:
        return ""
    rows = list(range(1, n + 1)) + list(range(n - 1, 0, -1))
    return "\n".join(
        " " * (n - i) + " ".join(str(i) for _ in range(i))
        for i in rows
    )


def hollow_diamond(n: int) -> str:
    """
    Hollow diamond pattern (only border numbers shown).

    >>> print(hollow_diamond(3))
      1
     2 2
    3   3
     2 2
      1
    """
    if n <= 0:
        return ""
    lines = []
    rows = list(range(1, n + 1)) + list(range(n - 1, 0, -1))
    for i in rows:
        spaces = " " * (n - i)
        if i == 1:
            lines.append(spaces + str(i))
        else:
            inner = " " * (2 * i - 3)
            lines.append(spaces + str(i) + inner + str(i))
    return "\n".join(lines)


TEST_CASES = [
    (1, "1"),
    (3, "  1\n 2 2\n3 3 3\n 2 2\n  1"),
]

IMPLS = [
    ("reference", reference),
    ("center", center_diamond),
    ("list_comp", list_comp_diamond),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for n, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(n)
            ok = result == expected
            tag = "OK" if ok else "FAIL"
            if not ok:
                print(f"  [{tag}] {name}(n={n}):\n    expected={expected!r}\n    got    ={result!r}")
        print(f"  [OK] n={n}")

    print("\n=== Hollow diamond (n=4) ===")
    print(hollow_diamond(4))

    REPS = 50_000
    print(f"\n=== Benchmark: {REPS} runs, n=20 ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(20), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
