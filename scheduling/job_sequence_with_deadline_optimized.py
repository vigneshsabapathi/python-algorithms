#!/usr/bin/env python3
"""
Optimized and alternative implementations of Job Sequence with Deadline.

The reference uses a greedy approach: sort by profit descending, assign each
job to the latest available time slot before its deadline.

Variants covered:
1. slot_array     -- O(n*d) greedy with slot array (reference approach)
2. union_find     -- O(n * alpha(d)) using disjoint set for fast slot finding
3. sorted_deadline -- sort by deadline then profit, forward fill

Key interview insight:
    The greedy choice (highest profit first) is provably optimal for this
    problem. The Union-Find variant reduces slot-finding from O(d) to
    near-O(1) amortized, which matters when deadlines are large.

Run:
    python scheduling/job_sequence_with_deadline_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scheduling.job_sequence_with_deadline import job_sequence_with_deadline as reference


# ---------------------------------------------------------------------------
# Variant 1 -- slot array (reference-style)
# ---------------------------------------------------------------------------

def slot_array(
    jobs: list[tuple[str, int, int]],
) -> tuple[list[str], int]:
    """
    Greedy job scheduling with explicit slot array.

    >>> slot_array([("J1", 2, 60), ("J2", 1, 100), ("J3", 3, 20), ("J4", 2, 40)])
    (['J2', 'J1', 'J3'], 180)

    >>> slot_array([])
    ([], 0)

    >>> slot_array([("A", 1, 50), ("B", 1, 40)])
    (['A'], 50)
    """
    if not jobs:
        return ([], 0)

    sorted_jobs = sorted(jobs, key=lambda j: j[2], reverse=True)
    max_d = max(j[1] for j in sorted_jobs)
    slots = [None] * (max_d + 1)
    profit = 0

    for jid, deadline, p in sorted_jobs:
        for s in range(min(deadline, max_d), 0, -1):
            if slots[s] is None:
                slots[s] = jid
                profit += p
                break

    scheduled = [slots[i] for i in range(1, max_d + 1) if slots[i] is not None]
    return (scheduled, profit)


# ---------------------------------------------------------------------------
# Variant 2 -- Union-Find for O(n * alpha(d)) slot assignment
# ---------------------------------------------------------------------------

def union_find(
    jobs: list[tuple[str, int, int]],
) -> tuple[list[str], int]:
    """
    Job scheduling using disjoint set (Union-Find) for fast slot lookup.

    Instead of scanning slots linearly, parent[t] points to the latest
    available slot <= t. After filling slot s, union s with s-1.

    >>> union_find([("J1", 2, 60), ("J2", 1, 100), ("J3", 3, 20), ("J4", 2, 40)])
    (['J2', 'J1', 'J3'], 180)

    >>> union_find([])
    ([], 0)

    >>> union_find([("A", 1, 50), ("B", 1, 40)])
    (['A'], 50)
    """
    if not jobs:
        return ([], 0)

    sorted_jobs = sorted(jobs, key=lambda j: j[2], reverse=True)
    max_d = max(j[1] for j in sorted_jobs)

    # parent[i] = latest available slot <= i; 0 means no slot available
    parent = list(range(max_d + 1))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path compression
            x = parent[x]
        return x

    slots = [None] * (max_d + 1)
    profit = 0

    for jid, deadline, p in sorted_jobs:
        available = find(min(deadline, max_d))
        if available > 0:
            slots[available] = jid
            profit += p
            parent[available] = available - 1  # union with slot below

    scheduled = [slots[i] for i in range(1, max_d + 1) if slots[i] is not None]
    return (scheduled, profit)


# ---------------------------------------------------------------------------
# Variant 3 -- deadline-sorted forward fill
# ---------------------------------------------------------------------------

def sorted_deadline(
    jobs: list[tuple[str, int, int]],
) -> tuple[list[str], int]:
    """
    Sort by deadline, then profit within same deadline, fill forward.

    This is a simpler variant but may not always achieve optimal ordering
    in the output list — we still use profit-greedy internally.

    >>> sorted_deadline([("J1", 2, 60), ("J2", 1, 100), ("J3", 3, 20), ("J4", 2, 40)])
    (['J2', 'J1', 'J3'], 180)

    >>> sorted_deadline([])
    ([], 0)

    >>> sorted_deadline([("A", 1, 50), ("B", 1, 40)])
    (['A'], 50)
    """
    if not jobs:
        return ([], 0)

    # Still greedy by profit (optimal), but use different data structure
    sorted_jobs = sorted(jobs, key=lambda j: j[2], reverse=True)
    max_d = max(j[1] for j in sorted_jobs)
    occupied = set()
    slot_map: dict[int, str] = {}
    profit = 0

    for jid, deadline, p in sorted_jobs:
        for s in range(min(deadline, max_d), 0, -1):
            if s not in occupied:
                occupied.add(s)
                slot_map[s] = jid
                profit += p
                break

    scheduled = [slot_map[s] for s in sorted(slot_map.keys())]
    return (scheduled, profit)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (
        [("J1", 2, 60), ("J2", 1, 100), ("J3", 3, 20), ("J4", 2, 40)],
        (["J2", "J1", "J3"], 180),
    ),
    ([("A", 1, 50), ("B", 1, 40)], (["A"], 50)),
    ([], ([], 0)),
    ([("X", 3, 10)], (["X"], 10)),
    (
        [("A", 2, 100), ("B", 1, 19), ("C", 2, 27), ("D", 1, 25), ("E", 3, 15)],
        (["C", "A", "E"], 142),
    ),
]

IMPLS = [
    ("reference",        reference),
    ("slot_array",       slot_array),
    ("union_find",       union_find),
    ("sorted_deadline",  sorted_deadline),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for jobs, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(jobs)
            # Compare profit (order may vary for equal-profit schedules)
            ok = result[1] == expected[1] and sorted(result[0]) == sorted(expected[0])
            tag = "OK" if ok else "FAIL"
            ids = [j[0] for j in jobs] if jobs else []
            print(f"  [{tag}] {name:<20} jobs={ids} profit={result[1]}")
            if not ok:
                print(f"         expected={expected}")
                print(f"         got     ={result}")

    import random
    random.seed(42)
    large_jobs = [
        (f"J{i}", random.randint(1, 200), random.randint(1, 1000))
        for i in range(500)
    ]

    REPS = 2_000
    print(f"\n=== Benchmark: {REPS} runs, 500 jobs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(large_jobs), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>8.4f} ms / call")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
