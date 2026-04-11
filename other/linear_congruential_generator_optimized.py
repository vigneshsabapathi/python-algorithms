#!/usr/bin/env python3
"""
Optimized and alternative implementations of Linear Congruential Generator.

Variants covered:
1. standard_lcg     -- X_{n+1} = (a*X_n + c) mod m (reference)
2. glibc_params     -- glibc parameters (a=1103515245, c=12345, m=2^31)
3. minstd_params    -- MINSTD (a=16807, c=0, m=2^31-1)
4. xorshift         -- Xorshift generator (non-LCG alternative)

Run:
    python other/linear_congruential_generator_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.linear_congruential_generator import LinearCongruentialGenerator as Reference


class MinstdGenerator:
    """
    MINSTD (Lehmer RNG): a=16807, c=0, m=2^31-1.

    >>> gen = MinstdGenerator(1)
    >>> gen.next()
    16807
    >>> gen.next()
    282475249
    """

    def __init__(self, seed: int = 1) -> None:
        self.state = seed

    def next(self) -> int:
        self.state = (16807 * self.state) % (2**31 - 1)
        return self.state

    def generate(self, n: int) -> list[int]:
        return [self.next() for _ in range(n)]


class XorshiftGenerator:
    """
    Xorshift32 pseudorandom number generator.

    >>> gen = XorshiftGenerator(42)
    >>> gen.next() > 0
    True
    """

    def __init__(self, seed: int = 42) -> None:
        self.state = seed & 0xFFFFFFFF
        if self.state == 0:
            self.state = 1

    def next(self) -> int:
        x = self.state
        x ^= (x << 13) & 0xFFFFFFFF
        x ^= (x >> 17) & 0xFFFFFFFF
        x ^= (x << 5) & 0xFFFFFFFF
        self.state = x & 0xFFFFFFFF
        return self.state

    def generate(self, n: int) -> list[int]:
        return [self.next() for _ in range(n)]


class MultiplyWithCarry:
    """
    Multiply-with-carry generator.

    >>> gen = MultiplyWithCarry(42)
    >>> gen.next() > 0
    True
    """

    def __init__(self, seed: int = 42) -> None:
        self.state = seed & 0xFFFFFFFF
        self.carry = 0

    def next(self) -> int:
        t = 698769069 * self.state + self.carry
        self.carry = (t >> 32) & 0xFFFFFFFF
        self.state = t & 0xFFFFFFFF
        return self.state

    def generate(self, n: int) -> list[int]:
        return [self.next() for _ in range(n)]


IMPLS = [
    ("glibc_lcg", lambda: Reference(seed=42)),
    ("minstd", lambda: MinstdGenerator(seed=42)),
    ("xorshift", lambda: XorshiftGenerator(seed=42)),
    ("mwc", lambda: MultiplyWithCarry(seed=42)),
]


def run_all() -> None:
    print("\n=== Sample output (first 5 values) ===")
    for name, factory in IMPLS:
        gen = factory()
        vals = gen.generate(5)
        print(f"  {name:<15} {vals}")

    N = 100_000
    REPS = 100
    print(f"\n=== Benchmark: {REPS} runs, generate {N} numbers ===")
    for name, factory in IMPLS:
        gen = factory()
        t = timeit.timeit(lambda: gen.generate(N), number=REPS) * 1000 / REPS
        print(f"  {name:<15} {t:>7.2f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
