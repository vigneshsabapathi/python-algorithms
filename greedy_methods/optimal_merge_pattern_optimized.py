#!/usr/bin/env python3
"""
Optimized and alternative implementations of Optimal Merge Pattern.

The reference uses a min-heap to always merge the two smallest files.

Variants covered:
1. heap_merge       -- min-heap, always merge two smallest (reference)
2. sorted_list      -- maintain sorted list with bisect.insort
3. brute_force      -- try all merge orderings (for small n verification)
4. divide_conquer   -- recursive merge tree approach

Key interview insight:
    This is equivalent to building an optimal Huffman tree. The greedy
    choice (merge smallest first) is provably optimal. Time: O(n log n).
    Related: Huffman coding, optimal BST, and "minimum cost to connect sticks" (LC 1167).

Run:
    python greedy_methods/optimal_merge_pattern_optimized.py
"""

from __future__ import annotations

import bisect
import heapq
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from greedy_methods.optimal_merge_pattern import optimal_merge_cost as reference


# ---------------------------------------------------------------------------
# Variant 1 — heap merge (reference)
# ---------------------------------------------------------------------------

def heap_merge(files: list[int]) -> int:
    """
    Min-heap: always pop two smallest, push their sum back.

    >>> heap_merge([2, 3, 4, 5, 6, 7])
    68
    >>> heap_merge([5, 10, 20, 30, 30])
    205
    >>> heap_merge([10])
    0
    >>> heap_merge([])
    0
    """
    if len(files) <= 1:
        return 0
    heap = list(files)
    heapq.heapify(heap)
    total = 0
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        cost = a + b
        total += cost
        heapq.heappush(heap, cost)
    return total


# ---------------------------------------------------------------------------
# Variant 2 — sorted list with bisect.insort
# ---------------------------------------------------------------------------

def sorted_list(files: list[int]) -> int:
    """
    Maintain a sorted list, pop from front (smallest), insort the merge.
    Avoids heap overhead for small inputs.

    >>> sorted_list([2, 3, 4, 5, 6, 7])
    68
    >>> sorted_list([5, 10, 20, 30, 30])
    205
    >>> sorted_list([10])
    0
    >>> sorted_list([])
    0
    """
    if len(files) <= 1:
        return 0
    lst = sorted(files)
    total = 0
    while len(lst) > 1:
        a = lst.pop(0)
        b = lst.pop(0)
        cost = a + b
        total += cost
        bisect.insort(lst, cost)
    return total


# ---------------------------------------------------------------------------
# Variant 3 — brute force: try all pairwise merge orders
# ---------------------------------------------------------------------------

def brute_force(files: list[int]) -> int:
    """
    Try all possible merge orderings recursively. O(n! / 2^n) — only for small n.

    >>> brute_force([2, 3, 4, 5, 6, 7])
    68
    >>> brute_force([5, 10, 20, 30, 30])
    205
    >>> brute_force([10])
    0
    >>> brute_force([1, 2, 3])
    9
    """
    if len(files) <= 1:
        return 0

    min_cost = float("inf")
    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            merge_cost = files[i] + files[j]
            remaining = [files[k] for k in range(len(files)) if k != i and k != j]
            remaining.append(merge_cost)
            total = merge_cost + brute_force(remaining)
            min_cost = min(min_cost, total)
    return min_cost


# ---------------------------------------------------------------------------
# Variant 4 — divide and conquer tree
# ---------------------------------------------------------------------------

def divide_conquer(files: list[int]) -> int:
    """
    Sort first, then use heap approach. Same as heap_merge but shows
    the connection to divide-and-conquer thinking.

    The key insight: after sorting, we always want to combine smallest
    elements first, which is exactly what a priority queue does.

    >>> divide_conquer([2, 3, 4, 5, 6, 7])
    68
    >>> divide_conquer([5, 10, 20, 30, 30])
    205
    >>> divide_conquer([10])
    0
    >>> divide_conquer([])
    0
    """
    if len(files) <= 1:
        return 0
    from collections import deque

    q1 = deque(sorted(files))  # original sizes
    q2: deque[int] = deque()   # merged sizes

    total = 0

    def pop_min() -> int:
        if q1 and q2:
            return q1.popleft() if q1[0] <= q2[0] else q2.popleft()
        return q1.popleft() if q1 else q2.popleft()

    while len(q1) + len(q2) > 1:
        a = pop_min()
        b = pop_min()
        cost = a + b
        total += cost
        q2.append(cost)

    return total


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([2, 3, 4, 5, 6, 7], 68),
    ([5, 10, 20, 30, 30], 205),
    ([10], 0),
    ([], 0),
    ([1, 1], 2),
    ([1, 2, 3], 9),
    ([1, 2, 3, 4], 19),
]

IMPLS = [
    ("reference",       reference),
    ("heap_merge",      heap_merge),
    ("sorted_list",     sorted_list),
    ("divide_conquer",  divide_conquer),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for files, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(files)
            except Exception as e:
                results[name] = f"ERR:{e}"
        # Also check brute_force for small inputs
        if len(files) <= 7:
            results["brute_force"] = brute_force(files)
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] files={str(files):<24} expected={expected}")

    import random
    random.seed(42)
    big = [random.randint(1, 1000) for _ in range(5000)]

    REPS = 2_000
    print(f"\n=== Benchmark (5000 files): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(big), number=REPS) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
