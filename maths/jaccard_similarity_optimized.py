"""Jaccard — variants + benchmark."""

import time
import random


def jac_sets(a, b):
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def jac_inclusion_exclusion(a, b):
    """|A∪B| = |A| + |B| - |A∩B|."""
    if not a and not b:
        return 1.0
    inter = len(a & b)
    return inter / (len(a) + len(b) - inter)


def jac_manual_iter(a, b):
    if not a and not b:
        return 1.0
    inter = 0
    smaller, larger = (a, b) if len(a) < len(b) else (b, a)
    for x in smaller:
        if x in larger:
            inter += 1
    union = len(a) + len(b) - inter
    return inter / union if union else 1.0


def benchmark():
    a = set(random.randint(0, 100_000) for _ in range(20_000))
    b = set(random.randint(0, 100_000) for _ in range(20_000))
    for name, fn in [
        ("set_ops", jac_sets),
        ("inclusion_exclusion", jac_inclusion_exclusion),
        ("manual_iter_smaller", jac_manual_iter),
    ]:
        start = time.perf_counter()
        r = fn(a, b)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{name:22s} jac={r:.6f}  time={elapsed:.3f} ms")


if __name__ == "__main__":
    benchmark()
