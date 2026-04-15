"""
Sin via Taylor Series
=====================
Approximate sin(x) using its Maclaurin series:

    sin(x) = x - x^3/3! + x^5/5! - x^7/7! + ...
"""
import math


def sin_taylor(x: float, terms: int = 20) -> float:
    """
    >>> round(sin_taylor(0), 6)
    0.0
    >>> round(sin_taylor(math.pi / 2), 6)
    1.0
    >>> abs(sin_taylor(math.pi)) < 1e-9
    True
    >>> round(sin_taylor(1.0), 6) == round(math.sin(1.0), 6)
    True
    """
    # reduce x into [-pi, pi] for accuracy
    x = ((x + math.pi) % (2 * math.pi)) - math.pi
    s = 0.0
    term = x
    for k in range(terms):
        s += term
        term *= -(x * x) / ((2 * k + 2) * (2 * k + 3))
    return s


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    for deg in (0, 30, 45, 60, 90, 180):
        r = math.radians(deg)
        print(f"sin({deg}°) ≈ {sin_taylor(r):.6f}  (math.sin = {math.sin(r):.6f})")
