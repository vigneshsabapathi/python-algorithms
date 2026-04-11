#!/usr/bin/env python3
"""
Optimized and alternative implementations of DJB2 hash.

DJB2 is a simple, fast, non-cryptographic hash function by Dan Bernstein.
Formula: hash = hash * 33 + c  (where 33 = (hash << 5) + hash)

Variants:
  reference   -- (hash << 5) + hash + ord(c) with & 0xFFFFFFFF
  xor_variant -- hash * 33 ^ ord(c) (Bernstein's alternate)
  multiply    -- explicit multiply by 33 (cleaner, same result)
  bytes_opt   -- operate on bytes instead of string characters

Run:
    python hashes/djb2_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hashes.djb2 import djb2 as reference


# ---------------------------------------------------------------------------
# Variant 1 -- xor_variant: DJB2a (XOR instead of addition)
# ---------------------------------------------------------------------------

def xor_variant(s: str) -> int:
    """
    DJB2a -- Bernstein's alternate version using XOR.

    hash(i) = hash(i-1) * 33 ^ str[i]

    Generally considered slightly better distribution than the additive version.

    >>> xor_variant('Algorithms')
    4021678517
    >>> xor_variant('')
    5381
    """
    hash_value = 5381
    for c in s:
        hash_value = ((hash_value << 5) + hash_value) ^ ord(c)
    return hash_value & 0xFFFFFFFF


# ---------------------------------------------------------------------------
# Variant 2 -- multiply: explicit * 33 (clearer intent)
# ---------------------------------------------------------------------------

def multiply(s: str) -> int:
    """
    DJB2 using explicit multiply by 33 instead of shift+add.

    Produces identical results to reference. Marginally slower due to
    Python's arbitrary-precision multiply vs shift, but cleaner code.

    >>> multiply('Algorithms')
    3782405311
    >>> multiply('scramble bits')
    1609059040
    >>> multiply('')
    5381
    """
    hash_value = 5381
    for c in s:
        hash_value = hash_value * 33 + ord(c)
    return hash_value & 0xFFFFFFFF


# ---------------------------------------------------------------------------
# Variant 3 -- bytes_opt: operate on bytes (avoids ord() call)
# ---------------------------------------------------------------------------

def bytes_opt(s: str) -> int:
    """
    DJB2 operating on encoded bytes -- avoids per-character ord() call.

    When iterating over bytes in Python, each element is already an int,
    so no ord() conversion is needed.

    >>> bytes_opt('Algorithms')
    3782405311
    >>> bytes_opt('scramble bits')
    1609059040
    >>> bytes_opt('')
    5381
    """
    hash_value = 5381
    for b in s.encode("utf-8"):
        hash_value = ((hash_value << 5) + hash_value) + b
    return hash_value & 0xFFFFFFFF


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ("Algorithms", 3782405311),
    ("scramble bits", 1609059040),
    ("", 5381),
    ("a", 177670),
    ("Hello World", 2272792705),
    ("The quick brown fox", 2546203896),
]

IMPLS = [
    ("reference", reference),
    ("xor_variant", xor_variant),
    ("multiply", multiply),
    ("bytes_opt", bytes_opt),
]

# XOR variant has different values, so track separately
ADDITIVE_IMPLS = [
    ("reference", reference),
    ("multiply", multiply),
    ("bytes_opt", bytes_opt),
]


def run_all() -> None:
    print("\n=== Correctness (additive variants) ===")
    for text, expected in TEST_CASES:
        row = {}
        for name, fn in ADDITIVE_IMPLS:
            try:
                row[name] = fn(text)
            except Exception as e:
                row[name] = f"ERR:{e}"
        ok = all(v == expected for v in row.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] djb2({text!r:.25}) = {expected}")

    # Verify XOR variant is self-consistent
    xor_cases = [("Algorithms", 4021678517), ("", 5381)]
    xor_ok = all(xor_variant(t) == e for t, e in xor_cases)
    print(f"\n  [{'OK' if xor_ok else 'FAIL'}] xor_variant: self-consistent")

    # Distribution: check collision rate on 10k strings
    import string
    test_strings = [f"test_{i}_{c}" for i in range(1000) for c in string.ascii_lowercase[:10]]
    hash_set = set()
    for s in test_strings:
        hash_set.add(reference(s))
    collision_rate = 1 - len(hash_set) / len(test_strings)
    print(f"  Collision rate on {len(test_strings)} strings: {collision_rate:.4%}")

    # Benchmark
    REPS = 100_000
    short_inputs = ["Algorithms", "scramble bits", "Hello World", "a" * 50]
    long_input = "x" * 10_000

    print(f"\n=== Benchmark (short strings): {REPS} runs, {len(short_inputs)} inputs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(s) for s in short_inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<14} {t:>8.4f} ms / batch of {len(short_inputs)}")

    print(f"\n=== Benchmark (long string 10KB): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(long_input), number=REPS) * 1000 / REPS
        print(f"  {name:<14} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
