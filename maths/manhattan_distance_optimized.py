"""Manhattan distance — variants + benchmark."""

import time
import random


def manhattan_gen(p, q):
    return sum(abs(a - b) for a, b in zip(p, q))


def manhattan_loop(p, q):
    total = 0
    for i in range(len(p)):
        total += abs(p[i] - q[i])
    return total


def manhattan_numpy(p, q):
    try:
        import numpy as np  # type: ignore
    except ImportError:
        return manhattan_gen(p, q)
    return float(np.sum(np.abs(np.asarray(p) - np.asarray(q))))


def benchmark():
    dim = 1000
    p = [random.random() for _ in range(dim)]
    q = [random.random() for _ in range(dim)]
    for name, fn in [
        ("generator_sum", manhattan_gen),
        ("indexed_loop", manhattan_loop),
        ("numpy_vector", manhattan_numpy),
    ]:
        start = time.perf_counter()
        for _ in range(1000):
            fn(p, q)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:18s} time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
