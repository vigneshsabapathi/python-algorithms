"""
Strassen Matrix Multiplication — Divide and Conquer

Standard matrix multiplication: O(n^3).
Strassen's algorithm: O(n^2.807) — uses 7 multiplications instead of 8
for 2x2 block multiplication, then applies recursively.

The 7 products (M1..M7) replace 8 multiplications with clever
additions/subtractions, reducing the recurrence from T(n) = 8T(n/2) + O(n^2)
to T(n) = 7T(n/2) + O(n^2).

Reference: https://github.com/TheAlgorithms/Python/blob/master/divide_and_conquer/strassen_matrix_multiplication.py
"""

from __future__ import annotations


Matrix = list[list[int | float]]


def standard_multiply(a: Matrix, b: Matrix) -> Matrix:
    """
    Standard O(n^3) matrix multiplication.

    >>> standard_multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]])
    [[19, 22], [43, 50]]
    >>> standard_multiply([[1]], [[2]])
    [[2]]
    """
    n = len(a)
    m = len(b[0])
    k = len(b)
    result = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for p in range(k):
                result[i][j] += a[i][p] * b[p][j]
    return result


def _add_matrix(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    return [[a[i][j] + b[i][j] for j in range(n)] for i in range(n)]


def _sub_matrix(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    return [[a[i][j] - b[i][j] for j in range(n)] for i in range(n)]


def _split(matrix: Matrix) -> tuple[Matrix, Matrix, Matrix, Matrix]:
    """Split a matrix into 4 quadrants."""
    n = len(matrix)
    mid = n // 2
    a11 = [row[:mid] for row in matrix[:mid]]
    a12 = [row[mid:] for row in matrix[:mid]]
    a21 = [row[:mid] for row in matrix[mid:]]
    a22 = [row[mid:] for row in matrix[mid:]]
    return a11, a12, a21, a22


def _combine(c11: Matrix, c12: Matrix, c21: Matrix, c22: Matrix) -> Matrix:
    """Combine 4 quadrants into one matrix."""
    n = len(c11)
    top = [c11[i] + c12[i] for i in range(n)]
    bottom = [c21[i] + c22[i] for i in range(n)]
    return top + bottom


def strassen(a: Matrix, b: Matrix) -> Matrix:
    """
    Strassen matrix multiplication for square matrices of size 2^k.

    >>> strassen([[1, 2], [3, 4]], [[5, 6], [7, 8]])
    [[19, 22], [43, 50]]
    >>> strassen([[1, 0], [0, 1]], [[5, 6], [7, 8]])
    [[5, 6], [7, 8]]
    >>> strassen([[2]], [[3]])
    [[6]]
    """
    n = len(a)
    if n == 1:
        return [[a[0][0] * b[0][0]]]

    # Pad to even size if needed
    if n % 2 != 0:
        a = [row + [0] for row in a] + [[0] * (n + 1)]
        b = [row + [0] for row in b] + [[0] * (n + 1)]
        result = strassen(a, b)
        return [row[:n] for row in result[:n]]

    a11, a12, a21, a22 = _split(a)
    b11, b12, b21, b22 = _split(b)

    # 7 Strassen multiplications
    m1 = strassen(_add_matrix(a11, a22), _add_matrix(b11, b22))
    m2 = strassen(_add_matrix(a21, a22), b11)
    m3 = strassen(a11, _sub_matrix(b12, b22))
    m4 = strassen(a22, _sub_matrix(b21, b11))
    m5 = strassen(_add_matrix(a11, a12), b22)
    m6 = strassen(_sub_matrix(a21, a11), _add_matrix(b11, b12))
    m7 = strassen(_sub_matrix(a12, a22), _add_matrix(b21, b22))

    # Combine results
    c11 = _add_matrix(_sub_matrix(_add_matrix(m1, m4), m5), m7)
    c12 = _add_matrix(m3, m5)
    c21 = _add_matrix(m2, m4)
    c22 = _add_matrix(_sub_matrix(_add_matrix(m1, m3), m2), m6)

    return _combine(c11, c12, c21, c22)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
