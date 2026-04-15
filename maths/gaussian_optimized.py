"""Gaussian PDF — variants + benchmark."""

import math
import time


def pdf_direct(x, mu=0.0, sigma=1.0):
    c = 1 / (sigma * math.sqrt(2 * math.pi))
    return c * math.exp(-0.5 * ((x - mu) / sigma) ** 2)


_INV_SQRT_2PI = 1 / math.sqrt(2 * math.pi)


def pdf_precomputed(x, mu=0.0, sigma=1.0):
    z = (x - mu) / sigma
    return (_INV_SQRT_2PI / sigma) * math.exp(-0.5 * z * z)


def pdf_standard_only(x):
    """Standard normal — no mu/sigma overhead."""
    return _INV_SQRT_2PI * math.exp(-0.5 * x * x)


def benchmark():
    xs = [i * 0.01 for i in range(-500, 500)]
    for name, fn in [
        ("direct", lambda: [pdf_direct(v) for v in xs]),
        ("precomputed_const", lambda: [pdf_precomputed(v) for v in xs]),
        ("standard_normal", lambda: [pdf_standard_only(v) for v in xs]),
    ]:
        start = time.perf_counter()
        fn()
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:20s} time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
