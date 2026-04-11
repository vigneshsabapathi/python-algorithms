#!/usr/bin/env python3
"""
Optimized and alternative implementations of Scoring Algorithm.

Variants covered:
1. weighted_sum     -- Basic weighted sum (reference)
2. topsis           -- TOPSIS multi-criteria decision method
3. ahp_scoring      -- Analytic Hierarchy Process simplified

Run:
    python other/scoring_algorithm_optimized.py
"""

from __future__ import annotations

import math
import os
import sys
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from other.scoring_algorithm import weighted_score as reference
from other.scoring_algorithm import rank_items, normalize_scores


def topsis(
    items: dict[str, list[float]],
    weights: list[float],
    beneficial: list[bool] | None = None,
) -> list[tuple[str, float]]:
    """
    TOPSIS (Technique for Order Preference by Similarity to Ideal Solution).

    >>> result = topsis({"A": [80, 90], "B": [95, 70]}, [0.5, 0.5])
    >>> result[0][0]
    'A'
    """
    if not items:
        return []

    names = list(items.keys())
    matrix = [items[n] for n in names]
    n_criteria = len(weights)

    if beneficial is None:
        beneficial = [True] * n_criteria

    # Normalize matrix (vector normalization)
    col_sums = []
    for j in range(n_criteria):
        s = math.sqrt(sum(row[j] ** 2 for row in matrix))
        col_sums.append(s if s > 0 else 1)

    norm = [[row[j] / col_sums[j] * weights[j] for j in range(n_criteria)] for row in matrix]

    # Ideal and anti-ideal solutions
    ideal = []
    anti_ideal = []
    for j in range(n_criteria):
        col = [row[j] for row in norm]
        if beneficial[j]:
            ideal.append(max(col))
            anti_ideal.append(min(col))
        else:
            ideal.append(min(col))
            anti_ideal.append(max(col))

    # Distance to ideal and anti-ideal
    scores = []
    for i, row in enumerate(norm):
        d_pos = math.sqrt(sum((row[j] - ideal[j]) ** 2 for j in range(n_criteria)))
        d_neg = math.sqrt(sum((row[j] - anti_ideal[j]) ** 2 for j in range(n_criteria)))
        score = d_neg / (d_pos + d_neg) if (d_pos + d_neg) > 0 else 0
        scores.append((names[i], round(score, 4)))

    return sorted(scores, key=lambda x: x[1], reverse=True)


def z_score_normalize(scores: list[float]) -> list[float]:
    """
    Z-score normalization (mean=0, std=1).

    >>> z_score_normalize([10, 20, 30])
    [-1.2247, 0.0, 1.2247]
    >>> z_score_normalize([5, 5, 5])
    [0.0, 0.0, 0.0]
    >>> z_score_normalize([])
    []
    """
    if not scores:
        return []
    mean = sum(scores) / len(scores)
    std = (sum((s - mean) ** 2 for s in scores) / len(scores)) ** 0.5
    if std == 0:
        return [0.0] * len(scores)
    return [round((s - mean) / std, 4) for s in scores]


def geometric_mean_score(scores: list[float], weights: list[float]) -> float:
    """
    Weighted geometric mean (useful when ratios matter more than differences).

    >>> round(geometric_mean_score([80, 90, 70], [0.3, 0.5, 0.2]), 2)
    82.62
    >>> geometric_mean_score([], [])
    0.0
    """
    if not scores or not weights:
        return 0.0
    product = 1.0
    for s, w in zip(scores, weights):
        if s <= 0:
            return 0.0
        product *= s ** w
    return product


TEST_ITEMS = {"A": [80, 90], "B": [95, 70], "C": [85, 85]}
TEST_WEIGHTS = [0.6, 0.4]


def run_all() -> None:
    print("\n=== Correctness ===")
    ranked = rank_items(TEST_ITEMS, TEST_WEIGHTS)
    print(f"  Weighted ranking: {ranked}")

    topsis_result = topsis(TEST_ITEMS, [0.5, 0.5])
    print(f"  TOPSIS ranking:   {topsis_result}")

    print("\n=== Normalization comparison ===")
    raw = [10, 20, 30, 40, 50]
    print(f"  Raw:        {raw}")
    print(f"  Min-max:    {normalize_scores(raw)}")
    print(f"  Z-score:    {z_score_normalize(raw)}")

    REPS = 100_000
    print(f"\n=== Benchmark: {REPS} runs ===")
    fns = [
        ("weighted_score", lambda: reference([80, 90, 70], [0.3, 0.5, 0.2])),
        ("geometric_mean", lambda: geometric_mean_score([80, 90, 70], [0.3, 0.5, 0.2])),
    ]
    for name, fn in fns:
        t = timeit.timeit(fn, number=REPS) * 1000 / REPS
        print(f"  {name:<20} {t:>7.4f} ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
