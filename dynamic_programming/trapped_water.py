# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/trapped_water.py


def trapped_water(heights: list[int]) -> int:
    """
    Calculate the amount of water that can be trapped between bars.

    >>> trapped_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])
    6
    >>> trapped_water([4, 2, 0, 3, 2, 5])
    9
    >>> trapped_water([1, 2, 3, 4, 5])
    0
    >>> trapped_water([5, 4, 3, 2, 1])
    0
    >>> trapped_water([])
    0
    >>> trapped_water([3])
    0
    >>> trapped_water([3, 0, 3])
    3
    """
    if len(heights) < 3:
        return 0

    n = len(heights)
    left_max = [0] * n
    right_max = [0] * n

    left_max[0] = heights[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], heights[i])

    right_max[n - 1] = heights[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], heights[i])

    water = 0
    for i in range(n):
        water += min(left_max[i], right_max[i]) - heights[i]

    return water


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        ([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], 6),
        ([4, 2, 0, 3, 2, 5], 9),
        ([1, 2, 3, 4, 5], 0),
        ([5, 4, 3, 2, 1], 0),
        ([], 0),
        ([3, 0, 3], 3),
    ]
    for heights, expected in cases:
        result = trapped_water(heights)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] trapped_water({heights}) = {result}  (expected {expected})")
