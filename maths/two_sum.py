"""
Two Sum (LeetCode 1)
====================
Return indices of the two numbers in ``nums`` such that they add up to ``target``.
Each input has exactly one solution; you may not use the same element twice.
"""
from typing import List, Optional, Tuple


def two_sum(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """
    >>> two_sum([2, 7, 11, 15], 9)
    (0, 1)
    >>> two_sum([3, 2, 4], 6)
    (1, 2)
    >>> two_sum([3, 3], 6)
    (0, 1)
    >>> two_sum([1, 2, 3], 100)

    """
    seen = {}
    for i, x in enumerate(nums):
        comp = target - x
        if comp in seen:
            return (seen[comp], i)
        seen[x] = i
    return None


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(two_sum([2, 7, 11, 15], 9))
