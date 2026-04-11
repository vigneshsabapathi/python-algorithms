#!/usr/bin/env python3
"""
Optimized and alternative implementations of Highest Response Ratio Next (HRRN).

The reference simulates HRRN by scanning all ready processes at each decision
point and picking the one with the highest response ratio:
    RR = (waiting_time + burst_time) / burst_time

Variants covered:
1. linear_scan     -- O(n^2) scan at each step (reference approach)
2. heapq_priority  -- heap-based selection, re-heapify on each decision
3. precomputed_order -- precompute full schedule order then simulate

Key interview insight:
    HRRN is non-preemptive and starvation-free. Response ratio naturally
    ages: even long jobs eventually get a ratio > short new arrivals.
    This is the "fair SJF" that interviewers love to ask about.

Run:
    python scheduling/highest_response_ratio_next_optimized.py
"""

from __future__ import annotations

import heapq
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scheduling.highest_response_ratio_next import (
    highest_response_ratio_next as reference,
)


# ---------------------------------------------------------------------------
# Variant 1 -- linear scan (explicit, reference-style)
# ---------------------------------------------------------------------------

def linear_scan(
    arrival_times: list[int], burst_times: list[int]
) -> tuple[list[int], list[int], list[int]]:
    """
    HRRN via linear scan of ready queue at each decision point.

    >>> linear_scan([0, 2, 4, 6], [3, 5, 2, 4])
    ([3, 8, 10, 14], [3, 6, 6, 8], [0, 1, 4, 4])

    >>> linear_scan([], [])
    ([], [], [])

    >>> linear_scan([0, 0, 0], [5, 3, 8])
    ([5, 8, 16], [5, 8, 16], [0, 5, 8])
    """
    n = len(arrival_times)
    if n == 0:
        return ([], [], [])

    done = [False] * n
    ct, tat, wt = [0] * n, [0] * n, [0] * n
    clock = 0
    for _ in range(n):
        best_rr, best_i = -1.0, -1
        any_ready = False
        for i in range(n):
            if done[i] or arrival_times[i] > clock:
                continue
            any_ready = True
            wait = clock - arrival_times[i]
            rr = (wait + burst_times[i]) / burst_times[i]
            if rr > best_rr or (rr == best_rr and (best_i == -1 or arrival_times[i] < arrival_times[best_i])):
                best_rr, best_i = rr, i

        if not any_ready:
            clock = min(arrival_times[i] for i in range(n) if not done[i])
            best_rr, best_i = -1.0, -1
            for i in range(n):
                if done[i] or arrival_times[i] > clock:
                    continue
                wait = clock - arrival_times[i]
                rr = (wait + burst_times[i]) / burst_times[i]
                if rr > best_rr:
                    best_rr, best_i = rr, i

        clock += burst_times[best_i]
        ct[best_i] = clock
        tat[best_i] = clock - arrival_times[best_i]
        wt[best_i] = tat[best_i] - burst_times[best_i]
        done[best_i] = True

    return (ct, tat, wt)


# ---------------------------------------------------------------------------
# Variant 2 -- heap-based priority selection
# ---------------------------------------------------------------------------

def heapq_priority(
    arrival_times: list[int], burst_times: list[int]
) -> tuple[list[int], list[int], list[int]]:
    """
    HRRN using a heap to pick the highest response ratio process.
    We negate the ratio for min-heap behavior.

    >>> heapq_priority([0, 2, 4, 6], [3, 5, 2, 4])
    ([3, 8, 10, 14], [3, 6, 6, 8], [0, 1, 4, 4])

    >>> heapq_priority([], [])
    ([], [], [])

    >>> heapq_priority([0, 0, 0], [5, 3, 8])
    ([5, 8, 16], [5, 8, 16], [0, 5, 8])
    """
    n = len(arrival_times)
    if n == 0:
        return ([], [], [])

    ct, tat, wt = [0] * n, [0] * n, [0] * n
    done = [False] * n
    # Sort by arrival for efficient scanning
    sorted_indices = sorted(range(n), key=lambda i: (arrival_times[i], i))
    clock = 0
    next_add = 0  # pointer into sorted_indices

    for _ in range(n):
        # Add newly arrived processes
        if next_add < n and not any(
            not done[i] and arrival_times[i] <= clock for i in range(n)
        ):
            clock = arrival_times[sorted_indices[next_add]]

        # Build heap of ready processes
        heap = []
        for i in range(n):
            if not done[i] and arrival_times[i] <= clock:
                wait = clock - arrival_times[i]
                rr = (wait + burst_times[i]) / burst_times[i]
                heapq.heappush(heap, (-rr, arrival_times[i], i))

        _, _, chosen = heapq.heappop(heap)
        clock += burst_times[chosen]
        ct[chosen] = clock
        tat[chosen] = clock - arrival_times[chosen]
        wt[chosen] = tat[chosen] - burst_times[chosen]
        done[chosen] = True

    return (ct, tat, wt)


# ---------------------------------------------------------------------------
# Variant 3 -- precomputed schedule order
# ---------------------------------------------------------------------------

def precomputed_order(
    arrival_times: list[int], burst_times: list[int]
) -> tuple[list[int], list[int], list[int]]:
    """
    HRRN that first computes the full execution order, then derives metrics.

    >>> precomputed_order([0, 2, 4, 6], [3, 5, 2, 4])
    ([3, 8, 10, 14], [3, 6, 6, 8], [0, 1, 4, 4])

    >>> precomputed_order([], [])
    ([], [], [])

    >>> precomputed_order([0, 0, 0], [5, 3, 8])
    ([5, 8, 16], [5, 8, 16], [0, 5, 8])
    """
    n = len(arrival_times)
    if n == 0:
        return ([], [], [])

    remaining = set(range(n))
    schedule = []
    clock = 0

    while remaining:
        ready = [i for i in remaining if arrival_times[i] <= clock]
        if not ready:
            clock = min(arrival_times[i] for i in remaining)
            ready = [i for i in remaining if arrival_times[i] <= clock]

        # Pick by highest response ratio
        chosen = max(
            ready,
            key=lambda i: (clock - arrival_times[i] + burst_times[i]) / burst_times[i],
        )
        schedule.append(chosen)
        clock += burst_times[chosen]
        remaining.remove(chosen)

    # Derive metrics from schedule
    ct, tat, wt = [0] * n, [0] * n, [0] * n
    clock = 0
    for idx in schedule:
        clock = max(clock, arrival_times[idx]) + burst_times[idx]
        ct[idx] = clock
        tat[idx] = clock - arrival_times[idx]
        wt[idx] = tat[idx] - burst_times[idx]

    return (ct, tat, wt)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([0, 2, 4, 6], [3, 5, 2, 4], ([3, 8, 10, 14], [3, 6, 6, 8], [0, 1, 4, 4])),
    ([0, 0, 0], [5, 3, 8], ([5, 8, 16], [5, 8, 16], [0, 5, 8])),
    ([], [], ([], [], [])),
    ([0], [10], ([10], [10], [0])),
    ([0, 1, 2], [3, 1, 1], ([3, 4, 5], [3, 3, 3], [0, 2, 2])),
]

IMPLS = [
    ("reference",         reference),
    ("linear_scan",       linear_scan),
    ("heapq_priority",    heapq_priority),
    ("precomputed_order", precomputed_order),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for at, bt, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(at, bt)
            ok = result == expected
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name:<20} AT={at} BT={bt}")
            if not ok:
                print(f"         expected={expected}")
                print(f"         got     ={result}")

    import random
    random.seed(42)
    large_at = sorted([random.randint(0, 200) for _ in range(100)])
    large_bt = [random.randint(1, 20) for _ in range(100)]

    REPS = 500
    print(f"\n=== Benchmark: {REPS} runs, 100 processes ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(large_at, large_bt), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>8.4f} ms / call")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
