#!/usr/bin/env python3
"""
Optimized and alternative implementations of Find Missing Number.

The reference uses XOR across the expected range and the actual values.
XOR is its own inverse: every number that appears in both cancels out,
leaving only the missing number.

Key identity used:
    XOR(expected_range) ^ XOR(actual_list) = missing_number

IMPORTANT CONSTRAINT in the reference and all inferred-range variants:
    The missing number must be STRICTLY BETWEEN min(nums) and max(nums).
    If the missing number is at the boundary (below min or above max),
    min/max inference fails and the result is wrong.
    Use explicit-range variants when the endpoint is not guaranteed interior.

Variants covered:
1. xor_inferred   -- XOR with min/max inferred (reference, interior-only)
2. arithmetic     -- expected_sum - actual_sum (interior-only, most readable)
3. xor_explicit   -- XOR with caller-supplied (lo, hi) — no boundary limit
4. arithmetic_explicit -- sum formula with explicit (lo, hi)
5. lc268          -- LeetCode 268: range always [0..n], n = len(nums)
6. set_diff       -- set(range) - set(nums) — clear but O(n) space

Key interview insight:
    Know BOTH the XOR and arithmetic approaches — interviewers often ask you
    to implement one then optimise to the other.
    `n*(n+1)//2 - sum(nums)` (LeetCode 268 form) is the most common answer.
    XOR is the "bit manipulation" version of the same O(n) / O(1) idea.
    Always clarify the range boundary: can the missing number be the minimum
    or maximum of the expected sequence?

Run:
    python bit_manipulation/missing_number_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from functools import reduce

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from bit_manipulation.missing_number import find_missing_number as reference


# ---------------------------------------------------------------------------
# Variant 1 — XOR with inferred range (mirrors reference exactly)
# ---------------------------------------------------------------------------

def xor_inferred(nums: list[int]) -> int:
    """
    Missing number via XOR; range inferred from min/max of nums.
    Interior-only constraint: missing must be strictly between min and max.

    >>> xor_inferred([0, 1, 3, 4])
    2
    >>> xor_inferred([4, 3, 1, 0])
    2
    >>> xor_inferred([-4, -3, -1, 0])
    -2
    >>> xor_inferred([1, 3, 4, 5, 6])
    2
    """
    low, high = min(nums), max(nums)
    result = high
    for i in range(low, high):
        result ^= i ^ nums[i - low]
    return result


# ---------------------------------------------------------------------------
# Variant 2 — Arithmetic: expected_sum - actual_sum (interior-only)
# ---------------------------------------------------------------------------

def arithmetic(nums: list[int]) -> int:
    """
    Missing number via sum formula; range inferred from min/max.
    Interior-only constraint: same as xor_inferred.

    expected_sum = (n_terms * (low + high)) // 2   where n_terms = high-low+1
    missing = expected_sum - sum(nums)

    >>> arithmetic([0, 1, 3, 4])
    2
    >>> arithmetic([4, 3, 1, 0])
    2
    >>> arithmetic([-4, -3, -1, 0])
    -2
    >>> arithmetic([1, 3, 4, 5, 6])
    2
    """
    low, high = min(nums), max(nums)
    n_terms = high - low + 1          # number of values in full range
    expected = n_terms * (low + high) // 2
    return expected - sum(nums)


# ---------------------------------------------------------------------------
# Variant 3 — XOR with explicit range (no boundary constraint)
# ---------------------------------------------------------------------------

def xor_explicit(nums: list[int], lo: int, hi: int) -> int:
    """
    Missing number via XOR; caller supplies the full range [lo, hi].
    Works even when the missing number is lo or hi.

    >>> xor_explicit([0, 1, 3, 4], 0, 4)
    2
    >>> xor_explicit([44, 45, 46], 43, 46)
    43
    >>> xor_explicit([15, 16, 17], 14, 17)
    14
    >>> xor_explicit([-3, 0, -1, -2], -3, 1)
    1
    """
    result = 0
    for v in range(lo, hi + 1):
        result ^= v
    for v in nums:
        result ^= v
    return result


# ---------------------------------------------------------------------------
# Variant 4 — Arithmetic with explicit range
# ---------------------------------------------------------------------------

def arithmetic_explicit(nums: list[int], lo: int, hi: int) -> int:
    """
    Missing number via sum formula; caller supplies the full range [lo, hi].
    Works even when the missing number is lo or hi.

    >>> arithmetic_explicit([0, 1, 3, 4], 0, 4)
    2
    >>> arithmetic_explicit([44, 45, 46], 43, 46)
    43
    >>> arithmetic_explicit([15, 16, 17], 14, 17)
    14
    >>> arithmetic_explicit([-3, 0, -1, -2], -3, 1)
    1
    """
    n_terms = hi - lo + 1
    expected = n_terms * (lo + hi) // 2
    return expected - sum(nums)


# ---------------------------------------------------------------------------
# Variant 5 — LeetCode 268: range always [0..n], n = len(nums)
# ---------------------------------------------------------------------------

def lc268(nums: list[int]) -> int:
    """
    LeetCode 268 — Missing Number in [0..n].
    Given n distinct numbers from [0..n], find the one missing.
    Uses Gauss sum formula: n*(n+1)//2 - sum(nums).

    >>> lc268([3, 0, 1])
    2
    >>> lc268([0, 1])
    2
    >>> lc268([9, 6, 4, 2, 3, 5, 7, 0, 1])
    8
    >>> lc268([0])
    1
    """
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)


def lc268_xor(nums: list[int]) -> int:
    """
    LeetCode 268 via XOR — XOR all indices 0..n with all nums.

    >>> lc268_xor([3, 0, 1])
    2
    >>> lc268_xor([0, 1])
    2
    >>> lc268_xor([9, 6, 4, 2, 3, 5, 7, 0, 1])
    8
    >>> lc268_xor([0])
    1
    """
    result = len(nums)
    for i, v in enumerate(nums):
        result ^= i ^ v
    return result


# ---------------------------------------------------------------------------
# Variant 6 — Set difference (O(n) space, most readable)
# ---------------------------------------------------------------------------

def set_diff(nums: list[int]) -> int:
    """
    Missing number via set difference; range inferred from min/max.
    Interior-only constraint: same as xor_inferred.

    >>> set_diff([0, 1, 3, 4])
    2
    >>> set_diff([4, 3, 1, 0])
    2
    >>> set_diff([-4, -3, -1, 0])
    -2
    >>> set_diff([1, 3, 4, 5, 6])
    2
    """
    low, high = min(nums), max(nums)
    return next(iter(set(range(low, high + 1)) - set(nums)))


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

INTERIOR_CASES = [
    ([0, 1, 3, 4], 2),
    ([4, 3, 1, 0], 2),
    ([-4, -3, -1, 0], -2),
    ([-2, 2, 1, 3, 0], -1),
    ([1, 3, 4, 5, 6], 2),
    ([6, 5, 4, 2, 1], 3),
    ([6, 1, 5, 3, 4], 2),
]

BOUNDARY_CASES = [
    # (nums, lo, hi, expected)
    ([44, 45, 46], 43, 46, 43),   # missing at low boundary
    ([15, 16, 17], 14, 17, 14),   # missing at low boundary
    ([-3, 0, -1, -2], -3, 1, 1), # missing at high boundary
]

LC268_CASES = [
    ([3, 0, 1], 2),
    ([0, 1], 2),
    ([9, 6, 4, 2, 3, 5, 7, 0, 1], 8),
    ([0], 1),
]


def run_all() -> None:
    print("\n=== Interior-range correctness ===")
    for nums, expected in INTERIOR_CASES:
        row = {
            "reference": reference(nums),
            "xor_inf":   xor_inferred(nums),
            "arith":     arithmetic(nums),
            "set_diff":  set_diff(nums),
        }
        ok = all(v == expected for v in row.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] {nums!s:<28} expected={expected:<4}  "
              + "  ".join(f"{k}={v}" for k, v in row.items()))

    print("\n=== Boundary correctness (explicit-range variants) ===")
    print("  (xor_inferred and arithmetic FAIL here — expected)")
    for nums, lo, hi, expected in BOUNDARY_CASES:
        inf_result = xor_inferred(nums)
        xor_exp = xor_explicit(nums, lo, hi)
        arith_exp = arithmetic_explicit(nums, lo, hi)
        xor_ok = "OK" if xor_exp == expected else "FAIL"
        arith_ok = "OK" if arith_exp == expected else "FAIL"
        inf_tag = "FAIL(expected)" if inf_result != expected else "OK"
        print(f"  inferred={inf_result:<4} [{inf_tag}]  "
              f"xor_explicit=[{xor_ok}]{xor_exp}  "
              f"arith_explicit=[{arith_ok}]{arith_exp}  "
              f"-- {nums} lo={lo} hi={hi}")

    print("\n=== LeetCode 268 correctness ===")
    for nums, expected in LC268_CASES:
        r1 = lc268(nums)
        r2 = lc268_xor(nums)
        ok = r1 == r2 == expected
        print(f"  [{'OK' if ok else 'FAIL'}] {nums}  lc268={r1}  lc268_xor={r2}  expected={expected}")

    REPS = 200_000
    test_nums = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15]  # missing 2 and 11
    # use a case where exactly one is missing for interior variants
    bench_nums = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10]  # missing 2, length 10
    lc_nums = [3, 0, 1, 4, 6, 5, 7, 9, 8]  # missing 2 from [0..9]

    print(f"\n=== Benchmark: {REPS} runs ===")
    benches = [
        ("reference",  lambda: reference(bench_nums)),
        ("xor_inf",    lambda: xor_inferred(bench_nums)),
        ("arithmetic", lambda: arithmetic(bench_nums)),
        ("set_diff",   lambda: set_diff(bench_nums)),
        ("lc268",      lambda: lc268(lc_nums)),
        ("lc268_xor",  lambda: lc268_xor(lc_nums)),
    ]
    for name, fn in benches:
        t = timeit.timeit(fn, number=REPS) * 1000 / REPS
        print(f"  {name:<14} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
