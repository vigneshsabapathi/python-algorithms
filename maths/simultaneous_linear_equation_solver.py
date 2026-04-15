"""
Simultaneous Linear Equation Solver (Gaussian Elimination)
==========================================================
Solve Ax = b for square A via Gaussian elimination with partial pivoting.
"""
from typing import List


def solve(A: List[List[float]], b: List[float]) -> List[float]:
    """
    >>> solve([[2, 1], [1, 3]], [4, 5])
    [1.4, 1.2]
    >>> solve([[1, 0, 0], [0, 1, 0], [0, 0, 1]], [3, 5, 7])
    [3.0, 5.0, 7.0]
    """
    n = len(A)
    # build augmented matrix as floats
    M = [list(map(float, row)) + [float(b[i])] for i, row in enumerate(A)]

    # forward elimination with partial pivot
    for i in range(n):
        # pivot
        pivot = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[pivot] = M[pivot], M[i]
        if M[i][i] == 0:
            raise ValueError("singular matrix")
        for k in range(i + 1, n):
            f = M[k][i] / M[i][i]
            for j in range(i, n + 1):
                M[k][j] -= f * M[i][j]

    # back substitution
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return [round(v, 10) for v in x]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    A = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
    b = [8, -11, -3]
    print(solve(A, b))  # [2, 3, -1]
