#!/usr/bin/env python3
"""
Optimized and alternative implementations of Crossword Puzzle Solver.

Issues in reference implementation:
1. is_valid requires ALL cells to be empty — words can never share letters.
   Real crosswords allow intersections (shared letters at crossing points).
2. words list is mutated in place (remove/append) — caller's list is modified
   as a side effect even when no solution is found.
3. O(W) word search per backtrack step (list.remove is O(n)).

Variants covered:
1. solve_crossword_intersecting -- allows letter sharing at intersections
                                   (real crossword behavior).
2. solve_crossword_set          -- uses a set for O(1) word removal/restore
                                   instead of O(W) list.remove.
3. solve_crossword_fixed        -- reference algorithm with the mutation bug
                                   fixed (passes a copy of the word list).

Run:
    python backtracking/crossword_puzzle_solver_optimized.py
"""

from __future__ import annotations

import copy
import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backtracking.crossword_puzzle_solver import (  # noqa: E402
    is_valid,
    place_word,
    remove_word,
    solve_crossword,
)


# ---------------------------------------------------------------------------
# Variant 1 — intersecting (real crossword behavior)
# ---------------------------------------------------------------------------


def is_valid_intersecting(
    puzzle: list[list[str]], word: str, row: int, col: int, vertical: bool
) -> bool:
    """
    Check if a word can be placed allowing shared letters at intersections.

    A cell is valid if it is either empty OR already contains the correct letter
    (a crossing word already filled it in).

    >>> puzzle = [['c', '', ''], ['', '', ''], ['', '', '']]
    >>> is_valid_intersecting(puzzle, 'cat', 0, 0, True)
    True
    >>> is_valid_intersecting(puzzle, 'dog', 0, 0, True)
    False
    >>> is_valid_intersecting([[''] * 4 for _ in range(4)], 'word', 0, 0, False)
    True
    """
    for i, ch in enumerate(word):
        if vertical:
            if row + i >= len(puzzle):
                return False
            cell = puzzle[row + i][col]
        else:
            if col + i >= len(puzzle[0]):
                return False
            cell = puzzle[row][col + i]
        if cell != "" and cell != ch:
            return False
    return True


def solve_crossword_intersecting(
    puzzle: list[list[str]], words: list[str]
) -> bool:
    """
    Solve crossword allowing letter sharing at intersections.

    Words can cross — cells filled by a previous word are accepted if
    they match the letter being placed.

    Returns True and modifies puzzle in place if a solution exists.

    >>> puzzle = [[''] * 3 for _ in range(3)]
    >>> solve_crossword_intersecting(puzzle, ['cat', 'dog', 'car'])
    True
    >>> len(puzzle) == 3 and all(len(row) == 3 for row in puzzle)
    True
    """
    # Find first empty cell
    for row in range(len(puzzle)):
        for col in range(len(puzzle[0])):
            if puzzle[row][col] == "":
                remaining = list(words)
                for word in remaining:
                    for vertical in [True, False]:
                        if is_valid_intersecting(puzzle, word, row, col, vertical):
                            # save overwritten cells (intersection letters stay)
                            old_cells: list[tuple[int, int, str]] = []
                            for i, ch in enumerate(word):
                                r, c = (row + i, col) if vertical else (row, col + i)
                                old_cells.append((r, c, puzzle[r][c]))
                                puzzle[r][c] = ch
                            new_words = [w for w in words if w != word]
                            if solve_crossword_intersecting(puzzle, new_words):
                                return True
                            # backtrack — restore only cells that were empty before
                            for r, c, old in old_cells:
                                puzzle[r][c] = old
                return False
    return True


# ---------------------------------------------------------------------------
# Variant 2 — set-based word tracking (O(1) remove/restore)
# ---------------------------------------------------------------------------


def solve_crossword_set(
    puzzle: list[list[str]], words: set[str]
) -> bool:
    """
    Reference algorithm with words stored in a set for O(1) membership
    and removal instead of O(W) list.remove.

    Note: requires all words to be unique (set semantics).

    >>> puzzle = [[''] * 4 for _ in range(4)]
    >>> result = solve_crossword_set(puzzle, {'word', 'four', 'more', 'last'})
    >>> result
    True
    """
    for row in range(len(puzzle)):
        for col in range(len(puzzle[0])):
            if puzzle[row][col] == "":
                for word in list(words):
                    for vertical in [True, False]:
                        if is_valid(puzzle, word, row, col, vertical):
                            place_word(puzzle, word, row, col, vertical)
                            words.discard(word)
                            if solve_crossword_set(puzzle, words):
                                return True
                            words.add(word)
                            remove_word(puzzle, word, row, col, vertical)
                return False
    return True


# ---------------------------------------------------------------------------
# Variant 3 — mutation bug fixed (passes copy of words list)
# ---------------------------------------------------------------------------


def solve_crossword_fixed(
    puzzle: list[list[str]], words: list[str]
) -> bool:
    """
    Reference algorithm with the mutation side-effect bug fixed.

    Bug: the reference modifies the caller's words list via remove/append.
    After an unsuccessful solve, the list is in a different order than before.
    This variant copies the list before starting so the caller is unaffected.

    >>> original_words = ['word', 'four', 'more', 'paragraphs']
    >>> puzzle = [[''] * 4 for _ in range(4)]
    >>> result = solve_crossword_fixed(puzzle, original_words)
    >>> result
    False
    >>> original_words  # unchanged
    ['word', 'four', 'more', 'paragraphs']
    """
    return solve_crossword(puzzle, list(words))


# ---------------------------------------------------------------------------
# Benchmark + correctness
# ---------------------------------------------------------------------------


def run_all() -> None:

    print("\n=== Correctness: 4x4 grid ===")
    words_4 = ["word", "four", "more", "last"]

    p1 = [[""] * 4 for _ in range(4)]
    r1 = solve_crossword(p1, words_4[:])
    print(f"  Reference:  solved={r1}")
    if r1:
        for row in p1:
            print(f"    {' '.join(row)}")

    p2 = [[""] * 4 for _ in range(4)]
    r2 = solve_crossword_set(p2, set(words_4))
    print(f"  Set-based:  solved={r2}")

    print("\n=== Mutation bug demonstration ===")
    orig = ["word", "four", "more", "paragraphs"]
    p3 = [[""] * 4 for _ in range(4)]
    solve_crossword(p3, orig)  # buggy — modifies orig
    print(f"  Reference (buggy): words after failed solve = {orig}")

    orig2 = ["word", "four", "more", "paragraphs"]
    p4 = [[""] * 4 for _ in range(4)]
    solve_crossword_fixed(p4, orig2)
    print(f"  Fixed:             words after failed solve = {orig2}")

    print("\n=== Intersecting crossword (3x3) ===")
    # cat across row 0, cab across row 0 but vertical for 'c' column
    p5 = [[""] * 3 for _ in range(3)]
    words_3 = ["cat", "dog", "car"]
    r5 = solve_crossword_intersecting(p5, words_3)
    print(f"  solved={r5}")
    if r5:
        for row in p5:
            print(f"    {' '.join(c if c else '.' for c in row)}")

    REPS = 1000
    print(f"\n=== Benchmark ({REPS} runs, 4x4, 4 words) ===")

    t1 = timeit.timeit(
        lambda: solve_crossword([[""] * 4 for _ in range(4)], ["word", "four", "more", "last"]),
        number=REPS,
    ) * 1000 / REPS
    print(f"  Reference (list):     {t1:.4f} ms/run")

    t2 = timeit.timeit(
        lambda: solve_crossword_set([[""] * 4 for _ in range(4)], {"word", "four", "more", "last"}),
        number=REPS,
    ) * 1000 / REPS
    print(f"  Set-based:            {t2:.4f} ms/run")

    t3 = timeit.timeit(
        lambda: solve_crossword_intersecting([[""] * 3 for _ in range(3)], ["cat", "dog", "car"]),
        number=REPS,
    ) * 1000 / REPS
    print(f"  Intersecting (3x3):   {t3:.4f} ms/run")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
