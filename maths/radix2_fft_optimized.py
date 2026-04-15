"""
FFT variants + benchmark.

1. naive_dft   - O(n^2) definitional DFT (baseline)
2. iter_fft    - O(n log n) iterative Cooley-Tukey
3. recursive   - O(n log n) recursive Cooley-Tukey
4. numpy_fft   - numpy.fft.fft
"""
from __future__ import annotations

import cmath
import math
import time
from typing import List


def naive_dft(x: List[complex]) -> List[complex]:
    n = len(x)
    out = []
    for k in range(n):
        s = 0j
        for t in range(n):
            s += x[t] * cmath.exp(-2j * cmath.pi * k * t / n)
        out.append(s)
    return out


def iter_fft(x: List[complex]) -> List[complex]:
    n = len(x)
    if n & (n - 1):
        raise ValueError("length must be power of 2")
    a = [complex(v) for v in x]
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j |= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    size = 2
    while size <= n:
        half = size // 2
        w0 = cmath.exp(-2j * cmath.pi / size)
        for start in range(0, n, size):
            w = 1 + 0j
            for k in range(half):
                t = w * a[start + k + half]
                a[start + k + half] = a[start + k] - t
                a[start + k] = a[start + k] + t
                w *= w0
        size <<= 1
    return a


def recursive_fft(x: List[complex]) -> List[complex]:
    n = len(x)
    if n == 1:
        return [complex(x[0])]
    if n & (n - 1):
        raise ValueError("length must be power of 2")
    even = recursive_fft(x[0::2])
    odd = recursive_fft(x[1::2])
    out = [0j] * n
    for k in range(n // 2):
        w = cmath.exp(-2j * cmath.pi * k / n) * odd[k]
        out[k] = even[k] + w
        out[k + n // 2] = even[k] - w
    return out


def numpy_fft(x: List[complex]):
    try:
        import numpy as np
    except ImportError:
        return iter_fft(x)
    return np.fft.fft(np.array(x, dtype=complex)).tolist()


def benchmark() -> None:
    import random

    rng = random.Random(0)
    print(f"{'fn':<16}{'n':>8}{'ms':>12}")
    for n in (64, 512, 4096):
        x = [rng.random() for _ in range(n)]
        for fn in (naive_dft, iter_fft, recursive_fft, numpy_fft):
            if fn is naive_dft and n > 512:
                continue
            t = time.perf_counter()
            fn(x)
            dt = (time.perf_counter() - t) * 1000
            print(f"{fn.__name__:<16}{n:>8}{dt:>12.3f}")


if __name__ == "__main__":
    benchmark()
