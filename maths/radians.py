"""
Radians
=======
Convert degrees to radians.
"""
import math


def radians(degrees: float) -> float:
    """
    >>> round(radians(180), 6)
    3.141593
    >>> radians(0)
    0.0
    >>> round(radians(90), 6)
    1.570796
    >>> round(radians(-45), 6)
    -0.785398
    """
    return degrees * math.pi / 180


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    for d in (0, 30, 45, 90, 180, 360, -45):
        print(f"{d}° = {radians(d):.6f} rad")
