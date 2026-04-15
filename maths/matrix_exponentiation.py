"""
Matrix exponentiation: compute M^n in O(log n) matrix multiplications.

Classic use: O(log n) Fibonacci via [[1,1],[1,0]]^n.

>>> M = [[1, 1], [1, 0]]
>>> matrix_power(M, 10)
[[89, 55], [55, 34]]
>>> fib_via_matrix(10)
55
>>> fib_via_matrix(0)
0
"""

from typing import List

Matrix = List[List[int]]


def mat_mul(a: Matrix, b: Matrix) -> Matrix:
    """Multiply two square matrices."""
    n = len(a)
    m = len(b[0])
    k = len(b)
    result = [[0] * m for _ in range(n)]
    for i in range(n):
        for p in range(k):
            if a[i][p] == 0:
                continue
            for j in range(m):
                result[i][j] += a[i][p] * b[p][j]
    return result


def identity(n: int) -> Matrix:
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def matrix_power(m: Matrix, p: int) -> Matrix:
    """M^p via fast exponentiation.

    >>> matrix_power([[2, 0], [0, 2]], 5)
    [[32, 0], [0, 32]]
    """
    if p < 0:
        raise ValueError("negative power not supported")
    n = len(m)
    result = identity(n)
    base = [row[:] for row in m]
    while p:
        if p & 1:
            result = mat_mul(result, base)
        base = mat_mul(base, base)
        p >>= 1
    return result


def fib_via_matrix(n: int) -> int:
    """Compute Fibonacci F(n) via matrix exponentiation.

    >>> fib_via_matrix(20)
    6765
    """
    if n == 0:
        return 0
    return matrix_power([[1, 1], [1, 0]], n)[0][1]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(fib_via_matrix(10))
