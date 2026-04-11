"""

Task:
Find the median of all elements in a 2D matrix.

Implementation notes: Flatten the matrix, sort, and return the middle element.
Time: O(m*n * log(m*n)) due to sorting.

Reference: https://github.com/TheAlgorithms/Python/blob/master/matrix/median_matrix.py
"""


def median(matrix: list[list[int]]) -> int:
    """
    Calculate the median of a matrix.

    >>> median([[1, 3, 5], [2, 6, 9], [3, 6, 9]])
    5
    >>> median([[1, 2, 3], [4, 5, 6]])
    3
    >>> median([[1]])
    1
    >>> median([[7, 2], [3, 8]])
    3
    """
    linear = sorted(num for row in matrix for num in row)
    mid = (len(linear) - 1) // 2
    return linear[mid]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
