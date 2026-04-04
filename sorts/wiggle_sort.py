"""
Wiggle Sort.

Given an unsorted array nums, reorder it in-place such that:
    nums[0] < nums[1] > nums[2] < nums[3] > nums[4] ...

i.e. values alternate between local minima (even indices) and local maxima
(odd indices).  Multiple valid outputs exist for most inputs.

Example:
    input  = [3, 5, 2, 1, 6, 4]
    output = [3, 5, 1, 6, 2, 4]  (one valid answer)

Algorithm: single-pass O(n) adjacent-swap.
    For each index i, if the pair (nums[i-1], nums[i]) violates the
    required relationship, swap them.  Swapping two adjacent elements
    can only fix the current pair without breaking any previously
    corrected pair.

Note on i=0: Python's negative indexing means nums[i-1] at i=0 accesses
nums[-1] (the last element).  This occasionally triggers a swap between
the first and last elements before the main pass, which is harmless — the
subsequent iterations restore a correct wiggle pattern.

Limitation: if all elements are equal, strict wiggle order is impossible.
"""


def wiggle_sort(nums: list) -> list:
    """
    Reorder nums in-place into wiggle order: a < b > c < d > ...

    Returns the mutated list for convenience.

    >>> wiggle_sort([0, 5, 3, 2, 2])
    [0, 5, 2, 3, 2]
    >>> wiggle_sort([])
    []
    >>> wiggle_sort([-2, -5, -45])
    [-45, -2, -5]
    >>> wiggle_sort([-2.1, -5.68, -45.11])
    [-45.11, -2.1, -5.68]
    >>> wiggle_sort([1])
    [1]
    >>> wiggle_sort([1, 2])
    [1, 2]
    >>> wiggle_sort([3, 5, 2, 1, 6, 4])
    [3, 5, 1, 6, 2, 4]
    """
    for i, _ in enumerate(nums):
        if (i % 2 == 1) == (nums[i - 1] > nums[i]):
            nums[i - 1], nums[i] = nums[i], nums[i - 1]
    return nums


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    examples = [
        [3, 5, 2, 1, 6, 4],
        [0, 5, 3, 2, 2],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [-2, -5, -45],
        [],
        [42],
    ]
    for ex in examples:
        result = wiggle_sort(list(ex))
        print(f"wiggle_sort({ex}) = {result}")
