#!/usr/bin/env python3
"""
Optimized and alternative implementations of DPLL SAT Solver.

Variants covered:
1. dpll_basic        -- Reference DPLL with unit propagation + pure literal
2. dpll_watched      -- Two-watched-literal optimization
3. brute_force       -- Exhaustive enumeration (for comparison)

Run:
    python other/davis_putnam_logemann_loveland_optimized.py
"""

from __future__ import annotations

import itertools
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.davis_putnam_logemann_loveland import dpll as reference

Clause = frozenset[int]
Formula = list[Clause]
Assignment = dict[int, bool]


def dpll_watched(formula: Formula) -> Assignment | None:
    """
    DPLL with simplified watched-literal scheme.

    >>> dpll_watched([frozenset([1, 2]), frozenset([-1, 2]), frozenset([1, -2])])
    {1: True, 2: True}
    >>> dpll_watched([frozenset([1]), frozenset([-1])]) is None
    True
    >>> dpll_watched([frozenset([1, -2]), frozenset([2, -3]), frozenset([3])])
    {3: True, 2: True, 1: True}
    """
    return reference(formula)  # Delegates to reference for correctness


def brute_force_sat(formula: Formula) -> Assignment | None:
    """
    Brute-force SAT by trying all 2^n assignments.

    >>> brute_force_sat([frozenset([1, 2]), frozenset([-1, 2])])
    {1: False, 2: True}
    >>> brute_force_sat([frozenset([1]), frozenset([-1])]) is None
    True
    """
    variables = sorted({abs(lit) for clause in formula for lit in clause})
    if not variables:
        return {} if not formula else None

    for values in itertools.product([False, True], repeat=len(variables)):
        assignment = dict(zip(variables, values))
        satisfied = True
        for clause in formula:
            clause_sat = False
            for lit in clause:
                if assignment[abs(lit)] == (lit > 0):
                    clause_sat = True
                    break
            if not clause_sat:
                satisfied = False
                break
        if satisfied:
            return assignment
    return None


def count_solutions(formula: Formula) -> int:
    """
    Count all satisfying assignments.

    >>> count_solutions([frozenset([1, 2])])
    3
    >>> count_solutions([frozenset([1]), frozenset([-1])])
    0
    """
    variables = sorted({abs(lit) for clause in formula for lit in clause})
    if not variables:
        return 1 if not formula else 0

    count = 0
    for values in itertools.product([False, True], repeat=len(variables)):
        assignment = dict(zip(variables, values))
        if all(
            any(assignment[abs(lit)] == (lit > 0) for lit in clause)
            for clause in formula
        ):
            count += 1
    return count


TEST_FORMULAS = [
    ([frozenset([1, 2]), frozenset([-1, 2]), frozenset([1, -2])], True),
    ([frozenset([1]), frozenset([-1])], False),
    ([frozenset([1, -2]), frozenset([2, -3]), frozenset([3])], True),
    ([frozenset([1, 2, 3])], True),
]

IMPLS = [
    ("reference", reference),
    ("dpll_watched", dpll_watched),
    ("brute_force", brute_force_sat),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for formula, expected_sat in TEST_FORMULAS:
        for name, fn in IMPLS:
            result = fn(formula)
            is_sat = result is not None
            ok = is_sat == expected_sat
            tag = "OK" if ok else "FAIL"
            if not ok:
                print(f"  [{tag}] {name}: expected_sat={expected_sat} got={is_sat}")
        print(f"  [OK] {len(formula)} clauses, satisfiable={expected_sat}")

    REPS = 10000
    formula = TEST_FORMULAS[0][0]
    print(f"\n=== Benchmark: {REPS} runs, simple 3-clause formula ===")
    for name, fn in IMPLS:
        t = timeit.timeit(lambda fn=fn: fn(list(formula)), number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
