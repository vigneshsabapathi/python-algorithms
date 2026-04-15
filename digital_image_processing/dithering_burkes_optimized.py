"""
Burkes Dithering - Optimized Variants

Three approaches:
1. Standard loop (baseline) - pixel-by-pixel with error diffusion
2. Row-buffer approach - only keep current + next row error buffer
3. Vectorized threshold with error accumulation - process row chunks
"""

import time
import numpy as np


def burkes_standard(image: np.ndarray, threshold: int = 128) -> np.ndarray:
    """
    Standard pixel-by-pixel Burkes dithering.

    >>> img = np.array([[100, 200], [150, 50]], dtype=np.uint8)
    >>> result = burkes_standard(img)
    >>> set(np.unique(result)).issubset({0, 255})
    True
    """
    img = image.astype(np.float64)
    h, w = img.shape

    for y in range(h):
        for x in range(w):
            old = img[y, x]
            new = 255.0 if old >= threshold else 0.0
            img[y, x] = new
            err = old - new

            if x + 1 < w:
                img[y, x + 1] += err * 8 / 32
            if x + 2 < w:
                img[y, x + 2] += err * 4 / 32

            if y + 1 < h:
                for dx, wt in [(-2, 2), (-1, 4), (0, 8), (1, 4), (2, 2)]:
                    nx = x + dx
                    if 0 <= nx < w:
                        img[y + 1, nx] += err * wt / 32

    return np.clip(img, 0, 255).astype(np.uint8)


def burkes_row_buffer(image: np.ndarray, threshold: int = 128) -> np.ndarray:
    """
    Row-buffer approach: maintain error buffer for next row only.
    Reduces memory footprint for large images.

    >>> img = np.array([[100, 200], [150, 50]], dtype=np.uint8)
    >>> result = burkes_row_buffer(img)
    >>> set(np.unique(result)).issubset({0, 255})
    True
    """
    h, w = image.shape
    output = np.zeros_like(image)
    current_errors = np.zeros(w + 4, dtype=np.float64)  # padding
    next_errors = np.zeros(w + 4, dtype=np.float64)

    for y in range(h):
        # Load current row + accumulated errors
        row = image[y].astype(np.float64) + current_errors[2:w + 2]
        next_errors[:] = 0

        for x in range(w):
            old = row[x]
            new = 255.0 if old >= threshold else 0.0
            output[y, x] = int(new)
            err = old - new

            # Diffuse to current row
            if x + 1 < w:
                row[x + 1] += err * 8 / 32
            if x + 2 < w:
                row[x + 2] += err * 4 / 32

            # Diffuse to next row buffer (with +2 offset for padding)
            bx = x + 2
            next_errors[bx - 2] += err * 2 / 32
            next_errors[bx - 1] += err * 4 / 32
            next_errors[bx] += err * 8 / 32
            if bx + 1 < w + 4:
                next_errors[bx + 1] += err * 4 / 32
            if bx + 2 < w + 4:
                next_errors[bx + 2] += err * 2 / 32

        current_errors, next_errors = next_errors, current_errors

    return output.astype(np.uint8)


def burkes_serpentine(image: np.ndarray, threshold: int = 128) -> np.ndarray:
    """
    Serpentine (bidirectional) scanning to reduce directional artifacts.
    Even rows left-to-right, odd rows right-to-left.

    >>> img = np.array([[100, 200], [150, 50]], dtype=np.uint8)
    >>> result = burkes_serpentine(img)
    >>> set(np.unique(result)).issubset({0, 255})
    True
    """
    img = image.astype(np.float64)
    h, w = img.shape

    for y in range(h):
        if y % 2 == 0:
            x_range = range(w)
        else:
            x_range = range(w - 1, -1, -1)

        for x in x_range:
            old = img[y, x]
            new = 255.0 if old >= threshold else 0.0
            img[y, x] = new
            err = old - new
            direction = 1 if y % 2 == 0 else -1

            if 0 <= x + direction < w:
                img[y, x + direction] += err * 8 / 32
            if 0 <= x + 2 * direction < w:
                img[y, x + 2 * direction] += err * 4 / 32

            if y + 1 < h:
                for dx, wt in [(-2, 2), (-1, 4), (0, 8), (1, 4), (2, 2)]:
                    nx = x + dx * direction
                    if 0 <= nx < w:
                        img[y + 1, nx] += err * wt / 32

    return np.clip(img, 0, 255).astype(np.uint8)


def benchmark(size: int = 128, iterations: int = 5) -> None:
    """Benchmark all variants."""
    image = np.random.randint(0, 256, (size, size), dtype=np.uint8)

    variants = [
        ("Standard", burkes_standard),
        ("Row-buffer", burkes_row_buffer),
        ("Serpentine", burkes_serpentine),
    ]

    print(f"Benchmark: {size}x{size} image, {iterations} iterations\n")
    print(f"{'Variant':<20} {'Total (ms)':>12} {'Per-call (ms)':>14}")
    print("-" * 48)

    for name, func in variants:
        func(image)
        start = time.perf_counter()
        for _ in range(iterations):
            func(image)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:<20} {elapsed:>12.2f} {elapsed / iterations:>14.4f}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
