#!/usr/bin/env python3
"""
Optimized and alternative implementations of Narcissistic Number check.

Variants covered:
1. is_narcissistic_precompute  -- precomputed power table
2. is_narcissistic_math        -- no string conversion, pure arithmetic
3. is_narcissistic_cache       -- digit-power cache across calls

Run:
    python dynamic_programming/narcissistic_number_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.narcissistic_number import is_narcissistic as reference


# ---------------------------------------------------------------------------
# Variant 1 — Precomputed power table
# ---------------------------------------------------------------------------

def is_narcissistic_precompute(n: int) -> bool:
    """
    Narcissistic check with precomputed digit powers.

    >>> is_narcissistic_precompute(153)
    True
    >>> is_narcissistic_precompute(370)
    True
    >>> is_narcissistic_precompute(9474)
    True
    >>> is_narcissistic_precompute(9475)
    False
    >>> is_narcissistic_precompute(1)
    True
    >>> is_narcissistic_precompute(10)
    False
    """
    if n < 0:
        return False
    digits = str(n)
    power = len(digits)
    # Precompute 0^p through 9^p
    powers = [d ** power for d in range(10)]
    return sum(powers[int(d)] for d in digits) == n


# ---------------------------------------------------------------------------
# Variant 2 — Pure arithmetic (no string conversion)
# ---------------------------------------------------------------------------

def is_narcissistic_math(n: int) -> bool:
    """
    Narcissistic check using only arithmetic operations.

    >>> is_narcissistic_math(153)
    True
    >>> is_narcissistic_math(370)
    True
    >>> is_narcissistic_math(9474)
    True
    >>> is_narcissistic_math(9475)
    False
    >>> is_narcissistic_math(0)
    True
    >>> is_narcissistic_math(10)
    False
    """
    if n < 0:
        return False
    if n == 0:
        return True

    # Count digits
    temp = n
    num_digits = 0
    while temp > 0:
        num_digits += 1
        temp //= 10

    # Sum of digit^power
    temp = n
    total = 0
    while temp > 0:
        digit = temp % 10
        total += digit ** num_digits
        temp //= 10

    return total == n


# ---------------------------------------------------------------------------
# Variant 3 — Cached power lookup
# ---------------------------------------------------------------------------

_POWER_CACHE: dict[tuple[int, int], int] = {}


def is_narcissistic_cache(n: int) -> bool:
    """
    Narcissistic check with a global cache for digit powers.

    Amortizes repeated calls (e.g., finding all narcissistic numbers).

    >>> is_narcissistic_cache(153)
    True
    >>> is_narcissistic_cache(370)
    True
    >>> is_narcissistic_cache(9474)
    True
    >>> is_narcissistic_cache(9475)
    False
    >>> is_narcissistic_cache(0)
    True
    """
    if n < 0:
        return False
    digits = str(n)
    power = len(digits)
    total = 0
    for d in digits:
        key = (int(d), power)
        if key not in _POWER_CACHE:
            _POWER_CACHE[key] = int(d) ** power
        total += _POWER_CACHE[key]
    return total == n


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (153, True), (370, True), (9474, True),
    (9475, False), (1, True), (0, True), (10, False),
]

IMPLS = [
    ("reference", reference),
    ("precompute", is_narcissistic_precompute),
    ("math", is_narcissistic_math),
    ("cache", is_narcissistic_cache),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for n, expected in TEST_CASES:
        results = {name: fn(n) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] n={n}  expected={expected}  " +
              "  ".join(f"{name}={v}" for name, v in results.items()))

    REPS = 50_000
    bench_vals = [153, 370, 9474, 9475, 12345, 54748]
    print(f"\n=== Benchmark: {REPS} runs, batch of {len(bench_vals)} ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(v) for v in bench_vals], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<14} {t:>8.4f} ms / batch")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
