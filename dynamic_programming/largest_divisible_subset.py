"""
Largest Divisible Subset (LeetCode 368)

Find the largest subset S of a given set of integers such that for every
pair (Si, Sj) in S, either Si % Sj == 0 or Sj % Si == 0.

Approach: Sort the array, then use DP similar to LIS (Longest Increasing
Subsequence) but with divisibility check instead of comparison.

>>> largest_divisible_subset([1, 16, 7, 8, 4])
[16, 8, 4, 1]
>>> largest_divisible_subset([1, 2, 3])
[2, 1]
>>> largest_divisible_subset([1, 2, 4, 8])
[8, 4, 2, 1]
>>> largest_divisible_subset([])
[]
"""

from __future__ import annotations


def largest_divisible_subset(items: list[int]) -> list[int]:
    """
    Return the largest divisible subset of the given list.

    >>> largest_divisible_subset([1, 16, 7, 8, 4])
    [16, 8, 4, 1]
    >>> largest_divisible_subset([1, 2, 3])
    [2, 1]
    >>> largest_divisible_subset([-1, -2, -3])
    [-3]
    >>> largest_divisible_subset([1, 1, 1])
    [1, 1, 1]
    >>> largest_divisible_subset([0, 0, 0])
    [0, 0, 0]
    >>> largest_divisible_subset([])
    []
    """
    items = sorted(items)
    number_of_items = len(items)

    memo = [1] * number_of_items
    hash_array = list(range(number_of_items))

    for i, item in enumerate(items):
        for prev_index in range(i):
            if ((items[prev_index] != 0 and item % items[prev_index]) == 0) and (
                (1 + memo[prev_index]) > memo[i]
            ):
                memo[i] = 1 + memo[prev_index]
                hash_array[i] = prev_index

    ans = -1
    last_index = -1

    for i, memo_item in enumerate(memo):
        if memo_item > ans:
            ans = memo_item
            last_index = i

    if last_index == -1:
        return []
    result = [items[last_index]]
    while hash_array[last_index] != last_index:
        last_index = hash_array[last_index]
        result.append(items[last_index])

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    tests = [
        [1, 16, 7, 8, 4],
        [1, 2, 3],
        [1, 2, 4, 8],
        [3, 6, 12, 24, 48],
    ]
    for items in tests:
        print(f"  largest_divisible_subset({items}) = {largest_divisible_subset(items)}")
