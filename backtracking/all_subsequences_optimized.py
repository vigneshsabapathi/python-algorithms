#!/usr/bin/env python3
"""
Optimized and alternative implementations of All Subsequences (Power Set).

Variants covered:
1. subsequences_backtrack    -- reference algorithm adapted to return a list
                                instead of printing; same DFS include/exclude logic.
2. subsequences_bitmask      -- iterate 0..2^n, read each bit to include/exclude.
                                The classic O(1) space interview trick.
3. subsequences_itertools    -- use itertools.combinations for each length k=0..n.
                                Stdlib baseline; produces sorted-length order.
4. subsequences_generator    -- generator version; yields lazily without storing all.
5. count_subsequences        -- count-only: 2^n (no generation needed).

Key insight for interviews:
    All three generation methods (backtrack, bitmask, itertools) produce the same
    2^n subsets. The bitmask approach is the elegant O(1)-space interview answer.
    For counting: never enumerate — just return 2^n or 1 << n.

Run:
    python backtracking/all_subsequences_optimized.py
"""

from __future__ import annotations

import timeit
from itertools import combinations
from typing import Any, Generator


# ---------------------------------------------------------------------------
# Variant 1 — backtracking returning a list (reference DFS, usable in practice)
# ---------------------------------------------------------------------------


def subsequences_backtrack(sequence: list[Any]) -> list[list[Any]]:
    """
    Same DFS include/exclude logic as the reference, but returns a list
    instead of printing. Useful when you need the results for further processing.

    At each index we make a binary choice: skip the element (go right in the tree)
    or include it (append, recurse, pop).

    >>> sorted(map(tuple, subsequences_backtrack([1, 2, 3])))
    [(), (1,), (1, 2), (1, 2, 3), (1, 3), (2,), (2, 3), (3,)]
    >>> subsequences_backtrack([])
    [[]]
    >>> len(subsequences_backtrack(list(range(4)))) == 16
    True
    """
    result: list[list[Any]] = []

    def _dfs(index: int, current: list[Any]) -> None:
        if index == len(sequence):
            result.append(current[:])
            return
        # exclude sequence[index]
        _dfs(index + 1, current)
        # include sequence[index]
        current.append(sequence[index])
        _dfs(index + 1, current)
        current.pop()

    _dfs(0, [])
    return result


# ---------------------------------------------------------------------------
# Variant 2 — bitmask (O(1) extra space, classic interview trick)
# ---------------------------------------------------------------------------


def subsequences_bitmask(sequence: list[Any]) -> list[list[Any]]:
    """
    Bitmask approach: iterate over all 2^n integers from 0 to 2^n - 1.
    Each integer's bits represent a subset: bit j set means include sequence[j].

    Example for n=3:
        000 -> []
        001 -> [seq[0]]
        010 -> [seq[1]]
        011 -> [seq[0], seq[1]]
        ...
        111 -> [seq[0], seq[1], seq[2]]

    O(n * 2^n) time, O(1) extra space (excluding output).
    The cleanest interview answer for power set.

    >>> sorted(map(tuple, subsequences_bitmask([1, 2, 3])))
    [(), (1,), (1, 2), (1, 2, 3), (1, 3), (2,), (2, 3), (3,)]
    >>> subsequences_bitmask([])
    [[]]
    >>> len(subsequences_bitmask(list(range(4)))) == 16
    True
    """
    n = len(sequence)
    result: list[list[Any]] = []
    for mask in range(1 << n):  # 0 to 2^n - 1
        subset = [sequence[j] for j in range(n) if mask >> j & 1]
        result.append(subset)
    return result


# ---------------------------------------------------------------------------
# Variant 3 — itertools (stdlib, sorted by length)
# ---------------------------------------------------------------------------


def subsequences_itertools(sequence: list[Any]) -> list[list[Any]]:
    """
    Build the power set by iterating over all combination lengths 0..n
    using itertools.combinations.

    Produces subsets in sorted-length order (all size-0 first, then size-1, etc.).

    >>> sorted(map(tuple, subsequences_itertools([1, 2, 3])))
    [(), (1,), (1, 2), (1, 2, 3), (1, 3), (2,), (2, 3), (3,)]
    >>> subsequences_itertools([])
    [[]]
    >>> len(subsequences_itertools(list(range(4)))) == 16
    True
    """
    n = len(sequence)
    result: list[list[Any]] = []
    for k in range(n + 1):
        result.extend(list(c) for c in combinations(sequence, k))
    return result


# ---------------------------------------------------------------------------
# Variant 4 — generator (memory-efficient, lazy)
# ---------------------------------------------------------------------------


def subsequences_generator(sequence: list[Any]) -> Generator[list[Any], None, None]:
    """
    Generator-based: yields one subsequence at a time using bitmask enumeration.
    O(n) peak memory regardless of 2^n output size — use when streaming results
    or performing early-exit searches.

    >>> sorted(map(tuple, subsequences_generator([1, 2, 3])))
    [(), (1,), (1, 2), (1, 2, 3), (1, 3), (2,), (2, 3), (3,)]
    >>> list(subsequences_generator([]))
    [[]]
    """
    n = len(sequence)
    for mask in range(1 << n):
        yield [sequence[j] for j in range(n) if mask >> j & 1]


# ---------------------------------------------------------------------------
# Variant 5 — count only
# ---------------------------------------------------------------------------


def count_subsequences(n: int) -> int:
    """
    Returns the total number of subsequences (power set size) for a
    sequence of length n. Always 2^n. O(1).

    >>> count_subsequences(0)
    1
    >>> count_subsequences(3)
    8
    >>> count_subsequences(10)
    1024
    >>> count_subsequences(20)
    1048576
    """
    return 1 << n  # 2^n via bit shift


# ---------------------------------------------------------------------------
# Benchmark + correctness
# ---------------------------------------------------------------------------


def run_all() -> None:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    print("\n=== Correctness check ===")
    for seq in [[1, 2, 3], ["A", "B"], [], [1], [1, 2, 3, 4]]:
        ref = sorted(map(tuple, subsequences_bitmask(seq)))
        r_bt = sorted(map(tuple, subsequences_backtrack(seq)))
        r_it = sorted(map(tuple, subsequences_itertools(seq)))
        r_gen = sorted(map(tuple, subsequences_generator(seq)))
        cnt = count_subsequences(len(seq))
        all_match = r_bt == ref and r_it == ref and r_gen == ref and len(ref) == cnt
        print(f"  {str(seq):>20}  n={len(seq)}  2^n={cnt:>5}  "
              f"{'OK' if all_match else 'MISMATCH'}")

    cases_reps = [
        ((10,), 5000),
        ((15,), 500),
        ((18,), 50),
    ]
    print(f"\n=== Benchmark ===")
    print(f"  {'n':>4} {'2^n':>8}  {'backtrack':>12}  {'bitmask':>12}  "
          f"{'itertools':>12}  {'generator':>12}")

    for (n,), reps in cases_reps:
        seq = list(range(1, n + 1))
        cnt = 1 << n
        t_bt = timeit.timeit(lambda: subsequences_backtrack(seq), number=reps) * 1000 / reps
        t_bm = timeit.timeit(lambda: subsequences_bitmask(seq), number=reps) * 1000 / reps
        t_it = timeit.timeit(lambda: subsequences_itertools(seq), number=reps) * 1000 / reps
        t_gen = timeit.timeit(lambda: list(subsequences_generator(seq)), number=reps) * 1000 / reps
        print(f"  {n:>4} {cnt:>8}  {t_bt:>11.3f}ms  {t_bm:>11.3f}ms  "
              f"{t_it:>11.3f}ms  {t_gen:>11.3f}ms")

    print("\n=== count_subsequences (2^n, no generation) ===")
    for n in [10, 20, 30, 64]:
        print(f"  2^{n:>2} = {count_subsequences(n)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
