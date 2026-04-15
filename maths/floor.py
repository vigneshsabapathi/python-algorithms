"""
Floor function: largest integer <= x.

>>> floor(1.7)
1
>>> floor(-1.2)
-2
>>> floor(5)
5
>>> floor(-5)
-5
"""


def floor(x: float) -> int:
    """Return floor(x) without using math.floor.

    >>> floor(3.999)
    3
    >>> floor(-0.5)
    -1
    """
    i = int(x)
    return i if x >= 0 or x == i else i - 1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(floor(1.7), floor(-1.2))
