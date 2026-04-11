#!/usr/bin/env python3
"""
Optimized and alternative implementations of Median of Matrix.

The reference flattens and sorts: O(m*n*log(m*n)). Simple but not optimal
for row-sorted matrices.

Three alternatives:
  binary_search_median  -- For row-sorted matrices, binary search on value range O(32*m*log(n))
  quickselect           -- O(m*n) average case using quickselect on flattened array
  heapq_merge           -- Merge sorted rows with heapq, pick middle element

Run:
    python matrix/median_matrix_optimized.py
"""

from __future__ import annotations

import heapq
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matrix.median_matrix import median as reference


# ---------------------------------------------------------------------------
# Variant 1 -- Binary search on value range (for row-sorted matrices)
# ---------------------------------------------------------------------------

def median_binary_search(matrix: list[list[int]]) -> int:
    """
    For row-sorted matrices: binary search on the value range.
    Count elements <= mid to determine if mid is too high or low.

    >>> median_binary_search([[1, 3, 5], [2, 6, 9], [3, 6, 9]])
    5
    >>> median_binary_search([[1, 2, 3], [4, 5, 6]])
    3
    >>> median_binary_search([[1]])
    1
    """
    import bisect

    rows = len(matrix)
    total = sum(len(row) for row in matrix)
    target = (total - 1) // 2  # match reference lower-median convention

    lo = min(row[0] for row in matrix if row)
    hi = max(row[-1] for row in matrix if row)

    while lo < hi:
        mid = (lo + hi) // 2
        # Count elements <= mid across all rows
        count = sum(bisect.bisect_right(row, mid) for row in matrix)
        if count <= target:
            lo = mid + 1
        else:
            hi = mid

    return lo


# ---------------------------------------------------------------------------
# Variant 2 -- Quickselect on flattened array (O(m*n) average)
# ---------------------------------------------------------------------------

def median_quickselect(matrix: list[list[int]]) -> int:
    """
    Flatten and use quickselect to find median in O(m*n) average time.

    >>> median_quickselect([[1, 3, 5], [2, 6, 9], [3, 6, 9]])
    5
    >>> median_quickselect([[1, 2, 3], [4, 5, 6]])
    3
    >>> median_quickselect([[1]])
    1
    """
    flat = [num for row in matrix for num in row]
    k = (len(flat) - 1) // 2

    def quickselect(arr: list[int], k: int) -> int:
        if len(arr) == 1:
            return arr[0]
        pivot = arr[len(arr) // 2]
        lows = [x for x in arr if x < pivot]
        highs = [x for x in arr if x > pivot]
        pivots = [x for x in arr if x == pivot]
        if k < len(lows):
            return quickselect(lows, k)
        elif k < len(lows) + len(pivots):
            return pivots[0]
        else:
            return quickselect(highs, k - len(lows) - len(pivots))

    return quickselect(flat, k)


# ---------------------------------------------------------------------------
# Variant 3 -- Heap merge of sorted rows
# ---------------------------------------------------------------------------

def median_heap_merge(matrix: list[list[int]]) -> int:
    """
    Merge sorted rows using heapq.merge and pick the median element.
    Only processes half the elements.

    >>> median_heap_merge([[1, 3, 5], [2, 6, 9], [3, 6, 9]])
    5
    >>> median_heap_merge([[1, 2, 3], [4, 5, 6]])
    3
    >>> median_heap_merge([[1]])
    1
    """
    total = sum(len(row) for row in matrix)
    target = (total - 1) // 2

    merged = heapq.merge(*matrix)
    for i, val in enumerate(merged):
        if i == target:
            return val
    return 0  # Should not reach here


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    import random
    random.seed(42)
    matrix = [sorted(random.randint(1, 10000) for _ in range(500)) for _ in range(500)]

    number = 50
    print(f"Benchmark ({number} runs on 500x500 row-sorted matrix):\n")

    funcs = [
        ("reference (flatten+sort)", lambda: reference(matrix)),
        ("binary_search (value range)", lambda: median_binary_search(matrix)),
        ("quickselect (O(n) avg)", lambda: median_quickselect(matrix)),
        ("heap_merge (sorted rows)", lambda: median_heap_merge(matrix)),
    ]

    for name, func in funcs:
        t = timeit.timeit(func, number=number)
        print(f"  {name:35s} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
