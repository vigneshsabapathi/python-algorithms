"""Joint probability distribution — variants + benchmark."""

import time
import random
from collections import Counter, defaultdict


def joint_counter(xs, ys):
    n = len(xs)
    c = Counter(zip(xs, ys))
    return {k: v / n for k, v in c.items()}


def joint_defaultdict(xs, ys):
    n = len(xs)
    d = defaultdict(int)
    for pair in zip(xs, ys):
        d[pair] += 1
    return {k: v / n for k, v in d.items()}


def joint_numpy(xs, ys):
    try:
        import numpy as np  # type: ignore
    except ImportError:
        return joint_counter(xs, ys)
    xs_arr = np.asarray(xs)
    ys_arr = np.asarray(ys)
    pairs, counts = np.unique(np.stack([xs_arr, ys_arr], axis=1), axis=0, return_counts=True)
    n = len(xs)
    return {tuple(p): c / n for p, c in zip(pairs, counts)}


def benchmark():
    N = 100_000
    xs = [random.randint(0, 9) for _ in range(N)]
    ys = [random.randint(0, 9) for _ in range(N)]
    for name, fn in [
        ("Counter", joint_counter),
        ("defaultdict", joint_defaultdict),
        ("numpy_unique", joint_numpy),
    ]:
        start = time.perf_counter()
        r = fn(xs, ys)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:15s} unique_pairs={len(r)}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
