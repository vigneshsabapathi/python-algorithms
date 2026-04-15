"""
Find minimum in a list.

>>> find_min([1, 5, 3, 9, 2])
1
>>> find_min([-10, -5, -20])
-20
>>> find_min([42])
42
"""


def find_min(nums: list[int | float]) -> int | float:
    """Return min element. O(n).

    >>> find_min([3, 1, 4, 1, 5, 9, 2, 6])
    1
    """
    if not nums:
        raise ValueError("empty list")
    best = nums[0]
    for x in nums[1:]:
        if x < best:
            best = x
    return best


def find_min_recursive(nums: list, i: int = 0) -> int | float:
    """Recursive version."""
    if i == len(nums) - 1:
        return nums[i]
    rest = find_min_recursive(nums, i + 1)
    return nums[i] if nums[i] < rest else rest


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(find_min([1, 5, 3, 9, 2]))
