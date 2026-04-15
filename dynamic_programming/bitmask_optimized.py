#!/usr/bin/env python3
"""
Optimized and alternative implementations of Task Assignment Using Bitmask DP.

Three variants:
  class_based     — OOP with memoization table (reference)
  functools_cache — uses @lru_cache for cleaner memoization
  iterative       — bottom-up iterative DP with bitmask states

Run:
    python dynamic_programming/bitmask_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from collections import defaultdict
from functools import lru_cache

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.bitmask import AssignmentUsingBitmask


# ---------------------------------------------------------------------------
# Variant 1 — class_based: Reference implementation wrapper
# ---------------------------------------------------------------------------

def class_based(task_performed: list[list[int]], total_tasks: int) -> int:
    """
    >>> class_based([[1, 3, 4], [1, 2, 5], [3, 4]], 5)
    10
    """
    return AssignmentUsingBitmask(task_performed, total_tasks).count_no_of_ways(
        task_performed
    )


# ---------------------------------------------------------------------------
# Variant 2 — functools_cache: Clean memoization with @lru_cache
# ---------------------------------------------------------------------------

def functools_cache(task_performed: list[list[int]], total_tasks: int) -> int:
    """
    >>> functools_cache([[1, 3, 4], [1, 2, 5], [3, 4]], 5)
    10
    """
    num_people = len(task_performed)
    final_mask = (1 << num_people) - 1

    # Build task -> person mapping
    task_to_people: dict[int, list[int]] = defaultdict(list)
    for person_idx, tasks in enumerate(task_performed):
        for task in tasks:
            task_to_people[task].append(person_idx)

    @lru_cache(maxsize=None)
    def solve(mask: int, task_no: int) -> int:
        if mask == final_mask:
            return 1
        if task_no > total_tasks:
            return 0
        # Skip this task
        total = solve(mask, task_no + 1)
        # Assign this task to each eligible person
        for p in task_to_people.get(task_no, []):
            if not (mask & (1 << p)):
                total += solve(mask | (1 << p), task_no + 1)
        return total

    return solve(0, 1)


# ---------------------------------------------------------------------------
# Variant 3 — iterative: Bottom-up iterative DP
# ---------------------------------------------------------------------------

def iterative(task_performed: list[list[int]], total_tasks: int) -> int:
    """
    >>> iterative([[1, 3, 4], [1, 2, 5], [3, 4]], 5)
    10
    """
    num_people = len(task_performed)
    final_mask = (1 << num_people) - 1

    task_to_people: dict[int, list[int]] = defaultdict(list)
    for person_idx, tasks in enumerate(task_performed):
        for task in tasks:
            task_to_people[task].append(person_idx)

    # dp[mask] = number of ways to reach this mask state
    # Process tasks from total_tasks down to 1
    dp = defaultdict(int)
    dp[0] = 1  # starting state: no one assigned

    for task_no in range(1, total_tasks + 1):
        new_dp = defaultdict(int)
        for mask, ways in dp.items():
            if ways == 0:
                continue
            # Skip this task
            new_dp[mask] += ways
            # Assign this task to each eligible person
            for p in task_to_people.get(task_no, []):
                if not (mask & (1 << p)):
                    new_dp[mask | (1 << p)] += ways
        dp = new_dp

    return dp[final_mask]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([[1, 3, 4], [1, 2, 5], [3, 4]], 5, 10),
    ([[1, 2], [1, 2]], 2, 2),
    ([[1], [2], [3]], 3, 1),
]

IMPLS = [
    ("class_based", class_based),
    ("functools_cache", functools_cache),
    ("iterative", iterative),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    all_pass = True
    for tasks, total, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(tasks, total)
            ok = result == expected
            if not ok:
                all_pass = False
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name}(tasks, {total}) = {result}  (expected {expected})")

    print(f"\n  Overall: {'ALL PASSED' if all_pass else 'SOME FAILED'}")

    REPS = 10_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    tasks, total = [[1, 3, 4], [1, 2, 5], [3, 4]], 5
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(tasks, total), number=REPS) * 1000 / REPS
        print(f"  {name:<18} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
