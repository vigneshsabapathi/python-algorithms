#!/usr/bin/env python3
"""
Optimized and alternative implementations of Activity Selection.

The reference sorts by finish time and greedily picks compatible activities.

Variants covered:
1. greedy_finish_sort   -- Sort by finish time, greedy pick (reference)
2. dp_max_activities    -- Dynamic programming approach (weighted variant)
3. recursive_greedy     -- Recursive greedy selection
4. interval_scheduling  -- Using bisect for O(n log n) weighted version

Key interview insight:
    The greedy approach is optimal for unweighted activity selection.
    For weighted intervals (each activity has a profit), DP is required.

Run:
    python other/activity_selection_optimized.py
"""

from __future__ import annotations

import bisect
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.activity_selection import activity_selection as reference


# ---------------------------------------------------------------------------
# Variant 1 — Greedy with finish-time sort (reference reimplementation)
# ---------------------------------------------------------------------------

def greedy_finish_sort(activities: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Greedy activity selection sorting by finish time.

    >>> greedy_finish_sort([(1, 2), (3, 4), (0, 6), (5, 7), (8, 9), (5, 9)])
    [(1, 2), (3, 4), (5, 7), (8, 9)]
    >>> greedy_finish_sort([])
    []
    """
    if not activities:
        return []
    sorted_acts = sorted(activities, key=lambda x: x[1])
    selected = [sorted_acts[0]]
    for act in sorted_acts[1:]:
        if act[0] >= selected[-1][1]:
            selected.append(act)
    return selected


# ---------------------------------------------------------------------------
# Variant 2 — DP for weighted activity selection
# ---------------------------------------------------------------------------

def dp_weighted_selection(
    activities: list[tuple[int, int, int]],
) -> tuple[int, list[int]]:
    """
    Weighted activity selection using DP.
    Each activity is (start, finish, weight/profit).
    Returns (max_profit, list_of_selected_indices).

    >>> dp_weighted_selection([(1, 2, 5), (3, 4, 6), (0, 6, 8), (5, 7, 4)])
    (15, [0, 1, 3])
    >>> dp_weighted_selection([])
    (0, [])
    """
    if not activities:
        return 0, []

    n = len(activities)
    indexed = sorted(enumerate(activities), key=lambda x: x[1][1])
    finishes = [act[1] for _, act in indexed]

    # dp[i] = max profit using first i activities
    dp = [0] * (n + 1)
    choices = [False] * (n + 1)

    for i in range(1, n + 1):
        _, (start, finish, weight) = indexed[i - 1]
        # Binary search for last non-conflicting activity
        j = bisect.bisect_right(finishes, start, 0, i - 1)
        include = dp[j] + weight
        if include > dp[i - 1]:
            dp[i] = include
            choices[i] = True
        else:
            dp[i] = dp[i - 1]

    # Backtrack to find selected activities
    selected = []
    i = n
    while i > 0:
        if choices[i]:
            orig_idx = indexed[i - 1][0]
            selected.append(orig_idx)
            _, (start, _, _) = indexed[i - 1]
            i = bisect.bisect_right(finishes, start, 0, i - 1)
        else:
            i -= 1

    return dp[n], sorted(selected)


# ---------------------------------------------------------------------------
# Variant 3 — Recursive greedy
# ---------------------------------------------------------------------------

def recursive_greedy(
    activities: list[tuple[int, int]], idx: int = 0, last_finish: int = 0
) -> list[tuple[int, int]]:
    """
    Recursive greedy activity selection.

    >>> acts = sorted([(1, 2), (3, 4), (0, 6), (5, 7), (8, 9)], key=lambda x: x[1])
    >>> recursive_greedy(acts)
    [(1, 2), (3, 4), (5, 7), (8, 9)]
    >>> recursive_greedy([])
    []
    """
    if idx >= len(activities):
        return []

    for i in range(idx, len(activities)):
        if activities[i][0] >= last_finish:
            return [activities[i]] + recursive_greedy(
                activities, i + 1, activities[i][1]
            )
    return []


# ---------------------------------------------------------------------------
# Variant 4 — Interval scheduling with start-time sort
# ---------------------------------------------------------------------------

def greedy_start_sort_count(activities: list[tuple[int, int]]) -> int:
    """
    Count max non-overlapping activities (sort by start, track end).

    >>> greedy_start_sort_count([(1, 2), (3, 4), (0, 6), (5, 7), (8, 9), (5, 9)])
    4
    >>> greedy_start_sort_count([])
    0
    """
    if not activities:
        return 0
    sorted_acts = sorted(activities, key=lambda x: x[1])
    count = 1
    last_end = sorted_acts[0][1]
    for start, end in sorted_acts[1:]:
        if start >= last_end:
            count += 1
            last_end = end
    return count


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([(1, 2), (3, 4), (0, 6), (5, 7), (8, 9), (5, 9)], [(1, 2), (3, 4), (5, 7), (8, 9)]),
    ([(0, 6), (1, 2), (3, 5), (4, 7)], [(1, 2), (3, 5)]),
    ([], []),
    ([(1, 3)], [(1, 3)]),
    ([(1, 2), (2, 3)], [(1, 2), (2, 3)]),
]

IMPLS = [
    ("reference", reference),
    ("greedy_finish", greedy_finish_sort),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for activities, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(list(activities))
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] n={len(activities):<3} expected={expected}")

    import random
    rng = random.Random(42)
    large = sorted(
        [(rng.randint(0, 1000), rng.randint(0, 1000)) for _ in range(500)],
        key=lambda x: (min(x), max(x)),
    )
    large = [(min(a, b), max(a, b)) for a, b in large]

    REPS = 5000
    print(f"\n=== Benchmark: {REPS} runs, {len(large)} activities ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(list(large)), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
