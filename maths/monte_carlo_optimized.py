"""Monte Carlo π — variants + benchmark."""

import math
import random
import time


def pi_loop(n):
    hits = 0
    for _ in range(n):
        x, y = random.random(), random.random()
        if x * x + y * y <= 1:
            hits += 1
    return 4 * hits / n


def pi_sum(n):
    r = random.random
    return 4 * sum(1 for _ in range(n) if r() ** 2 + r() ** 2 <= 1) / n


def pi_numpy(n):
    try:
        import numpy as np  # type: ignore
    except ImportError:
        return pi_loop(n)
    xy = np.random.random((n, 2))
    return 4.0 * float(np.sum(xy[:, 0] ** 2 + xy[:, 1] ** 2 <= 1)) / n


def benchmark():
    n = 500_000
    for name, fn in [
        ("python_loop", pi_loop),
        ("genexpr_sum", pi_sum),
        ("numpy_vectorized", pi_numpy),
    ]:
        start = time.perf_counter()
        p = fn(n)
        elapsed = (time.perf_counter() - start) * 1000
        err = abs(p - math.pi)
        print(f"{name:20s} pi~{p:.5f}  err={err:.5f}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
