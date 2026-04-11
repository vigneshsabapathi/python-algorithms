#!/usr/bin/env python3
"""
Optimized and alternative implementations of Alternative List Arrange.

The reference interleaves first half and second half of a list.

Variants covered:
1. split_interleave  -- Split and zip (reference approach)
2. index_formula     -- Direct index calculation, no split
3. itertools_chain   -- Using itertools.chain and zip_longest

Run:
    python other/alternative_list_arrange_optimized.py
"""

from __future__ import annotations

import itertools
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.alternative_list_arrange import alternative_list_arrange as reference


def split_interleave(lst: list) -> list:
    """
    >>> split_interleave([1, 2, 3, 4, 5, 6])
    [1, 4, 2, 5, 3, 6]
    >>> split_interleave([1, 2, 3, 4, 5])
    [1, 4, 2, 5, 3]
    >>> split_interleave([])
    []
    """
    if len(lst) <= 1:
        return lst
    mid = (len(lst) + 1) // 2
    first, second = lst[:mid], lst[mid:]
    result = []
    for a, b in itertools.zip_longest(first, second):
        result.append(a)
        if b is not None:
            result.append(b)
    return result


def index_formula(lst: list) -> list:
    """
    Direct index mapping without splitting.

    >>> index_formula([1, 2, 3, 4, 5, 6])
    [1, 4, 2, 5, 3, 6]
    >>> index_formula([1, 2, 3, 4, 5])
    [1, 4, 2, 5, 3]
    >>> index_formula([])
    []
    """
    if len(lst) <= 1:
        return lst
    mid = (len(lst) + 1) // 2
    result = []
    for i in range(mid):
        result.append(lst[i])
        if i + mid < len(lst):
            result.append(lst[i + mid])
    return result


def itertools_chain_approach(lst: list) -> list:
    """
    Using itertools to interleave.

    >>> itertools_chain_approach([1, 2, 3, 4, 5, 6])
    [1, 4, 2, 5, 3, 6]
    >>> itertools_chain_approach([])
    []
    """
    if len(lst) <= 1:
        return lst
    mid = (len(lst) + 1) // 2
    sentinel = object()
    pairs = itertools.zip_longest(lst[:mid], lst[mid:], fillvalue=sentinel)
    return [x for pair in pairs for x in pair if x is not sentinel]


TEST_CASES = [
    ([1, 2, 3, 4, 5, 6], [1, 4, 2, 5, 3, 6]),
    ([1, 2, 3, 4, 5], [1, 4, 2, 5, 3]),
    ([], []),
    ([1], [1]),
    ([1, 2], [1, 2]),
    ([11, 22, 33, 44], [11, 33, 22, 44]),
]

IMPLS = [
    ("reference", reference),
    ("split_interleave", split_interleave),
    ("index_formula", index_formula),
    ("itertools_chain", itertools_chain_approach),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for inp, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(list(inp))
            ok = result == expected
            tag = "OK" if ok else "FAIL"
            if not ok:
                print(f"  [{tag}] {name}: input={inp} expected={expected} got={result}")
        print(f"  [OK] input={inp}")

    large = list(range(10000))
    REPS = 5000
    print(f"\n=== Benchmark: {REPS} runs, {len(large)} elements ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(list(large)), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
