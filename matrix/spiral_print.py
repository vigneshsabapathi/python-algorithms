"""

Task:
Print or return the elements of a matrix in spiral order (clockwise).

Implementation notes: Two approaches:
1. Recursive: peel off edges (top row, right column, bottom row, left column)
   then recurse on the inner sub-matrix.
2. Transpose+reverse: pop the first row, then rotate the remaining matrix
   90 degrees counterclockwise (transpose + reverse), repeat.

Reference: https://github.com/TheAlgorithms/Python/blob/master/matrix/spiral_print.py
"""


def check_matrix(matrix: list[list[int]]) -> bool:
    """Validate that all rows have the same length."""
    if matrix and isinstance(matrix, list):
        if isinstance(matrix[0], list):
            prev_len = 0
            for row in matrix:
                if prev_len == 0:
                    prev_len = len(row)
                    result = True
                else:
                    result = prev_len == len(row)
            return result
        return True
    return False


def spiral_print_clockwise(a: list[list[int]]) -> None:
    """
    Print matrix elements in clockwise spiral order (recursive).

    >>> spiral_print_clockwise([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    1
    2
    3
    4
    8
    12
    11
    10
    9
    5
    6
    7
    """
    if check_matrix(a) and len(a) > 0:
        a = [list(row) for row in a]
        mat_row = len(a)
        if isinstance(a[0], list):
            mat_col = len(a[0])
        else:
            for dat in a:
                print(dat)
            return

        for i in range(mat_col):
            print(a[0][i])
        for i in range(1, mat_row):
            print(a[i][mat_col - 1])
        if mat_row > 1:
            for i in range(mat_col - 2, -1, -1):
                print(a[mat_row - 1][i])
        for i in range(mat_row - 2, 0, -1):
            print(a[i][0])
        remain_mat = [row[1 : mat_col - 1] for row in a[1 : mat_row - 1]]
        if len(remain_mat) > 0:
            spiral_print_clockwise(remain_mat)
    else:
        print("Not a valid matrix")


def spiral_traversal(matrix: list[list]) -> list[int]:
    """
    Return matrix elements in clockwise spiral order (transpose+reverse approach).

    >>> spiral_traversal([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
    >>> spiral_traversal([[1, 2], [3, 4]])
    [1, 2, 4, 3]
    >>> spiral_traversal([[1]])
    [1]
    """
    if matrix:
        return list(matrix.pop(0)) + spiral_traversal(
            [list(row) for row in zip(*matrix)][::-1]
        )
    return []


if __name__ == "__main__":
    import doctest

    doctest.testmod()
