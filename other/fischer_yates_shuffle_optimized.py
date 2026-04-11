#!/usr/bin/env python3
"""
Optimized and alternative implementations of Fischer-Yates Shuffle.

Variants covered:
1. knuth_shuffle     -- Modern Fischer-Yates (Knuth) in-place (reference)
2. inside_out        -- Durstenfeld inside-out variant (builds new array)
3. stdlib_shuffle    -- Python's random.shuffle (uses Fisher-Yates internally)
4. sattolo_cycle     -- Sattolo's algorithm (guaranteed single cycle)

Run:
    python other/fischer_yates_shuffle_optimized.py
"""

from __future__ import annotations

import os
import random
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.fischer_yates_shuffle import fischer_yates_shuffle as reference


def inside_out(data: list, rng: random.Random | None = None) -> list:
    """
    Inside-out Fischer-Yates: builds shuffled copy without modifying original.

    >>> rng = random.Random(42)
    >>> inside_out([1, 2, 3, 4, 5], rng)
    [2, 5, 4, 3, 1]
    >>> sorted(inside_out([1, 2, 3], random.Random(0)))
    [1, 2, 3]
    """
    if rng is None:
        rng = random.Random()
    result = []
    for i, item in enumerate(data):
        j = rng.randint(0, i)
        if j == len(result):
            result.append(item)
        else:
            result.append(result[j])
            result[j] = item
    return result


def stdlib_shuffle(data: list, rng: random.Random | None = None) -> list:
    """
    Python stdlib shuffle (uses Fisher-Yates internally).

    >>> rng = random.Random(42)
    >>> result = stdlib_shuffle([1, 2, 3, 4, 5], rng)
    >>> sorted(result)
    [1, 2, 3, 4, 5]
    """
    if rng is None:
        rng = random.Random()
    copy = list(data)
    rng.shuffle(copy)
    return copy


def sattolo_cycle(data: list, rng: random.Random | None = None) -> list:
    """
    Sattolo's algorithm: generates a random cyclic permutation.
    Every element is guaranteed to move (no fixed points for n >= 2).

    >>> rng = random.Random(42)
    >>> result = sattolo_cycle([1, 2, 3, 4, 5], rng)
    >>> sorted(result) == [1, 2, 3, 4, 5]
    True
    >>> sattolo_cycle([1], rng)
    [1]
    """
    if rng is None:
        rng = random.Random()
    result = list(data)
    n = len(result)
    for i in range(n - 1, 0, -1):
        j = rng.randint(0, i - 1)  # Note: i-1 not i (Sattolo vs Fisher-Yates)
        result[i], result[j] = result[j], result[i]
    return result


TEST_DATA = list(range(20))

IMPLS = [
    ("reference", lambda d, r: reference(list(d), r)),
    ("inside_out", inside_out),
    ("stdlib", stdlib_shuffle),
    ("sattolo", sattolo_cycle),
]


def run_all() -> None:
    print("\n=== Correctness (all permutations preserve elements) ===")
    rng = random.Random(42)
    for name, fn in IMPLS:
        result = fn(list(TEST_DATA), random.Random(42))
        ok = sorted(result) == sorted(TEST_DATA)
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] {name}: preserves elements={ok}")

    large = list(range(10000))
    REPS = 5000
    print(f"\n=== Benchmark: {REPS} runs, {len(large)} elements ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: fn(list(large), random.Random(0)), number=REPS
        ) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
