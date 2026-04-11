#!/usr/bin/env python3
"""
Optimized and alternative implementations of Smallest Range (LC 632).

The reference uses a min-heap with one pointer per list, tracking current max.

Variants covered:
1. heap_track_max   -- min-heap + max tracking (reference)
2. merge_sort_style -- merge all lists, slide window with k-list coverage
3. brute_force      -- check all pairs of elements (for verification)
4. sorted_events    -- event-based with sorted merge

Key interview insight:
    This is LC 632 (Hard). The heap approach is O(n*k * log k) where n = max list
    length and k = number of lists. The sliding window approach after merging
    is O(N log N) where N = total elements. Both are valid interview answers.

Run:
    python greedy_methods/smallest_range_optimized.py
"""

from __future__ import annotations

import heapq
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from greedy_methods.smallest_range import smallest_range as reference


# ---------------------------------------------------------------------------
# Variant 1 — heap with max tracking (reference)
# ---------------------------------------------------------------------------

def heap_track_max(nums: list[list[int]]) -> list[int]:
    """
    Min-heap of (value, list_idx, elem_idx). Track running max.
    Advance the minimum each step.

    >>> heap_track_max([[4,10,15,24,26],[0,9,12,20],[5,18,22,30]])
    [20, 24]
    >>> heap_track_max([[1,2,3],[1,2,3],[1,2,3]])
    [1, 1]
    >>> heap_track_max([[1]])
    [1, 1]
    """
    heap: list[tuple[int, int, int]] = []
    cur_max = float("-inf")
    for i, lst in enumerate(nums):
        heapq.heappush(heap, (lst[0], i, 0))
        cur_max = max(cur_max, lst[0])
    best = [heap[0][0], cur_max]
    while True:
        _, li, ei = heapq.heappop(heap)
        if ei + 1 >= len(nums[li]):
            break
        nxt = nums[li][ei + 1]
        heapq.heappush(heap, (nxt, li, ei + 1))
        cur_max = max(cur_max, nxt)
        new_min = heap[0][0]
        if cur_max - new_min < best[1] - best[0]:
            best = [new_min, cur_max]
    return best


# ---------------------------------------------------------------------------
# Variant 2 — merge + sliding window with k-list coverage
# ---------------------------------------------------------------------------

def merge_window(nums: list[list[int]]) -> list[int]:
    """
    Merge all elements with list labels, sort, then slide a window that
    covers all k lists. Track minimum range.

    >>> merge_window([[4,10,15,24,26],[0,9,12,20],[5,18,22,30]])
    [20, 24]
    >>> merge_window([[1,2,3],[1,2,3],[1,2,3]])
    [1, 1]
    >>> merge_window([[1]])
    [1, 1]
    """
    k = len(nums)
    # (value, list_index)
    merged = []
    for i, lst in enumerate(nums):
        for val in lst:
            merged.append((val, i))
    merged.sort()

    count = [0] * k
    covered = 0
    left = 0
    best = [merged[0][0], merged[-1][0]]

    for right in range(len(merged)):
        val_r, idx_r = merged[right]
        if count[idx_r] == 0:
            covered += 1
        count[idx_r] += 1

        while covered == k:
            val_l, idx_l = merged[left]
            if val_r - val_l < best[1] - best[0]:
                best = [val_l, val_r]
            count[idx_l] -= 1
            if count[idx_l] == 0:
                covered -= 1
            left += 1

    return best


# ---------------------------------------------------------------------------
# Variant 3 — brute force: all pairs
# ---------------------------------------------------------------------------

def brute_force(nums: list[list[int]]) -> list[int]:
    """
    Check all possible ranges: for each pair of elements, check if the
    range covers all lists. O(N^2 * k) — only for small inputs.

    >>> brute_force([[4,10,15,24,26],[0,9,12,20],[5,18,22,30]])
    [20, 24]
    >>> brute_force([[1,2,3],[1,2,3],[1,2,3]])
    [1, 1]
    >>> brute_force([[1]])
    [1, 1]
    """
    k = len(nums)
    all_vals = []
    for i, lst in enumerate(nums):
        for val in lst:
            all_vals.append((val, i))
    all_vals.sort()

    best = [all_vals[0][0], all_vals[-1][0]]

    for i in range(len(all_vals)):
        for j in range(i, len(all_vals)):
            lo, hi = all_vals[i][0], all_vals[j][0]
            if hi - lo >= best[1] - best[0]:
                break
            # Check if range [lo, hi] covers all lists
            lists_covered = set()
            for vi in range(i, j + 1):
                lists_covered.add(all_vals[vi][1])
            if len(lists_covered) == k:
                best = [lo, hi]
                break

    return best


# ---------------------------------------------------------------------------
# Variant 4 — sorted events with heapq.merge
# ---------------------------------------------------------------------------

def sorted_events(nums: list[list[int]]) -> list[int]:
    """
    Use heapq.merge to efficiently merge sorted lists, then sliding window.

    >>> sorted_events([[4,10,15,24,26],[0,9,12,20],[5,18,22,30]])
    [20, 24]
    >>> sorted_events([[1,2,3],[1,2,3],[1,2,3]])
    [1, 1]
    >>> sorted_events([[1]])
    [1, 1]
    """
    k = len(nums)
    # Tag each element with its list index
    tagged = []
    for i, lst in enumerate(nums):
        tagged.append([(val, i) for val in lst])

    merged = list(heapq.merge(*tagged, key=lambda x: x[0]))

    count = [0] * k
    covered = 0
    left = 0
    best = [merged[0][0], merged[-1][0]]

    for right in range(len(merged)):
        val_r, idx_r = merged[right]
        if count[idx_r] == 0:
            covered += 1
        count[idx_r] += 1
        while covered == k:
            val_l, idx_l = merged[left]
            if val_r - val_l < best[1] - best[0]:
                best = [val_l, val_r]
            count[idx_l] -= 1
            if count[idx_l] == 0:
                covered -= 1
            left += 1

    return best


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]], [20, 24]),
    ([[1, 2, 3], [1, 2, 3], [1, 2, 3]], [1, 1]),
    ([[1]], [1, 1]),
    ([[1, 5, 8], [4, 12], [7, 8, 10]], [4, 7]),
]

IMPLS = [
    ("reference",      reference),
    ("heap_track_max", heap_track_max),
    ("merge_window",   merge_window),
    ("sorted_events",  sorted_events),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for nums, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(nums)
            except Exception as e:
                results[name] = f"ERR:{e}"
        if len(sum(nums, [])) <= 30:
            results["brute_force"] = brute_force(nums)
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] expected={expected}  results={results}")

    import random
    random.seed(42)
    big = [sorted(random.sample(range(10000), 200)) for _ in range(20)]

    REPS = 1_000
    print(f"\n=== Benchmark (20 lists x 200 elements): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(big), number=REPS) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
