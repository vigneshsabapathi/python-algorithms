"""
Index Calculation - Optimized Variants

Three approaches for NDVI computation:
1. Standard division - basic (NIR-R)/(NIR+R)
2. Pre-allocated output - avoid temporary arrays
3. Batch multi-index - compute NDVI+SAVI+BNDVI in single pass
"""

import time
import numpy as np


def ndvi_standard(nir: np.ndarray, red: np.ndarray) -> np.ndarray:
    """
    Standard NDVI with division-by-zero guard.

    >>> nir = np.array([[0.8, 0.6]], dtype=np.float64)
    >>> red = np.array([[0.2, 0.4]], dtype=np.float64)
    >>> np.round(ndvi_standard(nir, red), 4)
    array([[0.6, 0.2]])
    """
    denom = nir + red
    return np.where(denom == 0, 0.0, (nir - red) / denom)


def ndvi_preallocated(nir: np.ndarray, red: np.ndarray) -> np.ndarray:
    """
    Pre-allocated output arrays to reduce memory allocation overhead.

    >>> nir = np.array([[0.8, 0.6]], dtype=np.float64)
    >>> red = np.array([[0.2, 0.4]], dtype=np.float64)
    >>> np.round(ndvi_preallocated(nir, red), 4)
    array([[0.6, 0.2]])
    """
    out = np.empty_like(nir, dtype=np.float64)
    denom = np.add(nir, red)
    np.subtract(nir, red, out=out)
    mask = denom != 0
    out[mask] /= denom[mask]
    out[~mask] = 0.0
    return out


def batch_indices(
    nir: np.ndarray, red: np.ndarray, blue: np.ndarray, soil_l: float = 0.5
) -> dict:
    """
    Compute NDVI, SAVI, and BNDVI in a single pass over bands.
    Shares intermediate computations.

    >>> nir = np.array([[0.8]], dtype=np.float64)
    >>> red = np.array([[0.2]], dtype=np.float64)
    >>> blue = np.array([[0.1]], dtype=np.float64)
    >>> result = batch_indices(nir, red, blue)
    >>> round(result['ndvi'][0, 0], 4)
    0.6
    """
    nir_f = nir.astype(np.float64)
    red_f = red.astype(np.float64)
    blue_f = blue.astype(np.float64)

    diff_nr = nir_f - red_f
    sum_nr = nir_f + red_f

    # NDVI
    ndvi_out = np.where(sum_nr == 0, 0.0, diff_nr / sum_nr)

    # SAVI
    savi_denom = sum_nr + soil_l
    savi_out = np.where(savi_denom == 0, 0.0, (diff_nr / savi_denom) * (1 + soil_l))

    # BNDVI
    sum_nb = nir_f + blue_f
    bndvi_out = np.where(sum_nb == 0, 0.0, (nir_f - blue_f) / sum_nb)

    return {"ndvi": ndvi_out, "savi": savi_out, "bndvi": bndvi_out}


def benchmark(size: int = 1024, iterations: int = 100) -> None:
    """Benchmark NDVI variants."""
    nir = np.random.uniform(0.3, 0.9, (size, size))
    red = np.random.uniform(0.1, 0.5, (size, size))

    variants = [
        ("Standard", lambda: ndvi_standard(nir, red)),
        ("Pre-allocated", lambda: ndvi_preallocated(nir, red)),
    ]

    print(f"Benchmark NDVI: {size}x{size}, {iterations} iterations\n")
    print(f"{'Variant':<20} {'Total (ms)':>12} {'Per-call (ms)':>14}")
    print("-" * 48)

    for name, func in variants:
        func()
        start = time.perf_counter()
        for _ in range(iterations):
            func()
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:<20} {elapsed:>12.2f} {elapsed / iterations:>14.4f}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
