#!/usr/bin/env python3
"""
Optimized and alternative implementations of Polynomial Interpolation.

The reference uses Gaussian elimination on the Vandermonde system to find
polynomial coefficients from given points.

Three variants:
  lagrange          — Lagrange interpolation (no system solving needed)
  newton_divided    — Newton's divided differences (incremental, numerically stable)
  numpy_polyfit     — np.polyfit (uses least squares on Vandermonde matrix)

Key interview insight:
    Lagrange and Newton both produce the SAME unique polynomial (degree n-1 for n points).
    Newton is preferred when adding points incrementally — just append one more term.
    Lagrange is simpler to implement from scratch in an interview.
    Vandermonde matrix can be ill-conditioned for large n.

Run:
    python linear_algebra/polynom_for_points_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from linear_algebra.polynom_for_points import points_to_polynomial as reference


# ---------------------------------------------------------------------------
# Variant 1 — lagrange: direct Lagrange interpolation
# ---------------------------------------------------------------------------
def lagrange_interpolation(coordinates: list[list[int]]) -> str:
    """
    Lagrange polynomial interpolation — returns polynomial string.

    >>> lagrange_interpolation([[1, 1], [2, 4], [3, 9]])
    'f(x)=x^2*1.0+x^1*0.0+x^0*0.0'
    >>> lagrange_interpolation([[1, 1], [2, 2], [3, 3]])
    'f(x)=x^2*0.0+x^1*1.0+x^0*0.0'
    """
    n = len(coordinates)
    xs = [c[0] for c in coordinates]
    ys = [c[1] for c in coordinates]

    # Build coefficients using numpy for evaluation
    # Evaluate Lagrange basis polynomials and combine
    coeffs = np.zeros(n)
    for i in range(n):
        # Basis polynomial coefficients for L_i
        basis = np.array([1.0])
        for j in range(n):
            if i != j:
                basis = np.convolve(basis, [1, -xs[j]]) / (xs[i] - xs[j])
        coeffs += ys[i] * basis

    # Format output to match reference
    result = "f(x)="
    for i in range(n):
        val = round(coeffs[i], 10)
        if val == 0:
            val = 0.0
        result += f"x^{n - 1 - i}*{float(val)}"
        if i < n - 1:
            result += "+"
    return result


# ---------------------------------------------------------------------------
# Variant 2 — newton_divided: Newton's divided differences
# ---------------------------------------------------------------------------
def newton_divided_differences(coordinates: list[list[int]]) -> list[float]:
    """
    Newton's divided differences — returns coefficients [c0, c1, ...].
    P(x) = c0 + c1(x-x0) + c2(x-x0)(x-x1) + ...

    >>> newton_divided_differences([[1, 1], [2, 4], [3, 9]])
    [1.0, 3.0, 1.0]
    >>> newton_divided_differences([[1, 1], [2, 2], [3, 3]])
    [1.0, 1.0, 0.0]
    """
    n = len(coordinates)
    xs = [float(c[0]) for c in coordinates]
    table = [float(c[1]) for c in coordinates]

    coeffs = [table[0]]
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            table[i] = (table[i] - table[i - 1]) / (xs[i] - xs[i - j])
        coeffs.append(table[j])

    return coeffs


def newton_evaluate(coeffs: list[float], xs: list[float], x: float) -> float:
    """
    Evaluate Newton polynomial at point x using Horner's method.

    >>> newton_evaluate([1.0, 3.0, 1.0], [1.0, 2.0, 3.0], 2.0)
    4.0
    """
    n = len(coeffs)
    result = coeffs[-1]
    for i in range(n - 2, -1, -1):
        result = result * (x - xs[i]) + coeffs[i]
    return result


# ---------------------------------------------------------------------------
# Variant 3 — numpy_polyfit: least-squares polynomial fitting
# ---------------------------------------------------------------------------
def numpy_polyfit_interpolation(coordinates: list[list[int]]) -> str:
    """
    Polynomial interpolation via numpy.polyfit.

    >>> numpy_polyfit_interpolation([[1, 1], [2, 4], [3, 9]])
    'f(x)=x^2*1.0+x^1*0.0+x^0*0.0'
    >>> numpy_polyfit_interpolation([[1, 1], [2, 2], [3, 3]])
    'f(x)=x^2*0.0+x^1*1.0+x^0*0.0'
    """
    n = len(coordinates)
    xs = [c[0] for c in coordinates]
    ys = [c[1] for c in coordinates]

    coeffs = np.polyfit(xs, ys, n - 1)

    result = "f(x)="
    for i in range(n):
        val = round(coeffs[i], 10)
        if val == 0:
            val = 0.0
        result += f"x^{n - 1 - i}*{float(val)}"
        if i < n - 1:
            result += "+"
    return result


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    """Compare all variants on polynomial interpolation."""
    import random

    random.seed(42)

    # Generate n random points
    n = 20
    xs = list(range(1, n + 1))
    ys = [random.randint(-50, 50) for _ in range(n)]
    coords = [[x, y] for x, y in zip(xs, ys)]

    number = 200

    t_ref = timeit.timeit(lambda: reference(coords[:]), number=number)
    t_lag = timeit.timeit(lambda: lagrange_interpolation(coords), number=number)
    t_ndd = timeit.timeit(lambda: newton_divided_differences(coords), number=number)
    t_npf = timeit.timeit(lambda: numpy_polyfit_interpolation(coords), number=number)

    print(f"Polynomial Interpolation Benchmark ({n} points, {number} runs)")
    print(f"{'Variant':<25} {'Total (s)':>10} {'Speedup':>10}")
    print("-" * 47)
    for name, t in [
        ("reference (Vandermonde)", t_ref),
        ("lagrange", t_lag),
        ("newton_divided_diff", t_ndd),
        ("numpy_polyfit", t_npf),
    ]:
        speedup = t_ref / t if t > 0 else float("inf")
        print(f"{name:<25} {t:>10.4f} {speedup:>9.1f}x")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
