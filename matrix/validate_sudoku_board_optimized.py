#!/usr/bin/env python3
"""
Optimized and alternative implementations of Sudoku Board Validation.

The reference uses defaultdict of sets: O(81) = O(1) time and space.
Already very efficient for the fixed 9x9 size.

Three alternatives:
  bitmask_validation  -- Use integers as bitmasks instead of sets
  array_validation    -- Use fixed arrays instead of dicts
  one_pass_encoding   -- Encode (value, row/col/box) into a single set

Run:
    python matrix/validate_sudoku_board_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matrix.validate_sudoku_board import is_valid_sudoku_board as reference


valid_board = [
    ["5","3",".",".","7",".",".",".","."],
    ["6",".",".","1","9","5",".",".","."],
    [".","9","8",".",".",".",".","6","."],
    ["8",".",".",".","6",".",".",".","3"],
    ["4",".",".","8",".","3",".",".","1"],
    ["7",".",".",".","2",".",".",".","6"],
    [".","6",".",".",".",".","2","8","."],
    [".",".",".","4","1","9",".",".","5"],
    [".",".",".",".","8",".",".","7","9"],
]

invalid_board = [
    ["8","3",".",".","7",".",".",".","."],
    ["6",".",".","1","9","5",".",".","."],
    [".","9","8",".",".",".",".","6","."],
    ["8",".",".",".","6",".",".",".","3"],
    ["4",".",".","8",".","3",".",".","1"],
    ["7",".",".",".","2",".",".",".","6"],
    [".","6",".",".",".",".","2","8","."],
    [".",".",".","4","1","9",".",".","5"],
    [".",".",".",".","8",".",".","7","9"],
]


# ---------------------------------------------------------------------------
# Variant 1 -- Bitmask validation (integer bits instead of sets)
# ---------------------------------------------------------------------------

def validate_bitmask(board: list[list[str]]) -> bool:
    """
    Use integer bitmasks to track seen digits. Bit i represents digit i.

    >>> validate_bitmask(valid_board)
    True
    >>> validate_bitmask(invalid_board)
    False
    """
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9

    for r in range(9):
        for c in range(9):
            if board[r][c] == ".":
                continue
            bit = 1 << int(board[r][c])
            box_idx = (r // 3) * 3 + (c // 3)
            if rows[r] & bit or cols[c] & bit or boxes[box_idx] & bit:
                return False
            rows[r] |= bit
            cols[c] |= bit
            boxes[box_idx] |= bit

    return True


# ---------------------------------------------------------------------------
# Variant 2 -- Array-based validation (pre-allocated arrays)
# ---------------------------------------------------------------------------

def validate_arrays(board: list[list[str]]) -> bool:
    """
    Use pre-allocated boolean arrays instead of dicts/sets.

    >>> validate_arrays(valid_board)
    True
    >>> validate_arrays(invalid_board)
    False
    """
    rows = [[False] * 10 for _ in range(9)]
    cols = [[False] * 10 for _ in range(9)]
    boxes = [[False] * 10 for _ in range(9)]

    for r in range(9):
        for c in range(9):
            if board[r][c] == ".":
                continue
            num = int(board[r][c])
            box_idx = (r // 3) * 3 + (c // 3)
            if rows[r][num] or cols[c][num] or boxes[box_idx][num]:
                return False
            rows[r][num] = True
            cols[c][num] = True
            boxes[box_idx][num] = True

    return True


# ---------------------------------------------------------------------------
# Variant 3 -- Single set with encoded keys
# ---------------------------------------------------------------------------

def validate_encoded_set(board: list[list[str]]) -> bool:
    """
    Encode each constraint as a string and check for duplicates in one set.
    E.g., "5 in row 0", "5 in col 0", "5 in box (0,0)".

    >>> validate_encoded_set(valid_board)
    True
    >>> validate_encoded_set(invalid_board)
    False
    """
    seen = set()
    for r in range(9):
        for c in range(9):
            v = board[r][c]
            if v == ".":
                continue
            row_key = (v, "r", r)
            col_key = (v, "c", c)
            box_key = (v, "b", r // 3, c // 3)
            if row_key in seen or col_key in seen or box_key in seen:
                return False
            seen.add(row_key)
            seen.add(col_key)
            seen.add(box_key)
    return True


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    number = 100_000
    print(f"Benchmark ({number} validations):\n")

    print("Valid board:")
    funcs = [
        ("reference (defaultdict sets)", lambda: reference(valid_board)),
        ("bitmask", lambda: validate_bitmask(valid_board)),
        ("arrays", lambda: validate_arrays(valid_board)),
        ("encoded_set", lambda: validate_encoded_set(valid_board)),
    ]
    for name, func in funcs:
        t = timeit.timeit(func, number=number)
        print(f"  {name:35s} {t:.4f}s")

    print("\nInvalid board (early exit):")
    funcs_inv = [
        ("reference", lambda: reference(invalid_board)),
        ("bitmask", lambda: validate_bitmask(invalid_board)),
        ("arrays", lambda: validate_arrays(invalid_board)),
        ("encoded_set", lambda: validate_encoded_set(invalid_board)),
    ]
    for name, func in funcs_inv:
        t = timeit.timeit(func, number=number)
        print(f"  {name:35s} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
