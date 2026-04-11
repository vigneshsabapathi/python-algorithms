#!/usr/bin/env python3
"""
Optimized and alternative implementations of Strassen Matrix Multiplication.

The reference is pure-Python Strassen: O(n^2.807) via 7 recursive multiplications.

Three variants:
  numpy_matmul    — numpy's @ operator (BLAS-accelerated, O(n^3) but ~100x faster)
  hybrid_strassen — switch to standard multiply below threshold (reduces overhead)
  standard        — naive O(n^3) triple loop for comparison

Run:
    python divide_and_conquer/strassen_matrix_multiplication_optimized.py
"""

from __future__ import annotations

import os
import random
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from divide_and_conquer.strassen_matrix_multiplication import strassen as reference
from divide_and_conquer.strassen_matrix_multiplication import (
    standard_multiply,
    _add_matrix,
    _sub_matrix,
    _split,
    _combine,
)

Matrix = list[list[int | float]]


# ---------------------------------------------------------------------------
# Variant 1 — Numpy matrix multiply (BLAS-accelerated)
# ---------------------------------------------------------------------------

def numpy_matmul(a: Matrix, b: Matrix) -> Matrix:
    """
    Matrix multiplication using numpy — BLAS optimized.

    >>> numpy_matmul([[1, 2], [3, 4]], [[5, 6], [7, 8]])
    [[19, 22], [43, 50]]
    """
    try:
        import numpy as np
    except ImportError:
        raise ImportError("numpy required")
    result = (np.array(a) @ np.array(b)).tolist()
    return [[int(x) if isinstance(x, (float, int)) and x == int(x) else x for x in row] for row in result]


# ---------------------------------------------------------------------------
# Variant 2 — Hybrid Strassen with threshold
# ---------------------------------------------------------------------------

_THRESHOLD = 64


def hybrid_strassen(a: Matrix, b: Matrix) -> Matrix:
    """
    Strassen with cutoff to standard multiply for small matrices.
    Reduces constant-factor overhead of Strassen for small n.

    >>> hybrid_strassen([[1, 2], [3, 4]], [[5, 6], [7, 8]])
    [[19, 22], [43, 50]]
    >>> hybrid_strassen([[1, 0], [0, 1]], [[5, 6], [7, 8]])
    [[5, 6], [7, 8]]
    """
    n = len(a)
    if n <= _THRESHOLD:
        return standard_multiply(a, b)

    if n % 2 != 0:
        a = [row + [0] for row in a] + [[0] * (n + 1)]
        b = [row + [0] for row in b] + [[0] * (n + 1)]
        result = hybrid_strassen(a, b)
        return [row[:n] for row in result[:n]]

    a11, a12, a21, a22 = _split(a)
    b11, b12, b21, b22 = _split(b)

    m1 = hybrid_strassen(_add_matrix(a11, a22), _add_matrix(b11, b22))
    m2 = hybrid_strassen(_add_matrix(a21, a22), b11)
    m3 = hybrid_strassen(a11, _sub_matrix(b12, b22))
    m4 = hybrid_strassen(a22, _sub_matrix(b21, b11))
    m5 = hybrid_strassen(_add_matrix(a11, a12), b22)
    m6 = hybrid_strassen(_sub_matrix(a21, a11), _add_matrix(b11, b12))
    m7 = hybrid_strassen(_sub_matrix(a12, a22), _add_matrix(b21, b22))

    c11 = _add_matrix(_sub_matrix(_add_matrix(m1, m4), m5), m7)
    c12 = _add_matrix(m3, m5)
    c21 = _add_matrix(m2, m4)
    c22 = _add_matrix(_sub_matrix(_add_matrix(m1, m3), m2), m6)

    return _combine(c11, c12, c21, c22)


# ---------------------------------------------------------------------------
# Variant 3 — Standard (naive) O(n^3) — reference baseline
# ---------------------------------------------------------------------------

def standard(a: Matrix, b: Matrix) -> Matrix:
    """
    Naive O(n^3) matrix multiplication — thin wrapper for benchmarking.

    >>> standard([[1, 2], [3, 4]], [[5, 6], [7, 8]])
    [[19, 22], [43, 50]]
    """
    return standard_multiply(a, b)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

def _random_matrix(n: int) -> Matrix:
    return [[random.randint(-10, 10) for _ in range(n)] for _ in range(n)]


TEST_CASES = [
    ([[1, 2], [3, 4]], [[5, 6], [7, 8]], [[19, 22], [43, 50]]),
    ([[1, 0], [0, 1]], [[5, 6], [7, 8]], [[5, 6], [7, 8]]),
    ([[2]], [[3]], [[6]]),
]

IMPLS: list[tuple[str, any]] = [
    ("reference", reference),
    ("hybrid", hybrid_strassen),
    ("standard", standard),
]

try:
    import numpy as np
    IMPLS.append(("numpy", numpy_matmul))
except ImportError:
    pass


def run_all() -> None:
    print("\n=== Correctness ===")
    for a, b, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            results[name] = fn(a, b)
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] {len(a)}x{len(a)} -> {expected[0]}")

    # Random matrix correctness
    for _ in range(10):
        n = random.choice([2, 4, 8])
        a, b = _random_matrix(n), _random_matrix(n)
        ref = standard_multiply(a, b)
        for name, fn in IMPLS:
            r = fn(a, b)
            if r != ref:
                print(f"  [FAIL] {name} disagrees for {n}x{n}")
                break
    else:
        print(f"  [OK] 10 random matrix tests all agree")

    sizes = [4, 8, 16, 32, 64]
    REPS = 10

    for n in sizes:
        a, b = _random_matrix(n), _random_matrix(n)
        print(f"\n=== Benchmark {n}x{n}, {REPS} runs ===")
        for name, fn in IMPLS:
            t = timeit.timeit(lambda fn=fn: fn(a, b), number=REPS) * 1000 / REPS
            print(f"  {name:<14} {t:>8.3f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
