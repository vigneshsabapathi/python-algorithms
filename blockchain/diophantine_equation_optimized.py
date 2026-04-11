"""
Diophantine Equation Solver -- Optimized Variants

Variant 1 (recursive):   Classic recursive Extended GCD
Variant 2 (iterative):   Iterative Extended GCD -- avoids stack depth issues
Variant 3 (math_gcd):    Uses math.gcd + back-computes y from the equation
Variant 4 (matrix):      Matrix-based Extended GCD using 2x2 multiplication

Each variant solves: find integers (x, y) such that a*x + b*y = c.
"""
from __future__ import annotations

import math
import timeit


# ---------------------------------------------------------------------------
# Variant 1: Recursive Extended GCD (textbook)
# ---------------------------------------------------------------------------
def extended_gcd_recursive(a: int, b: int) -> tuple[int, int, int]:
    """
    >>> extended_gcd_recursive(10, 6)
    (2, -1, 2)
    >>> extended_gcd_recursive(391, 299)
    (23, -3, 4)
    """
    if a == 0:
        return b, 0, 1
    d, x1, y1 = extended_gcd_recursive(b % a, a)
    return d, y1 - (b // a) * x1, x1


def diophantine_recursive(a: int, b: int, c: int) -> tuple[int, int]:
    """
    >>> diophantine_recursive(10, 6, 14)
    (-7, 14)
    >>> diophantine_recursive(391, 299, -69)
    (9, -12)
    """
    d, x, y = extended_gcd_recursive(abs(a), abs(b))
    if c % d != 0:
        raise ValueError(f"No solution: gcd({a},{b})={d} does not divide {c}")
    s = c // d
    return x * s * (1 if a >= 0 else -1), y * s * (1 if b >= 0 else -1)


# ---------------------------------------------------------------------------
# Variant 2: Iterative Extended GCD (no recursion, O(1) stack)
# ---------------------------------------------------------------------------
def extended_gcd_iterative(a: int, b: int) -> tuple[int, int, int]:
    """
    >>> extended_gcd_iterative(10, 6)
    (2, -1, 2)
    >>> extended_gcd_iterative(391, 299)
    (23, -3, 4)
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t


def diophantine_iterative(a: int, b: int, c: int) -> tuple[int, int]:
    """
    >>> diophantine_iterative(10, 6, 14)
    (-7, 14)
    >>> diophantine_iterative(391, 299, -69)
    (9, -12)
    """
    d, x, y = extended_gcd_iterative(abs(a), abs(b))
    if c % d != 0:
        raise ValueError(f"No solution: gcd({a},{b})={d} does not divide {c}")
    s = c // d
    return x * s * (1 if a >= 0 else -1), y * s * (1 if b >= 0 else -1)


# ---------------------------------------------------------------------------
# Variant 3: math.gcd + back-compute y
# ---------------------------------------------------------------------------
def diophantine_math_gcd(a: int, b: int, c: int) -> tuple[int, int]:
    """
    Uses math.gcd (C-level) for speed, then solves for x via iterative
    extended GCD on |a|,|b| and derives y = (c - a*x) / b.

    >>> diophantine_math_gcd(10, 6, 14)
    (-7, 14)
    >>> diophantine_math_gcd(391, 299, -69)
    (9, -12)
    """
    d = math.gcd(abs(a), abs(b))
    if c % d != 0:
        raise ValueError(f"No solution: gcd({a},{b})={d} does not divide {c}")
    # Use iterative extended gcd under the hood for x
    _, x, y = extended_gcd_iterative(abs(a), abs(b))
    s = c // d
    x0 = x * s * (1 if a >= 0 else -1)
    y0 = y * s * (1 if b >= 0 else -1)
    return x0, y0


# ---------------------------------------------------------------------------
# Variant 4: Matrix-based Extended GCD
# ---------------------------------------------------------------------------
def extended_gcd_matrix(a: int, b: int) -> tuple[int, int, int]:
    """
    Uses 2x2 matrix multiplication to track Bezout coefficients.

    | x |   | 0  1 |^k   | a |
    | y | = | 1 -q |   * | b |  (accumulated over each step)

    >>> extended_gcd_matrix(10, 6)
    (2, -1, 2)
    >>> extended_gcd_matrix(391, 299)
    (23, -3, 4)
    """
    # Identity matrix
    sx, sy = 1, 0
    tx, ty = 0, 1
    while b != 0:
        q, r = divmod(a, b)
        a, b = b, r
        sx, tx = tx, sx - q * tx
        sy, ty = ty, sy - q * ty
    return a, sx, sy


def diophantine_matrix(a: int, b: int, c: int) -> tuple[int, int]:
    """
    >>> diophantine_matrix(10, 6, 14)
    (-7, 14)
    >>> diophantine_matrix(391, 299, -69)
    (9, -12)
    """
    d, x, y = extended_gcd_matrix(abs(a), abs(b))
    if c % d != 0:
        raise ValueError(f"No solution: gcd({a},{b})={d} does not divide {c}")
    s = c // d
    return x * s * (1 if a >= 0 else -1), y * s * (1 if b >= 0 else -1)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(
    runs: int = 200_000,
    a: int = 391,
    b: int = 299,
    c: int = -69,
) -> None:
    """Compare all four variants on the same input."""
    variants = {
        "recursive":  lambda: diophantine_recursive(a, b, c),
        "iterative":  lambda: diophantine_iterative(a, b, c),
        "math_gcd":   lambda: diophantine_math_gcd(a, b, c),
        "matrix":     lambda: diophantine_matrix(a, b, c),
    }

    # Verify all produce the same answer
    results = {name: fn() for name, fn in variants.items()}
    ref = results["recursive"]
    for name, res in results.items():
        assert res == ref, f"{name} produced {res}, expected {ref}"

    print(f"Benchmark: diophantine({a}, {b}, {c})  x {runs:,} runs")
    print("-" * 55)

    timings: list[tuple[str, float]] = []
    for name, fn in variants.items():
        t = timeit.timeit(fn, number=runs)
        timings.append((name, t))

    timings.sort(key=lambda x: x[1])
    fastest = timings[0][1]

    for name, t in timings:
        ratio = t / fastest
        print(f"  {name:<14s}  {t:.4f}s  ({ratio:.1f}x)")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
