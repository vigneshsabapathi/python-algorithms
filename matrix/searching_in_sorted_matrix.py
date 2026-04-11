"""

Task:
Search for a key in a matrix where rows are sorted (left to right)
and columns are sorted (top to bottom). Uses the staircase search
starting from bottom-left corner.

Implementation notes: Start at bottom-left. If current < key, move right.
If current > key, move up. Time: O(m + n).

Reference: https://github.com/TheAlgorithms/Python/blob/master/matrix/searching_in_sorted_matrix.py
"""

from __future__ import annotations


def search_in_a_sorted_matrix(
    mat: list[list[int]], m: int, n: int, key: float
) -> tuple[bool, int, int]:
    """
    Search for key in a row-sorted and column-sorted matrix.
    Returns (found, row, col). Row/col are 1-indexed if found.

    >>> search_in_a_sorted_matrix([[2, 5, 7], [4, 8, 13], [9, 11, 15], [12, 17, 20]], 4, 3, 5)
    (True, 1, 2)
    >>> search_in_a_sorted_matrix([[2, 5, 7], [4, 8, 13], [9, 11, 15], [12, 17, 20]], 4, 3, 21)
    (False, -1, -1)
    >>> search_in_a_sorted_matrix([[2, 5, 7], [4, 8, 13], [9, 11, 15], [12, 17, 20]], 4, 3, 2)
    (True, 1, 1)
    >>> search_in_a_sorted_matrix([[2, 5, 7], [4, 8, 13], [9, 11, 15], [12, 17, 20]], 4, 3, 20)
    (True, 4, 3)
    """
    i, j = m - 1, 0
    while i >= 0 and j < n:
        if key == mat[i][j]:
            return (True, i + 1, j + 1)
        if key < mat[i][j]:
            i -= 1
        else:
            j += 1
    return (False, -1, -1)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
