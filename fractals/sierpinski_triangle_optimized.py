"""
Sierpinski Triangle — Optimized Variants with Benchmark

Variant 1 (recursive_coords): Original recursive midpoint subdivision
Variant 2 (chaos_game): Stochastic chaos-game Monte Carlo approach
Variant 3 (bitwise): Bitwise AND rule on a grid (no recursion)
"""

import random
import time

import numpy as np


# --- Variant 1: Recursive coordinate subdivision ---
def sierpinski_recursive(
    v1: tuple[float, float],
    v2: tuple[float, float],
    v3: tuple[float, float],
    depth: int,
) -> list[tuple]:
    """
    Return list of filled triangles via recursive midpoint subdivision.

    >>> len(sierpinski_recursive((0,0), (1,0), (0.5,1), 3))
    27
    """
    if depth == 0:
        return [(v1, v2, v3)]
    m12 = ((v1[0]+v2[0])/2, (v1[1]+v2[1])/2)
    m23 = ((v2[0]+v3[0])/2, (v2[1]+v3[1])/2)
    m13 = ((v1[0]+v3[0])/2, (v1[1]+v3[1])/2)
    return (
        sierpinski_recursive(v1, m12, m13, depth-1)
        + sierpinski_recursive(m12, v2, m23, depth-1)
        + sierpinski_recursive(m13, m23, v3, depth-1)
    )


# --- Variant 2: Chaos Game ---
def sierpinski_chaos_game(
    n_points: int = 10000,
    vertices: tuple = ((0, 0), (1, 0), (0.5, 0.866)),
    seed: int = 42,
) -> list[tuple[float, float]]:
    """
    Generate points via the chaos game: start anywhere, repeatedly jump
    halfway toward a randomly chosen vertex.  Converges to Sierpinski triangle.

    >>> pts = sierpinski_chaos_game(100, seed=42)
    >>> len(pts)
    100
    >>> all(0 <= x <= 1 and 0 <= y <= 0.866 for x, y in pts)
    True
    """
    rng = random.Random(seed)
    x, y = 0.5, 0.5
    points = []
    for _ in range(n_points):
        vx, vy = vertices[rng.randint(0, 2)]
        x, y = (x + vx) / 2, (y + vy) / 2
        points.append((x, y))
    return points


# --- Variant 3: Bitwise grid (Pascal's triangle mod 2) ---
def sierpinski_bitwise(size: int = 64) -> np.ndarray:
    """
    Build a Sierpinski pattern using the rule: pixel (r, c) is filled
    iff (r & c) == 0.  This is equivalent to Pascal's triangle mod 2.

    >>> grid = sierpinski_bitwise(8)
    >>> grid.shape
    (8, 8)
    >>> int(grid[0, 0])
    1
    >>> int(grid[3, 1])
    0
    >>> int(grid.sum())
    27
    """
    rows = np.arange(size).reshape((size, 1))
    cols = np.arange(size).reshape((1, size))
    return ((rows & cols) == 0).astype(np.int8)


def benchmark(depth: int = 7, n_points: int = 50000, grid_size: int = 256) -> None:
    """Run all three variants and compare timing."""
    print(f"Benchmark: depth={depth}, chaos_points={n_points}, grid={grid_size}\n")

    # Variant 1: recursive
    times = []
    for _ in range(3):
        start = time.perf_counter()
        tris = sierpinski_recursive((0, 0), (1, 0), (0.5, 0.866), depth)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    avg1 = sum(times) / 3
    print(f"  recursive_coords  {avg1*1000:8.2f} ms  -> {len(tris)} triangles")

    # Variant 2: chaos game
    times = []
    for _ in range(3):
        start = time.perf_counter()
        pts = sierpinski_chaos_game(n_points)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    avg2 = sum(times) / 3
    print(f"  chaos_game        {avg2*1000:8.2f} ms  -> {len(pts)} points")

    # Variant 3: bitwise grid
    times = []
    for _ in range(3):
        start = time.perf_counter()
        grid = sierpinski_bitwise(grid_size)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    avg3 = sum(times) / 3
    filled = int(grid.sum())
    print(f"  bitwise_grid      {avg3*1000:8.2f} ms  -> {filled}/{grid_size*grid_size} filled")

    fastest = min(avg1, avg2, avg3)
    print(f"\n  Fastest: {fastest*1000:.2f} ms")


if __name__ == "__main__":
    benchmark()
