"""
Langton's Ant - Optimized Variants with Benchmark
https://en.wikipedia.org/wiki/Langton%27s_ant

Variant 1: list_based    - 2D list grid with class-based ant
Variant 2: numpy_based   - NumPy array grid with direct indexing
Variant 3: set_based     - Sparse set tracks only black cells (fastest for large grids)
"""

from __future__ import annotations

import time

import numpy as np


# ---- Variant 1: List-based ----
def run_list_based(width: int, height: int, steps: int) -> tuple[int, int]:
    """
    Pure Python list-based implementation.
    Returns (steps_completed, black_cell_count).

    >>> run_list_based(21, 21, 100)
    (100, 20)
    """
    board = [[True] * width for _ in range(height)]
    x, y = height // 2, width // 2
    direction = 0  # 0=Up, 1=Right, 2=Down, 3=Left
    dx_dy = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    completed = 0
    for _ in range(steps):
        if board[x][y]:
            direction = (direction + 1) % 4
        else:
            direction = (direction - 1) % 4
        board[x][y] = not board[x][y]
        dx, dy = dx_dy[direction]
        x, y = x + dx, y + dy
        if not (0 <= x < height and 0 <= y < width):
            break
        completed += 1

    black = sum(1 for row in board for c in row if not c)
    return completed, black


# ---- Variant 2: NumPy-based ----
def run_numpy_based(width: int, height: int, steps: int) -> tuple[int, int]:
    """
    NumPy array grid. Board stored as int8 (1=white, 0=black).
    Returns (steps_completed, black_cell_count).

    >>> run_numpy_based(21, 21, 100)
    (100, 20)
    """
    board = np.ones((height, width), dtype=np.int8)
    x, y = height // 2, width // 2
    direction = 0
    dx_dy = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    completed = 0
    for _ in range(steps):
        if board[x, y]:
            direction = (direction + 1) % 4
        else:
            direction = (direction - 1) % 4
        board[x, y] ^= 1
        dx, dy = dx_dy[direction]
        x, y = x + dx, y + dy
        if not (0 <= x < height and 0 <= y < width):
            break
        completed += 1

    black = int((board == 0).sum())
    return completed, black


# ---- Variant 3: Set-based (sparse) ----
def run_set_based(width: int, height: int, steps: int) -> tuple[int, int]:
    """
    Sparse representation: only black cells stored in a set.
    Fastest for large grids with few black cells.
    Returns (steps_completed, black_cell_count).

    >>> run_set_based(21, 21, 100)
    (100, 20)
    """
    black_cells: set[tuple[int, int]] = set()
    x, y = height // 2, width // 2
    direction = 0
    dx_dy = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    completed = 0
    for _ in range(steps):
        pos = (x, y)
        if pos not in black_cells:
            # White -> turn clockwise, make black
            direction = (direction + 1) % 4
            black_cells.add(pos)
        else:
            # Black -> turn counter-clockwise, make white
            direction = (direction - 1) % 4
            black_cells.discard(pos)

        dx, dy = dx_dy[direction]
        x, y = x + dx, y + dy
        if not (0 <= x < height and 0 <= y < width):
            break
        completed += 1

    return completed, len(black_cells)


# ---- Benchmark ----
def benchmark(width: int = 201, height: int = 201, steps: int = 11000) -> None:
    """Run all three variants and compare performance."""
    print(f"Langton's Ant Benchmark")
    print(f"Grid: {width}x{height}, Steps: {steps}")
    print("=" * 55)

    start = time.perf_counter()
    s1, b1 = run_list_based(width, height, steps)
    t1 = time.perf_counter() - start

    start = time.perf_counter()
    s2, b2 = run_numpy_based(width, height, steps)
    t2 = time.perf_counter() - start

    start = time.perf_counter()
    s3, b3 = run_set_based(width, height, steps)
    t3 = time.perf_counter() - start

    assert s1 == s2 == s3, f"Step mismatch: {s1}, {s2}, {s3}"
    assert b1 == b2 == b3, f"Black cell mismatch: {b1}, {b2}, {b3}"

    print(f"{'Variant':<25} {'Time (s)':<12} {'Steps':<10} {'Black':<10} {'Speedup'}")
    print("-" * 55)
    print(f"{'1. list_based':<25} {t1:<12.4f} {s1:<10} {b1:<10}")
    print(f"{'2. numpy_based':<25} {t2:<12.4f} {s2:<10} {b2:<10} {t1/t2:.1f}x")
    print(f"{'3. set_based':<25} {t3:<12.4f} {s3:<10} {b3:<10} {t1/t3:.1f}x")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
