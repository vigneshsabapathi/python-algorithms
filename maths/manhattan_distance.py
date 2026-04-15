"""
Manhattan (L1) distance: sum of absolute coordinate differences.
    d(p, q) = Σ |p_i - q_i|

Also called taxicab or cityblock distance.

>>> manhattan_distance([0, 0], [3, 4])
7
>>> manhattan_distance([1, 2, 3], [4, 5, 6])
9
>>> manhattan_distance([1], [1])
0
"""


def manhattan_distance(p: list[float], q: list[float]) -> float:
    """L1 distance.

    >>> manhattan_distance([1.5, 2.5], [4.5, 0.5])
    5.0
    """
    if len(p) != len(q):
        raise ValueError("points must have same dimension")
    return sum(abs(a - b) for a, b in zip(p, q))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(manhattan_distance([0, 0], [3, 4]))
