"""
Sigmoid (Logistic Function)
===========================
σ(x) = 1 / (1 + e^-x).
"""
import math
from typing import List


def sigmoid(x: float) -> float:
    """
    >>> sigmoid(0)
    0.5
    >>> round(sigmoid(2), 6)
    0.880797
    >>> round(sigmoid(-2), 6)
    0.119203
    """
    return 1.0 / (1.0 + math.exp(-x))


def sigmoid_list(xs: List[float]) -> List[float]:
    """
    >>> [round(v, 4) for v in sigmoid_list([-1, 0, 1])]
    [0.2689, 0.5, 0.7311]
    """
    return [sigmoid(x) for x in xs]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    for x in (-4, -2, 0, 2, 4):
        print(f"sigmoid({x}) = {sigmoid(x):.6f}")
