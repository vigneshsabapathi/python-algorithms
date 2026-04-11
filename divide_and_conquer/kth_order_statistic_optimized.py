#!/usr/bin/env python3
"""
Optimized and alternative implementations of Kth Order Statistic.

The reference uses randomised quickselect: O(n) average, O(n^2) worst.

Three variants:
  median_of_medians — deterministic O(n) worst-case pivot selection
  heap_select       — min-heap approach: O(n + k log n)
  sort_select       — sort then index: O(n log n) but simple

Run:
    python divide_and_conquer/kth_order_statistic_optimized.py
"""

from __future__ import annotations

import heapq
import os
import random
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from divide_and_conquer.kth_order_statistic import kth_order_statistic as reference
from divide_and_conquer.kth_order_statistic import median_of_medians


# ---------------------------------------------------------------------------
# Variant 1 — Heap select: O(n + k log n)
# ---------------------------------------------------------------------------

def heap_select(arr: list[int], k: int) -> int:
    """
    Find kth smallest using a min-heap.
    O(n) to heapify + O(k log n) to extract k elements.

    >>> heap_select([3, 2, 1, 5, 4], 1)
    1
    >>> heap_select([3, 2, 1, 5, 4], 3)
    3
    >>> heap_select([3, 2, 1, 5, 4], 5)
    5
    >>> heap_select([7, 10, 4, 3, 20, 15], 3)
    7
    """
    if k < 1 or k > len(arr):
        raise ValueError(f"k={k} out of range")
    h = arr[:]
    heapq.heapify(h)
    for _ in range(k - 1):
        heapq.heappop(h)
    return heapq.heappop(h)


# ---------------------------------------------------------------------------
# Variant 2 — Sort and index: O(n log n)
# ---------------------------------------------------------------------------

def sort_select(arr: list[int], k: int) -> int:
    """
    Find kth smallest by sorting — simple but O(n log n).

    >>> sort_select([3, 2, 1, 5, 4], 1)
    1
    >>> sort_select([3, 2, 1, 5, 4], 3)
    3
    >>> sort_select([7, 10, 4, 3, 20, 15], 4)
    10
    """
    if k < 1 or k > len(arr):
        raise ValueError(f"k={k} out of range")
    return sorted(arr)[k - 1]


# ---------------------------------------------------------------------------
# Variant 3 — Max-heap for kth smallest: O(n log k) space-efficient
# ---------------------------------------------------------------------------

def maxheap_select(arr: list[int], k: int) -> int:
    """
    Find kth smallest using a max-heap of size k.
    Maintain a heap of k largest-seen; top is the kth smallest.
    O(n log k) time, O(k) space.

    >>> maxheap_select([3, 2, 1, 5, 4], 1)
    1
    >>> maxheap_select([3, 2, 1, 5, 4], 3)
    3
    >>> maxheap_select([3, 2, 1, 5, 4], 5)
    5
    >>> maxheap_select([7, 10, 4, 3, 20, 15], 3)
    7
    """
    if k < 1 or k > len(arr):
        raise ValueError(f"k={k} out of range")
    # Python heapq is min-heap; negate values for max-heap behavior
    heap: list[int] = []
    for val in arr:
        if len(heap) < k:
            heapq.heappush(heap, -val)
        elif -val > heap[0]:
            heapq.heapreplace(heap, -val)
    return -heap[0]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([3, 2, 1, 5, 4], 1, 1),
    ([3, 2, 1, 5, 4], 3, 3),
    ([3, 2, 1, 5, 4], 5, 5),
    ([7, 10, 4, 3, 20, 15], 3, 7),
    ([7, 10, 4, 3, 20, 15], 4, 10),
    ([1], 1, 1),
]

IMPLS = [
    ("reference", reference),
    ("mom", median_of_medians),
    ("heap", heap_select),
    ("sort", sort_select),
    ("maxheap", maxheap_select),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for arr, k, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            results[name] = fn(arr, k)
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] k={k} expected={expected}  "
              + "  ".join(f"{nm}={v}" for nm, v in results.items()))

    # Random validation
    for _ in range(100):
        arr = [random.randint(1, 1000) for _ in range(100)]
        k = random.randint(1, 100)
        expected = sorted(arr)[k - 1]
        for name, fn in IMPLS:
            if fn(arr, k) != expected:
                print(f"  [FAIL] random test: {name} got {fn(arr, k)}, expected {expected}")
                break
    else:
        print(f"  [OK] 100 random tests all match")

    sizes = [1000, 10000, 100000]
    REPS = 50

    for n in sizes:
        arr = [random.randint(1, n) for _ in range(n)]
        k = n // 2  # median
        print(f"\n=== Benchmark n={n}, k=n/2, {REPS} runs ===")
        for name, fn in IMPLS:
            t = timeit.timeit(lambda fn=fn: fn(arr, k), number=REPS) * 1000 / REPS
            print(f"  {name:<14} {t:>8.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
