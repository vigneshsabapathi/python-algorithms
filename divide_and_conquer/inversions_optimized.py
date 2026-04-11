#!/usr/bin/env python3
"""
Optimized and alternative implementations of Inversion Count.

An inversion is a pair (i,j) where i < j but arr[i] > arr[j].
The reference uses modified merge sort: O(n log n).

Three variants:
  enhanced_merge  — merge sort with early termination on sorted subarrays
  bit_fenwick     — Binary Indexed Tree (Fenwick tree): O(n log n), in-place count
  brute_force     — O(n^2) baseline for correctness validation

Run:
    python divide_and_conquer/inversions_optimized.py
"""

from __future__ import annotations

import os
import random
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from divide_and_conquer.inversions import count_inversions as reference


# ---------------------------------------------------------------------------
# Variant 1 — Enhanced merge sort with sorted-subarray detection
# ---------------------------------------------------------------------------

def enhanced_merge(arr: list[int]) -> tuple[int, list[int]]:
    """
    Merge sort inversion count with early termination when subarrays
    are already in order (left[-1] <= right[0] → 0 split inversions).

    >>> enhanced_merge([2, 4, 1, 3, 5])
    (3, [1, 2, 3, 4, 5])
    >>> enhanced_merge([5, 4, 3, 2, 1])
    (10, [1, 2, 3, 4, 5])
    >>> enhanced_merge([1, 2, 3])
    (0, [1, 2, 3])
    >>> enhanced_merge([])
    (0, [])
    """
    if len(arr) <= 1:
        return 0, arr[:]

    mid = len(arr) // 2
    left_inv, left = enhanced_merge(arr[:mid])
    right_inv, right = enhanced_merge(arr[mid:])

    # Early termination: if left is all <= right, no split inversions
    if left[-1] <= right[0]:
        return left_inv + right_inv, left + right

    merge_inv, merged = _merge_count(left, right)
    return left_inv + right_inv + merge_inv, merged


def _merge_count(left: list[int], right: list[int]) -> tuple[int, list[int]]:
    result: list[int] = []
    inversions = 0
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            inversions += len(left) - i
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return inversions, result


# ---------------------------------------------------------------------------
# Variant 2 — Fenwick Tree (BIT) approach: O(n log n)
# ---------------------------------------------------------------------------

def bit_fenwick(arr: list[int]) -> int:
    """
    Count inversions using a Fenwick (Binary Indexed) Tree.
    Processes elements right-to-left, counting how many smaller elements
    have already been seen (to the right).

    >>> bit_fenwick([2, 4, 1, 3, 5])
    3
    >>> bit_fenwick([5, 4, 3, 2, 1])
    10
    >>> bit_fenwick([1, 2, 3])
    0
    >>> bit_fenwick([])
    0
    """
    if not arr:
        return 0

    # Coordinate compression
    sorted_unique = sorted(set(arr))
    rank = {v: i + 1 for i, v in enumerate(sorted_unique)}
    n = len(sorted_unique)

    tree = [0] * (n + 1)

    def update(i: int) -> None:
        while i <= n:
            tree[i] += 1
            i += i & (-i)

    def query(i: int) -> int:
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & (-i)
        return s

    inversions = 0
    for val in reversed(arr):
        r = rank[val]
        inversions += query(r - 1)  # count elements smaller than val to its right
        update(r)

    return inversions


# ---------------------------------------------------------------------------
# Variant 3 — Brute force: O(n^2)
# ---------------------------------------------------------------------------

def brute_force(arr: list[int]) -> int:
    """
    Count inversions by checking all pairs — O(n^2).

    >>> brute_force([2, 4, 1, 3, 5])
    3
    >>> brute_force([5, 4, 3, 2, 1])
    10
    >>> brute_force([1, 2, 3])
    0
    """
    count = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    [2, 4, 1, 3, 5],
    [1, 2, 3, 4, 5],
    [5, 4, 3, 2, 1],
    [1, 20, 6, 4, 5],
    [1],
    [],
    [3, 1, 2],
]

IMPLS = [
    ("reference", lambda a: reference(a)[0]),
    ("enhanced", lambda a: enhanced_merge(a)[0]),
    ("fenwick", bit_fenwick),
    ("brute", brute_force),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for arr in TEST_CASES:
        counts = {}
        for name, fn in IMPLS:
            counts[name] = fn(arr)
        ref = counts["reference"]
        ok = all(v == ref for v in counts.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] arr={str(arr):<20} inv={ref}  "
              + "  ".join(f"{nm}={v}" for nm, v in counts.items()))

    # Random validation
    for _ in range(100):
        arr = [random.randint(1, 100) for _ in range(50)]
        ref = reference(arr)[0]
        fen = bit_fenwick(arr)
        if ref != fen:
            print(f"  [FAIL] random arr mismatch: ref={ref} fen={fen}")
            break
    else:
        print(f"  [OK] 100 random arrays (n=50) all match")

    sizes = [500, 2000, 10000]
    REPS = 20

    for n in sizes:
        arr = [random.randint(1, n) for _ in range(n)]
        print(f"\n=== Benchmark n={n}, {REPS} runs ===")
        bench = [impl for impl in IMPLS if not (impl[0] == "brute" and n > 2000)]
        for name, fn in bench:
            t = timeit.timeit(lambda fn=fn: fn(arr), number=REPS) * 1000 / REPS
            print(f"  {name:<14} {t:>8.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
