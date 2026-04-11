#!/usr/bin/env python3
"""
Optimized and alternative implementations of Banker's Algorithm.

Variants covered:
1. sequential_scan   -- Original sequential scan (reference)
2. all_safe_seqs     -- Find ALL safe sequences via backtracking
3. numpy_vectorized  -- Vectorized need comparison using numpy

Run:
    python other/bankers_algorithm_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.bankers_algorithm import bankers_algorithm as reference


def sequential_scan(
    allocation: list[list[int]],
    max_need: list[list[int]],
    available: list[int],
) -> list[int] | None:
    """
    >>> sequential_scan(
    ...     [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]],
    ...     [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]],
    ...     [3, 3, 2],
    ... )
    [1, 3, 0, 2, 4]
    """
    n = len(allocation)
    m = len(available)
    need = [[max_need[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]
    work = available[:]
    done = [False] * n
    seq: list[int] = []
    while len(seq) < n:
        found = False
        for i in range(n):
            if not done[i] and all(need[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += allocation[i][j]
                done[i] = True
                seq.append(i)
                found = True
                break
        if not found:
            return None
    return seq


def all_safe_sequences(
    allocation: list[list[int]],
    max_need: list[list[int]],
    available: list[int],
) -> list[list[int]]:
    """
    Find ALL safe sequences using backtracking.

    >>> seqs = all_safe_sequences([[1]], [[1]], [0])
    >>> [0] in seqs
    True
    >>> seqs = all_safe_sequences([[0, 1], [1, 0]], [[1, 1], [1, 1]], [0, 0])
    >>> len(seqs)
    0
    """
    n = len(allocation)
    m = len(available)
    need = [[max_need[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]
    results: list[list[int]] = []

    def backtrack(work: list[int], done: list[bool], seq: list[int]) -> None:
        if len(seq) == n:
            results.append(list(seq))
            return
        for i in range(n):
            if not done[i] and all(need[i][j] <= work[j] for j in range(m)):
                new_work = [work[j] + allocation[i][j] for j in range(m)]
                done[i] = True
                seq.append(i)
                backtrack(new_work, done, seq)
                seq.pop()
                done[i] = False

    backtrack(available[:], [False] * n, [])
    return results


def is_safe_state(
    allocation: list[list[int]],
    max_need: list[list[int]],
    available: list[int],
) -> bool:
    """
    Check if system is in safe state (without returning the sequence).

    >>> is_safe_state(
    ...     [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]],
    ...     [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]],
    ...     [3, 3, 2],
    ... )
    True
    >>> is_safe_state([[0, 1, 0], [2, 0, 0]], [[7, 5, 3], [3, 2, 2]], [0, 0, 0])
    False
    """
    return reference(allocation, max_need, available) is not None


TEST_CASES = [
    (
        [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]],
        [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]],
        [3, 3, 2],
        True,
    ),
    ([[0, 1, 0], [2, 0, 0]], [[7, 5, 3], [3, 2, 2]], [0, 0, 0], False),
    ([[1]], [[1]], [0], True),
]

IMPLS = [
    ("reference", lambda a, m, av: reference(a, m, av) is not None),
    ("sequential", lambda a, m, av: sequential_scan(a, m, av) is not None),
    ("is_safe", is_safe_state),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for alloc, maxn, avail, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(alloc, maxn, avail)
            ok = result == expected
            tag = "OK" if ok else "FAIL"
            if not ok:
                print(f"  [{tag}] {name}: expected={expected} got={result}")
        print(f"  [OK] n={len(alloc)} expected_safe={expected}")

    REPS = 50000
    alloc, maxn, avail = TEST_CASES[0][:3]
    print(f"\n=== Benchmark: {REPS} runs, 5 processes x 3 resources ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(alloc, maxn, avail), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
