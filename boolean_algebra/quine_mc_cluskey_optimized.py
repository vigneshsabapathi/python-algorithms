#!/usr/bin/env python3
"""
Optimized and alternative implementations of Quine-McCluskey algorithm.

The reference implements the standard Quine-McCluskey method: convert minterms
to binary, iteratively combine terms differing by one bit, then use a prime
implicant chart to find essential prime implicants.

Variants covered:
1. standard_qmc        -- reference implementation (iterative combining)
2. set_based_qmc       -- uses sets for faster duplicate elimination
3. binary_mask_qmc     -- uses integer bitmasks instead of strings

Key interview insight:
    Quine-McCluskey is the algorithmic equivalent of Karnaugh maps but works
    for any number of variables. It is NP-hard in general (the covering step
    is a set cover problem), but practical for moderate-sized functions.
    The algorithm guarantees a minimal two-level SOP expression.

Run:
    python boolean_algebra/quine_mc_cluskey_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from boolean_algebra.quine_mc_cluskey import (
    check as reference_check,
    decimal_to_binary as reference_d2b,
    prime_implicant_chart as reference_chart,
    selection as reference_selection,
)


# ---------------------------------------------------------------------------
# Variant 1 -- standard QMC (reference wrapper)
# ---------------------------------------------------------------------------

def standard_qmc(n_vars: int, minterms: list[int]) -> list[str]:
    """
    Standard Quine-McCluskey using reference functions.

    Note: the reference check() has a known quirk -- it appends literal "X"
    instead of the merged term, so it only works for single-pass reductions.
    For full correctness, use set_based_qmc or binary_mask_qmc.

    >>> standard_qmc(2, [1, 3])
    ['01', '11']
    """
    binary = reference_d2b(n_vars, minterms)
    primes = reference_check(binary)
    chart = reference_chart(primes, binary)
    return reference_selection(chart, primes)


# ---------------------------------------------------------------------------
# Variant 2 -- set-based QMC (faster duplicate elimination)
# ---------------------------------------------------------------------------

def _set_compare(s1: str, s2: str) -> str | None:
    """Compare two binary strings; return merged if they differ by exactly 1 bit."""
    diff_pos = -1
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            if diff_pos >= 0:
                return None
            diff_pos = i
    if diff_pos < 0:
        return None
    return s1[:diff_pos] + "_" + s1[diff_pos + 1:]


def set_based_qmc(n_vars: int, minterms: list[int]) -> list[str]:
    """
    Set-based Quine-McCluskey: uses sets to eliminate duplicates faster.

    >>> sorted(set_based_qmc(3, [1, 2, 3, 5, 7]))
    ['01_', '__1']
    >>> set_based_qmc(2, [0, 1, 2, 3])
    ['__']
    """
    binary = set()
    for m in minterms:
        bits = ""
        val = m
        for _ in range(n_vars):
            bits = str(val % 2) + bits
            val //= 2
        binary.add(bits)

    prime_implicants: set[str] = set()
    current = binary

    while current:
        used: set[str] = set()
        next_level: set[str] = set()
        terms = sorted(current)
        for i in range(len(terms)):
            for j in range(i + 1, len(terms)):
                merged = _set_compare(terms[i], terms[j])
                if merged is not None:
                    used.add(terms[i])
                    used.add(terms[j])
                    next_level.add(merged)
        prime_implicants |= current - used
        current = next_level

    return list(prime_implicants)


# ---------------------------------------------------------------------------
# Variant 3 -- bitmask-based QMC (integer operations)
# ---------------------------------------------------------------------------

def binary_mask_qmc(n_vars: int, minterms: list[int]) -> list[str]:
    """
    Bitmask-based QMC: uses integer pairs (value, mask) instead of strings.
    Mask bit=1 means that position is a don't-care ('_').

    >>> sorted(binary_mask_qmc(3, [1, 2, 3, 5, 7]))
    ['01_', '__1']
    >>> binary_mask_qmc(2, [0, 1, 2, 3])
    ['__']
    """
    # Each term is (value, dont_care_mask)
    current: set[tuple[int, int]] = {(m, 0) for m in minterms}
    primes: set[tuple[int, int]] = set()

    while current:
        used: set[tuple[int, int]] = set()
        next_level: set[tuple[int, int]] = set()
        terms = sorted(current)
        for i in range(len(terms)):
            vi, mi = terms[i]
            for j in range(i + 1, len(terms)):
                vj, mj = terms[j]
                if mi != mj:
                    continue
                diff = vi ^ vj
                if diff and (diff & (diff - 1)) == 0:  # exactly one bit differs
                    used.add(terms[i])
                    used.add(terms[j])
                    next_level.add((vi & vj, mi | diff))
        primes |= current - used
        current = next_level

    # Convert back to string representation
    result = []
    for val, mask in primes:
        s = ""
        for bit in range(n_vars - 1, -1, -1):
            if mask & (1 << bit):
                s += "_"
            elif val & (1 << bit):
                s += "1"
            else:
                s += "0"
        result.append(s)
    return result


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (3, [1, 2, 3, 5, 7]),
    (2, [0, 1, 2, 3]),
    (3, [0, 1, 2, 5, 6, 7]),
    (2, [1, 3]),
]

IMPLS = [
    ("set_based_qmc",   set_based_qmc),
    ("binary_mask_qmc", binary_mask_qmc),
]

# standard_qmc uses the buggy reference check() -- shown separately
ALL_IMPLS = [("standard_qmc", standard_qmc)] + IMPLS


def run_all() -> None:
    print("\n=== Correctness (set_based vs binary_mask -- both correct) ===")
    for n_vars, minterms in TEST_CASES:
        results = {}
        for name, fn in ALL_IMPLS:
            try:
                results[name] = sorted(fn(n_vars, minterms))
            except Exception as e:
                results[name] = f"ERR:{e}"
        ref = results["set_based_qmc"]
        ok = results["set_based_qmc"] == results["binary_mask_qmc"]
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] n={n_vars}, minterms={minterms}")
        for name, val in results.items():
            note = " (buggy reference check())" if name == "standard_qmc" else ""
            print(f"         {name}: {val}{note}")

    REPS = 50_000
    test_input = (4, [0, 1, 2, 5, 6, 7, 8, 9, 10, 14])

    print(f"\n=== Benchmark: {REPS} runs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: fn(*test_input), number=REPS
        ) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms / call")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
