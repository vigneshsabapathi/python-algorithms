"""
Scoring Algorithm — Rank items based on weighted criteria.

Implements a weighted scoring model for decision making, commonly used
in multi-criteria analysis.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/scoring_algorithm.py
"""

from __future__ import annotations


def weighted_score(
    scores: list[float], weights: list[float]
) -> float:
    """
    Calculate weighted score given scores and corresponding weights.

    >>> weighted_score([80, 90, 70], [0.3, 0.5, 0.2])
    83.0
    >>> weighted_score([100], [1.0])
    100.0
    >>> weighted_score([], [])
    0.0
    >>> weighted_score([50, 50], [0.5, 0.5])
    50.0
    """
    if not scores or not weights:
        return 0.0

    return sum(s * w for s, w in zip(scores, weights))


def rank_items(
    items: dict[str, list[float]], weights: list[float]
) -> list[tuple[str, float]]:
    """
    Rank items by weighted score.

    items: {name: [score1, score2, ...]}
    weights: corresponding weights for each criterion

    Returns sorted list of (name, total_score), highest first.

    >>> items = {"A": [80, 90], "B": [95, 70], "C": [85, 85]}
    >>> result = rank_items(items, [0.6, 0.4])
    >>> result[-1][0]
    'A'
    >>> result[-1][1]
    84.0
    """
    scored = [
        (name, weighted_score(item_scores, weights))
        for name, item_scores in items.items()
    ]
    return sorted(scored, key=lambda x: x[1], reverse=True)


def normalize_scores(scores: list[float]) -> list[float]:
    """
    Normalize scores to 0-1 range using min-max normalization.

    >>> normalize_scores([10, 20, 30])
    [0.0, 0.5, 1.0]
    >>> normalize_scores([5, 5, 5])
    [0.0, 0.0, 0.0]
    >>> normalize_scores([])
    []
    """
    if not scores:
        return []

    min_s = min(scores)
    max_s = max(scores)
    span = max_s - min_s

    if span == 0:
        return [0.0] * len(scores)

    return [(s - min_s) / span for s in scores]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
