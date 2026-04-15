"""
Softmax variants + benchmark.

1. naive            - exp(x) / sum(exp(x))          (overflows for large x)
2. stable           - subtract max first
3. log_sum_exp      - softmax via log-sum-exp trick  (numerically equivalent to stable)
4. numpy_softmax    - vectorized numpy
"""
from __future__ import annotations

import math
import time


def naive(x):
    e = [math.exp(v) for v in x]
    s = sum(e)
    return [v / s for v in e]


def stable(x):
    m = max(x)
    e = [math.exp(v - m) for v in x]
    s = sum(e)
    return [v / s for v in e]


def log_sum_exp(x):
    m = max(x)
    lse = m + math.log(sum(math.exp(v - m) for v in x))
    return [math.exp(v - lse) for v in x]


def numpy_softmax(x):
    try:
        import numpy as np
    except ImportError:
        return stable(x)
    a = np.array(x, dtype=float)
    a = a - a.max()
    e = np.exp(a)
    return (e / e.sum()).tolist()


def benchmark() -> None:
    import random

    rng = random.Random(0)
    vecs = {
        "small": [rng.random() for _ in range(10)],
        "medium": [rng.random() * 5 for _ in range(1000)],
        "large-values": [700 + rng.random() for _ in range(10)],  # naive will overflow
    }
    print(f"{'fn':<14}{'case':<14}{'ms':>12}")
    for case, v in vecs.items():
        for fn in (naive, stable, log_sum_exp, numpy_softmax):
            try:
                t = time.perf_counter()
                for _ in range(1000):
                    fn(v)
                dt = (time.perf_counter() - t) * 1000
            except OverflowError:
                dt = float("nan")
            print(f"{fn.__name__:<14}{case:<14}{dt:>12.3f}")


if __name__ == "__main__":
    benchmark()
