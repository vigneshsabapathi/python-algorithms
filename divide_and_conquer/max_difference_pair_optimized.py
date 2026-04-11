#!/usr/bin/env python3
"""
Optimized and alternative implementations of Max Difference Pair.

Given an array, find max arr[j] - arr[i] where j > i (buy low, sell high).
The reference uses D&C: O(n log n).

Three variants:
  linear_scan     — single-pass tracking minimum: O(n) — optimal
  kadane_style    — transform to max-subarray of differences: O(n)
  brute_force     — O(n^2) baseline

Run:
    python divide_and_conquer/max_difference_pair_optimized.py
"""

from __future__ import annotations

import os
import random
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from divide_and_conquer.max_difference_pair import max_difference_pair as reference


# ---------------------------------------------------------------------------
# Variant 1 — Linear scan: O(n) — track running minimum
# ---------------------------------------------------------------------------

def linear_scan(arr: list[int | float]) -> tuple[int | float, int, int]:
    """
    Max difference in O(n) by tracking running minimum.

    >>> linear_scan([2, 3, 10, 6, 4, 8, 1])
    (8, 0, 2)
    >>> linear_scan([7, 9, 5, 6, 3, 2])
    (2, 0, 1)
    >>> linear_scan([1, 2, 3, 4, 5])
    (4, 0, 4)
    >>> linear_scan([5, 4, 3, 2, 1])
    (-1, 0, 1)
    """
    if len(arr) < 2:
        raise ValueError("Need at least 2 elements")

    min_idx = 0
    best_diff = arr[1] - arr[0]
    best_buy = 0
    best_sell = 1

    for j in range(1, len(arr)):
        diff = arr[j] - arr[min_idx]
        if diff > best_diff:
            best_diff = diff
            best_buy = min_idx
            best_sell = j
        if arr[j] < arr[min_idx]:
            min_idx = j

    return best_diff, best_buy, best_sell


# ---------------------------------------------------------------------------
# Variant 2 — Kadane-style on differences: O(n)
# ---------------------------------------------------------------------------

def kadane_style(arr: list[int | float]) -> tuple[int | float, int, int]:
    """
    Transform to max subarray: differences[i] = arr[i+1] - arr[i].
    Max contiguous sum of differences = max profit.

    >>> kadane_style([2, 3, 10, 6, 4, 8, 1])
    (8, 0, 2)
    >>> kadane_style([7, 9, 5, 6, 3, 2])
    (2, 0, 1)
    >>> kadane_style([1, 2, 3, 4, 5])
    (4, 0, 4)
    """
    if len(arr) < 2:
        raise ValueError("Need at least 2 elements")

    best_diff = arr[1] - arr[0]
    best_start = 0
    best_end = 1
    current_sum = arr[1] - arr[0]
    current_start = 0

    for i in range(2, len(arr)):
        diff = arr[i] - arr[i - 1]
        if current_sum + diff > diff:
            current_sum += diff
        else:
            current_sum = diff
            current_start = i - 1

        if current_sum > best_diff:
            best_diff = current_sum
            best_start = current_start
            best_end = i

    return best_diff, best_start, best_end


# ---------------------------------------------------------------------------
# Variant 3 — Brute force: O(n^2)
# ---------------------------------------------------------------------------

def brute_force(arr: list[int | float]) -> tuple[int | float, int, int]:
    """
    Brute force max difference — check all pairs.

    >>> brute_force([2, 3, 10, 6, 4, 8, 1])
    (8, 0, 2)
    >>> brute_force([5, 4, 3, 2, 1])
    (-1, 0, 1)
    """
    if len(arr) < 2:
        raise ValueError("Need at least 2 elements")

    best = arr[1] - arr[0]
    bi, bj = 0, 1
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[j] - arr[i] > best:
                best = arr[j] - arr[i]
                bi, bj = i, j
    return best, bi, bj


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    [2, 3, 10, 6, 4, 8, 1],
    [7, 9, 5, 6, 3, 2],
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
    [1, 5, 2, 10, 3],
]

IMPLS = [
    ("reference", reference),
    ("linear", linear_scan),
    ("kadane", kadane_style),
    ("brute", brute_force),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for arr in TEST_CASES:
        diffs = {}
        for name, fn in IMPLS:
            d, _, _ = fn(arr)
            diffs[name] = d
        ref = diffs["reference"]
        ok = all(v == ref for v in diffs.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] arr={str(arr):<25} diff={ref}  "
              + "  ".join(f"{nm}={v}" for nm, v in diffs.items()))

    sizes = [1000, 10000, 100000]
    REPS = 100

    for n in sizes:
        arr = [random.randint(-1000, 1000) for _ in range(n)]
        print(f"\n=== Benchmark n={n}, {REPS} runs ===")
        bench = [impl for impl in IMPLS if not (impl[0] == "brute" and n > 1000)]
        for name, fn in bench:
            t = timeit.timeit(lambda fn=fn: fn(arr), number=REPS) * 1000 / REPS
            print(f"  {name:<14} {t:>8.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
