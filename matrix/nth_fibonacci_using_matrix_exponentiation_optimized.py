#!/usr/bin/env python3
"""
Optimized and alternative implementations of Nth Fibonacci via Matrix Exponentiation.

The reference uses 2x2 matrix exponentiation with O(log n) multiplications.
Each multiplication is O(1) for 2x2 matrices, so total is O(log n) for
fixed-precision arithmetic (O(log n * M(n)) with big integers where M(n)
is the cost of multiplying n-digit numbers).

Three alternatives:
  fast_doubling   -- F(2k) = F(k)[2F(k+1) - F(k)], F(2k+1) = F(k)^2 + F(k+1)^2
  tuple_matrix    -- Same matrix exponentiation but using tuples (less overhead)
  closed_form     -- Binet's formula (only accurate for small n due to float precision)

Run:
    python matrix/nth_fibonacci_using_matrix_exponentiation_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matrix.nth_fibonacci_using_matrix_exponentiation import (
    nth_fibonacci_matrix as reference,
    nth_fibonacci_bruteforce,
)


# ---------------------------------------------------------------------------
# Variant 1 -- Fast doubling: O(log n) with less overhead than matrix
# ---------------------------------------------------------------------------

def fibonacci_fast_doubling(n: int) -> int:
    """
    Fast doubling method. Uses the identities:
      F(2k)   = F(k) * [2*F(k+1) - F(k)]
      F(2k+1) = F(k)^2 + F(k+1)^2

    >>> fibonacci_fast_doubling(0)
    0
    >>> fibonacci_fast_doubling(1)
    1
    >>> fibonacci_fast_doubling(10)
    55
    >>> fibonacci_fast_doubling(100)
    354224848179261915075
    >>> fibonacci_fast_doubling(1000) == reference(1000)
    True
    """
    if n < 0:
        return n
    if n <= 1:
        return n

    def _fib(n: int) -> tuple[int, int]:
        """Return (F(n), F(n+1))."""
        if n == 0:
            return (0, 1)
        a, b = _fib(n >> 1)
        c = a * (2 * b - a)
        d = a * a + b * b
        if n & 1:
            return (d, c + d)
        return (c, d)

    return _fib(n)[0]


# ---------------------------------------------------------------------------
# Variant 2 -- Tuple-based matrix exponentiation (less overhead)
# ---------------------------------------------------------------------------

def fibonacci_tuple_matrix(n: int) -> int:
    """
    Matrix exponentiation using tuples instead of nested lists.
    Avoids list creation overhead.

    >>> fibonacci_tuple_matrix(0)
    0
    >>> fibonacci_tuple_matrix(1)
    1
    >>> fibonacci_tuple_matrix(10)
    55
    >>> fibonacci_tuple_matrix(100)
    354224848179261915075
    """
    if n < 0:
        return n
    if n <= 1:
        return n

    def mat_mul(a: tuple, b: tuple) -> tuple:
        """Multiply two 2x2 matrices stored as (a,b,c,d) for [[a,b],[c,d]]."""
        return (
            a[0]*b[0] + a[1]*b[2],
            a[0]*b[1] + a[1]*b[3],
            a[2]*b[0] + a[3]*b[2],
            a[2]*b[1] + a[3]*b[3],
        )

    result = (1, 0, 0, 1)  # Identity
    base = (1, 1, 1, 0)    # Fibonacci matrix
    n -= 1
    while n > 0:
        if n & 1:
            result = mat_mul(result, base)
        base = mat_mul(base, base)
        n >>= 1

    return result[0]


# ---------------------------------------------------------------------------
# Variant 3 -- Binet's formula (closed form, float precision limited)
# ---------------------------------------------------------------------------

def fibonacci_binet(n: int) -> int:
    """
    Binet's formula: F(n) = (phi^n - psi^n) / sqrt(5).
    Only accurate for n < ~70 due to floating point precision.

    >>> fibonacci_binet(0)
    0
    >>> fibonacci_binet(1)
    1
    >>> fibonacci_binet(10)
    55
    >>> fibonacci_binet(20)
    6765
    """
    if n < 0:
        return n
    if n <= 1:
        return n
    sqrt5 = 5 ** 0.5
    phi = (1 + sqrt5) / 2
    psi = (1 - sqrt5) / 2
    return round((phi ** n - psi ** n) / sqrt5)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    number = 100_000
    test_n = 100
    print(f"Benchmark ({number} computations of F({test_n})):\n")

    funcs = [
        ("reference (matrix exponentiation)", lambda: reference(test_n)),
        ("bruteforce (iterative)", lambda: nth_fibonacci_bruteforce(test_n)),
        ("fast_doubling", lambda: fibonacci_fast_doubling(test_n)),
        ("tuple_matrix", lambda: fibonacci_tuple_matrix(test_n)),
        ("binet (float, n<70 accurate)", lambda: fibonacci_binet(min(test_n, 60))),
    ]

    for name, func in funcs:
        t = timeit.timeit(func, number=number)
        print(f"  {name:42s} {t:.4f}s")

    print(f"\nLarge n test (F(10000)):")
    for name, func in [
        ("reference", lambda: reference(10000)),
        ("fast_doubling", lambda: fibonacci_fast_doubling(10000)),
        ("tuple_matrix", lambda: fibonacci_tuple_matrix(10000)),
    ]:
        t = timeit.timeit(func, number=100)
        print(f"  {name:42s} {t:.4f}s (100 runs)")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
