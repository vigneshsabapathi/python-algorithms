#!/usr/bin/env python3
"""
Optimized and alternative implementations of Peak Finding.

The reference finds peaks in 1D (binary search, O(log n)) and
2D (column-max + binary search, O(n log m)).

Three variants:
  iterative_1d    — iterative binary search (no recursion)
  linear_1d       — O(n) linear scan for all peaks
  greedy_2d       — greedy ascent for 2D peak (O(nm) worst, fast in practice)

Run:
    python divide_and_conquer/peak_optimized.py
"""

from __future__ import annotations

import os
import random
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from divide_and_conquer.peak import peak_1d as reference_1d
from divide_and_conquer.peak import peak_2d as reference_2d


# ---------------------------------------------------------------------------
# Variant 1 — Iterative binary search for 1D peak: O(log n)
# ---------------------------------------------------------------------------

def iterative_1d(arr: list[int | float]) -> int:
    """
    Find a 1D peak using iterative binary search.

    >>> arr = [1, 3, 20, 4, 1, 0]
    >>> i = iterative_1d(arr)
    >>> arr[i] >= (arr[i-1] if i > 0 else float('-inf'))
    True
    >>> arr[i] >= (arr[i+1] if i < len(arr)-1 else float('-inf'))
    True
    >>> iterative_1d([5, 4, 3, 2, 1])
    0
    >>> iterative_1d([1, 2, 3, 4, 5])
    4
    >>> iterative_1d([1])
    0
    """
    if not arr:
        raise ValueError("Array must not be empty")

    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        left_ok = mid == 0 or arr[mid] >= arr[mid - 1]
        right_ok = mid == len(arr) - 1 or arr[mid] >= arr[mid + 1]

        if left_ok and right_ok:
            return mid
        elif not left_ok:
            hi = mid - 1
        else:
            lo = mid + 1

    return lo


# ---------------------------------------------------------------------------
# Variant 2 — Linear scan finding ALL peaks: O(n)
# ---------------------------------------------------------------------------

def all_peaks_1d(arr: list[int | float]) -> list[int]:
    """
    Find ALL peak indices in a 1D array via linear scan.

    >>> all_peaks_1d([1, 3, 20, 4, 1, 0])
    [2]
    >>> all_peaks_1d([5, 4, 3, 2, 1])
    [0]
    >>> all_peaks_1d([1, 2, 3, 4, 5])
    [4]
    >>> all_peaks_1d([1, 3, 2, 4, 1])
    [1, 3]
    """
    if not arr:
        raise ValueError("Array must not be empty")

    peaks = []
    n = len(arr)
    for i in range(n):
        left_ok = i == 0 or arr[i] >= arr[i - 1]
        right_ok = i == n - 1 or arr[i] >= arr[i + 1]
        if left_ok and right_ok:
            peaks.append(i)
    return peaks


# ---------------------------------------------------------------------------
# Variant 3 — Greedy ascent for 2D peak
# ---------------------------------------------------------------------------

def greedy_2d(matrix: list[list[int | float]]) -> tuple[int, int]:
    """
    Find a 2D peak by greedy ascent — move to the largest neighbour.
    O(nm) worst case but usually much faster.

    >>> m = [[10, 8, 10, 10], [14, 13, 12, 11], [15, 9, 11, 21], [16, 17, 19, 20]]
    >>> r, c = greedy_2d(m)
    >>> val = m[r][c]
    >>> val >= (m[r-1][c] if r > 0 else float('-inf'))
    True
    >>> val >= (m[r+1][c] if r < len(m)-1 else float('-inf'))
    True
    >>> val >= (m[r][c-1] if c > 0 else float('-inf'))
    True
    >>> val >= (m[r][c+1] if c < len(m[0])-1 else float('-inf'))
    True
    """
    if not matrix or not matrix[0]:
        raise ValueError("Matrix must not be empty")

    rows, cols = len(matrix), len(matrix[0])
    r, c = rows // 2, cols // 2  # start from center

    while True:
        best_r, best_c = r, c
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if matrix[nr][nc] > matrix[best_r][best_c]:
                    best_r, best_c = nr, nc

        if (best_r, best_c) == (r, c):
            return r, c
        r, c = best_r, best_c


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

def _is_peak_1d(arr, i):
    left = i == 0 or arr[i] >= arr[i - 1]
    right = i == len(arr) - 1 or arr[i] >= arr[i + 1]
    return left and right


def _is_peak_2d(m, r, c):
    v = m[r][c]
    rows, cols = len(m), len(m[0])
    return (
        (r == 0 or v >= m[r-1][c]) and
        (r == rows-1 or v >= m[r+1][c]) and
        (c == 0 or v >= m[r][c-1]) and
        (c == cols-1 or v >= m[r][c+1])
    )


def run_all() -> None:
    # 1D tests
    test_1d = [
        [1, 3, 20, 4, 1, 0],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [1],
        [1, 3, 2, 4, 1],
    ]

    print("\n=== 1D Peak Correctness ===")
    for arr in test_1d:
        ref_i = reference_1d(arr)
        iter_i = iterative_1d(arr)
        all_p = all_peaks_1d(arr)
        ok = _is_peak_1d(arr, ref_i) and _is_peak_1d(arr, iter_i) and all(
            _is_peak_1d(arr, p) for p in all_p
        )
        print(f"  [{'OK' if ok else 'FAIL'}] arr={str(arr):<25} ref={ref_i} iter={iter_i} all={all_p}")

    # 2D tests
    test_2d = [
        [[10, 8, 10, 10], [14, 13, 12, 11], [15, 9, 11, 21], [16, 17, 19, 20]],
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    ]

    print("\n=== 2D Peak Correctness ===")
    for m in test_2d:
        r1, c1 = reference_2d(m)
        r2, c2 = greedy_2d(m)
        ok = _is_peak_2d(m, r1, c1) and _is_peak_2d(m, r2, c2)
        print(f"  [{'OK' if ok else 'FAIL'}] {len(m)}x{len(m[0])} ref=({r1},{c1})={m[r1][c1]} greedy=({r2},{c2})={m[r2][c2]}")

    # Benchmark 1D
    sizes = [10000, 100000, 1000000]
    REPS = 1000

    for n in sizes:
        arr = [random.randint(1, n) for _ in range(n)]
        print(f"\n=== 1D Benchmark n={n}, {REPS} runs ===")
        for name, fn in [("reference", reference_1d), ("iterative", iterative_1d)]:
            t = timeit.timeit(lambda fn=fn: fn(arr), number=REPS) * 1000 / REPS
            print(f"  {name:<14} {t:>8.4f} ms")

    # Benchmark 2D
    for n in [50, 100, 200]:
        m = [[random.randint(1, 10000) for _ in range(n)] for _ in range(n)]
        REPS2 = 200
        print(f"\n=== 2D Benchmark {n}x{n}, {REPS2} runs ===")
        for name, fn in [("reference", reference_2d), ("greedy", greedy_2d)]:
            t = timeit.timeit(lambda fn=fn: fn(m), number=REPS2) * 1000 / REPS2
            print(f"  {name:<14} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
