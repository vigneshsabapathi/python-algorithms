"""
Julia Sets — Optimized Variants with Benchmark

Variant 1 (numpy_vectorized): Original numpy-based vectorized iteration
Variant 2 (numba_jit_scalar): Per-pixel scalar loop (simulates numba-style)
Variant 3 (escape_time_grid): Escape-time coloring with early termination per-pixel
"""

import time
import warnings

import numpy as np


# --- Variant 1: Numpy vectorized (original approach) ---
def julia_numpy_vectorized(
    c: complex,
    grid_size: int = 200,
    window: float = 2.0,
    max_iter: int = 50,
    escape_radius: float = 2.0,
) -> np.ndarray:
    """
    Vectorized numpy iteration — processes entire grid per step.
    Returns boolean mask: True = bounded (in Julia set).

    >>> result = julia_numpy_vectorized(0.25 + 0j, 10, 2.0, 20)
    >>> result.shape
    (10, 10)
    >>> result.dtype
    dtype('bool')
    """
    x = np.linspace(-window, window, grid_size).reshape((grid_size, 1))
    y = np.linspace(-window, window, grid_size).reshape((1, grid_size))
    z = (x + 1j * y).astype(np.complex64)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        for _ in range(max_iter):
            z = z * z + c
            np.nan_to_num(z, copy=False, nan=1e10)
            z = np.where(np.abs(z) > 1e10, 1e10, z)

    return np.abs(z) < escape_radius


# --- Variant 2: Scalar per-pixel with early exit ---
def julia_scalar_escape(
    c: complex,
    grid_size: int = 200,
    window: float = 2.0,
    max_iter: int = 50,
    escape_radius: float = 2.0,
) -> np.ndarray:
    """
    Per-pixel scalar iteration with early escape detection.
    Returns 2-D array of iteration counts (max_iter = bounded).

    >>> result = julia_scalar_escape(0.25 + 0j, 10, 2.0, 20)
    >>> result.shape
    (10, 10)
    >>> int(result[5, 5])  # center point z=0
    20
    """
    escape_r2 = escape_radius * escape_radius
    grid = np.zeros((grid_size, grid_size), dtype=np.int32)
    xs = np.linspace(-window, window, grid_size)
    ys = np.linspace(-window, window, grid_size)

    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            zr, zi = x, y
            for n in range(max_iter):
                zr2, zi2 = zr * zr, zi * zi
                if zr2 + zi2 > escape_r2:
                    grid[i, j] = n
                    break
                zi = 2 * zr * zi + c.imag
                zr = zr2 - zi2 + c.real
            else:
                grid[i, j] = max_iter
    return grid


# --- Variant 3: Chunked vectorized with progressive escape ---
def julia_chunked_escape(
    c: complex,
    grid_size: int = 200,
    window: float = 2.0,
    max_iter: int = 50,
    escape_radius: float = 2.0,
) -> np.ndarray:
    """
    Numpy vectorized with per-step escape tracking — avoids wasted
    computation on already-escaped points.
    Returns 2-D array of escape times.

    >>> result = julia_chunked_escape(0.25 + 0j, 10, 2.0, 20)
    >>> result.shape
    (10, 10)
    """
    x = np.linspace(-window, window, grid_size).reshape((grid_size, 1))
    y = np.linspace(-window, window, grid_size).reshape((1, grid_size))
    z = (x + 1j * y).astype(np.complex128)

    escape_time = np.full((grid_size, grid_size), max_iter, dtype=np.int32)
    active = np.ones((grid_size, grid_size), dtype=bool)

    for step in range(max_iter):
        z[active] = z[active] ** 2 + c
        newly_escaped = active & (np.abs(z) > escape_radius)
        escape_time[newly_escaped] = step
        active[newly_escaped] = False
        if not active.any():
            break

    return escape_time


def benchmark(grid_size: int = 100, max_iter: int = 30) -> None:
    """Run all three variants and compare timing."""
    c = -0.4 + 0.6j
    print(f"Benchmark: grid={grid_size}x{grid_size}, max_iter={max_iter}, c={c}\n")

    variants = [
        ("numpy_vectorized", julia_numpy_vectorized),
        ("scalar_escape", julia_scalar_escape),
        ("chunked_escape", julia_chunked_escape),
    ]

    results = []
    for name, func in variants:
        times = []
        for _ in range(3):
            start = time.perf_counter()
            result = func(c, grid_size, 2.0, max_iter)
            elapsed = time.perf_counter() - start
            times.append(elapsed)
        avg = sum(times) / len(times)
        results.append((name, avg, result))

    fastest = min(r[1] for r in results)
    for name, avg, result in results:
        ratio = avg / fastest
        if hasattr(result, 'dtype') and result.dtype == bool:
            bounded = int(np.sum(result))
        else:
            bounded = int(np.sum(result == max_iter))
        print(f"  {name:25s}  {avg*1000:8.2f} ms  ({ratio:5.1f}x)  bounded={bounded}")


if __name__ == "__main__":
    benchmark()
