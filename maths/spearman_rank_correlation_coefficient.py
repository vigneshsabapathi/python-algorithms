"""
Spearman Rank Correlation Coefficient
=====================================
Non-parametric measure of monotonic relationship between two variables.

    ρ = 1 - (6 · Σ d_i^2) / (n (n^2 - 1))

where d_i is the difference between the ranks of x_i and y_i (no ties).
"""
from typing import List


def _rank(values: List[float]) -> List[float]:
    """Average-rank handling of ties."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1  # 1-based average rank
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def spearman(x: List[float], y: List[float]) -> float:
    """
    >>> round(spearman([1, 2, 3, 4, 5], [5, 6, 7, 8, 7]), 6)
    0.820783
    >>> round(spearman([1, 2, 3, 4], [1, 2, 3, 4]), 6)
    1.0
    >>> round(spearman([1, 2, 3, 4], [4, 3, 2, 1]), 6)
    -1.0
    """
    if len(x) != len(y):
        raise ValueError("x and y must have the same length")
    n = len(x)
    if n == 0:
        return 0.0
    rx = _rank(x)
    ry = _rank(y)
    # Use Pearson on ranks (handles ties correctly)
    mx = sum(rx) / n
    my = sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = sum((a - mx) ** 2 for a in rx) ** 0.5
    dy = sum((b - my) ** 2 for b in ry) ** 0.5
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    x = [106, 86, 100, 101, 99, 103, 97, 113, 112, 110]
    y = [7, 0, 27, 50, 28, 29, 20, 12, 6, 17]
    print(f"spearman = {spearman(x, y):.6f}")
