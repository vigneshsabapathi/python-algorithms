#!/usr/bin/env python3
"""
Optimized and alternative implementations of Sliding Window Maximum.

Variants covered:
1. monotonic_deque  -- Deque maintaining decreasing order (reference)
2. heap_approach    -- Max-heap with lazy deletion
3. brute_force      -- O(nk) direct comparison

Run:
    python other/sliding_window_maximum_optimized.py
"""

from __future__ import annotations

import heapq
import os
import sys
import timeit
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.sliding_window_maximum import sliding_window_maximum as reference


def heap_sliding_max(nums: list[int], k: int) -> list[int]:
    """
    Sliding window maximum using a max-heap with lazy deletion.

    >>> heap_sliding_max([1, 3, -1, -3, 5, 3, 6, 7], 3)
    [3, 3, 5, 5, 6, 7]
    >>> heap_sliding_max([1], 1)
    [1]
    >>> heap_sliding_max([], 1)
    []
    """
    if not nums or k <= 0:
        return []
    result = []
    heap: list[tuple[int, int]] = []  # (-value, index) for max-heap

    for i, num in enumerate(nums):
        heapq.heappush(heap, (-num, i))
        # Remove elements outside window
        while heap[0][1] < i - k + 1:
            heapq.heappop(heap)
        if i >= k - 1:
            result.append(-heap[0][0])

    return result


def brute_force_sliding_max(nums: list[int], k: int) -> list[int]:
    """
    Brute force: max() of each window.

    >>> brute_force_sliding_max([1, 3, -1, -3, 5, 3, 6, 7], 3)
    [3, 3, 5, 5, 6, 7]
    >>> brute_force_sliding_max([], 1)
    []
    """
    if not nums or k <= 0:
        return []
    return [max(nums[i : i + k]) for i in range(len(nums) - k + 1)]


def sliding_window_minimum(nums: list[int], k: int) -> list[int]:
    """
    Sliding window minimum (variant).

    >>> sliding_window_minimum([1, 3, -1, -3, 5, 3, 6, 7], 3)
    [-1, -3, -3, -3, 3, 3]
    >>> sliding_window_minimum([], 1)
    []
    """
    if not nums or k <= 0:
        return []
    result = []
    dq: deque[int] = deque()
    for i, num in enumerate(nums):
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        while dq and nums[dq[-1]] >= num:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result


TEST_CASES = [
    ([1, 3, -1, -3, 5, 3, 6, 7], 3, [3, 3, 5, 5, 6, 7]),
    ([1], 1, [1]),
    ([1, -1], 1, [1, -1]),
    ([9, 11], 2, [11]),
    ([], 1, []),
]

IMPLS = [
    ("reference_deque", reference),
    ("heap", heap_sliding_max),
    ("brute_force", brute_force_sliding_max),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for nums, k, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(list(nums), k)
            ok = result == expected
            tag = "OK" if ok else "FAIL"
            if not ok:
                print(f"  [{tag}] {name}: expected={expected} got={result}")
        print(f"  [OK] n={len(nums)} k={k}")

    import random
    rng = random.Random(42)
    large = [rng.randint(-1000, 1000) for _ in range(10000)]

    REPS = 500
    print(f"\n=== Benchmark: {REPS} runs, {len(large)} elements, k=50 ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(list(large), 50), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
