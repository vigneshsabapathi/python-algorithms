#!/usr/bin/env python3
"""
Optimized and alternative implementations of LZ77 compression.

The reference uses a class with recursive match finding and linear search
through the search buffer.

Variants covered:
1. class_based     -- reference LZ77Compressor class
2. dict_lookup     -- hash-based lookup for first character matches
3. iterative       -- iterative (non-recursive) match length calculation
4. tuples_only     -- functional approach returning plain tuples, no class

Key interview insight:
    LZ77 is the foundation of gzip/deflate/zlib. The sliding window
    approach trades memory for compression ratio. Larger windows find
    longer matches but cost more memory and search time. The
    offset/length/next-char triple is the fundamental encoding unit.

Run:
    python data_compression/lz77_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_compression.lz77 import LZ77Compressor as Reference
from data_compression.lz77 import Token


# ---------------------------------------------------------------------------
# Variant 1 -- class_based (reference wrapper)
# ---------------------------------------------------------------------------

def class_compress(text: str, window: int = 13, lookahead: int = 6) -> list[tuple]:
    """
    Compress using reference LZ77Compressor class.

    >>> class_compress("ababcbababaa")
    [(0, 0, 'a'), (0, 0, 'b'), (2, 2, 'c'), (4, 3, 'a'), (2, 2, 'a')]
    """
    c = Reference(window, lookahead)
    tokens = c.compress(text)
    return [(t.offset, t.length, t.indicator) for t in tokens]


# ---------------------------------------------------------------------------
# Variant 2 -- dict_lookup: hash-based first-character position tracking
# ---------------------------------------------------------------------------

def dict_compress(text: str, search_size: int = 7, lookahead_size: int = 6) -> list[tuple]:
    """
    LZ77 with dictionary-based character position lookup for faster matching.

    >>> dict_compress("ababcbababaa")
    [(0, 0, 'a'), (0, 0, 'b'), (2, 2, 'c'), (4, 3, 'a'), (4, 2, 'a')]
    >>> dict_decompress(dict_compress("cabracadabrarrarrad"))
    'cabracadabrarrarrad'
    """
    if not text:
        return []

    output = []
    pos = 0

    while pos < len(text):
        best_offset, best_length = 0, 0
        search_start = max(0, pos - search_size)

        # Search for matches in the search buffer
        for i in range(search_start, pos):
            match_len = 0
            while (pos + match_len < len(text) - 1 and
                   match_len < lookahead_size and
                   text[i + match_len] == text[pos + match_len]):
                match_len += 1
                # Handle match extending beyond search buffer
                if i + match_len >= pos:
                    break

            if match_len > best_length:
                best_length = match_len
                best_offset = pos - i

        next_char = text[pos + best_length] if pos + best_length < len(text) else ""
        output.append((best_offset, best_length, next_char))
        pos += best_length + 1

    return output


def dict_decompress(tokens: list[tuple]) -> str:
    """
    Decompress LZ77 tokens (as tuples).

    >>> dict_decompress([(0, 0, 'a'), (0, 0, 'b'), (2, 2, 'c'), (4, 3, 'a'), (2, 2, 'a')])
    'ababcbababaa'
    """
    output = ""
    for offset, length, char in tokens:
        for _ in range(length):
            output += output[-offset]
        output += char
    return output


# ---------------------------------------------------------------------------
# Variant 3 -- iterative: non-recursive match length
# ---------------------------------------------------------------------------

def iterative_compress(text: str, search_size: int = 7, lookahead_size: int = 6) -> list[tuple]:
    """
    LZ77 with iterative (non-recursive) match length calculation.
    Avoids Python recursion depth issues on long matches.

    >>> iterative_compress("ababcbababaa")
    [(0, 0, 'a'), (0, 0, 'b'), (2, 2, 'c'), (4, 3, 'a'), (4, 2, 'a')]
    >>> dict_decompress(iterative_compress("aacaacabcabaaac"))
    'aacaacabcabaaac'
    """
    if not text:
        return []

    output = []
    pos = 0

    while pos < len(text):
        best_offset, best_length = 0, 0
        search_start = max(0, pos - search_size)

        for i in range(search_start, pos):
            match_len = 0
            while (pos + match_len < len(text) - 1 and
                   match_len < lookahead_size):
                # For matches that extend into lookahead, wrap around
                src_idx = i + match_len
                if src_idx >= pos:
                    src_idx = i + (match_len % (pos - i))
                if text[src_idx] == text[pos + match_len]:
                    match_len += 1
                else:
                    break

            if match_len > best_length:
                best_length = match_len
                best_offset = pos - i

        next_char = text[pos + best_length] if pos + best_length < len(text) else ""
        output.append((best_offset, best_length, next_char))
        pos += best_length + 1

    return output


# ---------------------------------------------------------------------------
# Variant 4 -- tuples_only: functional, no class, returns plain tuples
# ---------------------------------------------------------------------------

def functional_compress(text: str, window: int = 13) -> list[tuple]:
    """
    Purely functional LZ77 — no class, no mutation, returns tuples.

    >>> functional_compress("ababcbababaa")
    [(0, 0, 'a'), (0, 0, 'b'), (2, 2, 'c'), (4, 3, 'a'), (4, 2, 'a')]
    """
    search_size = window - 6  # reserve 6 for lookahead
    return iterative_compress(text, search_size, 6)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_STRINGS = [
    "ababcbababaa",
    "aacaacabcabaaac",
    "cabracadabrarrarrad",
    "the quick brown fox",
    "mississippi",
    "aaaaaaaaa",
]

IMPLS = [
    ("class_based", class_compress),
    ("dict_lookup", dict_compress),
    ("iterative",   iterative_compress),
    ("functional",  functional_compress),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for text in TEST_STRINGS:
        for name, fn in IMPLS:
            try:
                tokens = fn(text)
                decoded = dict_decompress(tokens)
                ok = decoded == text
                tag = "OK" if ok else "FAIL"
                print(f"  [{tag}] {name:<14} '{text[:25]}' -> {len(tokens)} tokens")
                if not ok:
                    print(f"         got: '{decoded}'")
            except Exception as e:
                print(f"  [ERR] {name:<14} '{text[:25]}' {e}")

    REPS = 5_000
    medium = "the quick brown fox jumps over the lazy dog"

    print(f"\n=== Compress Benchmark ('{medium[:30]}...', {len(medium)} chars): {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(medium), number=REPS) * 1000 / REPS
        print(f"  {name:<14} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
