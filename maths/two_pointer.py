"""
Two Pointer
===========
Classic two-pointer template: in a sorted array, decide if there are two
elements summing to ``target``.
"""
from typing import List, Optional, Tuple


def two_pointer(nums: List[int], target: int) -> Optional[Tuple[int, int]]:
    """
    Return the (smaller, larger) pair if it exists, else None.

    Assumes nums is sorted ascending.

    >>> two_pointer([1, 2, 3, 4, 6], 6)
    (2, 4)
    >>> two_pointer([1, 2, 3, 4, 6], 11)

    >>> two_pointer([], 0)

    >>> two_pointer([5], 5)

    """
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        s = nums[lo] + nums[hi]
        if s == target:
            return nums[lo], nums[hi]
        if s < target:
            lo += 1
        else:
            hi -= 1
    return None


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(two_pointer([1, 2, 3, 4, 6], 6))
    print(two_pointer([1, 2, 3, 4, 6], 11))
