#!/usr/bin/env python3
"""
Optimized and alternative implementations of Karnaugh Map Simplification.

The reference iterates the 2x2 K-map and builds SOP (Sum of Products) terms
for every truthy cell. This is a brute-force approach for 2-variable maps.

Variants covered:
1. iterative_sop     -- nested loop with string building    (reference style)
2. dict_lookup       -- pre-built term dictionary           (O(1) lookup per cell)
3. list_comprehension -- single-expression Pythonic form    (compact)
4. bitfield_encode   -- encode K-map as 4-bit int, table   (hardware-style)

Key interview insight:
    K-maps are a visual simplification technique for up to ~6 variables.
    For larger functions, Quine-McCluskey (also in this folder) is the
    algorithmic equivalent. The reference implementation does NOT perform
    grouping/simplification of adjacent 1-cells -- it just enumerates
    minterms as product terms.

Run:
    python boolean_algebra/karnaugh_map_simplification_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from boolean_algebra.karnaugh_map_simplification import simplify_kmap as reference


# ---------------------------------------------------------------------------
# Variant 1 -- iterative SOP (reference style)
# ---------------------------------------------------------------------------

def iterative_sop(kmap: list[list[int]]) -> str:
    """
    Build SOP expression by iterating cells.

    >>> iterative_sop([[0, 1], [1, 1]])
    "A'B + AB' + AB"
    >>> iterative_sop([[0, 0], [0, 0]])
    ''
    """
    terms = []
    for a, row in enumerate(kmap):
        for b, item in enumerate(row):
            if item:
                terms.append(("A" if a else "A'") + ("B" if b else "B'"))
    return " + ".join(terms)


# ---------------------------------------------------------------------------
# Variant 2 -- dictionary lookup (no conditionals in inner loop)
# ---------------------------------------------------------------------------

_TERM_MAP = {(0, 0): "A'B'", (0, 1): "A'B", (1, 0): "AB'", (1, 1): "AB"}


def dict_lookup(kmap: list[list[int]]) -> str:
    """
    Build SOP using pre-built term dictionary.

    >>> dict_lookup([[0, 1], [1, 1]])
    "A'B + AB' + AB"
    >>> dict_lookup([[0, 0], [0, 0]])
    ''
    >>> dict_lookup([[1, 1], [1, 1]])
    "A'B' + A'B + AB' + AB"
    """
    return " + ".join(
        _TERM_MAP[(a, b)]
        for a, row in enumerate(kmap)
        for b, item in enumerate(row)
        if item
    )


# ---------------------------------------------------------------------------
# Variant 3 -- list comprehension (single expression)
# ---------------------------------------------------------------------------

def list_comprehension(kmap: list[list[int]]) -> str:
    """
    Build SOP in a single list comprehension.

    >>> list_comprehension([[0, 1], [1, 1]])
    "A'B + AB' + AB"
    >>> list_comprehension([[0, 0], [0, 0]])
    ''
    """
    return " + ".join(
        ("A" if a else "A'") + ("B" if b else "B'")
        for a, row in enumerate(kmap)
        for b, val in enumerate(row)
        if val
    )


# ---------------------------------------------------------------------------
# Variant 4 -- bitfield encode (hardware-style table lookup)
# ---------------------------------------------------------------------------

_BITFIELD_TABLE = {
    0b0000: "",
    0b0001: "A'B'",
    0b0010: "A'B",
    0b0100: "AB'",
    0b1000: "AB",
}


def bitfield_encode(kmap: list[list[int]]) -> str:
    """
    Encode 2x2 K-map as a 4-bit integer, then collect terms by set bits.
    Bit positions: [A'B', A'B, AB', AB] -> bits [0,1,2,3].

    >>> bitfield_encode([[0, 1], [1, 1]])
    "A'B + AB' + AB"
    >>> bitfield_encode([[0, 0], [0, 0]])
    ''
    >>> bitfield_encode([[1, 0], [0, 0]])
    "A'B'"
    """
    bits = 0
    if kmap[0][0]: bits |= 0b0001
    if kmap[0][1]: bits |= 0b0010
    if kmap[1][0]: bits |= 0b0100
    if kmap[1][1]: bits |= 0b1000
    terms = []
    for mask in (0b0001, 0b0010, 0b0100, 0b1000):
        if bits & mask:
            terms.append(_BITFIELD_TABLE[mask])
    return " + ".join(terms)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ([[0, 1], [1, 1]], "A'B + AB' + AB"),
    ([[0, 0], [0, 0]], ""),
    ([[1, 1], [1, 1]], "A'B' + A'B + AB' + AB"),
    ([[1, 0], [0, 0]], "A'B'"),
    ([[0, 0], [0, 1]], "AB"),
]

IMPLS = [
    ("reference",          reference),
    ("iterative_sop",      iterative_sop),
    ("dict_lookup",        dict_lookup),
    ("list_comprehension", list_comprehension),
    ("bitfield_encode",    bitfield_encode),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for kmap, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(kmap)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] kmap={kmap} expected='{expected}'")

    REPS = 500_000
    test_maps = [[[0, 1], [1, 1]], [[1, 1], [1, 1]], [[0, 0], [0, 0]]]

    print(f"\n=== Benchmark: {REPS} runs, {len(test_maps)} maps ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(m) for m in test_maps], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<22} {t:>7.4f} ms / batch of {len(test_maps)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
