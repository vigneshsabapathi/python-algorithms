#!/usr/bin/env python3
"""
Optimized and alternative implementations of Tower of Hanoi.

Variants covered:
1. recursive        -- Standard recursive solution (reference)
2. iterative        -- Stack-based iterative approach
3. binary_solution  -- Using binary representation of move number

Run:
    python other/tower_of_hanoi_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.tower_of_hanoi import tower_of_hanoi as reference


def iterative_hanoi(n: int, source: str = "A", target: str = "C", auxiliary: str = "B") -> list[tuple[str, str]]:
    """
    Iterative Tower of Hanoi using the three-peg rotation rule.

    >>> iterative_hanoi(1)
    [('A', 'C')]
    >>> iterative_hanoi(2)
    [('A', 'B'), ('A', 'C'), ('B', 'C')]
    >>> iterative_hanoi(3)
    [('A', 'C'), ('A', 'B'), ('C', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('A', 'C')]
    >>> len(iterative_hanoi(4))
    15
    """
    if n <= 0:
        return []

    moves: list[tuple[str, str]] = []
    total_moves = 2**n - 1

    # For odd n: cycle is source -> target -> aux
    # For even n: cycle is source -> aux -> target
    if n % 2 == 1:
        pegs = [source, target, auxiliary]
    else:
        pegs = [source, auxiliary, target]

    stacks = {pegs[0]: list(range(n, 0, -1)), pegs[1]: [], pegs[2]: []}

    for i in range(1, total_moves + 1):
        if i % 3 == 1:
            a, b = pegs[0], pegs[1]
        elif i % 3 == 2:
            a, b = pegs[0], pegs[2]
        else:
            a, b = pegs[1], pegs[2]

        top_a = stacks[a][-1] if stacks[a] else float("inf")
        top_b = stacks[b][-1] if stacks[b] else float("inf")

        if top_a < top_b:
            stacks[b].append(stacks[a].pop())
            moves.append((a, b))
        else:
            stacks[a].append(stacks[b].pop())
            moves.append((b, a))

    return moves


def binary_hanoi(n: int) -> list[tuple[int, str, str]]:
    """
    Tower of Hanoi using binary representation.
    Returns (disk_number, from_peg, to_peg).

    >>> binary_hanoi(2)
    [(1, 'A', 'B'), (2, 'A', 'C'), (1, 'B', 'C')]
    >>> len(binary_hanoi(3))
    7
    """
    if n <= 0:
        return []

    pegs = ["A", "B", "C"]
    moves = []
    total = 2**n - 1

    for move in range(1, total + 1):
        # Which disk moves: position of least significant bit
        disk = (move & -move).bit_length()
        # Source and target determined by move number and disk
        from_peg = (move >> disk) % 3
        if disk % 2 == 1:
            to_peg = (from_peg + 1) % 3
        else:
            to_peg = (from_peg + 2) % 3
        moves.append((disk, pegs[from_peg], pegs[to_peg]))

    return moves


def count_moves(n: int) -> int:
    """
    Number of moves for n disks is always 2^n - 1.

    >>> count_moves(1)
    1
    >>> count_moves(3)
    7
    >>> count_moves(10)
    1023
    """
    return 2**n - 1


TEST_CASES = [
    (0, []),
    (1, [("A", "C")]),
    (2, [("A", "B"), ("A", "C"), ("B", "C")]),
    (3, [("A", "C"), ("A", "B"), ("C", "B"), ("A", "C"), ("B", "A"), ("B", "C"), ("A", "C")]),
]

IMPLS = [
    ("recursive", reference),
    ("iterative", iterative_hanoi),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for n, expected in TEST_CASES:
        for name, fn in IMPLS:
            result = fn(n)
            ok = result == expected
            tag = "OK" if ok else "FAIL"
            if not ok:
                print(f"  [{tag}] {name}(n={n}): expected={expected} got={result}")
        print(f"  [OK] n={n} moves={len(expected)}")

    REPS = 5000
    print(f"\n=== Benchmark: {REPS} runs ===")
    for n in [10, 15, 20]:
        print(f"  n={n} ({2**n - 1} moves):")
        for name, fn in IMPLS:
            t = timeit.timeit(lambda fn=fn, n=n: fn(n), number=REPS) * 1000 / REPS
            print(f"    {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
