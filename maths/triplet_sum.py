"""
Triplet Sum
===========
Given an array and a target, decide whether any three elements sum to target.
"""
from typing import List


def triplet_sum(nums: List[int], target: int) -> bool:
    """
    >>> triplet_sum([1, 4, 45, 6, 10, 8], 22)
    True
    >>> triplet_sum([1, 2, 4, 3, 6], 24)
    False
    >>> triplet_sum([0, 0, 0], 0)
    True
    """
    nums = sorted(nums)
    n = len(nums)
    for i in range(n - 2):
        lo, hi = i + 1, n - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s == target:
                return True
            if s < target:
                lo += 1
            else:
                hi -= 1
    return False


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(triplet_sum([1, 4, 45, 6, 10, 8], 22))
