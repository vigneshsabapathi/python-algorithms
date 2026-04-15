"""
Linear-system solvers + benchmark.

1. gauss_partial    - Gaussian elimination w/ partial pivoting (reference)
2. lu_decomposition - Doolittle LU, then solve Ly=b then Ux=y
3. numpy_solve      - numpy.linalg.solve (LAPACK)
"""
from __future__ import annotations

import time
from typing import List


def gauss_partial(A, b):
    n = len(A)
    M = [list(map(float, row)) + [float(b[i])] for i, row in enumerate(A)]
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(M[r][i]))
        M[i], M[p] = M[p], M[i]
        for k in range(i + 1, n):
            f = M[k][i] / M[i][i]
            for j in range(i, n + 1):
                M[k][j] -= f * M[i][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return x


def lu_decomposition(A, b):
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for k in range(i, n):
            U[i][k] = A[i][k] - sum(L[i][j] * U[j][k] for j in range(i))
        L[i][i] = 1.0
        for k in range(i + 1, n):
            L[k][i] = (A[k][i] - sum(L[k][j] * U[j][i] for j in range(i))) / U[i][i]
    # Ly = b
    y = [0.0] * n
    for i in range(n):
        y[i] = b[i] - sum(L[i][j] * y[j] for j in range(i))
    # Ux = y
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
    return x


def numpy_solve(A, b):
    try:
        import numpy as np
    except ImportError:
        return gauss_partial(A, b)
    return np.linalg.solve(np.array(A, dtype=float), np.array(b, dtype=float)).tolist()


def benchmark() -> None:
    import random

    rng = random.Random(0)
    print(f"{'fn':<16}{'n':>6}{'ms':>12}")
    for n in (10, 50, 100):
        A = [[rng.random() for _ in range(n)] for _ in range(n)]
        for i in range(n):
            A[i][i] += n  # diagonal dominant, avoids singular
        b = [rng.random() for _ in range(n)]
        for fn in (gauss_partial, lu_decomposition, numpy_solve):
            t = time.perf_counter()
            fn(A, b)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<16}{n:>6}{dt:>12.3f}")


if __name__ == "__main__":
    benchmark()
