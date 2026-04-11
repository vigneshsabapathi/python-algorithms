#!/usr/bin/env python3
"""
Optimized and alternative implementations of Maximum Subarray.

The reference uses D&C: O(n log n).

Three variants:
  kadane          — classic Kadane's algorithm: O(n)
  prefix_sum      — prefix sum approach: O(n)
  dp_tracking     — dynamic programming with full subarray tracking: O(n)

Run:
    python divide_and_conquer/max_subarray_optimized.py
"""

from __future__ import annotations

import os
import random
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from divide_and_conquer.max_subarray import max_subarray as reference


# ---------------------------------------------------------------------------
# Variant 1 — Kadane's Algorithm: O(n) — the optimal solution
# ---------------------------------------------------------------------------

def kadane(arr: list[int | float]) -> tuple[int, int, int | float]:
    """
    Kadane's algorithm — O(n) maximum subarray.
    Returns (left, right, max_sum).

    >>> kadane([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    (3, 6, 6)
    >>> kadane([1, 2, 3, 4, 5])
    (0, 4, 15)
    >>> kadane([-1, -2, -3])
    (0, 0, -1)
    >>> kadane([5])
    (0, 0, 5)
    """
    if not arr:
        raise ValueError("Array must not be empty")

    best_sum = arr[0]
    best_start = best_end = 0
    current_sum = arr[0]
    current_start = 0

    for i in range(1, len(arr)):
        if current_sum + arr[i] > arr[i]:
            current_sum += arr[i]
        else:
            current_sum = arr[i]
            current_start = i

        if current_sum > best_sum:
            best_sum = current_sum
            best_start = current_start
            best_end = i

    return best_start, best_end, best_sum


# ---------------------------------------------------------------------------
# Variant 2 — Prefix sum approach: O(n)
# ---------------------------------------------------------------------------

def prefix_sum(arr: list[int | float]) -> tuple[int, int, int | float]:
    """
    Max subarray via prefix sums: sum(i..j) = prefix[j+1] - prefix[i].
    Track minimum prefix sum seen so far.

    >>> prefix_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    (3, 6, 6)
    >>> prefix_sum([1, 2, 3, 4, 5])
    (0, 4, 15)
    >>> prefix_sum([-1, -2, -3])
    (0, 0, -1)
    """
    if not arr:
        raise ValueError("Array must not be empty")

    # Build prefix sums
    n = len(arr)
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + arr[i]

    best_sum = arr[0]
    best_start = best_end = 0
    min_pre = 0
    min_pre_idx = 0

    for j in range(1, n + 1):
        if pre[j] - min_pre > best_sum:
            best_sum = pre[j] - min_pre
            best_start = min_pre_idx
            best_end = j - 1
        if pre[j] < min_pre:
            min_pre = pre[j]
            min_pre_idx = j

    return best_start, best_end, best_sum


# ---------------------------------------------------------------------------
# Variant 3 — DP with explicit tracking: O(n)
# ---------------------------------------------------------------------------

def dp_tracking(arr: list[int | float]) -> tuple[int, int, int | float]:
    """
    DP approach: dp[i] = max subarray ending at i.
    dp[i] = max(arr[i], dp[i-1] + arr[i]).

    >>> dp_tracking([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    (3, 6, 6)
    >>> dp_tracking([1, 2, 3, 4, 5])
    (0, 4, 15)
    >>> dp_tracking([-1, -2, -3])
    (0, 0, -1)
    """
    if not arr:
        raise ValueError("Array must not be empty")

    n = len(arr)
    dp = [0] * n
    dp[0] = arr[0]
    start = [0] * n  # start index for subarray ending at i

    best_sum = dp[0]
    best_start = best_end = 0

    for i in range(1, n):
        if dp[i - 1] + arr[i] > arr[i]:
            dp[i] = dp[i - 1] + arr[i]
            start[i] = start[i - 1]
        else:
            dp[i] = arr[i]
            start[i] = i

        if dp[i] > best_sum:
            best_sum = dp[i]
            best_start = start[i]
            best_end = i

    return best_start, best_end, best_sum


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    [-2, 1, -3, 4, -1, 2, 1, -5, 4],
    [1, 2, 3, 4, 5],
    [-1, -2, -3],
    [5],
    [-2, -1],
    [2, -1, 2, 3, 4, -5],
]

IMPLS = [
    ("reference", reference),
    ("kadane", kadane),
    ("prefix_sum", prefix_sum),
    ("dp_tracking", dp_tracking),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for arr in TEST_CASES:
        sums = {}
        for name, fn in IMPLS:
            _, _, s = fn(arr)
            sums[name] = s
        ref = sums["reference"]
        ok = all(v == ref for v in sums.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] arr={str(arr):<35} sum={ref}  "
              + "  ".join(f"{nm}={v}" for nm, v in sums.items()))

    sizes = [1000, 10000, 100000]
    REPS = 100

    for n in sizes:
        arr = [random.randint(-100, 100) for _ in range(n)]
        print(f"\n=== Benchmark n={n}, {REPS} runs ===")
        for name, fn in IMPLS:
            t = timeit.timeit(lambda fn=fn: fn(arr), number=REPS) * 1000 / REPS
            print(f"  {name:<14} {t:>8.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
