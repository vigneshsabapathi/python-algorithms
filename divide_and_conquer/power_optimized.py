#!/usr/bin/env python3
"""
Optimized and alternative implementations of Fast Power.

The reference uses recursive exponentiation by squaring: O(log n).

Three variants:
  iterative       — iterative binary exponentiation (no call stack)
  builtin_pow     — Python's built-in pow(x, n) (C-level, handles big ints)
  modular_power   — modular exponentiation for cryptography (RSA, DH)

Run:
    python divide_and_conquer/power_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from divide_and_conquer.power import power as reference
from divide_and_conquer.power import power_iterative, power_mod


# ---------------------------------------------------------------------------
# Variant 1 — Python builtin pow (C-level, optimized)
# ---------------------------------------------------------------------------

def builtin_pow(x: int | float, n: int) -> int | float:
    """
    Use Python's built-in pow() — C-level implementation.
    For integers, this uses binary exponentiation internally.

    >>> builtin_pow(2, 10)
    1024
    >>> builtin_pow(2, 0)
    1
    >>> builtin_pow(3, 3)
    27
    >>> builtin_pow(2, -3)
    0.125
    >>> builtin_pow(-2, 3)
    -8
    """
    if n < 0:
        return 1.0 / pow(x, -n)
    return pow(x, n)


# ---------------------------------------------------------------------------
# Variant 2 — Bit-manipulation iterative (explicit bit scanning)
# ---------------------------------------------------------------------------

def bit_scan_power(x: int | float, n: int) -> int | float:
    """
    Exponentiation by scanning bits of n from MSB to LSB.
    Same O(log n) but scans left-to-right (MSB first).

    >>> bit_scan_power(2, 10)
    1024
    >>> bit_scan_power(2, 0)
    1
    >>> bit_scan_power(3, 3)
    27
    >>> bit_scan_power(-2, 4)
    16
    """
    if n < 0:
        return 1.0 / bit_scan_power(x, -n)
    if n == 0:
        return 1

    # Find the highest bit
    result = 1
    bits = bin(n)[2:]  # e.g. '1010' for n=10
    for bit in bits:
        result = result * result
        if bit == '1':
            result *= x
    return result


# ---------------------------------------------------------------------------
# Variant 3 — Matrix exponentiation (for Fibonacci, linear recurrences)
# ---------------------------------------------------------------------------

def matrix_power(mat: list[list[int]], n: int) -> list[list[int]]:
    """
    Raise a square matrix to the nth power using binary exponentiation.
    Key technique for computing Fibonacci in O(log n).

    >>> matrix_power([[1, 1], [1, 0]], 10)
    [[89, 55], [55, 34]]
    >>> matrix_power([[1, 0], [0, 1]], 100)
    [[1, 0], [0, 1]]
    """
    size = len(mat)

    def mat_mul(a, b):
        return [
            [sum(a[i][k] * b[k][j] for k in range(size)) for j in range(size)]
            for i in range(size)
        ]

    # Identity matrix
    result = [[1 if i == j else 0 for j in range(size)] for i in range(size)]

    base = [row[:] for row in mat]
    while n > 0:
        if n % 2 == 1:
            result = mat_mul(result, base)
        base = mat_mul(base, base)
        n //= 2
    return result


def fibonacci_fast(n: int) -> int:
    """
    Compute nth Fibonacci number in O(log n) via matrix exponentiation.
    F(n) = [[1,1],[1,0]]^n [0][1]

    >>> fibonacci_fast(0)
    0
    >>> fibonacci_fast(1)
    1
    >>> fibonacci_fast(10)
    55
    >>> fibonacci_fast(50)
    12586269025
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1
    result = matrix_power([[1, 1], [1, 0]], n)
    return result[0][1]


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (2, 0, 1),
    (2, 1, 2),
    (2, 10, 1024),
    (3, 3, 27),
    (5, 4, 625),
    (-2, 3, -8),
    (-2, 4, 16),
    (0, 5, 0),
    (1, 1000, 1),
]

IMPLS = [
    ("reference", reference),
    ("iterative", power_iterative),
    ("builtin", builtin_pow),
    ("bit_scan", bit_scan_power),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for x, n, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            results[name] = fn(x, n)
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] {x}^{n}={expected}  "
              + "  ".join(f"{nm}={v}" for nm, v in results.items()))

    # Modular power
    print(f"\n  mod_power(2, 100, 1e9+7) = {power_mod(2, 100, 10**9 + 7)}")
    print(f"  fibonacci_fast(50) = {fibonacci_fast(50)}")

    # Matrix power correctness
    fib_ok = all(fibonacci_fast(i) == [0,1,1,2,3,5,8,13,21,34][i] for i in range(10))
    print(f"  [{'OK' if fib_ok else 'FAIL'}] fibonacci_fast(0..9)")

    REPS = 100_000
    exponents = [10, 100, 1000]

    for n in exponents:
        print(f"\n=== Benchmark x=2, n={n}, {REPS} runs ===")
        for name, fn in IMPLS:
            t = timeit.timeit(lambda fn=fn: fn(2, n), number=REPS) * 1000 / REPS
            print(f"  {name:<14} {t:>8.5f} ms")

    # Modular benchmark
    print(f"\n=== Modular Power Benchmark: 2^n mod (10^9+7), {REPS} runs ===")
    MOD = 10**9 + 7
    for n in [1000, 10000, 100000]:
        t = timeit.timeit(lambda: power_mod(2, n, MOD), number=REPS) * 1000 / REPS
        print(f"  mod_power n={n:<8} {t:>8.5f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
