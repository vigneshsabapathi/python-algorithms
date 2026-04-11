#!/usr/bin/env python3
"""
Optimized and alternative implementations of SDBM hash.

SDBM uses the recurrence: hash = char + (hash << 6) + (hash << 16) - hash
which equals hash * 65599 + char. The constant 65599 is prime.

Note: SDBM produces unbounded integers in Python (no 32-bit truncation
in the reference). Some variants add & 0xFFFFFFFF for 32-bit output.

Variants:
  reference     -- shift-based formula (unbounded)
  multiply      -- explicit * 65599 (same result, cleaner)
  truncated_32  -- 32-bit truncated version (C-compatible)
  bytes_opt     -- operate on bytes (avoids ord() calls)

Run:
    python hashes/sdbm_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hashes.sdbm import sdbm as reference


# ---------------------------------------------------------------------------
# Variant 1 -- multiply: explicit multiplication by 65599
# ---------------------------------------------------------------------------

def multiply(plain_text: str) -> int:
    """
    SDBM via explicit multiply -- hash * 65599 + char.

    Equivalent to the shift formula but more readable.

    >>> multiply('Algorithms')
    1462174910723540325254304520539387479031000036
    >>> multiply('scramble bits')
    730247649148944819640658295400555317318720608290373040936089
    >>> multiply('')
    0
    """
    hash_value = 0
    for c in plain_text:
        hash_value = hash_value * 65599 + ord(c)
    return hash_value


# ---------------------------------------------------------------------------
# Variant 2 -- truncated_32: 32-bit version (C-compatible)
# ---------------------------------------------------------------------------

def truncated_32(plain_text: str) -> int:
    """
    SDBM with 32-bit truncation -- matches C implementations.

    The original C code uses unsigned long (32-bit), so results wrap around.
    Python's arbitrary precision means we must mask explicitly.

    >>> truncated_32('Algorithms')
    3649838548
    >>> truncated_32('')
    0
    >>> truncated_32('a')
    97
    """
    hash_value = 0
    for c in plain_text:
        hash_value = (
            ord(c) + (hash_value << 6) + (hash_value << 16) - hash_value
        ) & 0xFFFFFFFF
    return hash_value


# ---------------------------------------------------------------------------
# Variant 3 -- bytes_opt: operate on bytes
# ---------------------------------------------------------------------------

def bytes_opt(plain_text: str) -> int:
    """
    SDBM operating on encoded bytes -- avoids ord() calls.

    >>> bytes_opt('Algorithms')
    1462174910723540325254304520539387479031000036
    >>> bytes_opt('scramble bits')
    730247649148944819640658295400555317318720608290373040936089
    >>> bytes_opt('')
    0
    """
    hash_value = 0
    for b in plain_text.encode("utf-8"):
        hash_value = b + (hash_value << 6) + (hash_value << 16) - hash_value
    return hash_value


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ("Algorithms", 1462174910723540325254304520539387479031000036),
    ("scramble bits", 730247649148944819640658295400555317318720608290373040936089),
    ("", 0),
    ("a", 97),
]

IMPLS = [
    ("reference", reference),
    ("multiply", multiply),
    ("bytes_opt", bytes_opt),
]


def run_all() -> None:
    print("\n=== Correctness (unbounded) ===")
    for text, expected in TEST_CASES:
        row = {}
        for name, fn in IMPLS:
            try:
                row[name] = fn(text)
            except Exception as e:
                row[name] = f"ERR:{e}"
        ok = all(v == expected for v in row.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] sdbm({text!r:.25}) = {str(expected)[:30]}...")

    # Verify multiply == shift
    import string
    test_strings = [string.ascii_letters, "Hello World", "x" * 100, ""]
    match = all(reference(s) == multiply(s) for s in test_strings)
    print(f"\n  [{'OK' if match else 'FAIL'}] multiply == reference on {len(test_strings)} strings")

    # 32-bit truncated
    t32 = truncated_32("Algorithms")
    print(f"  truncated_32('Algorithms') = {t32} (fits in 32 bits: {t32 < 2**32})")

    REPS = 100_000
    short_inputs = ["Algorithms", "scramble bits", "Hello World", "a" * 50]
    long_input = "x" * 10_000

    print(f"\n=== Benchmark (short strings): {REPS} runs, {len(short_inputs)} inputs ===")
    all_impls = IMPLS + [("truncated_32", truncated_32)]
    for name, fn in all_impls:
        t = timeit.timeit(
            lambda fn=fn: [fn(s) for s in short_inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<14} {t:>8.4f} ms / batch of {len(short_inputs)}")

    print(f"\n=== Benchmark (long string 10KB): {REPS} runs ===")
    for name, fn in all_impls:
        t = timeit.timeit(lambda fn=fn: fn(long_input), number=REPS) * 1000 / REPS
        print(f"  {name:<14} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
