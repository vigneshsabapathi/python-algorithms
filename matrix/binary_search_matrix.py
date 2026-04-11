"""

Task:
Given a sorted 2D matrix, search for a target value using binary search
on each row. Returns the [row, col] position or [-1, -1] if not found.

Implementation notes: Binary search is applied row by row. For each row,
check if the target could be in that row (first element <= target), then
binary search within the row.

Reference: https://github.com/TheAlgorithms/Python/blob/master/matrix/binary_search_matrix.py
"""


def binary_search(array: list, lower_bound: int, upper_bound: int, value: int) -> int:
    """
    Binary search on a 1D sorted array. Returns index or -1 if not found.

    >>> binary_search([1, 4, 7, 11, 15], 0, 4, 1)
    0
    >>> binary_search([1, 4, 7, 11, 15], 0, 4, 23)
    -1
    >>> binary_search([1, 4, 7, 11, 15], 0, 4, 7)
    2
    >>> binary_search([1, 4, 7, 11, 15], 0, 4, 15)
    4
    >>> binary_search([1], 0, 0, 1)
    0
    >>> binary_search([1], 0, 0, 2)
    -1
    """
    r = int((lower_bound + upper_bound) // 2)
    if array[r] == value:
        return r
    if lower_bound >= upper_bound:
        return -1
    if array[r] < value:
        return binary_search(array, r + 1, upper_bound, value)
    else:
        return binary_search(array, lower_bound, r - 1, value)


def mat_bin_search(value: int, matrix: list) -> list:
    """
    Search for a value in a 2D matrix using binary search per row.
    Returns [row, col] or [-1, -1] if not found.

    >>> matrix = [[1, 4, 7, 11, 15],
    ...           [2, 5, 8, 12, 19],
    ...           [3, 6, 9, 16, 22],
    ...           [10, 13, 14, 17, 24],
    ...           [18, 21, 23, 26, 30]]
    >>> mat_bin_search(1, matrix)
    [0, 0]
    >>> mat_bin_search(34, matrix)
    [-1, -1]
    >>> mat_bin_search(14, matrix)
    [3, 2]
    >>> mat_bin_search(30, matrix)
    [4, 4]
    """
    index = 0
    if matrix[index][0] == value:
        return [index, 0]
    while index < len(matrix) and matrix[index][0] < value:
        r = binary_search(matrix[index], 0, len(matrix[index]) - 1, value)
        if r != -1:
            return [index, r]
        index += 1
    return [-1, -1]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
