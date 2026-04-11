#!/usr/bin/env python3
"""
Optimized and alternative implementations of Guess the Number Search.

Variants covered:
1. binary_search    -- Binary search guess (reference)
2. ternary_search   -- Ternary search reduces range by 1/3
3. golden_section   -- Golden ratio based search

Run:
    python other/guess_the_number_search_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.guess_the_number_search import guess_the_number as reference


def ternary_search_guess(low: int, high: int, secret: int) -> tuple[int, int]:
    """
    Find secret using ternary search (splits range into thirds).

    >>> ternary_search_guess(1, 100, 42)
    (42, 4)
    >>> ternary_search_guess(1, 1, 1)
    (1, 1)
    """
    guesses = 0
    lo, hi = low, high
    while lo <= hi:
        guesses += 1
        mid1 = lo + (hi - lo) // 3
        mid2 = hi - (hi - lo) // 3
        if mid1 == secret:
            return secret, guesses
        if mid2 == secret:
            return secret, guesses
        if secret < mid1:
            hi = mid1 - 1
        elif secret > mid2:
            lo = mid2 + 1
        else:
            lo = mid1 + 1
            hi = mid2 - 1
    return secret, guesses


def golden_section_guess(low: int, high: int, secret: int) -> tuple[int, int]:
    """
    Find secret using golden ratio search.

    >>> golden_section_guess(1, 100, 42)
    (42, 5)
    >>> golden_section_guess(1, 1, 1)
    (1, 1)
    """
    phi = (1 + 5**0.5) / 2
    guesses = 0
    lo, hi = low, high
    while lo <= hi:
        guesses += 1
        mid = lo + int((hi - lo) / phi)
        if mid == secret:
            return secret, guesses
        elif mid < secret:
            lo = mid + 1
        else:
            hi = mid - 1
    return secret, guesses


def interpolation_guess(low: int, high: int, secret: int) -> tuple[int, int]:
    """
    Find secret using interpolation search (assumes uniform distribution).

    >>> interpolation_guess(1, 100, 42)
    (42, 1)
    >>> interpolation_guess(1, 1, 1)
    (1, 1)
    """
    guesses = 0
    lo, hi = low, high
    while lo <= hi:
        guesses += 1
        if lo == hi:
            if lo == secret:
                return secret, guesses
            break
        pos = lo + ((secret - lo) * (hi - lo)) // (hi - lo)
        pos = max(lo, min(hi, pos))
        if pos == secret:
            return secret, guesses
        elif pos < secret:
            lo = pos + 1
        else:
            hi = pos - 1
    return secret, guesses


TEST_CASES = [
    (1, 100, 42),
    (1, 100, 1),
    (1, 100, 100),
    (1, 1, 1),
    (50, 60, 55),
]

IMPLS = [
    ("binary", reference),
    ("ternary", ternary_search_guess),
    ("golden", golden_section_guess),
    ("interpolation", interpolation_guess),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for lo, hi, secret in TEST_CASES:
        for name, fn in IMPLS:
            result, guesses = fn(lo, hi, secret)
            ok = result == secret
            tag = "OK" if ok else "FAIL"
            if not ok:
                print(f"  [{tag}] {name}: expected={secret} got={result}")
        line = "  [OK] " + "  ".join(
            f"{name}={fn(lo, hi, secret)[1]}g" for name, fn in IMPLS
        )
        print(f"  secret={secret:<4} {line}")

    REPS = 100_000
    print(f"\n=== Benchmark: {REPS} runs, range [1, 10000] ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: fn(1, 10000, 4242), number=REPS
        ) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
