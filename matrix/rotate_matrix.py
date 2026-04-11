"""

Task:
Rotate a matrix by 90, 180, or 270 degrees counterclockwise.

Implementation notes: Uses transpose and row/column reversal:
  90 CCW  = reverse_row(transpose)   = transpose(reverse_column)
  180     = reverse_row(reverse_column)
  270 CCW = reverse_column(transpose) = transpose(reverse_row)

Reference: https://stackoverflow.com/questions/42519/how-do-you-rotate-a-two-dimensional-array
Reference: https://github.com/TheAlgorithms/Python/blob/master/matrix/rotate_matrix.py
"""

from __future__ import annotations


def make_matrix(row_size: int = 4) -> list[list[int]]:
    """
    Create a test matrix of given size.

    >>> make_matrix()
    [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    >>> make_matrix(1)
    [[1]]
    >>> make_matrix(3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    row_size = abs(row_size) or 4
    return [[1 + x + y * row_size for x in range(row_size)] for y in range(row_size)]


def rotate_90(matrix: list[list[int]]) -> list[list[int]]:
    """
    Rotate 90 degrees counterclockwise.

    >>> rotate_90(make_matrix())
    [[4, 8, 12, 16], [3, 7, 11, 15], [2, 6, 10, 14], [1, 5, 9, 13]]
    """
    return reverse_row(transpose(matrix))


def rotate_180(matrix: list[list[int]]) -> list[list[int]]:
    """
    Rotate 180 degrees.

    >>> rotate_180(make_matrix())
    [[16, 15, 14, 13], [12, 11, 10, 9], [8, 7, 6, 5], [4, 3, 2, 1]]
    """
    return reverse_row(reverse_column(matrix))


def rotate_270(matrix: list[list[int]]) -> list[list[int]]:
    """
    Rotate 270 degrees counterclockwise (= 90 clockwise).

    >>> rotate_270(make_matrix())
    [[13, 9, 5, 1], [14, 10, 6, 2], [15, 11, 7, 3], [16, 12, 8, 4]]
    """
    return reverse_column(transpose(matrix))


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    """
    >>> transpose([[1, 2], [3, 4]])
    [[1, 3], [2, 4]]
    """
    matrix[:] = [list(x) for x in zip(*matrix)]
    return matrix


def reverse_row(matrix: list[list[int]]) -> list[list[int]]:
    matrix[:] = matrix[::-1]
    return matrix


def reverse_column(matrix: list[list[int]]) -> list[list[int]]:
    matrix[:] = [x[::-1] for x in matrix]
    return matrix


if __name__ == "__main__":
    import doctest

    doctest.testmod()
