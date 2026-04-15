"""
Sumset
======
The sumset of A and B is { a + b : a ∈ A, b ∈ B }.
"""
from typing import Iterable, Set


def sumset(a: Iterable[float], b: Iterable[float]) -> Set[float]:
    """
    >>> sorted(sumset({1, 2, 3}, {4, 5, 6}))
    [5, 6, 7, 8, 9]
    >>> sorted(sumset({0}, {1, 2, 3}))
    [1, 2, 3]
    >>> sumset({}, {1, 2})
    set()
    """
    a = list(a)
    b = list(b)
    return {x + y for x in a for y in b}


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(sorted(sumset({1, 2, 3}, {4, 5, 6})))
    print(sorted(sumset({0, 1, 2}, {0, 1, 2})))
