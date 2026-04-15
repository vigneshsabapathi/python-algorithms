"""
Find maximum in a list.

>>> find_max([1, 5, 3, 9, 2])
9
>>> find_max([-10, -5, -20])
-5
>>> find_max([42])
42
"""


def find_max(nums: list[int | float]) -> int | float:
    """Return the max element. O(n).

    >>> find_max([3, 1, 4, 1, 5, 9, 2, 6])
    9
    """
    if not nums:
        raise ValueError("empty list")
    best = nums[0]
    for x in nums[1:]:
        if x > best:
            best = x
    return best


def find_max_recursive(nums: list, i: int = 0) -> int | float:
    """Recursive version.

    >>> find_max_recursive([3, 1, 4, 1, 5, 9, 2, 6])
    9
    """
    if i == len(nums) - 1:
        return nums[i]
    rest = find_max_recursive(nums, i + 1)
    return nums[i] if nums[i] > rest else rest


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(find_max([1, 5, 3, 9, 2]))
