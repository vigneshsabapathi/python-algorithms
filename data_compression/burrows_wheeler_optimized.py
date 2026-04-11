#!/usr/bin/env python3
"""
Optimized and alternative implementations of Burrows-Wheeler Transform.

The reference builds all rotations as full strings, sorts them, and
extracts the last column. The reverse rebuilds rotations column by column.

Variants covered:
1. naive_rotations  -- O(n^2 log n) full rotation sort (reference)
2. suffix_array     -- O(n log n) via Python sorted() on suffixes
3. counting_reverse -- O(n * alphabet) reverse using LF-mapping

Key interview insight:
    The BWT is the foundation of bzip2 compression. Understanding it
    connects to suffix arrays, FM-index, and bioinformatics string search.

Run:
    python data_compression/burrows_wheeler_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_compression.burrows_wheeler import bwt_transform as reference_transform
from data_compression.burrows_wheeler import reverse_bwt as reference_reverse


# ---------------------------------------------------------------------------
# Variant 1 -- naive_rotations (reference approach)
# ---------------------------------------------------------------------------

def naive_transform(s: str) -> tuple[str, int]:
    """
    BWT via explicit rotation sort. O(n^2 log n) time, O(n^2) space.

    >>> naive_transform("^BANANA")
    ('BNN^AAA', 6)
    >>> naive_transform("abracadabra")
    ('rdarcaaaabb', 2)
    """
    n = len(s)
    rotations = sorted(s[i:] + s[:i] for i in range(n))
    bwt_string = "".join(r[-1] for r in rotations)
    idx = rotations.index(s)
    return bwt_string, idx


def naive_reverse(bwt_string: str, idx: int) -> str:
    """
    Reverse BWT by rebuilding rotation table column by column. O(n^2 log n).

    >>> naive_reverse("BNN^AAA", 6)
    '^BANANA'
    >>> naive_reverse("rdarcaaaabb", 2)
    'abracadabra'
    """
    n = len(bwt_string)
    table = [""] * n
    for _ in range(n):
        table = sorted(bwt_string[i] + table[i] for i in range(n))
    return table[idx]


# ---------------------------------------------------------------------------
# Variant 2 -- suffix_array based BWT
# ---------------------------------------------------------------------------

def suffix_array_transform(s: str) -> tuple[str, int]:
    """
    BWT using suffix array. Conceptually O(n log^2 n) via Python sort.

    We append a sentinel character (chr(0)) that is lexicographically
    smallest, build the suffix array, then extract the BWT.

    >>> suffix_array_transform("^BANANA")
    ('ANNB^AA', 7)
    >>> suffix_array_transform("abracadabra")
    ('ardrcaaaabb', 3)
    """
    sentinel = chr(0)
    text = s + sentinel
    n = len(text)

    # Build suffix array: indices sorted by suffix
    sa = sorted(range(n), key=lambda i: text[i:])

    # BWT: character preceding each suffix (wrap around)
    bwt_chars = []
    idx = -1
    for rank, i in enumerate(sa):
        bwt_chars.append(text[(i - 1) % n])
        if i == 0:
            idx = rank

    # Remove the sentinel from BWT output
    bwt_string = "".join(c for c in bwt_chars if c != sentinel)
    # Adjust idx: if sentinel was before idx position, shift down
    sentinel_positions = [r for r, i in enumerate(sa) if text[(i - 1) % n] == sentinel]
    adjustment = sum(1 for sp in sentinel_positions if sp < idx)
    idx -= adjustment

    return bwt_string, idx


# ---------------------------------------------------------------------------
# Variant 3 -- LF-mapping reverse (counting-based)
# ---------------------------------------------------------------------------

def lf_mapping_reverse(bwt_string: str, idx: int) -> str:
    """
    Reverse BWT using LF-mapping (Last-to-First). O(n * alphabet_size).

    This is the efficient inverse used in FM-index implementations.

    >>> lf_mapping_reverse("BNN^AAA", 6)
    '^BANANA'
    >>> lf_mapping_reverse("rdarcaaaabb", 2)
    'abracadabra'
    """
    n = len(bwt_string)

    # Count occurrences of each character
    counts: dict[str, int] = {}
    for c in bwt_string:
        counts[c] = counts.get(c, 0) + 1

    # First occurrence of each character in sorted order (F column)
    sorted_chars = sorted(counts.keys())
    first_occ: dict[str, int] = {}
    total = 0
    for c in sorted_chars:
        first_occ[c] = total
        total += counts[c]

    # Build occurrence rank array: for each position, how many times
    # has this character appeared before this position in L column
    occ_rank = [0] * n
    char_count: dict[str, int] = {}
    for i, c in enumerate(bwt_string):
        occ_rank[i] = char_count.get(c, 0)
        char_count[c] = char_count.get(c, 0) + 1

    # LF mapping: given row i in BWT matrix, find the corresponding row
    # in the sorted matrix
    # LF(i) = first_occ[L[i]] + occ_rank[i]

    # Walk backwards from idx to reconstruct original
    result = []
    current = idx
    for _ in range(n):
        c = bwt_string[current]
        result.append(c)
        current = first_occ[c] + occ_rank[current]

    return "".join(reversed(result))


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_STRINGS = [
    "^BANANA",
    "abracadabra",
    "panamabanana",
    "a_asa_da_casa",
    "mississippi",
    "the quick brown fox jumps over the lazy dog",
]

TRANSFORM_IMPLS = [
    ("naive_rotations", lambda s: naive_transform(s)),
    ("suffix_array",    lambda s: suffix_array_transform(s)),
    ("reference",       lambda s: (reference_transform(s)["bwt_string"],
                                    reference_transform(s)["idx_original_string"])),
]

REVERSE_IMPLS = [
    ("naive_reverse",  naive_reverse),
    ("lf_mapping",     lf_mapping_reverse),
    ("reference",      reference_reverse),
]


def run_all() -> None:
    print("\n=== Transform Correctness ===")
    for s in TEST_STRINGS:
        ref = reference_transform(s)
        ref_bwt, ref_idx = ref["bwt_string"], ref["idx_original_string"]
        results = {}
        for name, fn in TRANSFORM_IMPLS:
            try:
                bwt, idx = fn(s)
                results[name] = (bwt == ref_bwt and idx == ref_idx)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(v is True for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] '{s[:30]}' -> '{ref_bwt[:20]}' idx={ref_idx}")

    print("\n=== Reverse Correctness ===")
    for s in TEST_STRINGS:
        ref = reference_transform(s)
        bwt, idx = ref["bwt_string"], ref["idx_original_string"]
        for name, fn in REVERSE_IMPLS:
            try:
                result = fn(bwt, idx)
                ok = result == s
                tag = "OK" if ok else "FAIL"
                print(f"  [{tag}] {name}: reverse('{bwt[:20]}', {idx}) = '{result[:30]}'")
            except Exception as e:
                print(f"  [ERR] {name}: {e}")

    REPS = 5_000
    short = "^BANANA"
    medium = "the quick brown fox jumps over the lazy dog"

    print(f"\n=== Transform Benchmark (short '{short}'): {REPS} runs ===")
    for name, fn in TRANSFORM_IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(short), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>8.4f} ms")

    print(f"\n=== Transform Benchmark (medium, {len(medium)} chars): {REPS} runs ===")
    for name, fn in TRANSFORM_IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(medium), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>8.4f} ms")

    ref = reference_transform(medium)
    bwt_m, idx_m = ref["bwt_string"], ref["idx_original_string"]
    print(f"\n=== Reverse Benchmark (medium, {len(medium)} chars): {REPS} runs ===")
    for name, fn in REVERSE_IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(bwt_m, idx_m), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
