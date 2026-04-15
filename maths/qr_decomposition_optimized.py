"""
QR decomposition variants + benchmark.

1. classical_gs    - classical Gram-Schmidt
2. modified_gs     - modified Gram-Schmidt (numerically safer)
3. householder     - Householder reflections, the standard numerical method
4. numpy_qr        - numpy.linalg.qr (LAPACK)
"""
from __future__ import annotations

import math
import time
from typing import List

Matrix = List[List[float]]


def _dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def classical_gs(A: Matrix):
    m, n = len(A), len(A[0])
    Q = [[0.0] * n for _ in range(m)]
    R = [[0.0] * n for _ in range(n)]
    for j in range(n):
        v = [A[i][j] for i in range(m)]
        for i in range(j):
            qi = [Q[k][i] for k in range(m)]
            R[i][j] = _dot(qi, [A[k][j] for k in range(m)])
            v = [v_k - R[i][j] * qi[k] for k, v_k in enumerate(v)]
        norm = math.sqrt(_dot(v, v))
        R[j][j] = norm
        for k in range(m):
            Q[k][j] = v[k] / norm if norm else 0.0
    return Q, R


def modified_gs(A: Matrix):
    m, n = len(A), len(A[0])
    V = [[A[i][j] for j in range(n)] for i in range(m)]
    Q = [[0.0] * n for _ in range(m)]
    R = [[0.0] * n for _ in range(n)]
    for j in range(n):
        vj = [V[i][j] for i in range(m)]
        norm = math.sqrt(_dot(vj, vj))
        R[j][j] = norm
        for i in range(m):
            Q[i][j] = vj[i] / norm if norm else 0.0
        for k in range(j + 1, n):
            qj = [Q[i][j] for i in range(m)]
            vk = [V[i][k] for i in range(m)]
            R[j][k] = _dot(qj, vk)
            for i in range(m):
                V[i][k] = vk[i] - R[j][k] * qj[i]
    return Q, R


def householder(A: Matrix):
    try:
        import numpy as np
    except ImportError:
        return modified_gs(A)
    M = np.array(A, dtype=float)
    m, n = M.shape
    R = M.copy()
    Q = np.eye(m)
    for k in range(min(m, n)):
        x = R[k:, k].copy()
        e = np.zeros_like(x)
        e[0] = -math.copysign(np.linalg.norm(x), x[0]) if x[0] != 0 else np.linalg.norm(x)
        v = x - e
        vn = np.linalg.norm(v)
        if vn == 0:
            continue
        v = v / vn
        H = np.eye(m)
        H[k:, k:] -= 2.0 * np.outer(v, v)
        R = H @ R
        Q = Q @ H.T
    return Q[:, :n].tolist(), R[:n, :].tolist()


def numpy_qr(A: Matrix):
    import numpy as np

    Q, R = np.linalg.qr(np.array(A, dtype=float))
    return Q.tolist(), R.tolist()


def benchmark() -> None:
    import random

    rng = random.Random(0)
    sizes = [(5, 5), (20, 20), (50, 50)]
    print(f"{'fn':<16}{'size':>10}{'ms':>12}")
    for m, n in sizes:
        A = [[rng.random() for _ in range(n)] for _ in range(m)]
        for fn in (classical_gs, modified_gs, householder, numpy_qr):
            t = time.perf_counter()
            fn(A)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<16}{f'{m}x{n}':>10}{dt:>12.3f}")


if __name__ == "__main__":
    benchmark()
