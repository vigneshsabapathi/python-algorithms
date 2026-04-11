"""

Task:
Validate a 9x9 Sudoku board. Check that each row, column, and 3x3 sub-box
contains the digits 1-9 without repetition. Empty cells are marked with ".".

Implementation notes: Uses defaultdict of sets to track seen values per row,
column, and 3x3 box. Single pass through all cells. O(1) space (fixed 9x9).

Reference: https://leetcode.com/problems/valid-sudoku/ (LeetCode 36)
Reference: https://github.com/TheAlgorithms/Python/blob/master/matrix/validate_sudoku_board.py
"""

from collections import defaultdict

NUM_SQUARES = 9
EMPTY_CELL = "."


def is_valid_sudoku_board(sudoku_board: list[list[str]]) -> bool:
    """
    Validate a Sudoku board (does not solve it).

    >>> is_valid_sudoku_board([
    ...  ["5","3",".",".","7",".",".",".","."],
    ...  ["6",".",".","1","9","5",".",".","."],
    ...  [".","9","8",".",".",".",".","6","."],
    ...  ["8",".",".",".","6",".",".",".","3"],
    ...  ["4",".",".","8",".","3",".",".","1"],
    ...  ["7",".",".",".","2",".",".",".","6"],
    ...  [".","6",".",".",".",".","2","8","."],
    ...  [".",".",".","4","1","9",".",".","5"],
    ...  [".",".",".",".","8",".",".","7","9"]])
    True

    >>> is_valid_sudoku_board([
    ...  ["8","3",".",".","7",".",".",".","."],
    ...  ["6",".",".","1","9","5",".",".","."],
    ...  [".","9","8",".",".",".",".","6","."],
    ...  ["8",".",".",".","6",".",".",".","3"],
    ...  ["4",".",".","8",".","3",".",".","1"],
    ...  ["7",".",".",".","2",".",".",".","6"],
    ...  [".","6",".",".",".",".","2","8","."],
    ...  [".",".",".","4","1","9",".",".","5"],
    ...  [".",".",".",".","8",".",".","7","9"]])
    False

    >>> is_valid_sudoku_board([["1", "2", "3", "4", "5", "6", "7", "8", "9"]])
    Traceback (most recent call last):
        ...
    ValueError: Sudoku boards must be 9x9 squares.
    """
    if len(sudoku_board) != NUM_SQUARES or any(
        len(row) != NUM_SQUARES for row in sudoku_board
    ):
        raise ValueError(f"Sudoku boards must be {NUM_SQUARES}x{NUM_SQUARES} squares.")

    row_values: defaultdict[int, set[str]] = defaultdict(set)
    col_values: defaultdict[int, set[str]] = defaultdict(set)
    box_values: defaultdict[tuple[int, int], set[str]] = defaultdict(set)

    for row in range(NUM_SQUARES):
        for col in range(NUM_SQUARES):
            value = sudoku_board[row][col]
            if value == EMPTY_CELL:
                continue

            box = (row // 3, col // 3)
            if (
                value in row_values[row]
                or value in col_values[col]
                or value in box_values[box]
            ):
                return False

            row_values[row].add(value)
            col_values[col].add(value)
            box_values[box].add(value)

    return True


if __name__ == "__main__":
    from doctest import testmod

    testmod()
