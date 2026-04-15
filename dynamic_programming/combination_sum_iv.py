"""
Combination Sum IV (LeetCode 377)

Given an array of distinct integers and a target, find the number of possible
combinations that add up to the target. Elements can be reused.

Example:
  array = [1, 2, 5], target = 5 => 9 combinations
  (1+1+1+1+1, 1+1+1+2, 1+1+2+1, 1+2+1+1, 2+1+1+1, 1+2+2, 2+1+2, 2+2+1, 5)

Three approaches:
  - Brute-force recursive
  - Top-down DP with memoization
  - Bottom-up DP with tabulation

>>> combination_sum_iv([1, 2, 5], 5)
9
>>> combination_sum_iv_dp_array([1, 2, 5], 5)
9
>>> combination_sum_iv_bottom_up(3, [1, 2, 5], 5)
9
"""

from __future__ import annotations


def combination_sum_iv(array: list[int], target: int) -> int:
    """
    Brute-force recursive solution. Exponential time complexity.

    >>> combination_sum_iv([1, 2, 5], 5)
    9
    >>> combination_sum_iv([1, 2, 3], 4)
    7
    """

    def count_of_possible_combinations(target: int) -> int:
        if target < 0:
            return 0
        if target == 0:
            return 1
        return sum(count_of_possible_combinations(target - item) for item in array)

    return count_of_possible_combinations(target)


def combination_sum_iv_dp_array(array: list[int], target: int) -> int:
    """
    Top-down with memoization array. O(target * len(array)) time.

    >>> combination_sum_iv_dp_array([1, 2, 5], 5)
    9
    >>> combination_sum_iv_dp_array([1, 2, 3], 4)
    7
    """

    def count_with_dp(target: int, dp_array: list[int]) -> int:
        if target < 0:
            return 0
        if target == 0:
            return 1
        if dp_array[target] != -1:
            return dp_array[target]
        answer = sum(
            count_with_dp(target - item, dp_array) for item in array
        )
        dp_array[target] = answer
        return answer

    dp_array = [-1] * (target + 1)
    return count_with_dp(target, dp_array)


def combination_sum_iv_bottom_up(n: int, array: list[int], target: int) -> int:
    """
    Bottom-up tabulation. O(target * n) time, O(target) space.

    >>> combination_sum_iv_bottom_up(3, [1, 2, 5], 5)
    9
    >>> combination_sum_iv_bottom_up(3, [1, 2, 3], 4)
    7
    """
    dp_array = [0] * (target + 1)
    dp_array[0] = 1

    for i in range(1, target + 1):
        for j in range(n):
            if i - array[j] >= 0:
                dp_array[i] += dp_array[i - array[j]]

    return dp_array[target]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    target = 5
    array = [1, 2, 5]
    print(f"  combination_sum_iv({array}, {target}) = {combination_sum_iv(array, target)}")
    print(f"  combination_sum_iv_dp_array({array}, {target}) = {combination_sum_iv_dp_array(array, target)}")
    print(f"  combination_sum_iv_bottom_up(3, {array}, {target}) = {combination_sum_iv_bottom_up(3, array, target)}")
