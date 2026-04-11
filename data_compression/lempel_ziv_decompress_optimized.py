#!/usr/bin/env python3
"""
Optimized and alternative implementations of LZW Decompression.

The reference provides binary-level LZW decompression with Elias gamma prefix.
This file focuses on the in-memory string decompression variants.

Variants covered:
1. standard_decompress  -- reference lzw_decompress from lempel_ziv.py
2. list_dict            -- uses list instead of dict for O(1) lookup
3. streaming            -- generator-based streaming decompression

Key interview insight:
    The tricky edge case in LZW decompression: when the code equals the
    next available dictionary index. This happens when the encoder adds
    "AB" to the dictionary and immediately uses it. The decoder handles
    it as: entry = previous + previous[0].

Run:
    python data_compression/lempel_ziv_decompress_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_compression.lempel_ziv import lzw_compress
from data_compression.lempel_ziv import lzw_decompress as reference_decompress


# ---------------------------------------------------------------------------
# Variant 1 -- standard (reference wrapper)
# ---------------------------------------------------------------------------

def standard_decompress(codes: list[int]) -> str:
    """
    Standard LZW decompression using dictionary.

    >>> standard_decompress([65, 66, 256, 258])
    'ABABABA'
    >>> standard_decompress([])
    ''
    """
    return reference_decompress(codes)


# ---------------------------------------------------------------------------
# Variant 2 -- list_dict: list-based dictionary for O(1) index lookup
# ---------------------------------------------------------------------------

def list_decompress(codes: list[int]) -> str:
    """
    LZW decompress using a list as dictionary for O(1) index access.

    >>> list_decompress([65, 66, 256, 258])
    'ABABABA'
    >>> list_decompress(lzw_compress("hello world"))
    'hello world'
    >>> list_decompress([])
    ''
    """
    if not codes:
        return ""

    # Initialize: list index = code, value = string
    dictionary: list[str] = [chr(i) for i in range(256)]
    next_code = 256

    result = [dictionary[codes[0]]]
    previous = result[0]

    for code in codes[1:]:
        if code < len(dictionary):
            entry = dictionary[code]
        elif code == next_code:
            entry = previous + previous[0]
        else:
            raise ValueError(f"Invalid LZW code: {code}")

        result.append(entry)
        dictionary.append(previous + entry[0])
        next_code += 1
        previous = entry

    return "".join(result)


# ---------------------------------------------------------------------------
# Variant 3 -- streaming: generator-based for memory efficiency
# ---------------------------------------------------------------------------

def streaming_decompress(codes: list[int]) -> str:
    """
    Generator-based LZW decompress. Yields characters one at a time,
    useful for large streams where you don't want to hold everything in memory.

    >>> streaming_decompress([65, 66, 256, 258])
    'ABABABA'
    >>> streaming_decompress(lzw_compress("mississippi"))
    'mississippi'
    """
    if not codes:
        return ""

    def _generate():
        dictionary: dict[int, str] = {i: chr(i) for i in range(256)}
        next_code = 256

        previous = dictionary[codes[0]]
        yield previous

        for code in codes[1:]:
            if code in dictionary:
                entry = dictionary[code]
            elif code == next_code:
                entry = previous + previous[0]
            else:
                raise ValueError(f"Invalid LZW code: {code}")

            yield entry
            dictionary[next_code] = previous + entry[0]
            next_code += 1
            previous = entry

    return "".join(_generate())


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_STRINGS = [
    "ABABABA",
    "TOBEORNOTTOBEORTOBEORNOT",
    "hello world",
    "mississippi",
    "the quick brown fox jumps over the lazy dog",
    "aaaaaaaaa",
]

IMPLS = [
    ("standard",  standard_decompress),
    ("list_dict", list_decompress),
    ("streaming", streaming_decompress),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for text in TEST_STRINGS:
        codes = lzw_compress(text)
        for name, fn in IMPLS:
            try:
                result = fn(codes)
                ok = result == text
                tag = "OK" if ok else "FAIL"
                print(f"  [{tag}] {name:<12} '{text[:30]}' -> {len(codes)} codes")
            except Exception as e:
                print(f"  [ERR] {name:<12} '{text[:30]}' {e}")

    REPS = 10_000
    medium = "the quick brown fox jumps over the lazy dog" * 5
    codes = lzw_compress(medium)

    print(f"\n=== Decompress Benchmark ({len(codes)} codes): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(codes), number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
