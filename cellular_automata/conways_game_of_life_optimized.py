"""
Conway's Game of Life - Optimized Variants with Benchmark
https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

Variant 1: list_based       - Nested lists with manual neighbour counting
Variant 2: numpy_convolve   - NumPy 2D convolution for neighbour counting
Variant 3: set_based        - Sparse set representation (only live cells tracked)
"""

from __future__ import annotations

import time
from typing import Any

import numpy as np
from scipy.signal import convolve2d

# ---- Patterns ----
BLINKER = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]

GLIDER = [
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]


# ---- Variant 1: List-Based ----
def new_generation_list(cells: list[list[int]]) -> list[list[int]]:
    """
    Pure Python nested-list approach with manual neighbour counting.

    >>> new_generation_list(BLINKER)
    [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
    """
    rows, cols = len(cells), len(cells[0])
    next_gen = []
    for i in range(rows):
        row = []
        for j in range(cols):
            count = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    r, c = i + dr, j + dc
                    if 0 <= r < rows and 0 <= c < cols:
                        count += cells[r][c]
            alive = cells[i][j] == 1
            if (alive and 2 <= count <= 3) or (not alive and count == 3):
                row.append(1)
            else:
                row.append(0)
        next_gen.append(row)
    return next_gen


# ---- Variant 2: NumPy Convolution ----
KERNEL = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=np.int8)


def new_generation_numpy(cells: np.ndarray) -> np.ndarray:
    """
    NumPy convolution-based approach. Counts neighbours via 2D convolution.

    >>> grid = np.array(BLINKER)
    >>> new_generation_numpy(grid).tolist()
    [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
    """
    neighbours = convolve2d(cells, KERNEL, mode="same", boundary="fill", fillvalue=0)
    # Apply rules: survive if alive with 2-3 neighbours, born if dead with 3
    survive = (cells == 1) & ((neighbours == 2) | (neighbours == 3))
    born = (cells == 0) & (neighbours == 3)
    return (survive | born).astype(np.int8)


# ---- Variant 3: Set-Based (Sparse) ----
def new_generation_set(
    live_cells: set[tuple[int, int]], rows: int, cols: int
) -> set[tuple[int, int]]:
    """
    Sparse set-based approach. Only tracks live cells. Ideal for large
    grids with few live cells.

    >>> cells = {(0, 1), (1, 1), (2, 1)}  # vertical blinker in 3x3
    >>> sorted(new_generation_set(cells, 3, 3))
    [(1, 0), (1, 1), (1, 2)]
    """
    # Count neighbours for all cells adjacent to any live cell
    neighbour_count: dict[tuple[int, int], int] = {}
    for r, c in live_cells:
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    neighbour_count[(nr, nc)] = neighbour_count.get((nr, nc), 0) + 1

    # Apply rules
    new_live: set[tuple[int, int]] = set()
    for pos, count in neighbour_count.items():
        if count == 3 or (count == 2 and pos in live_cells):
            new_live.add(pos)
    return new_live


# ---- Conversion helpers ----
def grid_to_set(grid: list[list[int]]) -> set[tuple[int, int]]:
    """
    >>> sorted(grid_to_set([[0, 1], [1, 0]]))
    [(0, 1), (1, 0)]
    """
    return {(r, c) for r, row in enumerate(grid) for c, v in enumerate(row) if v}


def set_to_grid(live: set[tuple[int, int]], rows: int, cols: int) -> list[list[int]]:
    """
    >>> set_to_grid({(0, 1), (1, 0)}, 2, 2)
    [[0, 1], [1, 0]]
    """
    return [[1 if (r, c) in live else 0 for c in range(cols)] for r in range(rows)]


# ---- Benchmark ----
def benchmark(grid_size: int = 100, generations: int = 50, density: float = 0.3) -> None:
    """Run all three variants and compare performance."""
    import random

    random.seed(42)

    # Create random grid
    grid = [
        [1 if random.random() < density else 0 for _ in range(grid_size)]
        for _ in range(grid_size)
    ]
    np_grid = np.array(grid, dtype=np.int8)
    set_grid = grid_to_set(grid)

    print(f"Conway's Game of Life Benchmark")
    print(f"Grid: {grid_size}x{grid_size}, Generations: {generations}, "
          f"Density: {density}")
    print("=" * 55)

    # Variant 1: List-based
    g = [row[:] for row in grid]
    start = time.perf_counter()
    for _ in range(generations):
        g = new_generation_list(g)
    t1 = time.perf_counter() - start
    list_alive = sum(sum(row) for row in g)

    # Variant 2: NumPy convolution
    g2 = np_grid.copy()
    start = time.perf_counter()
    for _ in range(generations):
        g2 = new_generation_numpy(g2)
    t2 = time.perf_counter() - start
    numpy_alive = int(g2.sum())

    # Variant 3: Set-based
    g3 = set_grid.copy()
    start = time.perf_counter()
    for _ in range(generations):
        g3 = new_generation_set(g3, grid_size, grid_size)
    t3 = time.perf_counter() - start
    set_alive = len(g3)

    print(f"{'Variant':<25} {'Time (s)':<12} {'Alive cells':<12} {'Speedup'}")
    print("-" * 55)
    print(f"{'1. list_based':<25} {t1:<12.4f} {list_alive:<12}")
    print(f"{'2. numpy_convolve':<25} {t2:<12.4f} {numpy_alive:<12} {t1/t2:.1f}x")
    print(f"{'3. set_based':<25} {t3:<12.4f} {set_alive:<12} {t1/t3:.1f}x")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
