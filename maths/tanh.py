"""
Hyperbolic Tangent (tanh)
=========================
tanh(x) = (e^x - e^-x) / (e^x + e^-x).
"""
import math
from typing import List


def tanh(x: float) -> float:
    """
    >>> round(tanh(0), 6)
    0.0
    >>> round(tanh(1), 6)
    0.761594
    >>> round(tanh(-1), 6)
    -0.761594
    >>> abs(tanh(50) - 1.0) < 1e-9
    True
    """
    if x > 350:
        return 1.0
    if x < -350:
        return -1.0
    e_pos = math.exp(x)
    e_neg = math.exp(-x)
    return (e_pos - e_neg) / (e_pos + e_neg)


def tanh_list(xs: List[float]) -> List[float]:
    """
    >>> [round(v, 4) for v in tanh_list([-1, 0, 1])]
    [-0.7616, 0.0, 0.7616]
    """
    return [tanh(x) for x in xs]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    for x in (-2, -1, 0, 1, 2, 5):
        print(f"tanh({x}) = {tanh(x):.6f}")
