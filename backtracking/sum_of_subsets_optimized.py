"""
Sum of Subsets — Optimized implementations.

Variants:
1. DP bitmask (enumerate all subsets that sum to target) — O(n × target)
2. Sorted backtracking with running sum (avoids sum(path) calls) — O(2^n) with pruning
3. itertools combinations — brute-force enumeration

The sum-of-subsets / subset-sum problem: given non-negative integers and a
target M, find ALL subsets whose elements sum to M (each element used at most once).
"""

from __future__ import annotations

from itertools import combinations


# ── Variant 1: DP bitmask — enumerate via DP table ───────────────────────


def solve_dp(nums: list[int], target: int) -> list[list[int]]:
    """
    Find all subsets summing to target using DP.
    dp[s] stores all index-bitmasks that produce sum s.
    Then decode each bitmask into the actual subset.

    >>> sorted(solve_dp([3, 34, 4, 12, 5, 2], 9))
    [[3, 4, 2], [4, 5]]
    >>> sorted(solve_dp([1, 2, 3, 4, 5], 5))
    [[1, 4], [2, 3], [5]]
    >>> solve_dp([3, 34, 4, 12, 5, 2], 1)
    []
    """
    n = len(nums)
    # dp[s] = list of bitmasks whose elements sum to s
    dp: list[list[int]] = [[] for _ in range(target + 1)]
    dp[0].append(0)

    for i, val in enumerate(nums):
        if val > target:
            continue
        bit = 1 << i
        for s in range(target, val - 1, -1):
            for mask in dp[s - val]:
                dp[s].append(mask | bit)

    # Decode bitmasks to actual values
    results: list[list[int]] = []
    for mask in dp[target]:
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        results.append(subset)
    return results


# ── Variant 2: Sorted backtracking with running sum ──────────────────────


def solve_sorted(nums: list[int], target: int) -> list[list[int]]:
    """
    Sort the input, then backtrack with a running sum instead of
    calling sum(path) at each node. Also uses remaining_sum for pruning.

    Sorting enables early termination: if current + nums[i] > target,
    all subsequent elements are also too large.

    >>> solve_sorted([3, 34, 4, 12, 5, 2], 9)
    [[2, 3, 4], [4, 5]]
    >>> solve_sorted([1, 2, 3, 4, 5], 5)
    [[1, 4], [2, 3], [5]]
    >>> solve_sorted([3, 34, 4, 12, 5, 2], 1)
    []
    """
    nums_sorted = sorted(nums)
    results: list[list[int]] = []

    def backtrack(idx: int, current_sum: int, path: list[int], remaining: int) -> None:
        if current_sum == target:
            results.append(path[:])
            return
        if current_sum > target or remaining + current_sum < target:
            return
        for i in range(idx, len(nums_sorted)):
            val = nums_sorted[i]
            if current_sum + val > target:
                break  # sorted — all subsequent values are also too large
            path.append(val)
            backtrack(i + 1, current_sum + val, path, remaining - val)
            path.pop()

    backtrack(0, 0, [], sum(nums_sorted))
    return results


# ── Variant 3: itertools combinations ─────────────────────────────────────


def solve_itertools(nums: list[int], target: int) -> list[list[int]]:
    """
    Brute-force: try all possible subset sizes and filter by sum.

    >>> sorted(solve_itertools([3, 34, 4, 12, 5, 2], 9))
    [[3, 4, 2], [4, 5]]
    >>> sorted(solve_itertools([1, 2, 3, 4, 5], 5))
    [[1, 4], [2, 3], [5]]
    >>> solve_itertools([3, 34, 4, 12, 5, 2], 1)
    []
    """
    results: list[list[int]] = []
    for size in range(1, len(nums) + 1):
        for combo in combinations(nums, size):
            if sum(combo) == target:
                results.append(list(combo))
    return results


if __name__ == "__main__":
    import time

    test_cases = [
        ([3, 34, 4, 12, 5, 2], 9),
        ([1, 2, 3, 4, 5], 5),
        (list(range(1, 21)), 50),
        (list(range(1, 26)), 60),
    ]

    print(f"{'case':>30} {'target':>6} {'solutions':>9} | {'backtrack':>10} {'sorted_bt':>10} {'dp':>10} {'itertools':>10}")
    print("-" * 100)

    from backtracking.sum_of_subsets import generate_sum_of_subsets_solutions as solve_bt

    for nums, target in test_cases:
        t = time.perf_counter()
        r_bt = solve_bt(nums, target)
        t_bt = time.perf_counter() - t

        t = time.perf_counter()
        r_sorted = solve_sorted(nums, target)
        t_sorted = time.perf_counter() - t

        t = time.perf_counter()
        r_dp = solve_dp(nums, target)
        t_dp = time.perf_counter() - t

        t = time.perf_counter()
        r_it = solve_itertools(nums, target)
        t_it = time.perf_counter() - t

        label = str(nums)[:28]
        counts = f"{len(r_bt)}>{len(r_sorted)}>{len(r_dp)}>{len(r_it)}"
        assert len(r_bt) == len(r_sorted) == len(r_dp) == len(r_it), f"MISMATCH: {counts}"
        print(f"{label:>30} {target:>6} {len(r_bt):>9} | {t_bt:>9.4f}s {t_sorted:>9.4f}s {t_dp:>9.4f}s {t_it:>9.4f}s")

    import doctest
    doctest.testmod()
