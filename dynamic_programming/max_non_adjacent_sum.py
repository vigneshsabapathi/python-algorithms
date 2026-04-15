# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/max_non_adjacent_sum.py


def max_non_adjacent_sum(nums: list[int]) -> int:
    """
    Find the maximum sum of non-adjacent elements in a list.

    Given a list of integers, find the maximum sum such that no two
    selected elements are adjacent in the original list.

    >>> max_non_adjacent_sum([1, 2, 3, 4, 5])
    9
    >>> max_non_adjacent_sum([5, 1, 1, 5])
    10
    >>> max_non_adjacent_sum([3, 2, 7, 10])
    13
    >>> max_non_adjacent_sum([3, 2, 5, 10, 7])
    15
    >>> max_non_adjacent_sum([-1, -2, -3])
    0
    >>> max_non_adjacent_sum([])
    0
    >>> max_non_adjacent_sum([5])
    5
    >>> max_non_adjacent_sum([10, 5])
    10
    """
    if not nums:
        return 0

    incl = 0  # max sum including current element
    excl = 0  # max sum excluding current element

    for num in nums:
        new_excl = max(incl, excl)
        incl = excl + num
        excl = new_excl

    return max(incl, excl)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        ([1, 2, 3, 4, 5], 9),
        ([5, 1, 1, 5], 10),
        ([3, 2, 7, 10], 13),
        ([3, 2, 5, 10, 7], 15),
        ([-1, -2, -3], 0),
        ([], 0),
        ([5], 5),
        ([10, 5], 10),
    ]
    for nums, expected in cases:
        result = max_non_adjacent_sum(nums)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] max_non_adjacent_sum({nums}) = {result}  (expected {expected})")
