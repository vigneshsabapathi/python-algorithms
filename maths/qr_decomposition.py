"""
QR Decomposition (Gram-Schmidt)
===============================
Factor A (m x n, m >= n) into Q (m x n, orthonormal columns) and R (n x n,
upper triangular) so that A = Q R.
"""
from typing import List

Matrix = List[List[float]]


def _dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def _col(A: Matrix, j: int) -> List[float]:
    return [row[j] for row in A]


def _set_col(M: Matrix, j: int, v: List[float]) -> None:
    for i, x in enumerate(v):
        M[i][j] = x


def qr_decompose(A: Matrix) -> tuple[Matrix, Matrix]:
    """
    Return (Q, R) using modified Gram-Schmidt.

    >>> A = [[12, -51, 4], [6, 167, -68], [-4, 24, -41]]
    >>> Q, R = qr_decompose(A)
    >>> # Check A == Q R (within tolerance)
    >>> m, n = len(A), len(A[0])
    >>> all(abs(sum(Q[i][k]*R[k][j] for k in range(n)) - A[i][j]) < 1e-9
    ...     for i in range(m) for j in range(n))
    True
    """
    m = len(A)
    n = len(A[0])
    Q = [[0.0] * n for _ in range(m)]
    R = [[0.0] * n for _ in range(n)]
    for j in range(n):
        v = _col(A, j)
        for i in range(j):
            q_i = _col(Q, i)
            R[i][j] = _dot(q_i, v)
            v = [v_k - R[i][j] * q_k for v_k, q_k in zip(v, q_i)]
        norm = _dot(v, v) ** 0.5
        R[j][j] = norm
        if norm == 0:
            _set_col(Q, j, [0.0] * m)
        else:
            _set_col(Q, j, [x / norm for x in v])
    return Q, R


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    A = [[12, -51, 4], [6, 167, -68], [-4, 24, -41]]
    Q, R = qr_decompose(A)
    print("Q =")
    for row in Q:
        print(["{:8.4f}".format(x) for x in row])
    print("R =")
    for row in R:
        print(["{:8.4f}".format(x) for x in row])
