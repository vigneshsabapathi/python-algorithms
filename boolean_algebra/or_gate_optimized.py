#!/usr/bin/env python3
"""
Optimized and alternative implementations of OR Gate.

The reference uses `int((input_1, input_2).count(1) != 0)` — counts how many
inputs are 1 and returns true if at least one is found.

Variants covered:
1. count_check   -- int((a,b).count(1) != 0)      (reference)
2. bitwise_or    -- a | b                          (single CPU instruction)
3. boolean_or    -- int(a or b)                    (Python short-circuit)
4. max_gate      -- max(a, b)                      (OR = maximum of inputs)

Key interview insight:
    OR is the dual of AND under De Morgan's laws. For single-bit values,
    `a | b` compiles to a single bitwise instruction. The `max()` approach
    generalizes: OR of n binary inputs equals max(inputs). In hardware,
    OR gates are built from parallel transistor paths.

Run:
    python boolean_algebra/or_gate_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from boolean_algebra.or_gate import or_gate as reference


# ---------------------------------------------------------------------------
# Variant 1 -- count check (reference)
# ---------------------------------------------------------------------------

def count_check(input_1: int, input_2: int) -> int:
    """
    OR via tuple count.

    >>> count_check(0, 0)
    0
    >>> count_check(0, 1)
    1
    >>> count_check(1, 0)
    1
    >>> count_check(1, 1)
    1
    """
    return int((input_1, input_2).count(1) != 0)


# ---------------------------------------------------------------------------
# Variant 2 -- bitwise OR (single instruction)
# ---------------------------------------------------------------------------

def bitwise_or(input_1: int, input_2: int) -> int:
    """
    OR via bitwise | operator. Maps to single CPU instruction.

    >>> bitwise_or(0, 0)
    0
    >>> bitwise_or(0, 1)
    1
    >>> bitwise_or(1, 0)
    1
    >>> bitwise_or(1, 1)
    1
    """
    return input_1 | input_2


# ---------------------------------------------------------------------------
# Variant 3 -- Python boolean or
# ---------------------------------------------------------------------------

def boolean_or(input_1: int, input_2: int) -> int:
    """
    OR via Python's short-circuit `or` operator.

    >>> boolean_or(0, 0)
    0
    >>> boolean_or(0, 1)
    1
    >>> boolean_or(1, 0)
    1
    >>> boolean_or(1, 1)
    1
    """
    return int(input_1 or input_2)


# ---------------------------------------------------------------------------
# Variant 4 -- max gate (OR = maximum)
# ---------------------------------------------------------------------------

def max_gate(input_1: int, input_2: int) -> int:
    """
    OR via max(): for binary inputs, OR equals the maximum value.

    >>> max_gate(0, 0)
    0
    >>> max_gate(0, 1)
    1
    >>> max_gate(1, 0)
    1
    >>> max_gate(1, 1)
    1
    """
    return max(input_1, input_2)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (0, 0, 0),
    (0, 1, 1),
    (1, 0, 1),
    (1, 1, 1),
]

IMPLS = [
    ("reference",    reference),
    ("count_check",  count_check),
    ("bitwise_or",   bitwise_or),
    ("boolean_or",   boolean_or),
    ("max_gate",     max_gate),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for a, b, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(a, b)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(
            f"  [{tag}] ({a},{b}) expected={expected}  "
            + "  ".join(f"{nm}={v}" for nm, v in results.items())
        )

    REPS = 500_000
    inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]

    print(f"\n=== Benchmark: {REPS} runs, {len(inputs)} input pairs ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(a, b) for a, b in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
