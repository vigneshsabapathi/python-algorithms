#!/usr/bin/env python3
"""
Optimized and alternative implementations of the ELF hash.

ELF hash (from UNIX ELF format) is a variant of PJW hash that operates on
32-bit values. It shifts left by 4, adds the character, and folds high bits
back into the hash.

Variants:
  reference     -- standard ELF hash from TheAlgorithms
  pjw_original  -- Peter J. Weinberger's original PJW hash
  bytes_opt     -- operates on bytes (avoids ord() calls)
  one_liner     -- compact functools.reduce version

Run:
    python hashes/elf_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from functools import reduce

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hashes.elf import elf_hash as reference


# ---------------------------------------------------------------------------
# Variant 1 -- pjw_original: Weinberger's PJW hash (ELF is derived from this)
# ---------------------------------------------------------------------------

def pjw_original(data: str) -> int:
    """
    Peter J. Weinberger's original hash function.

    ELF hash is a specific parametrization of PJW for 32-bit words.
    PJW uses: bits_in_word=32, three_quarters=24, one_eighth=4, high_bits=0xF0000000

    >>> pjw_original('lorem ipsum')
    253956621
    >>> pjw_original('')
    0
    >>> pjw_original('a')
    97
    """
    bits_in_word = 32
    three_quarters = (bits_in_word * 3) // 4  # 24
    one_eighth = bits_in_word // 8  # 4
    high_bits = 0xFFFFFFFF << (bits_in_word - one_eighth)  # 0xF0000000

    hash_ = 0
    for char in data:
        hash_ = (hash_ << one_eighth) + ord(char)
        test = hash_ & high_bits
        if test != 0:
            hash_ = (hash_ ^ (test >> three_quarters)) & ~test
    return hash_


# ---------------------------------------------------------------------------
# Variant 2 -- bytes_opt: operate on encoded bytes
# ---------------------------------------------------------------------------

def bytes_opt(data: str) -> int:
    """
    ELF hash operating on bytes -- avoids per-character ord() call.

    >>> bytes_opt('lorem ipsum')
    253956621
    >>> bytes_opt('')
    0
    >>> bytes_opt('a')
    97
    """
    hash_ = 0
    for b in data.encode("utf-8"):
        hash_ = (hash_ << 4) + b
        x = hash_ & 0xF0000000
        if x != 0:
            hash_ ^= x >> 24
        hash_ &= ~x
    return hash_


# ---------------------------------------------------------------------------
# Variant 3 -- one_liner: functools.reduce version
# ---------------------------------------------------------------------------

def one_liner(data: str) -> int:
    """
    ELF hash via functools.reduce -- compact but slower.

    >>> one_liner('lorem ipsum')
    253956621
    >>> one_liner('')
    0
    """
    def step(h: int, c: str) -> int:
        h = (h << 4) + ord(c)
        x = h & 0xF0000000
        if x:
            h ^= x >> 24
        return h & ~x

    return reduce(step, data, 0)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ("lorem ipsum", 253956621),
    ("", 0),
    ("a", 97),
    ("Hello World", 18131988),
    ("The quick brown fox jumps over the lazy dog", 69733463),
]

IMPLS = [
    ("reference", reference),
    ("pjw_original", pjw_original),
    ("bytes_opt", bytes_opt),
    ("one_liner", one_liner),
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
        print(f"  [{tag}] elf_hash({text!r:.30}) = {expected}")

    # Collision test
    test_strings = [f"sym_{i}" for i in range(10000)]
    hash_set = set(reference(s) for s in test_strings)
    collision_rate = 1 - len(hash_set) / len(test_strings)
    print(f"\n  Collision rate on {len(test_strings)} symbol names: {collision_rate:.4%}")

    REPS = 100_000
    short_inputs = ["lorem ipsum", "Hello World", "main", "__init__"]

    print(f"\n=== Benchmark (short strings): {REPS} runs, {len(short_inputs)} inputs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(s) for s in short_inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<14} {t:>8.4f} ms / batch of {len(short_inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
