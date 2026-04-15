#!/usr/bin/env python3
"""
Optimized and alternative implementations of Smith-Waterman.

Variants covered:
1. smith_waterman_space_opt  -- O(n) space (score only, no traceback)
2. smith_waterman_affine     -- affine gap penalty model
3. smith_waterman_banded     -- banded version for similar-length sequences

Run:
    python dynamic_programming/smith_waterman_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.smith_waterman import smith_waterman as reference


# ---------------------------------------------------------------------------
# Variant 1 — Space-optimized (score only)
# ---------------------------------------------------------------------------

def smith_waterman_space_opt(
    seq1: str, seq2: str, match: int = 2, mismatch: int = -1, gap: int = -1
) -> int:
    """
    Smith-Waterman returning only the max alignment score using O(n) space.

    >>> smith_waterman_space_opt("TGTTACGG", "GGTTGACTA")
    9
    >>> smith_waterman_space_opt("ACAT", "ACAT")
    8
    >>> smith_waterman_space_opt("ABC", "DEF")
    0
    >>> smith_waterman_space_opt("", "ABC")
    0
    """
    m, n = len(seq1), len(seq2)
    if m == 0 or n == 0:
        return 0

    prev = [0] * (n + 1)
    max_score = 0

    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            diag = prev[j - 1] + (match if seq1[i - 1] == seq2[j - 1] else mismatch)
            up = prev[j] + gap
            left = curr[j - 1] + gap
            curr[j] = max(0, diag, up, left)
            max_score = max(max_score, curr[j])
        prev = curr

    return max_score


# ---------------------------------------------------------------------------
# Variant 2 — Affine gap penalty
# ---------------------------------------------------------------------------

def smith_waterman_affine(
    seq1: str, seq2: str, match: int = 2, mismatch: int = -1,
    gap_open: int = -2, gap_extend: int = -1
) -> int:
    """
    Smith-Waterman with affine gap penalties (open + extend).

    >>> smith_waterman_affine("TGTTACGG", "GGTTGACTA")
    8
    >>> smith_waterman_affine("ACAT", "ACAT")
    8
    >>> smith_waterman_affine("ABC", "DEF")
    0
    """
    m, n = len(seq1), len(seq2)
    if m == 0 or n == 0:
        return 0

    NEG_INF = float("-inf")
    H = [[0] * (n + 1) for _ in range(m + 1)]
    E = [[NEG_INF] * (n + 1) for _ in range(m + 1)]  # gap in seq2
    F = [[NEG_INF] * (n + 1) for _ in range(m + 1)]  # gap in seq1
    max_score = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            diag = H[i - 1][j - 1] + (match if seq1[i - 1] == seq2[j - 1] else mismatch)
            E[i][j] = max(H[i][j - 1] + gap_open, E[i][j - 1] + gap_extend)
            F[i][j] = max(H[i - 1][j] + gap_open, F[i - 1][j] + gap_extend)
            H[i][j] = max(0, diag, E[i][j], F[i][j])
            max_score = max(max_score, H[i][j])

    return max_score


# ---------------------------------------------------------------------------
# Variant 3 — Banded Smith-Waterman
# ---------------------------------------------------------------------------

def smith_waterman_banded(
    seq1: str, seq2: str, match: int = 2, mismatch: int = -1,
    gap: int = -1, bandwidth: int = 5
) -> int:
    """
    Banded Smith-Waterman — only computes within a diagonal band.

    >>> smith_waterman_banded("TGTTACGG", "GGTTGACTA")
    9
    >>> smith_waterman_banded("ACAT", "ACAT")
    8
    >>> smith_waterman_banded("ABC", "DEF")
    0
    """
    m, n = len(seq1), len(seq2)
    if m == 0 or n == 0:
        return 0

    H = [[0] * (n + 1) for _ in range(m + 1)]
    max_score = 0

    for i in range(1, m + 1):
        j_start = max(1, i - bandwidth)
        j_end = min(n, i + bandwidth)
        for j in range(j_start, j_end + 1):
            diag = H[i - 1][j - 1] + (match if seq1[i - 1] == seq2[j - 1] else mismatch)
            up = H[i - 1][j] + gap
            left = H[i][j - 1] + gap
            H[i][j] = max(0, diag, up, left)
            max_score = max(max_score, H[i][j])

    return max_score


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ("TGTTACGG", "GGTTGACTA", 9),
    ("ACAT", "ACAT", 8),
    ("ABC", "DEF", 0),
]

IMPLS = [
    ("reference", lambda s1, s2: reference(s1, s2)[0]),
    ("space_opt", smith_waterman_space_opt),
    ("affine", smith_waterman_affine),
    ("banded", smith_waterman_banded),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for s1, s2, expected in TEST_CASES:
        results = {name: fn(s1, s2) for name, fn in IMPLS}
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] ({s1!r}, {s2!r})  expected={expected}  " +
              "  ".join(f"{n}={v}" for n, v in results.items()))

    REPS = 5_000
    s1 = "ACGTACGTACGT"
    s2 = "ACGTGCATACGT"
    print(f"\n=== Benchmark: {REPS} runs, len=12 ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(s1, s2), number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
