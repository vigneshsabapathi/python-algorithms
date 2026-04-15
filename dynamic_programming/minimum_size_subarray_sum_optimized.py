#!/usr/bin/env python3
"""
Optimized and alternative implementations of Minimum Size Subarray Sum.

Variants covered:
1. min_subarray_prefix_bisect  -- prefix sum + binary search O(n log n)
2. min_subarray_deque          -- deque-based sliding window
3. min_subarray_brute          -- O(n^2) brute force (baseline)

Run:
    python dynamic_programming/minimum_size_subarray_sum_optimized.py
"""

from __future__ import annotations

import bisect
import sys
import os
import timeit
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.minimum_size_subarray_sum import minimum_size_subarray_sum as reference


# ---------------------------------------------------------------------------
# Variant 1 — Prefix sum + binary search
# ---------------------------------------------------------------------------

def min_subarray_prefix_bisect(target: int, nums: list[int]) -> int:
    """
    Minimum size subarray sum using prefix sums and binary search.

    For each prefix[i], find smallest j where prefix[j] - prefix[i] >= target.

    >>> min_subarray_prefix_bisect(7, [2, 3, 1, 2, 4, 3])
    2
    >>> min_subarray_prefix_bisect(4, [1, 4, 4])
    1
    >>> min_subarray_prefix_bisect(11, [1, 1, 1, 1, 1, 1, 1, 1])
    0
    >>> min_subarray_prefix_bisect(1, [1])
    1
    """
    if not nums:
        return 0
    n = len(nums)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]

    min_len = n + 1
    for i in range(n):
        needed = prefix[i] + target
        j = bisect.bisect_left(prefix, needed, i + 1, n + 1)
        if j <= n:
            min_len = min(min_len, j - i)

    return 0 if min_len > n else min_len


# ---------------------------------------------------------------------------
# Variant 2 — Deque-based
# ---------------------------------------------------------------------------

def min_subarray_deque(target: int, nums: list[int]) -> int:
    """
    Minimum size subarray sum using a deque to maintain prefix indices.

    >>> min_subarray_deque(7, [2, 3, 1, 2, 4, 3])
    2
    >>> min_subarray_deque(4, [1, 4, 4])
    1
    >>> min_subarray_deque(11, [1, 1, 1, 1, 1, 1, 1, 1])
    0
    >>> min_subarray_deque(1, [1])
    1
    """
    if not nums:
        return 0
    n = len(nums)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]

    min_len = n + 1
    dq = deque()
    for i in range(n + 1):
        while dq and prefix[i] - prefix[dq[0]] >= target:
            min_len = min(min_len, i - dq.popleft())
        dq.append(i)

    return 0 if min_len > n else min_len


# ---------------------------------------------------------------------------
# Variant 3 — Brute force O(n^2) baseline
# ---------------------------------------------------------------------------

def min_subarray_brute(target: int, nums: list[int]) -> int:
    """
    Brute force O(n^2) — check all subarrays.

    >>> min_subarray_brute(7, [2, 3, 1, 2, 4, 3])
    2
    >>> min_subarray_brute(4, [1, 4, 4])
    1
    >>> min_subarray_brute(11, [1, 1, 1, 1, 1, 1, 1, 1])
    0
    >>> min_subarray_brute(1, [1])
    1
    """
    if not nums:
        return 0
    n = len(nums)
    min_len = n + 1
    for i in range(n):
        s = 0
        for j in range(i, n):
            s += nums[j]
            if s >= target:
                min_len = min(min_len, j - i + 1)
                break
    return 0 if min_len > n else min_len


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (7, [2, 3, 1, 2, 4, 3], 2),
    (4, [1, 4, 4], 1),
    (11, [1, 1, 1, 1, 1, 1, 1, 1], 0),
    (15, [5, 1, 3, 5, 10, 7, 4, 9, 2, 8], 2),
    (1, [1], 1),
]

IMPLS = [
    ("reference", reference),
    ("prefix_bisect", min_subarray_prefix_bisect),
    ("deque", min_subarray_deque),
    ("brute", min_subarray_brute),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for target, nums, expected in TEST_CASES:
        results = {name: fn(target, list(nums)) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] target={target}, len={len(nums)}  expected={expected}  " +
              "  ".join(f"{n}={v}" for n, v in results.items()))

    REPS = 20_000
    bench_nums = list(range(1, 51))
    bench_target = 50
    print(f"\n=== Benchmark: {REPS} runs, len={len(bench_nums)}, target={bench_target} ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(bench_target, bench_nums), number=REPS) * 1000 / REPS
        print(f"  {name:<16} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
