#!/usr/bin/env python3
"""
Optimized and alternative implementations of All Combinations (n choose k).

Variants covered:
1. itertools.combinations    -- stdlib, fastest; C-level generator.
2. backtracking (reference)  -- explicit recursion with mutable list.
3. generator_backtrack       -- generator version; yields one combo at a time,
                                no upfront list allocation — ideal when you
                                only need to iterate, not store all results.
4. dp_combinations           -- builds combinations via DP (Pascal's triangle
                                structure) — educational; shows the recurrence
                                C(n,k) = C(n-1,k-1) + C(n-1,k).
5. numpy / math.comb         -- count-only variants for when you just need
                                the number, not the actual combinations.

Key insight for interviews:
    itertools.combinations is always fastest for generation.
    For counting only: math.comb(n, k) is O(k) and the right answer.
    Backtracking is the interview implementation answer.

Run:
    python backtracking/all_combinations_optimized.py
"""

from __future__ import annotations

import math
import timeit
from itertools import combinations
from typing import Generator


# ---------------------------------------------------------------------------
# Variant 1 — itertools (baseline)
# ---------------------------------------------------------------------------


def combinations_itertools(n: int, k: int) -> list[list[int]]:
    """
    Fastest: delegates to C-level itertools.combinations.

    >>> combinations_itertools(4, 2)
    [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
    >>> combinations_itertools(0, 0)
    [[]]
    """
    return [list(c) for c in combinations(range(1, n + 1), k)]


# ---------------------------------------------------------------------------
# Variant 2 — generator backtracking (memory-efficient)
# ---------------------------------------------------------------------------


def combinations_generator(n: int, k: int) -> Generator[list[int], None, None]:
    """
    Generator-based backtracking: yields one combination at a time.
    No upfront list allocation — use when iterating over results without
    storing all of them (e.g., streaming, early exit on first match).

    >>> list(combinations_generator(4, 2))
    [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]
    >>> list(combinations_generator(3, 3))
    [[1, 2, 3]]
    >>> list(combinations_generator(0, 0))
    [[]]
    """

    def _backtrack(start: int, current: list[int]) -> Generator[list[int], None, None]:
        if len(current) == k:
            yield current[:]
            return
        remaining = k - len(current)
        for i in range(start, n - remaining + 2):
            current.append(i)
            yield from _backtrack(i + 1, current)
            current.pop()

    yield from _backtrack(1, [])


# ---------------------------------------------------------------------------
# Variant 3 — DP (Pascal's triangle approach)
# ---------------------------------------------------------------------------


def combinations_dp(n: int, k: int) -> list[list[int]]:
    """
    Builds combinations using the recurrence:
        C(n, k) = C(n-1, k-1) prepend(n) + C(n-1, k)

    Base cases:
        C(n, 0) = [[]]
        C(n, n) = [[1, 2, ..., n]]

    This mirrors Pascal's triangle: each combination either includes the
    current element or it doesn't.

    >>> combinations_dp(4, 2)
    [[1, 2], [1, 3], [2, 3], [1, 4], [2, 4], [3, 4]]
    >>> combinations_dp(3, 3)
    [[1, 2, 3]]
    >>> combinations_dp(0, 0)
    [[]]
    """
    if k == 0:
        return [[]]
    if k > n:
        return []

    # Build up from smaller subproblems
    # dp[i][j] = all combinations of j items from {1..i}
    dp: list[list[list[int]]] = [[[] for _ in range(k + 1)] for _ in range(n + 1)]

    # C(i, 0) = [[]] for all i
    for i in range(n + 1):
        dp[i][0] = [[]]

    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            # Combinations that include i: take C(i-1, j-1) and append i
            with_i = [combo + [i] for combo in dp[i - 1][j - 1]]
            # Combinations that exclude i: C(i-1, j)
            without_i = dp[i - 1][j]
            dp[i][j] = without_i + with_i

    return dp[n][k]


# ---------------------------------------------------------------------------
# Variant 4 — count only (math.comb)
# ---------------------------------------------------------------------------


def count_combinations(n: int, k: int) -> int:
    """
    Count-only: returns C(n, k) without generating the combinations.
    O(k) time, O(1) space.

    Use this when you only need the count, not the actual combinations.

    >>> count_combinations(4, 2)
    6
    >>> count_combinations(10, 5)
    252
    >>> count_combinations(20, 10)
    184756
    """
    return math.comb(n, k)


# ---------------------------------------------------------------------------
# Benchmark + correctness
# ---------------------------------------------------------------------------


def run_all() -> None:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from backtracking.all_combinations import (
        generate_all_combinations,
        combination_lists,
    )

    print("\n=== Correctness check ===")
    for n, k in [(4, 2), (5, 4), (3, 3), (3, 1), (0, 0), (1, 1), (6, 3)]:
        ref = sorted(map(tuple, combination_lists(n, k))) if n > 0 or k == 0 else [()]
        r1 = sorted(map(tuple, generate_all_combinations(n, k)))
        r2 = sorted(map(tuple, combinations_itertools(n, k)))
        r3 = sorted(map(tuple, combinations_generator(n, k)))
        r4 = sorted(map(tuple, combinations_dp(n, k)))
        all_match = r1 == ref and r2 == ref and r3 == ref and r4 == ref
        print(f"  n={n} k={k}  C(n,k)={math.comb(n,k):3}  {'OK' if all_match else 'MISMATCH'}")

    cases_reps = [((4, 2), 10000), ((10, 5), 2000), ((15, 7), 200), ((20, 10), 20)]
    print(f"\n=== Benchmark ===")
    print(f"  {'n':>3} {'k':>3} {'C(n,k)':>8}  {'itertools':>12}  {'backtrack':>12}  "
          f"{'generator':>12}  {'dp':>10}")

    for (n, k), REPS in cases_reps:
        cnt = math.comb(n, k)
        t_it = timeit.timeit(lambda: combinations_itertools(n, k), number=REPS) * 1000 / REPS
        t_bt = timeit.timeit(lambda: generate_all_combinations(n, k), number=REPS) * 1000 / REPS
        t_gen = timeit.timeit(lambda: list(combinations_generator(n, k)), number=REPS) * 1000 / REPS
        t_dp = timeit.timeit(lambda: combinations_dp(n, k), number=REPS) * 1000 / REPS
        print(f"  {n:>3} {k:>3} {cnt:>8}  {t_it:>11.4f}ms  {t_bt:>11.4f}ms  "
              f"{t_gen:>11.4f}ms  {t_dp:>9.4f}ms")

    print("\n=== math.comb (count only) ===")
    for n, k in [(10, 5), (20, 10), (50, 25), (100, 50)]:
        t = timeit.timeit(lambda: math.comb(n, k), number=100000) * 1000 / 100000
        print(f"  math.comb({n:3},{k:3}) = {math.comb(n,k):>15}  {t:.6f} ms/call")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
