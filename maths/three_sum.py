"""
Three Sum (LC 15)
=================
Find all unique triplets (a, b, c) in nums with a + b + c == 0.
"""
from typing import List


def three_sum(nums: List[int]) -> List[List[int]]:
    """
    >>> three_sum([-1, 0, 1, 2, -1, -4])
    [[-1, -1, 2], [-1, 0, 1]]
    >>> three_sum([0, 0, 0])
    [[0, 0, 0]]
    >>> three_sum([1, 2, 3])
    []
    """
    nums = sorted(nums)
    n = len(nums)
    out: List[List[int]] = []
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        lo, hi = i + 1, n - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s == 0:
                out.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                hi -= 1
                while lo < hi and nums[lo] == nums[lo - 1]:
                    lo += 1
                while lo < hi and nums[hi] == nums[hi + 1]:
                    hi -= 1
            elif s < 0:
                lo += 1
            else:
                hi -= 1
    return out


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(three_sum([-1, 0, 1, 2, -1, -4]))
