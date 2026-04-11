#!/usr/bin/env python3
"""
Optimized and alternative implementations of Round Robin Scheduling.

The reference uses a deque-based ready queue with a fixed time quantum,
admitting processes as they arrive and cycling through the queue.

Variants covered:
1. deque_queue      -- deque with admission tracking (reference approach)
2. array_simulation -- simple array-based simulation without deque
3. weighted_rr      -- weighted round robin where quantum scales with priority

Key interview insight:
    Round Robin's performance depends heavily on the time quantum:
    - q -> infinity: degenerates to FCFS (convoy effect)
    - q -> 0: perfect fairness but infinite context-switch overhead
    - Optimal q: slightly larger than average CPU burst (rule of thumb: 80%
      of bursts should complete within one quantum)

Run:
    python scheduling/round_robin_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scheduling.round_robin import round_robin as reference


# ---------------------------------------------------------------------------
# Variant 1 -- deque-based (reference style, clean)
# ---------------------------------------------------------------------------

def deque_queue(
    arrival_times: list[int], burst_times: list[int], time_quantum: int
) -> tuple[list[int], list[int], list[int]]:
    """
    RR via deque with process admission on arrival.

    >>> deque_queue([0, 1, 2, 3], [5, 4, 2, 1], 2)
    ([12, 11, 6, 9], [12, 10, 4, 6], [7, 6, 2, 5])

    >>> deque_queue([], [], 3)
    ([], [], [])

    >>> deque_queue([0, 0, 0], [4, 3, 2], 2)
    ([8, 9, 6], [8, 9, 6], [4, 6, 4])
    """
    n = len(arrival_times)
    if n == 0:
        return ([], [], [])

    rem = list(burst_times)
    ct = [0] * n
    q: deque[int] = deque()
    order = sorted(range(n), key=lambda i: (arrival_times[i], i))
    ni = 0
    clock = 0
    done = 0
    in_q = [False] * n
    fin = [False] * n

    def admit(t: int) -> None:
        nonlocal ni
        while ni < n and arrival_times[order[ni]] <= t:
            idx = order[ni]
            if not in_q[idx] and not fin[idx]:
                q.append(idx)
                in_q[idx] = True
            ni += 1

    admit(0)
    while done < n:
        if not q:
            if ni < n:
                clock = arrival_times[order[ni]]
                admit(clock)
                continue
            break
        idx = q.popleft()
        in_q[idx] = False
        run = min(time_quantum, rem[idx])
        clock += run
        rem[idx] -= run
        admit(clock)
        if rem[idx] == 0:
            ct[idx] = clock
            fin[idx] = True
            done += 1
        else:
            q.append(idx)
            in_q[idx] = True

    tat = [ct[i] - arrival_times[i] for i in range(n)]
    wt = [tat[i] - burst_times[i] for i in range(n)]
    return (ct, tat, wt)


# ---------------------------------------------------------------------------
# Variant 2 -- array simulation (no deque, explicit index tracking)
# ---------------------------------------------------------------------------

def array_simulation(
    arrival_times: list[int], burst_times: list[int], time_quantum: int
) -> tuple[list[int], list[int], list[int]]:
    """
    RR using a plain list as a queue (pop from front, append to back).
    Mirrors the deque logic but uses list operations for clarity.

    >>> array_simulation([0, 1, 2, 3], [5, 4, 2, 1], 2)
    ([12, 11, 6, 9], [12, 10, 4, 6], [7, 6, 2, 5])

    >>> array_simulation([], [], 3)
    ([], [], [])

    >>> array_simulation([0, 0, 0], [4, 3, 2], 2)
    ([8, 9, 6], [8, 9, 6], [4, 6, 4])
    """
    n = len(arrival_times)
    if n == 0:
        return ([], [], [])

    rem = list(burst_times)
    ct = [0] * n
    order = sorted(range(n), key=lambda i: (arrival_times[i], i))
    clock = 0
    done = 0

    ready: list[int] = []
    in_q = [False] * n
    fin = [False] * n
    oi = 0

    def admit(t: int) -> None:
        nonlocal oi
        while oi < n and arrival_times[order[oi]] <= t:
            idx = order[oi]
            if not in_q[idx] and not fin[idx]:
                ready.append(idx)
                in_q[idx] = True
            oi += 1

    admit(0)
    while done < n:
        if not ready:
            if oi < n:
                clock = arrival_times[order[oi]]
                admit(clock)
                continue
            break
        idx = ready.pop(0)  # O(n) but simple -- deque variant is faster
        in_q[idx] = False
        run = min(time_quantum, rem[idx])
        clock += run
        rem[idx] -= run
        admit(clock)
        if rem[idx] == 0:
            ct[idx] = clock
            fin[idx] = True
            done += 1
        else:
            ready.append(idx)
            in_q[idx] = True

    tat = [ct[i] - arrival_times[i] for i in range(n)]
    wt = [tat[i] - burst_times[i] for i in range(n)]
    return (ct, tat, wt)


# ---------------------------------------------------------------------------
# Variant 3 -- weighted round robin (priority-based quantum)
# ---------------------------------------------------------------------------

def weighted_rr(
    arrival_times: list[int],
    burst_times: list[int],
    time_quantum: int,
    weights: list[int] | None = None,
) -> tuple[list[int], list[int], list[int]]:
    """
    Weighted RR: each process gets quantum * weight time units per turn.
    Default weight = 1 (equivalent to standard RR).

    >>> weighted_rr([0, 1, 2, 3], [5, 4, 2, 1], 2)
    ([12, 11, 6, 9], [12, 10, 4, 6], [7, 6, 2, 5])

    >>> weighted_rr([], [], 3)
    ([], [], [])

    >>> weighted_rr([0, 0], [6, 4], 2, weights=[2, 1])
    ([8, 10], [8, 10], [2, 6])
    """
    n = len(arrival_times)
    if n == 0:
        return ([], [], [])
    if weights is None:
        weights = [1] * n

    rem = list(burst_times)
    ct = [0] * n
    q: deque[int] = deque()
    order = sorted(range(n), key=lambda i: (arrival_times[i], i))
    ni = 0
    clock = 0
    done = 0
    in_q = [False] * n
    fin = [False] * n

    def admit(t: int) -> None:
        nonlocal ni
        while ni < n and arrival_times[order[ni]] <= t:
            idx = order[ni]
            if not in_q[idx] and not fin[idx]:
                q.append(idx)
                in_q[idx] = True
            ni += 1

    admit(0)
    while done < n:
        if not q:
            if ni < n:
                clock = arrival_times[order[ni]]
                admit(clock)
                continue
            break
        idx = q.popleft()
        in_q[idx] = False
        effective_quantum = time_quantum * weights[idx]
        run = min(effective_quantum, rem[idx])
        clock += run
        rem[idx] -= run
        admit(clock)
        if rem[idx] == 0:
            ct[idx] = clock
            fin[idx] = True
            done += 1
        else:
            q.append(idx)
            in_q[idx] = True

    tat = [ct[i] - arrival_times[i] for i in range(n)]
    wt = [tat[i] - burst_times[i] for i in range(n)]
    return (ct, tat, wt)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([0, 1, 2, 3], [5, 4, 2, 1], 2, ([12, 11, 6, 9], [12, 10, 4, 6], [7, 6, 2, 5])),
    ([0, 0, 0], [4, 3, 2], 2, ([8, 9, 6], [8, 9, 6], [4, 6, 4])),
    ([], [], 3, ([], [], [])),
    ([0], [5], 2, ([5], [5], [0])),
    ([0, 0], [3, 3], 3, ([3, 6], [3, 6], [0, 3])),
]

IMPLS = [
    ("reference",         lambda at, bt, q: reference(at, bt, q)),
    ("deque_queue",       lambda at, bt, q: deque_queue(at, bt, q)),
    ("array_simulation",  lambda at, bt, q: array_simulation(at, bt, q)),
    ("weighted_rr",       lambda at, bt, q: weighted_rr(at, bt, q)),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for at, bt, q, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(at, bt, q)
            ok = result == expected
            tag = "OK" if ok else "FAIL"
            print(f"  [{tag}] {name:<20} AT={at} BT={bt} Q={q}")
            if not ok:
                print(f"         expected={expected}")
                print(f"         got     ={result}")

    import random
    random.seed(42)
    large_at = sorted([random.randint(0, 100) for _ in range(200)])
    large_bt = [random.randint(1, 30) for _ in range(200)]

    REPS = 500
    print(f"\n=== Benchmark: {REPS} runs, 200 processes, quantum=4 ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(large_at, large_bt, 4), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>8.4f} ms / call")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
