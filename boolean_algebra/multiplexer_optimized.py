#!/usr/bin/env python3
"""
Optimized and alternative implementations of 2-to-1 Multiplexer.

The reference uses `input1 if select else input0` — a conditional expression
that directly models the hardware behavior of a MUX.

Variants covered:
1. conditional     -- input1 if select else input0      (reference, Pythonic)
2. bitwise_mux     -- (input0 & ~s) | (input1 & s)     (gate-level, no branch)
3. index_mux       -- (input0, input1)[select]          (tuple indexing)
4. arithmetic_mux  -- input0*(1-s) + input1*s           (algebraic)

Key interview insight:
    A 2-to-1 MUX is a universal building block: any boolean function of n
    variables can be implemented using 2^(n-1) - 1 MUXes (Shannon decomposition).
    The bitwise variant `(a & ~s) | (b & s)` is exactly how hardware implements
    a MUX at the gate level with no branching.

Run:
    python boolean_algebra/multiplexer_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from boolean_algebra.multiplexer import mux as reference


# ---------------------------------------------------------------------------
# Variant 1 -- conditional (reference style)
# ---------------------------------------------------------------------------

def conditional(input0: int, input1: int, select: int) -> int:
    """
    MUX via conditional expression.

    >>> conditional(0, 1, 0)
    0
    >>> conditional(0, 1, 1)
    1
    >>> conditional(1, 0, 0)
    1
    >>> conditional(1, 0, 1)
    0
    """
    return input1 if select else input0


# ---------------------------------------------------------------------------
# Variant 2 -- bitwise (gate-level, branchless)
# ---------------------------------------------------------------------------

def bitwise_mux(input0: int, input1: int, select: int) -> int:
    """
    MUX via bitwise ops: (input0 & NOT select) OR (input1 & select).
    Maps directly to gate-level hardware implementation.

    >>> bitwise_mux(0, 1, 0)
    0
    >>> bitwise_mux(0, 1, 1)
    1
    >>> bitwise_mux(1, 0, 0)
    1
    >>> bitwise_mux(1, 0, 1)
    0
    """
    return (input0 & (~select & 1)) | (input1 & select)


# ---------------------------------------------------------------------------
# Variant 3 -- tuple indexing
# ---------------------------------------------------------------------------

def index_mux(input0: int, input1: int, select: int) -> int:
    """
    MUX via tuple indexing: select acts as the index.

    >>> index_mux(0, 1, 0)
    0
    >>> index_mux(0, 1, 1)
    1
    >>> index_mux(1, 0, 0)
    1
    >>> index_mux(1, 0, 1)
    0
    """
    return (input0, input1)[select]


# ---------------------------------------------------------------------------
# Variant 4 -- arithmetic (algebraic identity)
# ---------------------------------------------------------------------------

def arithmetic_mux(input0: int, input1: int, select: int) -> int:
    """
    MUX via arithmetic: input0*(1-s) + input1*s.
    When s=0, yields input0; when s=1, yields input1.

    >>> arithmetic_mux(0, 1, 0)
    0
    >>> arithmetic_mux(0, 1, 1)
    1
    >>> arithmetic_mux(1, 0, 0)
    1
    >>> arithmetic_mux(1, 0, 1)
    0
    """
    return input0 * (1 - select) + input1 * select


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    (0, 0, 0, 0),
    (0, 0, 1, 0),
    (0, 1, 0, 0),
    (0, 1, 1, 1),
    (1, 0, 0, 1),
    (1, 0, 1, 0),
    (1, 1, 0, 1),
    (1, 1, 1, 1),
]

IMPLS = [
    ("reference",      reference),
    ("conditional",    conditional),
    ("bitwise_mux",    bitwise_mux),
    ("index_mux",      index_mux),
    ("arithmetic_mux", arithmetic_mux),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for i0, i1, s, expected in TEST_CASES:
        results = {}
        for name, fn in IMPLS:
            try:
                results[name] = fn(i0, i1, s)
            except Exception as e:
                results[name] = f"ERR:{e}"
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(
            f"  [{tag}] ({i0},{i1},s={s}) expected={expected}  "
            + "  ".join(f"{nm}={v}" for nm, v in results.items())
        )

    REPS = 500_000
    inputs = [(i0, i1, s) for i0 in (0, 1) for i1 in (0, 1) for s in (0, 1)]

    print(f"\n=== Benchmark: {REPS} runs, {len(inputs)} input combos ===")
    for name, fn in IMPLS:
        t = timeit.timeit(
            lambda fn=fn: [fn(a, b, c) for a, b, c in inputs], number=REPS
        ) * 1000 / REPS
        print(f"  {name:<16} {t:>7.4f} ms / batch of {len(inputs)}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
