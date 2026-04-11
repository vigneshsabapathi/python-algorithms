"""
Mandelbrot Set — Optimized Variants with Benchmark

Variant 1 (scalar_loop): Original per-pixel scalar iteration
Variant 2 (numpy_vectorized): Full grid vectorized with numpy
Variant 3 (cardioid_skip): Scalar with cardioid/bulb pre-check optimization
"""

import time

import numpy as np


# --- Variant 1: Scalar loop (original) ---
def mandelbrot_scalar(
    width: int = 100,
    height: int = 75,
    x_min: float = -2.0,
    x_max: float = 0.5,
    y_min: float = -1.25,
    y_max: float = 1.25,
    max_iter: int = 50,
) -> np.ndarray:
    """
    Per-pixel scalar iteration, straightforward escape-time.

    >>> mandelbrot_scalar(10, 10, max_iter=20).shape
    (10, 10)
    >>> int(mandelbrot_scalar(5, 5, max_iter=20)[2, 2])  # center-ish
    20
    """
    grid = np.zeros((height, width), dtype=np.int32)
    for row in range(height):
        y = y_max - row * (y_max - y_min) / (height - 1)
        for col in range(width):
            x = x_min + col * (x_max - x_min) / (width - 1)
            a, b = 0.0, 0.0
            for n in range(1, max_iter + 1):
                a, b = a * a - b * b + x, 2 * a * b + y
                if a * a + b * b > 4:
                    grid[row, col] = n
                    break
            else:
                grid[row, col] = max_iter
    return grid


# --- Variant 2: Numpy vectorized ---
def mandelbrot_numpy(
    width: int = 100,
    height: int = 75,
    x_min: float = -2.0,
    x_max: float = 0.5,
    y_min: float = -1.25,
    y_max: float = 1.25,
    max_iter: int = 50,
) -> np.ndarray:
    """
    Fully vectorized numpy approach with progressive escape tracking.

    >>> mandelbrot_numpy(10, 10, max_iter=20).shape
    (10, 10)
    """
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_max, y_min, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    Z = np.zeros_like(C)

    escape = np.full((height, width), max_iter, dtype=np.int32)
    active = np.ones((height, width), dtype=bool)

    for step in range(1, max_iter + 1):
        Z[active] = Z[active] ** 2 + C[active]
        newly_escaped = active & (np.abs(Z) > 2)
        escape[newly_escaped] = step
        active[newly_escaped] = False
        if not active.any():
            break

    return escape


# --- Variant 3: Scalar with cardioid/period-2 bulb skip ---
def mandelbrot_cardioid_skip(
    width: int = 100,
    height: int = 75,
    x_min: float = -2.0,
    x_max: float = 0.5,
    y_min: float = -1.25,
    y_max: float = 1.25,
    max_iter: int = 50,
) -> np.ndarray:
    """
    Per-pixel iteration that skips points known to be inside the main
    cardioid or period-2 bulb, saving ~30% of iterations.

    >>> mandelbrot_cardioid_skip(10, 10, max_iter=20).shape
    (10, 10)
    """
    grid = np.zeros((height, width), dtype=np.int32)
    for row in range(height):
        y = y_max - row * (y_max - y_min) / (height - 1)
        for col in range(width):
            x = x_min + col * (x_max - x_min) / (width - 1)

            # Cardioid check: |c - 1/4| < 1/2(1 - cos(theta))
            # Simplified: q = (x-1/4)^2 + y^2; q(q + x - 1/4) <= y^2/4
            q = (x - 0.25) ** 2 + y * y
            if q * (q + x - 0.25) <= 0.25 * y * y:
                grid[row, col] = max_iter
                continue

            # Period-2 bulb check: (x+1)^2 + y^2 <= 1/16
            if (x + 1) ** 2 + y * y <= 0.0625:
                grid[row, col] = max_iter
                continue

            a, b = 0.0, 0.0
            for n in range(1, max_iter + 1):
                a, b = a * a - b * b + x, 2 * a * b + y
                if a * a + b * b > 4:
                    grid[row, col] = n
                    break
            else:
                grid[row, col] = max_iter
    return grid


def benchmark(width: int = 80, height: int = 60, max_iter: int = 50) -> None:
    """Run all three variants and compare timing."""
    print(f"Benchmark: {width}x{height}, max_iter={max_iter}\n")

    variants = [
        ("scalar_loop", mandelbrot_scalar),
        ("numpy_vectorized", mandelbrot_numpy),
        ("cardioid_skip", mandelbrot_cardioid_skip),
    ]

    results = []
    for name, func in variants:
        times = []
        for _ in range(3):
            start = time.perf_counter()
            grid = func(width, height, max_iter=max_iter)
            elapsed = time.perf_counter() - start
            times.append(elapsed)
        avg = sum(times) / len(times)
        bounded = int(np.sum(grid == max_iter))
        results.append((name, avg, bounded))

    fastest = min(r[1] for r in results)
    for name, avg, bounded in results:
        ratio = avg / fastest
        print(f"  {name:25s}  {avg*1000:8.2f} ms  ({ratio:5.1f}x)  bounded={bounded}")


if __name__ == "__main__":
    benchmark()
