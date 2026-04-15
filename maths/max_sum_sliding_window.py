"""
Max sum of any contiguous subarray of length k (sliding window).

>>> max_sum_sliding_window([1, 4, 2, 10, 23, 3, 1, 0, 20], 4)
39
>>> max_sum_sliding_window([2, 3], 2)
5
>>> max_sum_sliding_window([5], 1)
5
"""


def max_sum_sliding_window(nums: list[int], k: int) -> int:
    """Classic sliding window O(n).

    >>> max_sum_sliding_window([1, 2, 3, 4, 5], 3)
    12
    """
    if k <= 0 or k > len(nums):
        raise ValueError("invalid k")
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        if window > best:
            best = window
    return best


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(max_sum_sliding_window([1, 4, 2, 10, 23, 3, 1, 0, 20], 4))
