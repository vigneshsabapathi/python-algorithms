#!/usr/bin/env python3
"""
Optimized and alternative implementations of First Come First Served (FCFS).

The reference sorts processes by arrival time then simulates a FIFO queue,
computing Completion Time, Turnaround Time, and Waiting Time.

Variants covered:
1. sorted_pairs    -- sort (AT,BT) pairs, iterate (reference approach)
2. numpy_vectorized -- vectorized cumulative max + cumsum via NumPy
3. functools_reduce -- functional-style with reduce (no explicit loop)

Key interview insight:
    FCFS is O(n log n) due to sorting. The core simulation is O(n).
    The convoy effect is the main weakness: one long process blocks
    all shorter ones behind it, inflating average waiting time.

Run:
    python scheduling/first_come_first_served_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scheduling.first_come_first_served import first_come_first_served as reference


# ---------------------------------------------------------------------------
# Variant 1 -- sorted pairs (explicit, readable)
# ---------------------------------------------------------------------------

def sorted_pairs(
    arrival_times: list[int], burst_times: list[int]
) -> tuple[list[int], list[int], list[int]]:
    """
    FCFS via sorted (AT, BT) pairs -- explicit iteration.

    >>> sorted_pairs([0, 1, 2, 3], [4, 3, 1, 2])
    ([4, 7, 8, 10], [4, 6, 6, 7], [0, 3, 5, 5])

    >>> sorted_pairs([], [])
    ([], [], [])

    >>> sorted_pairs([0, 0, 0], [5, 3, 8])
    ([5, 8, 16], [5, 8, 16], [0, 5, 8])
    """
    n = len(arrival_times)
    if n == 0:
        return ([], [], [])

    order = sorted(range(n), key=lambda i: (arrival_times[i], i))
    ct = [0] * n
    tat = [0] * n
    wt = [0] * n
    clock = 0
    for i in order:
        clock = max(clock, arrival_times[i]) + burst_times[i]
        ct[i] = clock
        tat[i] = clock - arrival_times[i]
        wt[i] = tat[i] - burst_times[i]
    return (ct, tat, wt)


# ---------------------------------------------------------------------------
# Variant 2 -- NumPy vectorized (batch-friendly)
# ---------------------------------------------------------------------------

def numpy_vectorized(
    arrival_times: list[int], burst_times: list[int]
) -> tuple[list[int], list[int], list[int]]:
    """
    FCFS using NumPy cumulative operations for vectorized computation.

    >>> numpy_vectorized([0, 1, 2, 3], [4, 3, 1, 2])
    ([4, 7, 8, 10], [4, 6, 6, 7], [0, 3, 5, 5])

    >>> numpy_vectorized([], [])
    ([], [], [])

    >>> numpy_vectorized([0, 0, 0], [5, 3, 8])
    ([5, 8, 16], [5, 8, 16], [0, 5, 8])
    """
    import numpy as np

    n = len(arrival_times)
    if n == 0:
        return ([], [], [])

    at = np.array(arrival_times)
    bt = np.array(burst_times)
    order = np.lexsort((np.arange(n), at))

    sorted_at = at[order]
    sorted_bt = bt[order]

    # Compute completion times: CT[i] = max(CT[i-1], AT[i]) + BT[i]
    # This has a data dependency so we iterate (NumPy doesn't have scan-max)
    sorted_ct = np.zeros(n, dtype=int)
    sorted_ct[0] = sorted_at[0] + sorted_bt[0]
    for i in range(1, n):
        sorted_ct[i] = max(int(sorted_ct[i - 1]), int(sorted_at[i])) + int(sorted_bt[i])

    # Map back to original order
    ct = np.zeros(n, dtype=int)
    ct[order] = sorted_ct
    tat = ct - at
    wt = tat - bt

    return (ct.tolist(), tat.tolist(), wt.tolist())


# ---------------------------------------------------------------------------
# Variant 3 -- functools.reduce (functional style, no explicit index loop)
# ---------------------------------------------------------------------------

def functools_reduce(
    arrival_times: list[int], burst_times: list[int]
) -> tuple[list[int], list[int], list[int]]:
    """
    FCFS via functools.reduce -- accumulates completion times functionally.

    >>> functools_reduce([0, 1, 2, 3], [4, 3, 1, 2])
    ([4, 7, 8, 10], [4, 6, 6, 7], [0, 3, 5, 5])

    >>> functools_reduce([], [])
    ([], [], [])

    >>> functools_reduce([0, 0, 0], [5, 3, 8])
    ([5, 8, 16], [5, 8, 16], [0, 5, 8])
    """
    from functools import reduce

    n = len(arrival_times)
    if n == 0:
        return ([], [], [])

    order = sorted(range(n), key=lambda i: (arrival_times[i], i))

    def accumulate(state, idx):
        clock, ct_dict = state
        new_clock = max(clock, arrival_times[idx]) + burst_times[idx]
        ct_dict[idx] = new_clock
        return (new_clock, ct_dict)

    _, ct_dict = reduce(accumulate, order, (0, {}))
    ct = [ct_dict[i] for i in range(n)]
    tat = [ct[i] - arrival_times[i] for i in range(n)]
    wt = [tat[i] - burst_times[i] for i in range(n)]
    return (ct, tat, wt)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([0, 1, 2, 3], [4, 3, 1, 2], ([4, 7, 8, 10], [4, 6, 6, 7], [0, 3, 5, 5])),
    ([0, 0, 0], [5, 3, 8], ([5, 8, 16], [5, 8, 16], [0, 5, 8])),
    ([2, 0, 4], [3, 2, 1], ([5, 2, 6], [3, 2, 2], [0, 0, 1])),
    ([], [], ([], [], [])),
    ([0], [5], ([5], [5], [0])),
    ([5, 5, 5, 5], [1, 1, 1, 1], ([6, 7, 8, 9], [1, 2, 3, 4], [0, 1, 2, 3])),
]

IMPLS = [
    ("reference",        reference),
    ("sorted_pairs",     sorted_pairs),
    ("numpy_vectorized", numpy_vectorized),
    ("functools_reduce", functools_reduce),
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
    large_at = sorted([random.randint(0, 1000) for _ in range(500)])
    large_bt = [random.randint(1, 50) for _ in range(500)]

    REPS = 2_000
    print(f"\n=== Benchmark: {REPS} runs, 500 processes ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(large_at, large_bt), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>8.4f} ms / call")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
