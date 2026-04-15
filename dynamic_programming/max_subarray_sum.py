# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/max_subarray_sum.py


def max_subarray_sum(nums: list[int]) -> int:
    """
    Find the contiguous subarray with the largest sum (Kadane's Algorithm).

    >>> max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4])
    6
    >>> max_subarray_sum([1])
    1
    >>> max_subarray_sum([-1, -2, -3])
    -1
    >>> max_subarray_sum([5, 4, -1, 7, 8])
    23
    >>> max_subarray_sum([-2, -3, 4, -1, -2, 1, 5, -3])
    7
    >>> max_subarray_sum([])
    0
    """
    if not nums:
        return 0

    max_sum = nums[0]
    current_sum = nums[0]

    for i in range(1, len(nums)):
        current_sum = max(nums[i], current_sum + nums[i])
        max_sum = max(max_sum, current_sum)

    return max_sum


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        ([-2, 1, -3, 4, -1, 2, 1, -5, 4], 6),
        ([1], 1),
        ([-1, -2, -3], -1),
        ([5, 4, -1, 7, 8], 23),
        ([-2, -3, 4, -1, -2, 1, 5, -3], 7),
        ([], 0),
    ]
    for nums, expected in cases:
        result = max_subarray_sum(nums)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] max_subarray_sum({nums}) = {result}  (expected {expected})")
