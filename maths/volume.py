"""
Volume Formulas
===============
Closed-form volumes of common 3D solids.
"""
import math


def cube(side: float) -> float:
    """
    >>> cube(2)
    8
    """
    return side**3


def cuboid(l: float, w: float, h: float) -> float:
    """
    >>> cuboid(1, 2, 3)
    6
    """
    return l * w * h


def sphere(r: float) -> float:
    """
    >>> round(sphere(1), 6)
    4.18879
    """
    return 4 / 3 * math.pi * r**3


def hemisphere(r: float) -> float:
    """
    >>> round(hemisphere(1), 6)
    2.094395
    """
    return 2 / 3 * math.pi * r**3


def cylinder(r: float, h: float) -> float:
    """
    >>> round(cylinder(1, 2), 6)
    6.283185
    """
    return math.pi * r * r * h


def cone(r: float, h: float) -> float:
    """
    >>> round(cone(3, 4), 6)
    37.699112
    """
    return 1 / 3 * math.pi * r * r * h


def pyramid(base_area: float, h: float) -> float:
    """
    >>> pyramid(9, 3)
    9.0
    """
    return base_area * h / 3


def torus(R: float, r: float) -> float:
    """
    Volume of a torus with major radius R, minor radius r.

    >>> round(torus(3, 1), 4)
    59.2176
    """
    return 2 * math.pi**2 * R * r * r


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("cube(3) =", cube(3))
    print("sphere(2) =", sphere(2))
    print("cylinder(2, 5) =", cylinder(2, 5))
    print("cone(3, 4) =", cone(3, 4))
    print("torus(3, 1) =", torus(3, 1))
