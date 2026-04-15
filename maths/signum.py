"""
Signum Function
===============
sign(x) = -1 if x < 0, 0 if x == 0, +1 if x > 0.
"""


def signum(x: float) -> int:
    """
    >>> signum(5)
    1
    >>> signum(-3)
    -1
    >>> signum(0)
    0
    >>> signum(-0.0)
    0
    """
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    for x in (-3.5, -1, 0, 1, 42):
        print(f"signum({x}) = {signum(x)}")
