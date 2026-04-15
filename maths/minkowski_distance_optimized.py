"""Minkowski distance — variants + benchmark."""

import math
import time
import random


def mink_generic(p, q, r):
    return sum(abs(a - b) ** r for a, b in zip(p, q)) ** (1 / r)


def mink_specialized(p, q, r):
    if r == 1:
        return sum(abs(a - b) for a, b in zip(p, q))
    if r == 2:
        return math.sqrt(sum((a - b) * (a - b) for a, b in zip(p, q)))
    if math.isinf(r):
        return max(abs(a - b) for a, b in zip(p, q))
    return sum(abs(a - b) ** r for a, b in zip(p, q)) ** (1 / r)


def mink_numpy(p, q, r):
    try:
        import numpy as np  # type: ignore
    except ImportError:
        return mink_generic(p, q, r)
    arr = np.abs(np.asarray(p) - np.asarray(q))
    return float(np.power(np.sum(arr**r), 1 / r))


def benchmark():
    d = 1000
    p = [random.random() for _ in range(d)]
    q = [random.random() for _ in range(d)]
    for name, fn in [
        ("generic_pow", mink_generic),
        ("specialized_r12inf", mink_specialized),
        ("numpy", mink_numpy),
    ]:
        start = time.perf_counter()
        for _ in range(100):
            fn(p, q, 2)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:22s} r=2  time={elapsed:.3f} ms")
    # r=3 test
    start = time.perf_counter()
    for _ in range(100):
        mink_generic(p, q, 3)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"{'generic_r=3':22s} time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
