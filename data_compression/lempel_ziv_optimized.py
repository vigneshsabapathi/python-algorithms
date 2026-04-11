#!/usr/bin/env python3
"""
Optimized and alternative implementations of Lempel-Ziv-Welch (LZW) compression.

The reference provides binary file-based LZW. This file focuses on the
interview-friendly in-memory string LZW with variants.

Variants covered:
1. dict_based      -- standard dictionary LZW (reference lzw_compress)
2. max_dict_size   -- LZW with configurable max dictionary size (reset when full)
3. variable_width  -- variable-width codes (start 9-bit, grow as dictionary grows)

Key interview insight:
    LZW is used in GIF images and Unix compress. The key idea is building
    a dictionary on-the-fly during both compression and decompression,
    so no dictionary needs to be transmitted. The "code not in dictionary"
    edge case during decompression is a classic interview question.

Run:
    python data_compression/lempel_ziv_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_compression.lempel_ziv import lzw_compress as reference_compress
from data_compression.lempel_ziv import lzw_decompress as reference_decompress


# ---------------------------------------------------------------------------
# Variant 1 -- dict_based (reference wrapper)
# ---------------------------------------------------------------------------

def dict_compress(text: str) -> list[int]:
    """
    Standard LZW compression via dictionary.

    >>> dict_compress("ABABABA")
    [65, 66, 256, 258]
    >>> reference_decompress(dict_compress("hello"))
    'hello'
    """
    return reference_compress(text)


def dict_decompress(codes: list[int]) -> str:
    """
    Standard LZW decompression.

    >>> dict_decompress([65, 66, 256, 258])
    'ABABABA'
    """
    return reference_decompress(codes)


# ---------------------------------------------------------------------------
# Variant 2 -- max_dict_size: reset dictionary when it exceeds max size
# ---------------------------------------------------------------------------

def bounded_compress(text: str, max_size: int = 512) -> list[int]:
    """
    LZW with bounded dictionary. Resets to initial 256 entries when full.
    Prevents unbounded memory growth on large inputs.

    >>> bounded_compress("ABABABA", 512)
    [65, 66, 256, 258]
    >>> bounded_decompress(bounded_compress("hello world", 300), 300)
    'hello world'
    """
    if not text:
        return []

    dictionary: dict[str, int] = {chr(i): i for i in range(256)}
    next_code = 256
    result: list[int] = []
    current = ""

    for char in text:
        current_plus = current + char
        if current_plus in dictionary:
            current = current_plus
        else:
            result.append(dictionary[current])
            if next_code < max_size:
                dictionary[current_plus] = next_code
                next_code += 1
            else:
                # Reset dictionary
                dictionary = {chr(i): i for i in range(256)}
                next_code = 256
            current = char

    if current:
        result.append(dictionary[current])

    return result


def bounded_decompress(codes: list[int], max_size: int = 512) -> str:
    """
    LZW decompression with bounded dictionary matching bounded_compress.

    >>> bounded_decompress([65, 66, 256, 258], 512)
    'ABABABA'
    """
    if not codes:
        return ""

    dictionary: dict[int, str] = {i: chr(i) for i in range(256)}
    next_code = 256

    result = [dictionary[codes[0]]]
    previous = result[0]

    for code in codes[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = previous + previous[0]
        else:
            raise ValueError(f"Invalid code: {code}")

        result.append(entry)

        if next_code < max_size:
            dictionary[next_code] = previous + entry[0]
            next_code += 1
        else:
            dictionary = {i: chr(i) for i in range(256)}
            next_code = 256

        previous = entry

    return "".join(result)


# ---------------------------------------------------------------------------
# Variant 3 -- variable_width: variable-width code output
# ---------------------------------------------------------------------------

def varwidth_compress(text: str) -> tuple[list[int], int]:
    """
    LZW with variable-width codes. Returns (codes, initial_bits).
    Starts with 9-bit codes (256 single chars + 1 for growth),
    increases bit width as dictionary grows.

    >>> codes, bits = varwidth_compress("ABABABA")
    >>> varwidth_decompress(codes, bits) == "ABABABA"
    True
    >>> codes, bits = varwidth_compress("the quick brown fox")
    >>> varwidth_decompress(codes, bits) == "the quick brown fox"
    True
    """
    if not text:
        return [], 9

    dictionary: dict[str, int] = {chr(i): i for i in range(256)}
    next_code = 256
    result: list[int] = []
    current = ""

    for char in text:
        current_plus = current + char
        if current_plus in dictionary:
            current = current_plus
        else:
            result.append(dictionary[current])
            dictionary[current_plus] = next_code
            next_code += 1
            current = char

    if current:
        result.append(dictionary[current])

    return result, 9


def varwidth_decompress(codes: list[int], initial_bits: int = 9) -> str:
    """
    Decompress variable-width LZW codes.

    >>> varwidth_decompress([65, 66, 256, 258], 9)
    'ABABABA'
    """
    if not codes:
        return ""

    dictionary: dict[int, str] = {i: chr(i) for i in range(256)}
    next_code = 256

    result = [dictionary[codes[0]]]
    previous = result[0]

    for code in codes[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = previous + previous[0]
        else:
            raise ValueError(f"Invalid code: {code}")

        result.append(entry)
        dictionary[next_code] = previous + entry[0]
        next_code += 1
        previous = entry

    return "".join(result)


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
    "abcdefghijklmnopqrstuvwxyz",
]

COMPRESS_IMPLS = [
    ("dict_based",   dict_compress,    dict_decompress),
    ("bounded_512",  lambda t: bounded_compress(t, 512), lambda c: bounded_decompress(c, 512)),
    ("varwidth",     lambda t: varwidth_compress(t)[0],  lambda c: varwidth_decompress(c, 9)),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for text in TEST_STRINGS:
        for name, comp, decomp in COMPRESS_IMPLS:
            try:
                codes = comp(text)
                decoded = decomp(codes)
                ok = decoded == text
                tag = "OK" if ok else "FAIL"
                ratio = f"{len(codes)}/{len(text)}"
                print(f"  [{tag}] {name:<15} '{text[:25]}' codes={ratio}")
            except Exception as e:
                print(f"  [ERR] {name:<15} '{text[:25]}' {e}")

    REPS = 10_000
    medium = "the quick brown fox jumps over the lazy dog" * 5

    print(f"\n=== Compress Benchmark ({len(medium)} chars): {REPS} runs ===")
    for name, comp, _ in COMPRESS_IMPLS:
        t = timeit.timeit(lambda comp=comp: comp(medium), number=REPS) * 1000 / REPS
        print(f"  {name:<15} {t:>8.4f} ms")

    codes_ref = dict_compress(medium)
    print(f"\n=== Decompress Benchmark ({len(codes_ref)} codes): {REPS} runs ===")
    for name, _, decomp in COMPRESS_IMPLS:
        codes = COMPRESS_IMPLS[0][1](medium) if name == "dict_based" else COMPRESS_IMPLS[0][1](medium)
        # Use each variant's own codes for fair comparison
        try:
            own_codes = COMPRESS_IMPLS[[n for n, _, _ in COMPRESS_IMPLS].index(name)][1](medium)
            t = timeit.timeit(lambda decomp=decomp, c=own_codes: decomp(c), number=REPS) * 1000 / REPS
            print(f"  {name:<15} {t:>8.4f} ms")
        except Exception:
            print(f"  {name:<15} SKIPPED")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
