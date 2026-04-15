#!/usr/bin/env python3
"""
Optimized and alternative implementations of Minimum Partition.

Variants covered:
1. min_partition_bitset     -- bitset DP using Python int as bitmask
2. min_partition_meet_mid   -- meet-in-the-middle for smaller n
3. min_partition_recursive  -- top-down memoized recursion

Run:
    python dynamic_programming/minimum_partition_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.minimum_partition import minimum_partition as reference


# ---------------------------------------------------------------------------
# Variant 1 — Bitset DP (Python int as bitmask of reachable sums)
# ---------------------------------------------------------------------------

def min_partition_bitset(nums: list[int]) -> int:
    """
    Minimum partition using a single integer as a bitset of reachable sums.

    Each bit i in the integer means "sum i is reachable."
    Shifting by num and OR-ing adds that element to all existing subsets.

    >>> min_partition_bitset([1, 6, 11, 5])
    1
    >>> min_partition_bitset([1, 5, 11, 5])
    0
    >>> min_partition_bitset([3, 1, 4, 2, 2, 1])
    1
    >>> min_partition_bitset([1])
    1
    >>> min_partition_bitset([])
    0
    """
    if not nums:
        return 0
    total = sum(nums)
    bits = 1  # bit 0 is set (sum 0 is reachable)
    for num in nums:
        bits |= bits << num
    half = total // 2
    for j in range(half, -1, -1):
        if bits & (1 << j):
            return total - 2 * j
    return total


# ---------------------------------------------------------------------------
# Variant 2 — Meet in the middle
# ---------------------------------------------------------------------------

def min_partition_meet_mid(nums: list[int]) -> int:
    """
    Meet-in-the-middle approach: enumerate all subset sums of each half,
    then find the combination closest to total/2.

    O(2^(n/2)) — feasible for n <= ~40.

    >>> min_partition_meet_mid([1, 6, 11, 5])
    1
    >>> min_partition_meet_mid([1, 5, 11, 5])
    0
    >>> min_partition_meet_mid([3, 1, 4, 2, 2, 1])
    1
    >>> min_partition_meet_mid([1])
    1
    >>> min_partition_meet_mid([])
    0
    """
    if not nums:
        return 0
    total = sum(nums)
    half = total / 2

    def all_subset_sums(arr: list[int]) -> set[int]:
        sums = {0}
        for x in arr:
            sums = sums | {s + x for s in sums}
        return sums

    n = len(nums)
    mid = n // 2
    left_sums = sorted(all_subset_sums(nums[:mid]))
    right_sums = sorted(all_subset_sums(nums[mid:]))

    # Two-pointer to find pair closest to half
    best = float("inf")
    i, j = 0, len(right_sums) - 1
    while i < len(left_sums) and j >= 0:
        s = left_sums[i] + right_sums[j]
        best = min(best, abs(total - 2 * s))
        if s < half:
            i += 1
        elif s > half:
            j -= 1
        else:
            return 0
    return best


# ---------------------------------------------------------------------------
# Variant 3 — Top-down memoized recursion
# ---------------------------------------------------------------------------

def min_partition_recursive(nums: list[int]) -> int:
    """
    Minimum partition using memoized recursion.

    >>> min_partition_recursive([1, 6, 11, 5])
    1
    >>> min_partition_recursive([1, 5, 11, 5])
    0
    >>> min_partition_recursive([3, 1, 4, 2, 2, 1])
    1
    >>> min_partition_recursive([1])
    1
    >>> min_partition_recursive([])
    0
    """
    if not nums:
        return 0
    total = sum(nums)
    half = total // 2
    n = len(nums)
    memo: dict[tuple[int, int], bool] = {}

    def can_reach(idx: int, target: int) -> bool:
        if target == 0:
            return True
        if idx >= n or target < 0:
            return False
        key = (idx, target)
        if key in memo:
            return memo[key]
        result = can_reach(idx + 1, target - nums[idx]) or can_reach(idx + 1, target)
        memo[key] = result
        return result

    for j in range(half, -1, -1):
        if can_reach(0, j):
            return total - 2 * j
    return total


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([1, 6, 11, 5], 1),
    ([1, 5, 11, 5], 0),
    ([3, 1, 4, 2, 2, 1], 1),
    ([1], 1),
    ([], 0),
    ([10, 20, 15, 5, 25], 5),
]

IMPLS = [
    ("reference", reference),
    ("bitset", min_partition_bitset),
    ("meet_mid", min_partition_meet_mid),
    ("recursive", min_partition_recursive),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for nums, expected in TEST_CASES:
        results = {name: fn(list(nums)) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] nums={nums!r}  expected={expected}  " +
              "  ".join(f"{n}={v}" for n, v in results.items()))

    REPS = 10_000
    bench_input = [3, 1, 4, 2, 2, 1, 5, 7, 8, 3, 6, 2]
    print(f"\n=== Benchmark: {REPS} runs, len={len(bench_input)} ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(bench_input), number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
