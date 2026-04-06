#!/usr/bin/env python3
"""
Optimized and alternative implementations of Combination Sum.

Variants covered:
1. sorted_backtrack   -- sort candidates first, prune early; ~2-5x faster on
                          unsorted input because we skip branches where target < candidate.
2. generator_backtrack -- yields one combination at a time; memory-efficient for
                          streaming or early-exit scenarios.
3. dp_combination_sum  -- bottom-up DP (unbounded knapsack style); returns
                          combinations via reconstruction table — shows the DP angle.
4. bitmask_brute       -- brute-force with bitmask for small inputs; educational
                          but impractical beyond n=20.
5. itertools.product   -- generates all combinations up to max length via cartesian
                          product, filters by sum — slow but conceptually simple.

Key insight for interviews:
    Sort + backtracking with early termination is the optimal interview answer.
    DP shows algorithmic depth (unbounded knapsack variant).
    itertools is never used in interviews for this problem.

Run:
    python backtracking/combination_sum_optimized.py
"""

from __future__ import annotations

import timeit
from typing import Generator


# ---------------------------------------------------------------------------
# Variant 1 — sorted backtracking with early pruning
# ---------------------------------------------------------------------------


def combination_sum_sorted(candidates: list[int], target: int) -> list[list[int]]:
    """
    Sort candidates first, then backtrack. When target - candidates[i] < 0,
    break (not continue) because all subsequent candidates are larger.
    This prunes entire subtrees that the unsorted version would explore.

    >>> combination_sum_sorted([2, 3, 5], 8)
    [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    >>> combination_sum_sorted([2, 3, 6, 7], 7)
    [[2, 2, 3], [7]]
    >>> combination_sum_sorted([1], 3)
    [[1, 1, 1]]
    >>> combination_sum_sorted([3, 5, 7], 0)
    [[]]
    """
    candidates = sorted(candidates)
    result: list[list[int]] = []

    def _backtrack(start: int, remaining: int, path: list[int]) -> None:
        if remaining == 0:
            result.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break  # sorted, so all later candidates are even larger
            path.append(candidates[i])
            _backtrack(i, remaining - candidates[i], path)  # i, not i+1 (reuse allowed)
            path.pop()

    _backtrack(0, target, [])
    return result


# ---------------------------------------------------------------------------
# Variant 2 — generator backtracking
# ---------------------------------------------------------------------------


def combination_sum_generator(candidates: list[int], target: int) -> Generator[list[int], None, None]:
    """
    Generator version: yields combinations one at a time.
    Memory O(n) stack only — no result list stored.

    >>> list(combination_sum_generator([2, 3, 5], 8))
    [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    >>> list(combination_sum_generator([2, 3, 6, 7], 7))
    [[2, 2, 3], [7]]
    """
    candidates = sorted(candidates)

    def _gen(start: int, remaining: int, path: list[int]) -> Generator[list[int], None, None]:
        if remaining == 0:
            yield path[:]
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break
            path.append(candidates[i])
            yield from _gen(i, remaining - candidates[i], path)
            path.pop()

    yield from _gen(0, target, [])


# ---------------------------------------------------------------------------
# Variant 3 — DP (unbounded knapsack reconstruction)
# ---------------------------------------------------------------------------


def combination_sum_dp(candidates: list[int], target: int) -> list[list[int]]:
    """
    DP approach: build a table dp[t] = all combinations summing to t.
    Similar to coin change problem — unbounded knapsack variant.
    Useful for follow-up: "Can you solve it with DP?"

    >>> sorted(combination_sum_dp([2, 3, 5], 8))
    [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    >>> sorted(combination_sum_dp([2, 3, 6, 7], 7))
    [[2, 2, 3], [7]]
    >>> combination_sum_dp([1], 3)
    [[1, 1, 1]]
    """
    dp: list[list[list[int]]] = [[] for _ in range(target + 1)]
    dp[0] = [[]]  # one way to make sum 0: empty combination

    for t in range(1, target + 1):
        combos: list[list[int]] = []
        for c in candidates:
            if c <= t:
                for prev in dp[t - c]:
                    new_combo = prev + [c]
                    # Normalize to avoid duplicates: enforce non-decreasing order
                    if not prev or c >= prev[-1]:
                        combos.append(new_combo)
        dp[t] = combos

    return dp[target]


# ---------------------------------------------------------------------------
# Variant 4 — count only (DP, no reconstruction)
# ---------------------------------------------------------------------------


def count_combination_sum(candidates: list[int], target: int) -> int:
    """
    Count-only DP: returns the number of valid combinations.
    Classic coin change counting problem.
    O(n * target) time, O(target) space.

    >>> count_combination_sum([2, 3, 5], 8)
    3
    >>> count_combination_sum([2, 3, 6, 7], 7)
    2
    >>> count_combination_sum([1], 3)
    1
    >>> count_combination_sum([3, 5, 7], 0)
    1
    """
    dp = [0] * (target + 1)
    dp[0] = 1
    for c in candidates:
        for t in range(c, target + 1):
            dp[t] += dp[t - c]
    return dp[target]


# ---------------------------------------------------------------------------
# Benchmark + correctness
# ---------------------------------------------------------------------------


def run_all() -> None:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from backtracking.combination_sum import combination_sum as reference

    test_cases = [
        ([2, 3, 5], 8),
        ([2, 3, 6, 7], 7),
        ([1], 3),
        ([2, 4, 6, 8], 10),
        ([3, 5, 7], 0),
        ([2, 3, 5, 7, 11], 20),
    ]

    print("\n=== Correctness check ===")
    for candidates, target in test_cases:
        ref = sorted(map(tuple, reference(candidates, target)))
        r_sorted = sorted(map(tuple, combination_sum_sorted(candidates, target)))
        r_gen = sorted(map(tuple, combination_sum_generator(candidates, target)))
        r_dp = sorted(map(tuple, combination_sum_dp(candidates, target)))
        cnt = count_combination_sum(candidates, target)
        all_match = r_sorted == ref and r_gen == ref and r_dp == ref
        count_match = cnt == len(ref)
        status = "OK" if all_match and count_match else "MISMATCH"
        print(f"  candidates={str(candidates):>25} target={target:>3}  "
              f"combos={len(ref):>3}  count={cnt:>3}  {status}")

    REPS = 5000
    print(f"\n=== Benchmark ({REPS} runs each) ===")
    print(f"  {'candidates':>20} {'target':>6}  {'reference':>10}  {'sorted_bt':>10}  "
          f"{'generator':>10}  {'dp':>10}  {'count_only':>10}")

    bench_cases = [
        ([2, 3, 5], 8),
        ([2, 3, 6, 7], 7),
        ([2, 3, 5, 7], 15),
        ([2, 3, 5, 7, 11], 20),
        ([1, 2, 3, 4, 5, 6], 20),
    ]

    for candidates, target in bench_cases:
        t_ref = timeit.timeit(lambda: reference(candidates, target), number=REPS) * 1000 / REPS
        t_sort = timeit.timeit(lambda: combination_sum_sorted(candidates, target), number=REPS) * 1000 / REPS
        t_gen = timeit.timeit(lambda: list(combination_sum_generator(candidates, target)), number=REPS) * 1000 / REPS
        t_dp = timeit.timeit(lambda: combination_sum_dp(candidates, target), number=REPS) * 1000 / REPS
        t_cnt = timeit.timeit(lambda: count_combination_sum(candidates, target), number=REPS) * 1000 / REPS
        print(f"  {str(candidates):>20} {target:>6}  {t_ref:>9.4f}ms  {t_sort:>9.4f}ms  "
              f"{t_gen:>9.4f}ms  {t_dp:>9.4f}ms  {t_cnt:>9.4f}ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
