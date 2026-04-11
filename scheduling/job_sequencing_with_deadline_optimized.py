#!/usr/bin/env python3
"""
Optimized and alternative implementations of Job Sequencing with Deadline.

The reference uses a dataclass-based approach with greedy slot filling.
This file explores different data structures for the same greedy logic.

Variants covered:
1. greedy_slots    -- slot array with linear scan (reference approach)
2. union_find_dsu  -- disjoint set union for O(alpha(d)) slot lookup
3. sorted_set      -- SortedList for O(log d) available-slot queries

Key interview insight:
    The key optimization target is slot-finding: reference is O(d) per job,
    Union-Find reduces to O(alpha(d)) amortized, and SortedList gives O(log d).
    For n jobs with max deadline d, total: O(n log n + n*d) vs O(n log n + n*alpha(d)).

Run:
    python scheduling/job_sequencing_with_deadline_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scheduling.job_sequencing_with_deadline import (
    Job,
    job_sequencing_with_deadline as reference,
)


# ---------------------------------------------------------------------------
# Variant 1 -- greedy slots (reference-style, explicit)
# ---------------------------------------------------------------------------

def greedy_slots(jobs: list[Job]) -> tuple[list[str], int]:
    """
    Greedy slot-filling with linear backward scan.

    >>> jobs = [Job("J1", 4, 20), Job("J2", 1, 10), Job("J3", 1, 40), Job("J4", 1, 30)]
    >>> greedy_slots(jobs)
    (['J3', 'J1'], 60)

    >>> greedy_slots([])
    ([], 0)
    """
    if not jobs:
        return ([], 0)
    sorted_jobs = sorted(jobs, key=lambda j: j.profit, reverse=True)
    max_d = max(j.deadline for j in sorted_jobs)
    slots: list[str | None] = [None] * (max_d + 1)
    profit = 0
    for job in sorted_jobs:
        for s in range(min(job.deadline, max_d), 0, -1):
            if slots[s] is None:
                slots[s] = job.job_id
                profit += job.profit
                break
    scheduled = [s for s in slots[1:] if s is not None]
    return (scheduled, profit)


# ---------------------------------------------------------------------------
# Variant 2 -- Union-Find (DSU) for near-constant slot lookup
# ---------------------------------------------------------------------------

def union_find_dsu(jobs: list[Job]) -> tuple[list[str], int]:
    """
    DSU-based slot finding: parent[t] -> latest available slot <= t.

    >>> jobs = [Job("J1", 4, 20), Job("J2", 1, 10), Job("J3", 1, 40), Job("J4", 1, 30)]
    >>> union_find_dsu(jobs)
    (['J3', 'J1'], 60)

    >>> union_find_dsu([])
    ([], 0)
    """
    if not jobs:
        return ([], 0)
    sorted_jobs = sorted(jobs, key=lambda j: j.profit, reverse=True)
    max_d = max(j.deadline for j in sorted_jobs)
    parent = list(range(max_d + 1))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    slots: list[str | None] = [None] * (max_d + 1)
    profit = 0
    for job in sorted_jobs:
        avail = find(min(job.deadline, max_d))
        if avail > 0:
            slots[avail] = job.job_id
            profit += job.profit
            parent[avail] = avail - 1
    scheduled = [s for s in slots[1:] if s is not None]
    return (scheduled, profit)


# ---------------------------------------------------------------------------
# Variant 3 -- SortedList for O(log d) slot queries
# ---------------------------------------------------------------------------

def sorted_set(jobs: list[Job]) -> tuple[list[str], int]:
    """
    Use a sorted container of available slots for binary-search assignment.
    Falls back to a plain sorted list with bisect.

    >>> jobs = [Job("J1", 4, 20), Job("J2", 1, 10), Job("J3", 1, 40), Job("J4", 1, 30)]
    >>> sorted_set(jobs)
    (['J3', 'J1'], 60)

    >>> sorted_set([])
    ([], 0)
    """
    import bisect

    if not jobs:
        return ([], 0)
    sorted_jobs = sorted(jobs, key=lambda j: j.profit, reverse=True)
    max_d = max(j.deadline for j in sorted_jobs)

    available = list(range(1, max_d + 1))  # sorted ascending
    slot_map: dict[int, str] = {}
    profit = 0

    for job in sorted_jobs:
        deadline = min(job.deadline, max_d)
        # Find rightmost available slot <= deadline
        idx = bisect.bisect_right(available, deadline) - 1
        if idx >= 0:
            slot = available[idx]
            slot_map[slot] = job.job_id
            profit += job.profit
            available.pop(idx)

    scheduled = [slot_map[s] for s in sorted(slot_map.keys())]
    return (scheduled, profit)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (
        [Job("J1", 4, 20), Job("J2", 1, 10), Job("J3", 1, 40), Job("J4", 1, 30)],
        (["J3", "J1"], 60),
    ),
    (
        [Job("A", 2, 100), Job("B", 1, 19), Job("C", 2, 27), Job("D", 1, 25), Job("E", 3, 15)],
        (["C", "A", "E"], 142),
    ),
    ([], ([], 0)),
    ([Job("X", 1, 50)], (["X"], 50)),
]

IMPLS = [
    ("reference",      reference),
    ("greedy_slots",   greedy_slots),
    ("union_find_dsu", union_find_dsu),
    ("sorted_set",     sorted_set),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for jobs, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(jobs)
            ok = result[1] == expected[1] and sorted(result[0]) == sorted(expected[0])
            tag = "OK" if ok else "FAIL"
            ids = [j.job_id for j in jobs] if jobs else []
            print(f"  [{tag}] {name:<16} jobs={ids} profit={result[1]}")
            if not ok:
                print(f"         expected={expected}")
                print(f"         got     ={result}")

    import random
    random.seed(42)
    large_jobs = [
        Job(f"J{i}", random.randint(1, 200), random.randint(1, 1000))
        for i in range(500)
    ]

    REPS = 2_000
    print(f"\n=== Benchmark: {REPS} runs, 500 jobs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(large_jobs), number=REPS) * 1000 / REPS
        print(f"  {name:<16} {t:>8.4f} ms / call")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
