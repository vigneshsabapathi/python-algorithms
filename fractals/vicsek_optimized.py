"""
Vicsek Fractal — Optimized Variants with Benchmark

Variant 1 (recursive_cells): Original recursive cell enumeration
Variant 2 (grid_bitwise): Direct grid construction with modular arithmetic
Variant 3 (numpy_kronecker): Kronecker product approach for self-similar tiling
"""

import time

import numpy as np


# --- Variant 1: Recursive cell enumeration ---
def vicsek_recursive(
    x: float, y: float, length: float, depth: int
) -> list[tuple[float, float, float]]:
    """
    Recursively enumerate all filled cells as (cx, cy, size).

    >>> len(vicsek_recursive(0, 0, 9, 0))
    1
    >>> len(vicsek_recursive(0, 0, 9, 2))
    25
    """
    if depth == 0:
        return [(x, y, length)]
    sub = length / 3
    return (
        vicsek_recursive(x, y, sub, depth - 1)
        + vicsek_recursive(x + length / 3, y, sub, depth - 1)
        + vicsek_recursive(x - length / 3, y, sub, depth - 1)
        + vicsek_recursive(x, y + length / 3, sub, depth - 1)
        + vicsek_recursive(x, y - length / 3, sub, depth - 1)
    )


# --- Variant 2: Grid with modular arithmetic ---
def vicsek_grid_modular(depth: int) -> np.ndarray:
    """
    Build the Vicsek fractal grid using the rule: cell (r, c) is filled
    iff at every scale (base-3 digit), the digit pair is one of the
    5 allowed positions (center, NESW).

    >>> vicsek_grid_modular(1).shape
    (3, 3)
    >>> int(vicsek_grid_modular(1).sum())
    5
    >>> int(vicsek_grid_modular(2).sum())
    25
    """
    size = 3 ** depth
    grid = np.ones((size, size), dtype=np.int8)

    for d in range(depth):
        scale = 3 ** d
        r_digits = (np.arange(size) // scale) % 3
        c_digits = (np.arange(size) // scale) % 3
        R = r_digits.reshape((size, 1))
        C = c_digits.reshape((1, size))
        # A cell is NOT in the Vicsek pattern if at any scale
        # both r_digit and c_digit are non-center (i.e. both != 1)
        # and they form a corner (both odd or both even but not center)
        # Rule: allowed positions are (1,1), (0,1), (2,1), (1,0), (1,2)
        # i.e., at least one of r_digit, c_digit must be 1
        disallowed = (R != 1) & (C != 1)
        grid[disallowed] = 0

    return grid


# --- Variant 3: Kronecker product ---
def vicsek_kronecker(depth: int) -> np.ndarray:
    """
    Build the Vicsek fractal via repeated Kronecker product of the
    base 3x3 cross pattern.

    >>> vicsek_kronecker(0).shape
    (1, 1)
    >>> int(vicsek_kronecker(1).sum())
    5
    >>> int(vicsek_kronecker(2).sum())
    25
    >>> int(vicsek_kronecker(3).sum())
    125
    """
    # Base cross pattern
    cross = np.array([
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0],
    ], dtype=np.int8)

    result = np.array([[1]], dtype=np.int8)
    for _ in range(depth):
        result = np.kron(result, cross)

    return result


def benchmark(max_depth: int = 5) -> None:
    """Run all three variants and compare timing."""
    print(f"Benchmark: Vicsek fractal up to depth {max_depth}\n")

    for depth in range(max_depth + 1):
        size = 3 ** depth
        expected = 5 ** depth

        times = {}

        start = time.perf_counter()
        cells = vicsek_recursive(0, 0, size, depth)
        times["recursive"] = time.perf_counter() - start

        start = time.perf_counter()
        g1 = vicsek_grid_modular(depth)
        times["modular"] = time.perf_counter() - start

        start = time.perf_counter()
        g2 = vicsek_kronecker(depth)
        times["kronecker"] = time.perf_counter() - start

        fastest = min(times.values())
        print(f"  Depth {depth} ({size:>4}x{size:<4} = {expected:>5} cells):", end="")
        for name, t in times.items():
            print(f"  {name}={t*1000:.2f}ms", end="")
        print()


if __name__ == "__main__":
    benchmark()
