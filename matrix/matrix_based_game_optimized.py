#!/usr/bin/env python3
"""
Optimized and alternative implementations of Matrix-Based Game.

The reference uses recursive DFS for flood-fill, manual gravity simulation,
and manual column shifting. Score = n*(n+1)/2 for n removed elements.

Three alternatives:
  bfs_flood_fill    -- Use BFS instead of DFS (avoids stack overflow on large grids)
  numpy_gravity     -- Vectorized gravity using sorting approach
  optimized_game    -- Combined optimizations: iterative BFS + efficient column compaction

Run:
    python matrix/matrix_based_game_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from matrix.matrix_based_game import process_game as reference


# ---------------------------------------------------------------------------
# Variant 1 -- BFS flood fill (iterative, no recursion depth issues)
# ---------------------------------------------------------------------------

def find_connected_bfs(
    matrix: list[list[str]], row: int, col: int, size: int
) -> set[tuple[int, int]]:
    """
    Find connected same-colored cells using BFS.

    >>> m = [['A', 'B', 'A'], ['A', 'B', 'A'], ['A', 'A', 'A']]
    >>> sorted(find_connected_bfs(m, 0, 0, 3))
    [(0, 0), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
    >>> find_connected_bfs([['-', '-'], ['-', '-']], 0, 0, 2)
    set()
    """
    actual_row = size - 1 - col
    color = matrix[actual_row][row]
    if color == "-":
        return set()

    visited = set()
    queue = deque([(actual_row, row)])
    visited.add((actual_row, row))
    connected = set()

    while queue:
        r, c = queue.popleft()
        if matrix[r][c] == color:
            connected.add((r, c))
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < size and 0 <= nc < size and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc))

    return connected


# ---------------------------------------------------------------------------
# Variant 2 -- Efficient gravity using list filtering
# ---------------------------------------------------------------------------

def apply_gravity_efficient(matrix: list[list[str]], size: int) -> list[list[str]]:
    """
    Apply gravity by filtering non-empty cells per column, then padding with '-'.

    >>> apply_gravity_efficient([['-', 'A'], ['B', '-'], ['C', 'D']], 3)
    [['-', '-'], ['B', 'A'], ['C', 'D']]
    """
    for col in range(len(matrix[0])):
        # Collect non-empty cells from top to bottom
        non_empty = [matrix[r][col] for r in range(len(matrix)) if matrix[r][col] != "-"]
        padding = len(matrix) - len(non_empty)
        for r in range(len(matrix)):
            if r < padding:
                matrix[r][col] = "-"
            else:
                matrix[r][col] = non_empty[r - padding]
    return matrix


# ---------------------------------------------------------------------------
# Variant 3 -- Complete optimized game loop
# ---------------------------------------------------------------------------

def process_game_optimized(
    size: int, matrix: list[str], moves: list[tuple[int, int]]
) -> int:
    """
    Optimized game processing with BFS and efficient gravity.

    >>> process_game_optimized(3, ['aaa', 'bbb', 'ccc'], [(0, 0)])
    6
    >>> process_game_optimized(2, ['RG', 'RG'], [(0, 0)])
    3
    """
    game_matrix = [list(row) for row in matrix]
    total_score = 0

    for pos_x, pos_y in moves:
        connected = find_connected_bfs(game_matrix, pos_x, pos_y, size)
        if not connected:
            continue

        count = len(connected)
        total_score += count * (count + 1) // 2

        for r, c in connected:
            game_matrix[r][c] = "-"

        game_matrix = apply_gravity_efficient(game_matrix, size)

        # Compact empty columns to the right
        cols_data = list(zip(*game_matrix))
        non_empty = [list(col) for col in cols_data if any(c != "-" for c in col)]
        empty = [list(col) for col in cols_data if all(c == "-" for c in col)]
        all_cols = non_empty + empty
        if all_cols:
            game_matrix = [list(row) for row in zip(*all_cols)]

    return total_score


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------

def benchmark() -> None:
    size = 4
    matrix = ['RRBG', 'RBBG', 'YYGG', 'XYGG']
    moves = [(0, 1), (1, 1)]

    number = 10_000
    print(f"Benchmark ({number} runs):\n")

    funcs = [
        ("reference", lambda: reference(size, matrix, moves)),
        ("optimized (BFS + efficient gravity)", lambda: process_game_optimized(size, matrix, moves)),
    ]

    for name, func in funcs:
        t = timeit.timeit(func, number=number)
        print(f"  {name:45s} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
