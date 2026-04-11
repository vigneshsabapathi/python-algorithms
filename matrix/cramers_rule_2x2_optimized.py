#!/usr/bin/env python3
"""
Optimized and alternative implementations of Cramer's Rule for 2x2 systems.

The reference implements Cramer's Rule directly with determinant computation.
Time complexity is O(1) for 2x2 systems.

Three alternatives:
  cramers_3x3       -- Extends Cramer's Rule to 3x3 systems
  substitution      -- Solve by direct substitution (back-substitution)
  numpy_solve       -- Use numpy.linalg.solve for comparison

Run:
    python matrix/cramers_rule_2x2_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matrix.cramers_rule_2x2 import cramers_rule_2x2 as reference


# ---------------------------------------------------------------------------
# Variant 1 -- Cramer's Rule for 3x3 systems
# ---------------------------------------------------------------------------

def cramers_rule_3x3(
    eq1: list[float], eq2: list[float], eq3: list[float]
) -> tuple[float, float, float]:
    """
    Solve a 3-variable system using Cramer's Rule.
    Input: [a1,b1,c1,d1], [a2,b2,c2,d2], [a3,b3,c3,d3]
    Represents: a*x + b*y + c*z = d

    >>> cramers_rule_3x3([1, 0, 0, 5], [0, 1, 0, 3], [0, 0, 1, 7])
    (5.0, 3.0, 7.0)
    >>> cramers_rule_3x3([2, 1, -1, 8], [-3, -1, 2, -11], [-2, 1, 2, -3])
    (2.0, 3.0, -1.0)
    >>> cramers_rule_3x3([1, 1, 1, 6], [0, 2, 5, -4], [2, 5, -1, 27])
    (5.0, 3.0, -2.0)
    """
    def det3(m: list[list[float]]) -> float:
        return (
            m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
        )

    a = [[eq1[0], eq1[1], eq1[2]],
         [eq2[0], eq2[1], eq2[2]],
         [eq3[0], eq3[1], eq3[2]]]

    d = det3(a)
    if d == 0:
        raise ValueError("System has no unique solution (determinant is zero).")

    dx = det3([[eq1[3], eq1[1], eq1[2]],
               [eq2[3], eq2[1], eq2[2]],
               [eq3[3], eq3[1], eq3[2]]])

    dy = det3([[eq1[0], eq1[3], eq1[2]],
               [eq2[0], eq2[3], eq2[2]],
               [eq3[0], eq3[3], eq3[2]]])

    dz = det3([[eq1[0], eq1[1], eq1[3]],
               [eq2[0], eq2[1], eq2[3]],
               [eq3[0], eq3[1], eq3[3]]])

    return (dx / d, dy / d, dz / d)


# ---------------------------------------------------------------------------
# Variant 2 -- Direct substitution for 2x2
# ---------------------------------------------------------------------------

def solve_substitution(equation1: list[float], equation2: list[float]) -> tuple[float, float]:
    """
    Solve 2x2 system by substitution: express x from eq1, substitute into eq2.

    >>> solve_substitution([0, 4, 50], [2, 0, 26])
    (13.0, 12.5)
    >>> solve_substitution([4, 7, 1], [1, 2, 0])
    (2.0, -1.0)
    >>> x, y = solve_substitution([11, 2, 30], [1, 0, 4])
    >>> (round(x, 10), round(y, 10))
    (4.0, -7.0)
    """
    a1, b1, d1 = equation1
    a2, b2, d2 = equation2

    # Try to express from equation with non-zero leading coefficient
    if a1 != 0:
        # x = (d1 - b1*y) / a1, substitute into eq2
        # a2*(d1 - b1*y)/a1 + b2*y = d2
        # y*(b2 - a2*b1/a1) = d2 - a2*d1/a1
        denom = b2 - a2 * b1 / a1
        if denom == 0:
            raise ValueError("No unique solution.")
        y = (d2 - a2 * d1 / a1) / denom
        x = (d1 - b1 * y) / a1
    elif b1 != 0:
        # y = (d1 - a1*x) / b1 = d1/b1, substitute
        y = d1 / b1
        if a2 == 0:
            raise ValueError("No unique solution.")
        x = (d2 - b2 * y) / a2
    elif a2 != 0 or b2 != 0:
        raise ValueError("First equation is degenerate.")
    else:
        raise ValueError("Both equations are degenerate.")

    return (float(x), float(y))


# ---------------------------------------------------------------------------
# Variant 3 -- Matrix inverse method for 2x2
# ---------------------------------------------------------------------------

def solve_inverse(equation1: list[float], equation2: list[float]) -> tuple[float, float]:
    """
    Solve 2x2 system using the matrix inverse: [x, y] = A^(-1) * [d1, d2].
    For 2x2: A^(-1) = (1/det) * [[d, -b], [-c, a]] where A = [[a, b], [c, d]].

    >>> solve_inverse([0, 4, 50], [2, 0, 26])
    (13.0, 12.5)
    >>> solve_inverse([11, 2, 30], [1, 0, 4])
    (4.0, -7.0)
    >>> solve_inverse([4, 7, 1], [1, 2, 0])
    (2.0, -1.0)
    """
    a, b, d1 = equation1
    c, d, d2 = equation2

    det = a * d - b * c
    if det == 0:
        raise ValueError("Matrix is singular, no unique solution.")

    x = (d * d1 - b * d2) / det
    y = (a * d2 - c * d1) / det
    return (float(x), float(y))


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    eq1, eq2 = [11, 2, 30], [1, 0, 4]
    number = 500_000
    print(f"Benchmark ({number} solves of 2x2 system):\n")

    funcs = [
        ("reference (Cramer's Rule)", lambda: reference(eq1, eq2)),
        ("substitution", lambda: solve_substitution(eq1, eq2)),
        ("matrix inverse", lambda: solve_inverse(eq1, eq2)),
        ("Cramer's 3x3", lambda: cramers_rule_3x3([1, 0, 0, 5], [0, 1, 0, 3], [0, 0, 1, 7])),
    ]

    for name, func in funcs:
        t = timeit.timeit(func, number=number)
        print(f"  {name:35s} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
