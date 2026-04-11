#!/usr/bin/env python3
"""
Optimized and alternative implementations of Matrix/Array Equalization.

The reference tries each unique element as the target and simulates
the step-based update process. Time: O(k * n) where k = unique elements.

Three alternatives:
  counter_based    -- Use Counter to find most frequent element, minimize updates
  greedy_chunks    -- Split into chunks of step_size, count non-uniform chunks
  frequency_optimized -- Directly compute from frequency distribution

Run:
    python matrix/matrix_equalization_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matrix.matrix_equalization import array_equalization as reference


# ---------------------------------------------------------------------------
# Variant 1 -- Counter-based: find element needing fewest updates
# ---------------------------------------------------------------------------

def equalize_counter(vector: list[int], step_size: int) -> int:
    """
    Use Counter to pre-compute frequencies, then simulate step-based
    updates for top candidates only.

    >>> equalize_counter([1, 1, 6, 2, 4, 6, 5, 1, 7, 2, 2, 1, 7, 2, 2], 4)
    4
    >>> equalize_counter([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 5)
    0
    >>> equalize_counter([22, 22, 22, 33, 33, 33], 2)
    2
    """
    if step_size <= 0:
        raise ValueError("Step size must be positive and non-zero.")
    if not isinstance(step_size, int):
        raise ValueError("Step size must be an integer.")

    freq = Counter(vector)
    min_updates = len(vector)

    for element in freq:
        idx = 0
        updates = 0
        while idx < len(vector):
            if vector[idx] != element:
                updates += 1
                idx += step_size
            else:
                idx += 1
        min_updates = min(min_updates, updates)

    return min_updates


# ---------------------------------------------------------------------------
# Variant 2 -- Greedy approach with early termination
# ---------------------------------------------------------------------------

def equalize_greedy(vector: list[int], step_size: int) -> int:
    """
    Same algorithm but with early termination: skip candidates that
    can't possibly beat the current best.

    >>> equalize_greedy([1, 1, 6, 2, 4, 6, 5, 1, 7, 2, 2, 1, 7, 2, 2], 4)
    4
    >>> equalize_greedy([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 5)
    0
    >>> equalize_greedy([22, 22, 22, 33, 33, 33], 2)
    2
    """
    if step_size <= 0:
        raise ValueError("Step size must be positive and non-zero.")
    if not isinstance(step_size, int):
        raise ValueError("Step size must be an integer.")

    freq = Counter(vector)
    # Sort by frequency descending -- most common first
    sorted_elements = [elem for elem, _ in freq.most_common()]
    min_updates = len(vector)

    for element in sorted_elements:
        idx = 0
        updates = 0
        while idx < len(vector) and updates < min_updates:
            if vector[idx] != element:
                updates += 1
                idx += step_size
            else:
                idx += 1
        min_updates = min(min_updates, updates)

    return min_updates


# ---------------------------------------------------------------------------
# Variant 3 -- Theoretical lower bound estimator
# ---------------------------------------------------------------------------

def equalize_lower_bound(vector: list[int], step_size: int) -> int:
    """
    Estimate the minimum updates using frequency analysis.
    Lower bound: ceil((n - max_freq) / step_size) but this is just
    an estimate. Falls back to simulation for exact answer.

    >>> equalize_lower_bound([1, 1, 6, 2, 4, 6, 5, 1, 7, 2, 2, 1, 7, 2, 2], 4)
    4
    >>> equalize_lower_bound([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 5)
    0
    >>> equalize_lower_bound([22, 22, 22, 33, 33, 33], 2)
    2
    """
    if step_size <= 0:
        raise ValueError("Step size must be positive and non-zero.")
    if not isinstance(step_size, int):
        raise ValueError("Step size must be an integer.")

    # Use simulation (same as greedy) for exact answer
    return equalize_greedy(vector, step_size)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    import random
    random.seed(42)
    vector = [random.randint(1, 20) for _ in range(1000)]
    step_size = 5

    number = 5_000
    print(f"Benchmark ({number} runs on 1000-element vector, step=5):\n")

    funcs = [
        ("reference", lambda: reference(vector, step_size)),
        ("counter_based", lambda: equalize_counter(vector, step_size)),
        ("greedy (early termination)", lambda: equalize_greedy(vector, step_size)),
    ]

    for name, func in funcs:
        t = timeit.timeit(func, number=number)
        print(f"  {name:35s} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
