"""
Maclaurin series approximations (Taylor series around x=0):
    sin(x) = Σ (-1)^n * x^(2n+1) / (2n+1)!
    cos(x) = Σ (-1)^n * x^(2n) / (2n)!
    exp(x) = Σ x^n / n!

>>> round(maclaurin_sin(0), 6)
0.0
>>> round(maclaurin_sin(3.14159/2, 15), 6)
1.0
>>> round(maclaurin_cos(0, 15), 6)
1.0
>>> round(maclaurin_exp(1, 20), 5)
2.71828
"""

import math


def maclaurin_sin(x: float, terms: int = 10) -> float:
    """Approximate sin(x) via Maclaurin series.

    >>> round(maclaurin_sin(3.14159/6, 10), 3)
    0.5
    """
    result = 0.0
    for n in range(terms):
        result += ((-1) ** n) * (x ** (2 * n + 1)) / math.factorial(2 * n + 1)
    return result


def maclaurin_cos(x: float, terms: int = 10) -> float:
    result = 0.0
    for n in range(terms):
        result += ((-1) ** n) * (x ** (2 * n)) / math.factorial(2 * n)
    return result


def maclaurin_exp(x: float, terms: int = 20) -> float:
    result = 0.0
    for n in range(terms):
        result += (x**n) / math.factorial(n)
    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(round(maclaurin_exp(1, 20), 5))
