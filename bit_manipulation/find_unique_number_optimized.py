#!/usr/bin/env python3
"""
Optimized and alternative implementations of Find Unique Number.

The reference XORs all elements in a loop — O(n) time, O(1) space.
This is already the optimal solution. The alternatives below exist because
interviewers often ask "what if you couldn't use XOR?" or "can you do it
without extra space?".

Variants covered:
1. xor_reduce      -- functools.reduce(operator.xor, arr) — one-liner
2. counter         -- collections.Counter, find count == 1 — O(n) space
3. sort_pairwise   -- sort + pairwise scan — O(n log n), O(1) extra
4. set_math        -- 2*sum(set) - sum(arr) — O(n) space, no bit ops

Key interview insight:
    XOR is the gold standard: O(n) time, O(1) space, single pass.
    a ^ a = 0 and a ^ 0 = a. Pairs cancel, lone element survives.

Run:
    python bit_manipulation/find_unique_number_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
import operator
from collections import Counter
from functools import reduce

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bit_manipulation.find_unique_number import find_unique_number as reference


# ---------------------------------------------------------------------------
# Variant 1 — functools.reduce with operator.xor (one-liner)
# ---------------------------------------------------------------------------

def xor_reduce(arr: list[int]) -> int:
    """
    One-liner XOR using functools.reduce.

    >>> xor_reduce([1, 1, 2, 2, 3])
    3
    >>> xor_reduce([4, 5, 4, 6, 6])
    5
    >>> xor_reduce([7])
    7
    >>> xor_reduce([10, 20, 10])
    20
    """
    if not arr:
        raise ValueError("input list must not be empty")
    return reduce(operator.xor, arr)


# ---------------------------------------------------------------------------
# Variant 2 — collections.Counter (hash map)
# ---------------------------------------------------------------------------

def counter_method(arr: list[int]) -> int:
    """
    Find unique using Counter. O(n) time, O(n) space.

    Non-bitwise fallback interviewers may ask for.

    >>> counter_method([1, 1, 2, 2, 3])
    3
    >>> counter_method([4, 5, 4, 6, 6])
    5
    >>> counter_method([7])
    7
    >>> counter_method([10, 20, 10])
    20
    """
    if not arr:
        raise ValueError("input list must not be empty")
    counts = Counter(arr)
    for num, cnt in counts.items():
        if cnt == 1:
            return num
    raise ValueError("no unique element found")


# ---------------------------------------------------------------------------
# Variant 3 — sort + pairwise scan
# ---------------------------------------------------------------------------

def sort_pairwise(arr: list[int]) -> int:
    """
    Sort then check adjacent pairs. O(n log n) time, O(1) extra space
    (if sort is in-place).

    >>> sort_pairwise([1, 1, 2, 2, 3])
    3
    >>> sort_pairwise([4, 5, 4, 6, 6])
    5
    >>> sort_pairwise([7])
    7
    >>> sort_pairwise([10, 20, 10])
    20
    """
    if not arr:
        raise ValueError("input list must not be empty")
    if len(arr) == 1:
        return arr[0]
    sorted_arr = sorted(arr)
    for i in range(0, len(sorted_arr) - 1, 2):
        if sorted_arr[i] != sorted_arr[i + 1]:
            return sorted_arr[i]
    return sorted_arr[-1]


# ---------------------------------------------------------------------------
# Variant 4 — set math: 2*sum(set) - sum(arr)
# ---------------------------------------------------------------------------

def set_math(arr: list[int]) -> int:
    """
    Algebraic identity: if every element appears twice except one, then
    2 * sum(unique_elements) - sum(all_elements) = the lone element.

    O(n) time, O(n) space. No bit operations.

    >>> set_math([1, 1, 2, 2, 3])
    3
    >>> set_math([4, 5, 4, 6, 6])
    5
    >>> set_math([7])
    7
    >>> set_math([10, 20, 10])
    20
    """
    if not arr:
        raise ValueError("input list must not be empty")
    return 2 * sum(set(arr)) - sum(arr)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([1, 1, 2, 2, 3], 3),
    ([4, 5, 4, 6, 6], 5),
    ([7], 7),
    ([10, 20, 10], 20),
    ([0, 0, -1], -1),
    ([100, 100, 42], 42),
]

IMPLS = [
    ("reference", reference),
    ("xor_reduce", xor_reduce),
    ("counter",    counter_method),
    ("sort",       sort_pairwise),
    ("set_math",   set_math),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for arr, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(arr)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(
            f"  [{tag}] input={str(arr):<35} expected={expected:<5}  "
            + "  ".join(f"{n}={v}" for n, v in results.items())
        )

    REPS = 200_000
    inputs = [
        [1, 1, 2, 2, 3],
        [4, 5, 4, 6, 6],
        [7],
        [10, 20, 10],
        [0, 0, -1],
        [100, 100, 42],
    ]
    print(f"\n=== Benchmark: {REPS} runs, {len(inputs)} test arrays ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(a) for a in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<12} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
