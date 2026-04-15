"""
Spearman rank correlation variants + benchmark.

1. classic_formula   - ρ = 1 - 6·Σd² / (n(n²-1))     (no-ties formula)
2. pearson_on_ranks  - Pearson correlation applied to ranks (tie-safe)
3. scipy_spearman    - scipy.stats.spearmanr (reference)
"""
from __future__ import annotations

import time
from typing import List


def _rank(values: List[float]) -> List[float]:
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def classic_formula(x, y):
    n = len(x)
    rx, ry = _rank(x), _rank(y)
    d2 = sum((a - b) ** 2 for a, b in zip(rx, ry))
    return 1 - 6 * d2 / (n * (n * n - 1))


def pearson_on_ranks(x, y):
    n = len(x)
    rx, ry = _rank(x), _rank(y)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = sum((a - mx) ** 2 for a in rx) ** 0.5
    dy = sum((b - my) ** 2 for b in ry) ** 0.5
    return num / (dx * dy) if dx and dy else 0.0


def scipy_spearman(x, y):
    try:
        from scipy.stats import spearmanr
    except ImportError:
        return pearson_on_ranks(x, y)
    return float(spearmanr(x, y).statistic)


def benchmark() -> None:
    import random

    rng = random.Random(0)
    x = [rng.random() for _ in range(1000)]
    y = [v + rng.gauss(0, 0.1) for v in x]
    print(f"{'fn':<18}{'result':>12}{'ms':>12}")
    for fn in (classic_formula, pearson_on_ranks, scipy_spearman):
        t = time.perf_counter()
        for _ in range(100):
            r = fn(x, y)
        dt = (time.perf_counter() - t) * 1000
        print(f"{fn.__name__:<18}{r:>12.6f}{dt:>12.2f}")


if __name__ == "__main__":
    benchmark()
