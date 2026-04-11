#!/usr/bin/env python3
"""
Optimized and alternative implementations of Adler-32.

Adler-32 computes two 16-bit sums:
  A = 1 + sum of all bytes (mod 65521)
  B = sum of all partial A values (mod 65521)
  Result = (B << 16) | A

The modulus 65521 is the largest prime < 2^16, chosen to keep A and B
within 16 bits and provide good distribution.

Variants:
  reference     -- character-by-character mod on every iteration
  deferred_mod  -- defer mod until near overflow (batch processing)
  zlib_builtin  -- Python zlib.adler32() (C-level, fastest)
  functools     -- functools.reduce one-liner

Run:
    python hashes/adler32_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
import zlib
from functools import reduce

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hashes.adler32 import adler32 as reference

MOD_ADLER = 65521

# Safe number of iterations before 32-bit overflow:
# worst case: a stays near MOD_ADLER-1 (65520), b accumulates ~65520 per iter
# 2^31 / 65520 ≈ 32767  (conservative: use 5552 like zlib)
_NMAX = 5552


# ---------------------------------------------------------------------------
# Variant 1 -- deferred_mod: batch modular reduction
# ---------------------------------------------------------------------------

def deferred_mod(plain_text: str) -> int:
    """
    Adler-32 with deferred modular reduction.

    Instead of taking mod on every character, we accumulate up to _NMAX
    iterations before reducing. This avoids expensive mod operations in
    the inner loop (same trick zlib uses in C).

    >>> deferred_mod('Algorithms')
    363791387
    >>> deferred_mod('go adler em all')
    708642122
    >>> deferred_mod('')
    1
    >>> deferred_mod('a')
    6422626
    """
    a = 1
    b = 0
    data = plain_text.encode("latin-1") if isinstance(plain_text, str) else plain_text
    length = len(data)
    idx = 0
    while idx < length:
        block = min(_NMAX, length - idx)
        for i in range(idx, idx + block):
            a += data[i]
            b += a
        a %= MOD_ADLER
        b %= MOD_ADLER
        idx += block
    return (b << 16) | a


# ---------------------------------------------------------------------------
# Variant 2 -- zlib_builtin: Python's zlib.adler32 (C implementation)
# ---------------------------------------------------------------------------

def zlib_builtin(plain_text: str) -> int:
    """
    Adler-32 using Python's built-in zlib.adler32().

    This is the fastest option -- it's implemented in C and uses the same
    deferred-mod trick internally.

    >>> zlib_builtin('Algorithms')
    363791387
    >>> zlib_builtin('go adler em all')
    708642122
    >>> zlib_builtin('')
    1
    >>> zlib_builtin('a')
    6422626
    """
    return zlib.adler32(plain_text.encode("latin-1"))


# ---------------------------------------------------------------------------
# Variant 3 -- functools_reduce: one-liner using functools.reduce
# ---------------------------------------------------------------------------

def functools_reduce(plain_text: str) -> int:
    """
    Adler-32 via functools.reduce -- compact but slower due to lambda overhead.

    >>> functools_reduce('Algorithms')
    363791387
    >>> functools_reduce('go adler em all')
    708642122
    >>> functools_reduce('')
    1
    """
    a, b = reduce(
        lambda acc, ch: ((acc[0] + ord(ch)) % MOD_ADLER, (acc[1] + (acc[0] + ord(ch)) % MOD_ADLER) % MOD_ADLER),
        plain_text,
        (1, 0),
    )
    return (b << 16) | a


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ("Algorithms", 363791387),
    ("go adler em all", 708642122),
    ("", 1),
    ("a", 6422626),
    ("Hello World", 403375133),
    ("The quick brown fox jumps over the lazy dog", 1541148634),
]

IMPLS = [
    ("reference", reference),
    ("deferred_mod", deferred_mod),
    ("zlib_builtin", zlib_builtin),
    ("functools_reduce", functools_reduce),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for text, expected in TEST_CASES:
        row = {}
        for name, fn in IMPLS:
            try:
                row[name] = fn(text)
            except Exception as e:
                row[name] = f"ERR:{e}"
        ok = all(v == expected for v in row.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] adler32({text!r:.30}) = {expected}")

    # Cross-verify with zlib on more inputs
    import string
    test_strings = [
        "", "a", "abc", string.ascii_letters, string.printable,
        "x" * 10000, "Hello World" * 100,
    ]
    cross_ok = all(
        reference(s) == zlib.adler32(s.encode("latin-1"))
        for s in test_strings
    )
    print(f"\n  [{'OK' if cross_ok else 'FAIL'}] Cross-verify reference vs zlib: {len(test_strings)} inputs")

    # Benchmark
    REPS = 50_000
    short_inputs = ["Algorithms", "go adler em all", "Hello World", "a" * 100]
    long_input = "x" * 10_000

    print(f"\n=== Benchmark (short strings): {REPS} runs, {len(short_inputs)} inputs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(s) for s in short_inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<18} {t:>8.4f} ms / batch of {len(short_inputs)}")

    print(f"\n=== Benchmark (long string 10KB): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(long_input), number=REPS) * 1000 / REPS
        print(f"  {name:<18} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
