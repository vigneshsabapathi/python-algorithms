#!/usr/bin/env python3
"""
Optimized and alternative implementations of Gas Station (LC 134).

The reference uses a single-pass greedy: if total_gas >= total_cost,
a valid start exists. Track current_tank; reset start when it goes negative.

Variants covered:
1. single_pass      -- greedy reset (reference)
2. brute_force      -- try every starting station O(n^2) for comparison
3. prefix_sum       -- find the station where cumulative deficit is minimum
4. net_gain_array   -- precompute net gain, find min prefix index

Key interview insight:
    The single-pass greedy works because: (1) if total >= 0, solution exists,
    (2) if you can't reach station j from station i, you also can't from
    any station between i and j. This eliminates backtracking.

Run:
    python greedy_methods/gas_station_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from greedy_methods.gas_station import can_complete_circuit as reference


# ---------------------------------------------------------------------------
# Variant 1 — single pass greedy (reference)
# ---------------------------------------------------------------------------

def single_pass(gas: list[int], cost: list[int]) -> int:
    """
    Greedy: track total and current tank. Reset start when current < 0.

    >>> single_pass([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])
    3
    >>> single_pass([2, 3, 4], [3, 4, 3])
    -1
    >>> single_pass([5], [4])
    0
    """
    if not gas:
        return 0
    total = current = 0
    start = 0
    for i in range(len(gas)):
        diff = gas[i] - cost[i]
        total += diff
        current += diff
        if current < 0:
            start = i + 1
            current = 0
    return start if total >= 0 else -1


# ---------------------------------------------------------------------------
# Variant 2 — brute force O(n^2): try each start
# ---------------------------------------------------------------------------

def brute_force(gas: list[int], cost: list[int]) -> int:
    """
    Try every station as start, simulate full circuit.
    O(n^2) but useful for verification.

    >>> brute_force([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])
    3
    >>> brute_force([2, 3, 4], [3, 4, 3])
    -1
    >>> brute_force([5], [4])
    0
    """
    n = len(gas)
    if n == 0:
        return 0
    for start in range(n):
        tank = 0
        valid = True
        for j in range(n):
            idx = (start + j) % n
            tank += gas[idx] - cost[idx]
            if tank < 0:
                valid = False
                break
        if valid:
            return start
    return -1


# ---------------------------------------------------------------------------
# Variant 3 — prefix sum: find minimum cumulative point
# ---------------------------------------------------------------------------

def prefix_sum(gas: list[int], cost: list[int]) -> int:
    """
    The optimal start is right after the point where cumulative
    net fuel is at its minimum.

    >>> prefix_sum([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])
    3
    >>> prefix_sum([2, 3, 4], [3, 4, 3])
    -1
    >>> prefix_sum([5], [4])
    0
    """
    n = len(gas)
    if n == 0:
        return 0
    total = 0
    min_total = float("inf")
    min_idx = 0
    for i in range(n):
        total += gas[i] - cost[i]
        if total < min_total:
            min_total = total
            min_idx = i
    return (min_idx + 1) % n if total >= 0 else -1


# ---------------------------------------------------------------------------
# Variant 4 — net gain array with min prefix
# ---------------------------------------------------------------------------

def net_gain_array(gas: list[int], cost: list[int]) -> int:
    """
    Precompute net = gas[i] - cost[i], then find start using prefix sums.

    >>> net_gain_array([1, 2, 3, 4, 5], [3, 4, 5, 1, 2])
    3
    >>> net_gain_array([2, 3, 4], [3, 4, 3])
    -1
    >>> net_gain_array([5], [4])
    0
    """
    n = len(gas)
    if n == 0:
        return 0
    net = [gas[i] - cost[i] for i in range(n)]
    if sum(net) < 0:
        return -1
    # Find position after the minimum prefix sum
    prefix = 0
    min_prefix = float("inf")
    min_pos = 0
    for i in range(n):
        prefix += net[i]
        if prefix < min_prefix:
            min_prefix = prefix
            min_pos = i
    return (min_pos + 1) % n


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([1, 2, 3, 4, 5], [3, 4, 5, 1, 2], 3),
    ([2, 3, 4], [3, 4, 3], -1),
    ([5, 1, 2, 3, 4], [4, 4, 1, 5, 1], 4),
    ([5], [4], 0),
    ([1, 2], [2, 1], 1),
    ([], [], 0),
    ([3, 1, 1], [1, 2, 2], 0),
]

IMPLS = [
    ("reference",      reference),
    ("single_pass",    single_pass),
    ("brute_force",    brute_force),
    ("prefix_sum",     prefix_sum),
    ("net_gain_array", net_gain_array),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for gas, cost, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(gas, cost)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] gas={gas} cost={cost} expected={expected}")
        if not ok:
            print(f"         results={results}")

    import random
    random.seed(42)
    n = 10_000
    big_gas = [random.randint(1, 100) for _ in range(n)]
    big_cost = [random.randint(1, 100) for _ in range(n)]

    REPS = 5_000
    print(f"\n=== Benchmark ({n} stations): {REPS} runs ===")
    for name, fn in IMPLS:
        if name == "brute_force":
            reps = 50
        else:
            reps = REPS
        t = timeit.timeit(lambda fn=fn: fn(big_gas, big_cost), number=reps) * 1000 / reps
        print(f"  {name:<16} {t:>7.4f} ms  ({reps} runs)")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
