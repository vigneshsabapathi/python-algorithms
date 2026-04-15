"""
Pythagoras
==========
Missing-side solver for a right triangle.
"""
import math


def hypotenuse(a: float, b: float) -> float:
    """
    >>> hypotenuse(3, 4)
    5.0
    >>> hypotenuse(5, 12)
    13.0
    """
    return math.sqrt(a * a + b * b)


def leg(c: float, a: float) -> float:
    """
    Given hypotenuse c and one leg a, return the other leg.

    >>> leg(5, 3)
    4.0
    >>> leg(13, 5)
    12.0
    """
    if c <= a:
        raise ValueError("hypotenuse must exceed the given leg")
    return math.sqrt(c * c - a * a)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("hypotenuse(3, 4) =", hypotenuse(3, 4))
    print("hypotenuse(5, 12) =", hypotenuse(5, 12))
    print("leg(13, 5) =", leg(13, 5))
