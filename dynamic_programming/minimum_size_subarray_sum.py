# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/minimum_size_subarray_sum.py


def minimum_size_subarray_sum(target: int, nums: list[int]) -> int:
    """
    Find the minimal length of a contiguous subarray whose sum >= target.
    Returns 0 if no such subarray exists.

    This is a sliding window problem, often categorized under DP.

    >>> minimum_size_subarray_sum(7, [2, 3, 1, 2, 4, 3])
    2
    >>> minimum_size_subarray_sum(4, [1, 4, 4])
    1
    >>> minimum_size_subarray_sum(11, [1, 1, 1, 1, 1, 1, 1, 1])
    0
    >>> minimum_size_subarray_sum(15, [5, 1, 3, 5, 10, 7, 4, 9, 2, 8])
    2
    >>> minimum_size_subarray_sum(1, [1])
    1
    >>> minimum_size_subarray_sum(0, [])
    0
    """
    if not nums:
        return 0

    n = len(nums)
    min_len = n + 1
    window_sum = 0
    left = 0

    for right in range(n):
        window_sum += nums[right]
        while window_sum >= target:
            min_len = min(min_len, right - left + 1)
            window_sum -= nums[left]
            left += 1

    return 0 if min_len > n else min_len


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        (7, [2, 3, 1, 2, 4, 3], 2),
        (4, [1, 4, 4], 1),
        (11, [1, 1, 1, 1, 1, 1, 1, 1], 0),
        (15, [5, 1, 3, 5, 10, 7, 4, 9, 2, 8], 2),
        (1, [1], 1),
    ]
    for target, nums, expected in cases:
        result = minimum_size_subarray_sum(target, nums)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] target={target}, nums={nums} = {result}  (expected {expected})")
