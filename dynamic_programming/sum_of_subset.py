# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/sum_of_subset.py


def is_subset_sum(nums: list[int], target: int) -> bool:
    """
    Determine if any subset of nums sums to target.

    >>> is_subset_sum([3, 34, 4, 12, 5, 2], 9)
    True
    >>> is_subset_sum([3, 34, 4, 12, 5, 2], 30)
    False
    >>> is_subset_sum([1, 2, 3], 6)
    True
    >>> is_subset_sum([1, 2, 3], 7)
    False
    >>> is_subset_sum([], 0)
    True
    >>> is_subset_sum([], 1)
    False
    """
    n = len(nums)
    dp = [[False] * (target + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = True

    for i in range(1, n + 1):
        for j in range(1, target + 1):
            dp[i][j] = dp[i - 1][j]
            if j >= nums[i - 1]:
                dp[i][j] = dp[i][j] or dp[i - 1][j - nums[i - 1]]

    return dp[n][target]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        ([3, 34, 4, 12, 5, 2], 9, True),
        ([3, 34, 4, 12, 5, 2], 30, False),
        ([1, 2, 3], 6, True),
        ([1, 2, 3], 7, False),
        ([], 0, True),
    ]
    for nums, target, expected in cases:
        result = is_subset_sum(nums, target)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] is_subset_sum({nums}, {target}) = {result}  (expected {expected})")
