"""
Tower of Hanoi — Classic recursive problem.

Move n disks from source peg to target peg using an auxiliary peg,
moving only one disk at a time and never placing a larger disk on a smaller one.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/tower_of_hanoi.py
"""

from __future__ import annotations


def tower_of_hanoi(
    n: int, source: str = "A", target: str = "C", auxiliary: str = "B"
) -> list[tuple[str, str]]:
    """
    Solve Tower of Hanoi for n disks, returning the list of moves.

    Each move is a (from_peg, to_peg) tuple.

    >>> tower_of_hanoi(1)
    [('A', 'C')]
    >>> tower_of_hanoi(2)
    [('A', 'B'), ('A', 'C'), ('B', 'C')]
    >>> tower_of_hanoi(3)
    [('A', 'C'), ('A', 'B'), ('C', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('A', 'C')]
    >>> len(tower_of_hanoi(4))
    15
    >>> tower_of_hanoi(0)
    []
    """
    moves: list[tuple[str, str]] = []

    def _solve(n: int, src: str, tgt: str, aux: str) -> None:
        if n <= 0:
            return
        _solve(n - 1, src, aux, tgt)
        moves.append((src, tgt))
        _solve(n - 1, aux, tgt, src)

    _solve(n, source, target, auxiliary)
    return moves


if __name__ == "__main__":
    import doctest

    doctest.testmod()
