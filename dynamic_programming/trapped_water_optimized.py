#!/usr/bin/env python3
"""
Optimized and alternative implementations of Trapping Rain Water.

Variants covered:
1. trapped_water_two_pointer  -- O(1) space two-pointer approach
2. trapped_water_stack        -- monotonic stack approach
3. trapped_water_pythonic     -- compact Python one-pass

Run:
    python dynamic_programming/trapped_water_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.trapped_water import trapped_water as reference


# ---------------------------------------------------------------------------
# Variant 1 — Two-pointer O(1) space
# ---------------------------------------------------------------------------

def trapped_water_two_pointer(heights: list[int]) -> int:
    """
    Trapping rain water using two pointers — O(n) time, O(1) space.

    >>> trapped_water_two_pointer([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])
    6
    >>> trapped_water_two_pointer([4, 2, 0, 3, 2, 5])
    9
    >>> trapped_water_two_pointer([1, 2, 3, 4, 5])
    0
    >>> trapped_water_two_pointer([])
    0
    >>> trapped_water_two_pointer([3, 0, 3])
    3
    """
    if len(heights) < 3:
        return 0
    left, right = 0, len(heights) - 1
    left_max = right_max = 0
    water = 0

    while left < right:
        if heights[left] < heights[right]:
            if heights[left] >= left_max:
                left_max = heights[left]
            else:
                water += left_max - heights[left]
            left += 1
        else:
            if heights[right] >= right_max:
                right_max = heights[right]
            else:
                water += right_max - heights[right]
            right -= 1

    return water


# ---------------------------------------------------------------------------
# Variant 2 — Monotonic stack
# ---------------------------------------------------------------------------

def trapped_water_stack(heights: list[int]) -> int:
    """
    Trapping rain water using a monotonic decreasing stack.

    >>> trapped_water_stack([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])
    6
    >>> trapped_water_stack([4, 2, 0, 3, 2, 5])
    9
    >>> trapped_water_stack([1, 2, 3, 4, 5])
    0
    >>> trapped_water_stack([])
    0
    >>> trapped_water_stack([3, 0, 3])
    3
    """
    stack: list[int] = []
    water = 0

    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] < h:
            bottom = heights[stack.pop()]
            if not stack:
                break
            width = i - stack[-1] - 1
            bounded_height = min(h, heights[stack[-1]]) - bottom
            water += width * bounded_height
        stack.append(i)

    return water


# ---------------------------------------------------------------------------
# Variant 3 — Compact Pythonic
# ---------------------------------------------------------------------------

def trapped_water_pythonic(heights: list[int]) -> int:
    """
    Compact Python implementation using accumulate.

    >>> trapped_water_pythonic([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])
    6
    >>> trapped_water_pythonic([4, 2, 0, 3, 2, 5])
    9
    >>> trapped_water_pythonic([1, 2, 3, 4, 5])
    0
    >>> trapped_water_pythonic([])
    0
    >>> trapped_water_pythonic([3, 0, 3])
    3
    """
    if len(heights) < 3:
        return 0
    from itertools import accumulate
    left_max = list(accumulate(heights, max))
    right_max = list(accumulate(reversed(heights), max))[::-1]
    return sum(min(l, r) - h for l, r, h in zip(left_max, right_max, heights))


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
    ([4, 2, 0, 3, 2, 5], 9),
    ([1, 2, 3, 4, 5], 0),
    ([5, 4, 3, 2, 1], 0),
    ([], 0),
    ([3, 0, 3], 3),
]

IMPLS = [
    ("reference", reference),
    ("two_pointer", trapped_water_two_pointer),
    ("stack", trapped_water_stack),
    ("pythonic", trapped_water_pythonic),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for heights, expected in TEST_CASES:
        results = {name: fn(list(heights)) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] heights={heights}  expected={expected}  " +
              "  ".join(f"{n}={v}" for n, v in results.items()))

    REPS = 50_000
    import random
    random.seed(42)
    bench = [random.randint(0, 20) for _ in range(100)]
    print(f"\n=== Benchmark: {REPS} runs, len={len(bench)} ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(bench), number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
