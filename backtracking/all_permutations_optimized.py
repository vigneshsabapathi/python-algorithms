#!/usr/bin/env python3
"""
Optimized and alternative implementations of All Permutations.

Variants covered:
1. itertools.permutations  -- stdlib, fastest; C-level generator.
2. swap_backtrack          -- in-place swapping, O(1) extra space (no used[]).
3. heaps_algorithm         -- classic minimal-swap algorithm; generates each
                              permutation with exactly one swap from the prior.
4. generator_backtrack     -- generator version; yields one permutation at a time,
                              no upfront list allocation.
5. math.factorial          -- count-only variant for when you just need the number.

Key insight for interviews:
    itertools.permutations is always fastest for generation.
    For counting only: math.factorial(n) is O(n) and the right answer.
    Swap-based backtracking is the interview answer (saves the used[] array).

Run:
    python backtracking/all_permutations_optimized.py
"""

from __future__ import annotations

import math
import timeit
from itertools import permutations
from typing import Generator


# ---------------------------------------------------------------------------
# Variant 1 — itertools (baseline)
# ---------------------------------------------------------------------------


def permutations_itertools(sequence: list[int | str]) -> list[list[int | str]]:
    """
    Fastest: delegates to C-level itertools.permutations.

    >>> permutations_itertools([1, 2, 3])
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    >>> permutations_itertools([1])
    [[1]]
    >>> permutations_itertools([])
    [[]]
    """
    return [list(p) for p in permutations(sequence)]


# ---------------------------------------------------------------------------
# Variant 2 — swap-based backtracking (O(1) extra space)
# ---------------------------------------------------------------------------


def permutations_swap(sequence: list[int | str]) -> list[list[int | str]]:
    """
    In-place swapping: no auxiliary used[] array needed.
    At each level, swap the current index with every index >= current,
    recurse, then swap back. Space: O(n) stack only.

    >>> sorted(permutations_swap([1, 2, 3]))
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    >>> permutations_swap([1])
    [[1]]
    >>> permutations_swap([])
    [[]]
    """
    result: list[list[int | str]] = []

    def _swap_backtrack(start: int) -> None:
        if start == len(sequence):
            result.append(sequence[:])
            return
        for i in range(start, len(sequence)):
            sequence[start], sequence[i] = sequence[i], sequence[start]
            _swap_backtrack(start + 1)
            sequence[start], sequence[i] = sequence[i], sequence[start]

    _swap_backtrack(0)
    return result


# ---------------------------------------------------------------------------
# Variant 3 — Heap's algorithm (minimal writes)
# ---------------------------------------------------------------------------


def permutations_heaps(sequence: list[int | str]) -> list[list[int | str]]:
    """
    Heap's algorithm: generates each permutation with a single swap.
    Produces exactly n! permutations with minimal write operations.
    Often the fastest pure-Python recursive approach.

    >>> sorted(permutations_heaps([1, 2, 3]))
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    >>> permutations_heaps([1])
    [[1]]
    >>> permutations_heaps([])
    [[]]
    """
    result: list[list[int | str]] = []
    if not sequence:
        return [[]]

    def _heap(k: int) -> None:
        if k == 1:
            result.append(sequence[:])
            return
        _heap(k - 1)
        for i in range(k - 1):
            if k % 2 == 0:
                sequence[i], sequence[k - 1] = sequence[k - 1], sequence[i]
            else:
                sequence[0], sequence[k - 1] = sequence[k - 1], sequence[0]
            _heap(k - 1)

    _heap(len(sequence))
    return result


# ---------------------------------------------------------------------------
# Variant 4 — generator backtracking (memory-efficient)
# ---------------------------------------------------------------------------


def permutations_generator(sequence: list[int | str]) -> Generator[list[int | str], None, None]:
    """
    Generator-based backtracking: yields one permutation at a time.
    No upfront list allocation — use when iterating without storing all.

    >>> sorted(permutations_generator([1, 2, 3]))
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    >>> list(permutations_generator([1]))
    [[1]]
    >>> list(permutations_generator([]))
    [[]]
    """
    n = len(sequence)
    used = [False] * n

    def _gen(path: list[int | str]) -> Generator[list[int | str], None, None]:
        if len(path) == n:
            yield path[:]
            return
        for i in range(n):
            if not used[i]:
                used[i] = True
                path.append(sequence[i])
                yield from _gen(path)
                path.pop()
                used[i] = False

    yield from _gen([])


# ---------------------------------------------------------------------------
# Variant 5 — count only (math.factorial)
# ---------------------------------------------------------------------------


def count_permutations(n: int) -> int:
    """
    Count-only: returns n! without generating the permutations.
    O(n) time, O(1) space.

    >>> count_permutations(4)
    24
    >>> count_permutations(10)
    3628800
    >>> count_permutations(0)
    1
    """
    return math.factorial(n)


# ---------------------------------------------------------------------------
# Benchmark + correctness
# ---------------------------------------------------------------------------


def run_all() -> None:
    print("\n=== Correctness check ===")
    for original in [[1, 2, 3], ["A", "B", "C"], [1], [3, 1, 2], [1, 2, 3, 4]]:
        seq = original[:]
        ref = sorted(map(tuple, permutations_itertools(seq[:])))
        r_swap = sorted(map(tuple, permutations_swap(seq[:])))
        r_heap = sorted(map(tuple, permutations_heaps(seq[:])))
        r_gen = sorted(map(tuple, permutations_generator(seq[:])))
        all_match = r_swap == ref and r_heap == ref and r_gen == ref
        print(f"  {str(original):>25}  n={len(original)}  n!={math.factorial(len(original)):>6}  "
              f"{'OK' if all_match else 'MISMATCH'}")

    REPS = 3000
    print(f"\n=== Benchmark ({REPS} runs each) ===")
    print(f"  {'n':>3} {'n!':>8}  {'itertools':>12}  {'swap_bt':>12}  "
          f"{'heaps':>12}  {'generator':>12}")

    for n in [3, 4, 5, 6, 7]:
        seq = list(range(1, n + 1))
        cnt = math.factorial(n)
        t_it = timeit.timeit(lambda: permutations_itertools(seq[:]), number=REPS) * 1000 / REPS
        t_swap = timeit.timeit(lambda: permutations_swap(seq[:]), number=REPS) * 1000 / REPS
        t_heap = timeit.timeit(lambda: permutations_heaps(seq[:]), number=REPS) * 1000 / REPS
        t_gen = timeit.timeit(lambda: list(permutations_generator(seq[:])), number=REPS) * 1000 / REPS
        print(f"  {n:>3} {cnt:>8}  {t_it:>11.4f}ms  {t_swap:>11.4f}ms  "
              f"{t_heap:>11.4f}ms  {t_gen:>11.4f}ms")

    print("\n=== math.factorial (count only) ===")
    for n in [5, 10, 15, 20]:
        t = timeit.timeit(lambda: math.factorial(n), number=100000) * 1000 / 100000
        print(f"  {n}! = {math.factorial(n):>18}  {t:.6f} ms/call")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
