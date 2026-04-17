"""
Optimized variants of Equilibrium Index in Array.

The equilibrium index is an index i where:
    sum(arr[:i]) == sum(arr[i+1:])

Benchmarks three approaches using timeit.
"""

import timeit


# Variant 1: Original single-pass O(n) approach
def equilibrium_index_single_pass(arr: list[int]) -> int:
    """
    Single pass using prefix sum trick.
    Time: O(n), Space: O(1)

    >>> equilibrium_index_single_pass([-7, 1, 5, 2, -4, 3, 0])
    3
    >>> equilibrium_index_single_pass([1, 2, 3, 4, 5])
    -1
    >>> equilibrium_index_single_pass([0])
    0
    """
    total_sum = sum(arr)
    left_sum = 0
    for i, value in enumerate(arr):
        total_sum -= value
        if left_sum == total_sum:
            return i
        left_sum += value
    return -1


# Variant 2: Brute force O(n^2) approach
def equilibrium_index_brute(arr: list[int]) -> int:
    """
    Brute force: check every index.
    Time: O(n^2), Space: O(1)

    >>> equilibrium_index_brute([-7, 1, 5, 2, -4, 3, 0])
    3
    >>> equilibrium_index_brute([1, 2, 3, 4, 5])
    -1
    >>> equilibrium_index_brute([0])
    0
    """
    n = len(arr)
    for i in range(n):
        if sum(arr[:i]) == sum(arr[i + 1 :]):
            return i
    return -1


# Variant 3: Prefix sum array O(n) time, O(n) space
def equilibrium_index_prefix_array(arr: list[int]) -> int:
    """
    Build prefix sum array, then check balance.
    Time: O(n), Space: O(n)

    >>> equilibrium_index_prefix_array([-7, 1, 5, 2, -4, 3, 0])
    3
    >>> equilibrium_index_prefix_array([1, 2, 3, 4, 5])
    -1
    >>> equilibrium_index_prefix_array([0])
    0
    """
    n = len(arr)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    total = prefix[n]
    for i in range(n):
        if prefix[i] == total - prefix[i + 1]:
            return i
    return -1


def benchmark():
    data = list(range(-500, 500))  # 1000 elements, equilibrium near middle

    n = 1000
    t1 = timeit.timeit(lambda: equilibrium_index_single_pass(data), number=n)
    t2 = timeit.timeit(lambda: equilibrium_index_brute(data), number=n)
    t3 = timeit.timeit(lambda: equilibrium_index_prefix_array(data), number=n)

    print(f"single_pass:    {t1:.4f}s for {n} runs")
    print(f"brute_force:    {t2:.4f}s for {n} runs")
    print(f"prefix_array:   {t3:.4f}s for {n} runs")


if __name__ == "__main__":
    benchmark()
