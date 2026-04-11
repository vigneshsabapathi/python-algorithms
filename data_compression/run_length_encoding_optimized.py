#!/usr/bin/env python3
"""
Optimized and alternative implementations of Run-Length Encoding.

The reference uses index-based iteration with count tracking.

Variants covered:
1. index_based     -- reference approach with manual counting
2. groupby         -- itertools.groupby (most Pythonic)
3. regex_based     -- re.findall with backreference grouping
4. string_format   -- encodes to string "A4B3C2" instead of tuple list

Key interview insight:
    RLE is the simplest compression algorithm. Best for data with long
    runs (e.g., bitmap images, fax machines). Worst case: alternating
    characters double the size. Interview twist: "implement for a 2D
    matrix" or "what if runs > 9 in string format?"

Run:
    python data_compression/run_length_encoding_optimized.py
"""

from __future__ import annotations

import os
import re
import sys
import timeit
from itertools import groupby

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_compression.run_length_encoding import run_length_encode as reference_encode
from data_compression.run_length_encoding import run_length_decode as reference_decode


# ---------------------------------------------------------------------------
# Variant 1 -- index_based (reference wrapper)
# ---------------------------------------------------------------------------

def index_encode(text: str) -> list[tuple[str, int]]:
    """
    RLE using reference index-based counting.

    >>> index_encode("AAAABBBCCDAA")
    [('A', 4), ('B', 3), ('C', 2), ('D', 1), ('A', 2)]
    >>> index_encode("")
    []
    """
    return reference_encode(text)


def index_decode(encoded: list[tuple[str, int]]) -> str:
    """
    Decode using reference.

    >>> index_decode([('A', 4), ('B', 3)])
    'AAAABBB'
    """
    return reference_decode(encoded)


# ---------------------------------------------------------------------------
# Variant 2 -- groupby: itertools.groupby (most Pythonic)
# ---------------------------------------------------------------------------

def groupby_encode(text: str) -> list[tuple[str, int]]:
    """
    RLE using itertools.groupby — the idiomatic Python approach.

    >>> groupby_encode("AAAABBBCCDAA")
    [('A', 4), ('B', 3), ('C', 2), ('D', 1), ('A', 2)]
    >>> groupby_encode("A")
    [('A', 1)]
    >>> groupby_encode("")
    []
    """
    if not text:
        return []
    return [(char, sum(1 for _ in group)) for char, group in groupby(text)]


def groupby_decode(encoded: list[tuple[str, int]]) -> str:
    """
    Decode RLE tuples back to string.

    >>> groupby_decode([('A', 4), ('B', 3), ('C', 2), ('D', 1), ('A', 2)])
    'AAAABBBCCDAA'
    """
    return "".join(c * n for c, n in encoded)


# ---------------------------------------------------------------------------
# Variant 3 -- regex_based: re.findall with backreference
# ---------------------------------------------------------------------------

def regex_encode(text: str) -> list[tuple[str, int]]:
    """
    RLE using regex to find consecutive character runs.

    >>> regex_encode("AAAABBBCCDAA")
    [('A', 4), ('B', 3), ('C', 2), ('D', 1), ('A', 2)]
    >>> regex_encode("AA")
    [('A', 2)]
    >>> regex_encode("")
    []
    """
    if not text:
        return []
    # (.)\\1* matches a char followed by zero or more of the same char
    return [(m[1], len(m[0])) for m in re.findall(r"((.)\2*)", text)]


def regex_decode(encoded: list[tuple[str, int]]) -> str:
    """
    Decode RLE tuples.

    >>> regex_decode([('A', 4), ('B', 3)])
    'AAAABBB'
    """
    return "".join(c * n for c, n in encoded)


# ---------------------------------------------------------------------------
# Variant 4 -- string_format: encode to "A4B3C2D1A2" string
# ---------------------------------------------------------------------------

def string_encode(text: str) -> str:
    """
    RLE encoding to a string format like "A4B3C2D1A2".

    >>> string_encode("AAAABBBCCDAA")
    'A4B3C2D1A2'
    >>> string_encode("A")
    'A1'
    >>> string_encode("")
    ''
    """
    if not text:
        return ""
    return "".join(
        f"{char}{sum(1 for _ in group)}" for char, group in groupby(text)
    )


def string_decode(encoded: str) -> str:
    """
    Decode string-format RLE like "A4B3C2D1A2" back to original.

    >>> string_decode("A4B3C2D1A2")
    'AAAABBBCCDAA'
    >>> string_decode("A1")
    'A'
    >>> string_decode("")
    ''
    """
    if not encoded:
        return ""
    # Parse pairs of (char, digits)
    result = []
    i = 0
    while i < len(encoded):
        char = encoded[i]
        i += 1
        num_str = ""
        while i < len(encoded) and encoded[i].isdigit():
            num_str += encoded[i]
            i += 1
        result.append(char * int(num_str))
    return "".join(result)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_STRINGS = [
    "AAAABBBCCDAA",
    "A",
    "AA",
    "AAADDDDDDFFFCCCAAVVVV",
    "ABCDE",
    "aabbccddee",
    "",
    "AAAAAAAAAA",
]

TUPLE_IMPLS = [
    ("index_based", index_encode, index_decode),
    ("groupby",     groupby_encode, groupby_decode),
    ("regex_based", regex_encode, regex_decode),
]


def run_all() -> None:
    print("\n=== Tuple-based Correctness ===")
    for text in TEST_STRINGS:
        ref = reference_encode(text)
        for name, enc, dec in TUPLE_IMPLS:
            try:
                encoded = enc(text)
                decoded = dec(encoded)
                ok = decoded == text and encoded == ref
                tag = "OK" if ok else "FAIL"
                print(f"  [{tag}] {name:<12} '{text[:20]}' -> {encoded[:5]}...")
            except Exception as e:
                print(f"  [ERR] {name:<12} '{text[:20]}' {e}")

    print("\n=== String-format Correctness ===")
    for text in TEST_STRINGS:
        encoded = string_encode(text)
        decoded = string_decode(encoded)
        ok = decoded == text
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] string_fmt   '{text[:20]}' -> '{encoded[:20]}'")

    REPS = 50_000
    short = "AAAABBBCCDAA"
    long_str = "A" * 1000 + "B" * 500 + "C" * 300 + "D" * 200

    print(f"\n=== Encode Benchmark (short '{short}'): {REPS} runs ===")
    for name, enc, _ in TUPLE_IMPLS:
        t = timeit.timeit(lambda enc=enc: enc(short), number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>8.4f} ms")
    t = timeit.timeit(lambda: string_encode(short), number=REPS) * 1000 / REPS
    print(f"  {'string_fmt':<12} {t:>8.4f} ms")

    REPS2 = 10_000
    print(f"\n=== Encode Benchmark (long, {len(long_str)} chars): {REPS2} runs ===")
    for name, enc, _ in TUPLE_IMPLS:
        t = timeit.timeit(lambda enc=enc: enc(long_str), number=REPS2) * 1000 / REPS2
        print(f"  {name:<12} {t:>8.4f} ms")
    t = timeit.timeit(lambda: string_encode(long_str), number=REPS2) * 1000 / REPS2
    print(f"  {'string_fmt':<12} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
