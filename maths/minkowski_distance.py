"""
Minkowski distance (generalization of Euclidean/Manhattan/Chebyshev):
    d(p, q; r) = ( Σ |p_i - q_i|^r )^(1/r)

r=1: Manhattan, r=2: Euclidean, r→∞: Chebyshev.

>>> round(minkowski_distance([1, 1], [4, 5], 2), 4)
5.0
>>> round(minkowski_distance([1, 1], [4, 5], 1), 4)
7.0
>>> round(minkowski_distance([0, 0], [3, 4], 3), 4)
4.4979
"""


def minkowski_distance(p: list[float], q: list[float], r: float) -> float:
    """Minkowski distance of order r.

    >>> round(minkowski_distance([1, 2, 3], [4, 5, 6], 2), 4)
    5.1962
    """
    if len(p) != len(q):
        raise ValueError("points must have same dimension")
    if r <= 0:
        raise ValueError("order r must be positive")
    total = sum(abs(a - b) ** r for a, b in zip(p, q))
    return total ** (1 / r)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(round(minkowski_distance([1, 1], [4, 5], 2), 4))
