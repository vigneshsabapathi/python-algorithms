"""
Rectangular to Polar Conversion

Convert between rectangular (Cartesian) and polar coordinate systems.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/rectangular_to_polar.py
"""

import math


def rectangular_to_polar(x: float, y: float) -> tuple[float, float]:
    """
    Convert rectangular (x, y) to polar (r, theta) coordinates.
    Theta is in radians.

    >>> rectangular_to_polar(1, 0)
    (1.0, 0.0)
    >>> rectangular_to_polar(0, 1)
    (1.0, 1.5708)
    >>> rectangular_to_polar(1, 1)
    (1.41421, 0.7854)
    >>> rectangular_to_polar(-1, 0)
    (1.0, 3.1416)
    >>> rectangular_to_polar(0, 0)
    (0.0, 0.0)
    >>> rectangular_to_polar(3, 4)
    (5.0, 0.9273)
    """
    r = math.sqrt(x ** 2 + y ** 2)
    theta = math.atan2(y, x)
    return round(r, 5), round(theta, 4)


def polar_to_rectangular(r: float, theta: float) -> tuple[float, float]:
    """
    Convert polar (r, theta) to rectangular (x, y) coordinates.
    Theta is in radians.

    >>> polar_to_rectangular(1, 0)
    (1.0, 0.0)
    >>> polar_to_rectangular(1, 1.5707963267948966)
    (0.0, 1.0)
    >>> polar_to_rectangular(5, 0.9272952180016122)
    (3.0, 4.0)
    >>> polar_to_rectangular(0, 0)
    (0.0, 0.0)
    """
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return round(x, 5), round(y, 5)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    points = [(1, 0), (0, 1), (1, 1), (3, 4), (-1, -1)]
    for x, y in points:
        r, theta = rectangular_to_polar(x, y)
        deg = math.degrees(theta)
        back_x, back_y = polar_to_rectangular(r, theta)
        print(f"  ({x}, {y}) -> (r={r}, theta={theta:.4f} rad / {deg:.1f} deg) -> ({back_x}, {back_y})")
