"""

Task:
Multiply two square matrices using a recursive algorithm.

Implementation notes: The recursive approach uses three nested indices
(i, j, k) and recurses on each. Base cases advance to next row/column
when indices exceed bounds. Only works for same-size square matrices.

Reference: https://en.wikipedia.org/wiki/Matrix_multiplication
Reference: https://github.com/TheAlgorithms/Python/blob/master/matrix/matrix_multiplication_recursion.py
"""

Matrix = list[list[int]]


def is_square(matrix: Matrix) -> bool:
    """
    >>> is_square([])
    True
    >>> is_square([[1, 2], [3, 4]])
    True
    >>> is_square([[1, 2], [3, 4], [5]])
    False
    """
    len_matrix = len(matrix)
    return all(len(row) == len_matrix for row in matrix)


def matrix_multiply(matrix_a: Matrix, matrix_b: Matrix) -> Matrix:
    """
    Standard iterative matrix multiplication.

    >>> matrix_multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]])
    [[19, 22], [43, 50]]
    """
    return [
        [sum(a * b for a, b in zip(row, col)) for col in zip(*matrix_b)]
        for row in matrix_a
    ]


def matrix_multiply_recursive(matrix_a: Matrix, matrix_b: Matrix) -> Matrix:
    """
    Recursive matrix multiplication for same-size square matrices.

    >>> matrix_multiply_recursive([], [])
    []
    >>> matrix_multiply_recursive([[1, 2], [3, 4]], [[5, 6], [7, 8]])
    [[19, 22], [43, 50]]
    >>> matrix_multiply_recursive(
    ...     [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]],
    ...     [[5,8,1,2],[6,7,3,0],[4,5,9,1],[2,6,10,14]])
    [[37, 61, 74, 61], [105, 165, 166, 129], [173, 269, 258, 197], [241, 373, 350, 265]]
    >>> matrix_multiply_recursive([[1, 2], [3, 4]], [[5, 6], [7, 8, 9]])
    Traceback (most recent call last):
        ...
    ValueError: Invalid matrix dimensions
    """
    if not matrix_a or not matrix_b:
        return []
    if not all(
        (len(matrix_a) == len(matrix_b), is_square(matrix_a), is_square(matrix_b))
    ):
        raise ValueError("Invalid matrix dimensions")

    result = [[0] * len(matrix_b[0]) for _ in range(len(matrix_a))]

    def multiply(
        i_loop: int, j_loop: int, k_loop: int,
        matrix_a: Matrix, matrix_b: Matrix, result: Matrix,
    ) -> None:
        if i_loop >= len(matrix_a):
            return
        if j_loop >= len(matrix_b[0]):
            return multiply(i_loop + 1, 0, 0, matrix_a, matrix_b, result)
        if k_loop >= len(matrix_b):
            return multiply(i_loop, j_loop + 1, 0, matrix_a, matrix_b, result)
        result[i_loop][j_loop] += matrix_a[i_loop][k_loop] * matrix_b[k_loop][j_loop]
        return multiply(i_loop, j_loop, k_loop + 1, matrix_a, matrix_b, result)

    multiply(0, 0, 0, matrix_a, matrix_b, result)
    return result


if __name__ == "__main__":
    from doctest import testmod

    testmod()
