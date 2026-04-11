"""
Game of Life - Optimized Variants with Benchmark
https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

Variant 1: numpy_loop       - NumPy grid with per-cell loop (baseline)
Variant 2: numpy_vectorized - Fully vectorized with roll-based neighbour sum
Variant 3: scipy_convolve   - scipy.signal.convolve2d for neighbour counting
"""

from __future__ import annotations

import time

import numpy as np
from scipy.signal import convolve2d


# ---- Variant 1: NumPy with per-cell loop ----
def run_numpy_loop(canvas: np.ndarray) -> np.ndarray:
    """
    NumPy grid but iterates cell by cell. Baseline approach.

    >>> import numpy as np
    >>> blinker = np.array([[0,1,0],[0,1,0],[0,1,0]], dtype=np.int8)
    >>> run_numpy_loop(blinker).tolist()
    [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
    """
    rows, cols = canvas.shape
    next_gen = np.zeros_like(canvas)
    for r in range(rows):
        for c in range(cols):
            r0, r1 = max(0, r - 1), min(rows, r + 2)
            c0, c1 = max(0, c - 1), min(cols, c + 2)
            alive_count = int(canvas[r0:r1, c0:c1].sum()) - int(canvas[r, c])
            if canvas[r, c]:
                next_gen[r, c] = 1 if 2 <= alive_count <= 3 else 0
            else:
                next_gen[r, c] = 1 if alive_count == 3 else 0
    return next_gen


# ---- Variant 2: Fully vectorized with np.roll ----
def run_numpy_vectorized(canvas: np.ndarray) -> np.ndarray:
    """
    Fully vectorized approach using np.roll to count neighbours.
    No Python loops over cells.

    >>> import numpy as np
    >>> blinker = np.array([[0,1,0],[0,1,0],[0,1,0]], dtype=np.int8)
    >>> run_numpy_vectorized(blinker).tolist()
    [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
    """
    # Pad with zeros to handle boundaries (non-wrapping)
    padded = np.pad(canvas, 1, mode="constant", constant_values=0)
    # Sum all 8 neighbours using slicing on the padded array
    neighbours = (
        padded[:-2, :-2] + padded[:-2, 1:-1] + padded[:-2, 2:]
        + padded[1:-1, :-2]                    + padded[1:-1, 2:]
        + padded[2:, :-2]  + padded[2:, 1:-1]  + padded[2:, 2:]
    )
    # Apply rules vectorized
    survive = (canvas == 1) & ((neighbours == 2) | (neighbours == 3))
    born = (canvas == 0) & (neighbours == 3)
    return (survive | born).astype(canvas.dtype)


# ---- Variant 3: scipy convolve2d ----
KERNEL = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=np.int8)


def run_scipy_convolve(canvas: np.ndarray) -> np.ndarray:
    """
    Uses scipy.signal.convolve2d with a kernel that counts the 8 neighbours.

    >>> import numpy as np
    >>> blinker = np.array([[0,1,0],[0,1,0],[0,1,0]], dtype=np.int8)
    >>> run_scipy_convolve(blinker).tolist()
    [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
    """
    neighbours = convolve2d(canvas, KERNEL, mode="same", boundary="fill", fillvalue=0)
    survive = (canvas == 1) & ((neighbours == 2) | (neighbours == 3))
    born = (canvas == 0) & (neighbours == 3)
    return (survive | born).astype(canvas.dtype)


# ---- Benchmark ----
def benchmark(grid_size: int = 200, generations: int = 100, density: float = 0.3) -> None:
    """Run all three variants and compare performance."""
    np.random.seed(42)
    grid = (np.random.random((grid_size, grid_size)) < density).astype(np.int8)

    print(f"Game of Life Benchmark")
    print(f"Grid: {grid_size}x{grid_size}, Generations: {generations}, "
          f"Density: {density}")
    print("=" * 55)

    # Variant 1: loop
    g = grid.copy()
    start = time.perf_counter()
    for _ in range(generations):
        g = run_numpy_loop(g)
    t1 = time.perf_counter() - start

    # Variant 2: vectorized
    g2 = grid.copy()
    start = time.perf_counter()
    for _ in range(generations):
        g2 = run_numpy_vectorized(g2)
    t2 = time.perf_counter() - start

    # Variant 3: scipy
    g3 = grid.copy()
    start = time.perf_counter()
    for _ in range(generations):
        g3 = run_scipy_convolve(g3)
    t3 = time.perf_counter() - start

    assert np.array_equal(g, g2), "Mismatch: loop vs vectorized"
    assert np.array_equal(g, g3), "Mismatch: loop vs scipy"

    print(f"{'Variant':<25} {'Time (s)':<12} {'Speedup'}")
    print("-" * 55)
    print(f"{'1. numpy_loop':<25} {t1:<12.4f}")
    print(f"{'2. numpy_vectorized':<25} {t2:<12.4f} {t1/t2:.1f}x")
    print(f"{'3. scipy_convolve':<25} {t3:<12.4f} {t1/t3:.1f}x")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
