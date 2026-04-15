#!/usr/bin/env python3
"""
Optimized and alternative implementations of Subset Generation.

Variants covered:
1. subsets_backtrack    -- recursive backtracking
2. subsets_itertools    -- using itertools.combinations
3. subsets_binary_str   -- binary string approach

Run:
    python dynamic_programming/subset_generation_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.subset_generation import generate_subsets as reference


# ---------------------------------------------------------------------------
# Variant 1 — Backtracking
# ---------------------------------------------------------------------------

def subsets_backtrack(nums: list[int]) -> list[list[int]]:
    """
    Generate subsets using backtracking.

    >>> sorted([sorted(s) for s in subsets_backtrack([1, 2, 3])])
    [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
    >>> subsets_backtrack([])
    [[]]
    """
    result = []

    def backtrack(start: int, current: list[int]) -> None:
        result.append(current[:])
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()

    backtrack(0, [])
    return result


# ---------------------------------------------------------------------------
# Variant 2 — itertools.combinations
# ---------------------------------------------------------------------------

def subsets_itertools(nums: list[int]) -> list[list[int]]:
    """
    Generate subsets using itertools.combinations.

    >>> sorted([sorted(s) for s in subsets_itertools([1, 2, 3])])
    [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
    >>> subsets_itertools([])
    [[]]
    """
    result = []
    for r in range(len(nums) + 1):
        result.extend(list(c) for c in combinations(nums, r))
    return result


# ---------------------------------------------------------------------------
# Variant 3 — Binary string enumeration
# ---------------------------------------------------------------------------

def subsets_binary_str(nums: list[int]) -> list[list[int]]:
    """
    Generate subsets by iterating binary strings.

    >>> sorted([sorted(s) for s in subsets_binary_str([1, 2, 3])])
    [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
    >>> subsets_binary_str([])
    [[]]
    """
    n = len(nums)
    if n == 0:
        return [[]]
    result = []
    for i in range(1 << n):
        bits = format(i, f"0{n}b")
        result.append([nums[j] for j, b in enumerate(bits) if b == "1"])
    return result


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

def _canonical(subsets: list[list[int]]) -> list[tuple[int, ...]]:
    return sorted(tuple(sorted(s)) for s in subsets)


TEST_CASES = [
    [1, 2, 3],
    [],
    [1],
    [1, 2, 3, 4],
]

IMPLS = [
    ("reference", reference),
    ("backtrack", subsets_backtrack),
    ("itertools", subsets_itertools),
    ("binary_str", subsets_binary_str),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for nums in TEST_CASES:
        results = {name: _canonical(fn(list(nums))) for name, fn in IMPLS}
        expected = results["reference"]
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] nums={nums}  count={len(expected)}")

    REPS = 20_000
    bench_nums = list(range(10))
    print(f"\n=== Benchmark: {REPS} runs, n={len(bench_nums)} ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(bench_nums), number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
