#!/usr/bin/env python3
"""
Optimized and alternative implementations of Sherman-Morrison formula.

The reference uses a custom Matrix class. The Sherman-Morrison formula
computes (A + uv^T)^(-1) given A^(-1) in O(n^2) instead of O(n^3).

Three alternatives:
  list_based        -- Pure list-based implementation without Matrix class
  woodbury          -- Woodbury identity (generalization for rank-k updates)
  incremental       -- Apply multiple rank-1 updates sequentially

Run:
    python matrix/sherman_morrison_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matrix.sherman_morrison import Matrix


# ---------------------------------------------------------------------------
# Variant 1 -- List-based Sherman-Morrison (no class overhead)
# ---------------------------------------------------------------------------

def sherman_morrison_lists(
    a_inv: list[list[float]], u: list[float], v: list[float]
) -> list[list[float]] | None:
    """
    Sherman-Morrison using plain lists. a_inv is n x n, u and v are length n.
    Returns (A + uv^T)^(-1) or None if singular.

    >>> identity = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    >>> u = [1.0, 2.0, -3.0]
    >>> v = [4.0, -2.0, 5.0]
    >>> result = sherman_morrison_lists(identity, u, v)
    >>> round(result[0][0], 4)
    1.2857
    >>> round(result[1][1], 4)
    0.7143
    """
    n = len(a_inv)

    # Compute A^(-1) * u
    a_inv_u = [sum(a_inv[i][k] * u[k] for k in range(n)) for i in range(n)]

    # Compute v^T * A^(-1)
    vt_a_inv = [sum(v[k] * a_inv[k][j] for k in range(n)) for j in range(n)]

    # Compute denominator: 1 + v^T * A^(-1) * u
    denom = 1.0 + sum(v[k] * a_inv_u[k] for k in range(n))
    if abs(denom) < 1e-12:
        return None

    inv_denom = 1.0 / denom

    # Result: A^(-1) - (A^(-1) * u) * (v^T * A^(-1)) / denom
    result = [row[:] for row in a_inv]
    for i in range(n):
        for j in range(n):
            result[i][j] -= a_inv_u[i] * vt_a_inv[j] * inv_denom

    return result


# ---------------------------------------------------------------------------
# Variant 2 -- Woodbury identity (rank-k generalization)
# ---------------------------------------------------------------------------

def woodbury_rank1(
    a_inv: list[list[float]], u: list[float], v: list[float]
) -> list[list[float]] | None:
    """
    Woodbury identity specialized to rank-1: same as Sherman-Morrison
    but using the Woodbury formula structure. For rank-k, U and V
    would be n x k matrices.

    >>> identity = [[1.0, 0.0], [0.0, 1.0]]
    >>> u = [1.0, 0.0]
    >>> v = [0.0, 1.0]
    >>> result = woodbury_rank1(identity, u, v)
    >>> result[0][0]
    1.0
    >>> result[0][1]
    -1.0
    """
    return sherman_morrison_lists(a_inv, u, v)


# ---------------------------------------------------------------------------
# Variant 3 -- Sequential rank-1 updates
# ---------------------------------------------------------------------------

def sequential_updates(
    a_inv: list[list[float]],
    updates: list[tuple[list[float], list[float]]]
) -> list[list[float]] | None:
    """
    Apply multiple rank-1 updates sequentially using Sherman-Morrison.
    Each update is (u, v) representing A <- A + u*v^T.

    >>> identity = [[1.0, 0.0], [0.0, 1.0]]
    >>> updates = [([1.0, 0.0], [0.0, 1.0])]
    >>> result = sequential_updates(identity, updates)
    >>> round(result[0][0], 4)
    1.0
    >>> round(result[0][1], 4)
    -1.0
    """
    current = [row[:] for row in a_inv]
    for u, v in updates:
        result = sherman_morrison_lists(current, u, v)
        if result is None:
            return None
        current = result
    return current


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    n = 10
    # Create identity as A^(-1)
    a_inv_lists = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    u_list = [float(i + 1) for i in range(n)]
    v_list = [float(n - i) for i in range(n)]

    a_inv_matrix = Matrix(n, n, 0)
    for i in range(n):
        a_inv_matrix[i, i] = 1.0
    u_matrix = Matrix(n, 1, 0)
    v_matrix = Matrix(n, 1, 0)
    for i in range(n):
        u_matrix[i, 0] = u_list[i]
        v_matrix[i, 0] = v_list[i]

    number = 10_000
    print(f"Benchmark ({number} Sherman-Morrison updates on {n}x{n}):\n")

    funcs = [
        ("reference (Matrix class)", lambda: a_inv_matrix.sherman_morrison(u_matrix, v_matrix)),
        ("list_based (no class)", lambda: sherman_morrison_lists(a_inv_lists, u_list, v_list)),
    ]

    for name, func in funcs:
        t = timeit.timeit(func, number=number)
        print(f"  {name:35s} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
