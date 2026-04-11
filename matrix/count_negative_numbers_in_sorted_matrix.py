"""

Task:
Given a matrix where all rows and all columns are sorted in decreasing order,
return the number of negative numbers in the grid.

Implementation notes: Uses binary search per row to find the boundary between
non-negative and negative numbers, then counts negatives from that point.
The bound from the previous row is used to narrow the search range.

Reference: https://leetcode.com/problems/count-negative-numbers-in-a-sorted-matrix
Reference: https://github.com/TheAlgorithms/Python/blob/master/matrix/count_negative_numbers_in_sorted_matrix.py
"""


def generate_large_matrix() -> list[list[int]]:
    """
    >>> generate_large_matrix()[0][:3]
    [1000, 999, 998]
    >>> len(generate_large_matrix())
    1000
    """
    return [list(range(1000 - i, -1000 - i, -1)) for i in range(1000)]


grid = generate_large_matrix()
test_grids = (
    [[4, 3, 2, -1], [3, 2, 1, -1], [1, 1, -1, -2], [-1, -1, -2, -3]],
    [[3, 2], [1, 0]],
    [[7, 7, 6]],
    [[7, 7, 6], [-1, -2, -3]],
    grid,
)


def find_negative_index(array: list[int]) -> int:
    """
    Find the index of the first negative number using binary search.

    >>> find_negative_index([0, 0, 0, 0])
    4
    >>> find_negative_index([4, 3, 2, -1])
    3
    >>> find_negative_index([1, 0, -1, -10])
    2
    >>> find_negative_index([-1, -1, -2, -3])
    0
    >>> find_negative_index([5, 1, 0])
    3
    >>> find_negative_index([])
    0
    """
    left = 0
    right = len(array) - 1

    if not array or array[0] < 0:
        return 0

    while right + 1 > left:
        mid = (left + right) // 2
        num = array[mid]

        if num < 0 and array[mid - 1] >= 0:
            return mid

        if num >= 0:
            left = mid + 1
        else:
            right = mid - 1
    return len(array)


def count_negatives_binary_search(grid: list[list[int]]) -> int:
    """
    O(m log n) solution using binary search per row with bound narrowing.

    >>> [count_negatives_binary_search(g) for g in test_grids]
    [8, 0, 0, 3, 1498500]
    """
    total = 0
    bound = len(grid[0])

    for i in range(len(grid)):
        bound = find_negative_index(grid[i][:bound])
        total += bound
    return (len(grid) * len(grid[0])) - total


def count_negatives_brute_force(grid: list[list[int]]) -> int:
    """
    O(m*n) brute force: count all negative numbers.

    >>> [count_negatives_brute_force(g) for g in test_grids]
    [8, 0, 0, 3, 1498500]
    """
    return len([number for row in grid for number in row if number < 0])


def count_negatives_brute_force_with_break(grid: list[list[int]]) -> int:
    """
    O(m*n) worst case but breaks early when first negative found in a row.

    >>> [count_negatives_brute_force_with_break(g) for g in test_grids]
    [8, 0, 0, 3, 1498500]
    """
    total = 0
    for row in grid:
        for i, number in enumerate(row):
            if number < 0:
                total += len(row) - i
                break
    return total


if __name__ == "__main__":
    import doctest

    doctest.testmod()
