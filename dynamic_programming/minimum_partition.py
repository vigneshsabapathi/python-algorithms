# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/minimum_partition.py


def minimum_partition(nums: list[int]) -> int:
    """
    Partition a set of integers into two subsets such that the
    absolute difference of their sums is minimized.

    >>> minimum_partition([1, 6, 11, 5])
    1
    >>> minimum_partition([1, 5, 11, 5])
    0
    >>> minimum_partition([3, 1, 4, 2, 2, 1])
    1
    >>> minimum_partition([1])
    1
    >>> minimum_partition([])
    0
    >>> minimum_partition([10, 20, 15, 5, 25])
    5
    """
    if not nums:
        return 0

    total = sum(nums)
    half = total // 2

    # dp[j] = True if a subset with sum j is achievable
    dp = [False] * (half + 1)
    dp[0] = True

    for num in nums:
        for j in range(half, num - 1, -1):
            if dp[j - num]:
                dp[j] = True

    # Find the largest achievable sum <= half
    for j in range(half, -1, -1):
        if dp[j]:
            return total - 2 * j

    return total  # fallback


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        ([1, 6, 11, 5], 1),
        ([1, 5, 11, 5], 0),
        ([3, 1, 4, 2, 2, 1], 1),
        ([1], 1),
        ([], 0),
        ([10, 20, 15, 5, 25], 5),
    ]
    for nums, expected in cases:
        result = minimum_partition(nums)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] minimum_partition({nums}) = {result}  (expected {expected})")
