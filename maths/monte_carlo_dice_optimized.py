"""Monte Carlo dice — variants + benchmark."""

import random
import time
from collections import Counter


def dice_loop(n, d):
    c = Counter()
    for _ in range(n):
        c[sum(random.randint(1, 6) for _ in range(d))] += 1
    return {k: v / n for k, v in sorted(c.items())}


def dice_choices(n, d):
    c = Counter()
    pop = [1, 2, 3, 4, 5, 6]
    for _ in range(n):
        c[sum(random.choices(pop, k=d))] += 1
    return {k: v / n for k, v in sorted(c.items())}


def dice_numpy(n, d):
    try:
        import numpy as np  # type: ignore
    except ImportError:
        return dice_loop(n, d)
    rolls = np.random.randint(1, 7, size=(n, d))
    sums = rolls.sum(axis=1)
    vals, counts = np.unique(sums, return_counts=True)
    return {int(k): int(v) / n for k, v in zip(vals, counts)}


def benchmark():
    n, d = 200_000, 2
    for name, fn in [
        ("loop_randint", dice_loop),
        ("random.choices", dice_choices),
        ("numpy_vectorized", dice_numpy),
    ]:
        start = time.perf_counter()
        r = fn(n, d)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:22s} P(sum=7)={r.get(7, 0):.4f}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
