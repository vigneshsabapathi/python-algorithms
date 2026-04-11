"""
Diophantine Equation Solver

A linear Diophantine equation is of the form:  a*x + b*y = c
where a, b, c are given integers and x, y are unknown integers.

A solution exists if and only if gcd(a, b) divides c.

The Extended Euclidean Algorithm finds integers x, y such that
a*x + b*y = gcd(a, b), which is then scaled to solve a*x + b*y = c.

Once one particular solution (x0, y0) is known, the general solution is:
    x = x0 + (b/d)*t
    y = y0 - (a/d)*t
for any integer t, where d = gcd(a, b).

Example:
>>> diophantine(10, 6, 14)
(-7, 14)
>>> diophantine(391, 299, -69)
(9, -12)
"""
from __future__ import annotations

import math


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Extended Euclidean Algorithm.

    Returns (gcd, x, y) such that a*x + b*y = gcd(a, b).

    >>> extended_gcd(10, 6)
    (2, -1, 2)
    >>> extended_gcd(7, 5)
    (1, -2, 3)
    >>> extended_gcd(0, 5)
    (5, 0, 1)
    >>> extended_gcd(12, 0)
    (12, 1, 0)
    >>> extended_gcd(35, 15)
    (5, 1, -2)
    """
    if a == 0:
        return b, 0, 1
    d, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return d, x, y


def diophantine(a: int, b: int, c: int) -> tuple[int, int]:
    """
    Find one integer solution (x, y) to a*x + b*y = c.

    Raises ValueError if no solution exists (i.e., gcd(a,b) does not divide c).

    >>> diophantine(10, 6, 14)
    (-7, 14)
    >>> diophantine(391, 299, -69)
    (9, -12)
    >>> diophantine(4, 6, 3)
    Traceback (most recent call last):
        ...
    ValueError: No solution: gcd(4, 6) = 2 does not divide 3
    >>> diophantine(3, 0, 9)
    (3, 0)
    >>> diophantine(0, 7, 21)
    (0, 3)
    """
    if a == 0 and b == 0:
        if c == 0:
            return 0, 0
        raise ValueError("No solution: a and b are both zero but c is nonzero")

    d, x, y = extended_gcd(abs(a), abs(b))
    if c % d != 0:
        raise ValueError(f"No solution: gcd({a}, {b}) = {d} does not divide {c}")

    scale = c // d
    # Adjust signs: extended_gcd works on |a|, |b|
    x0 = x * scale * (1 if a >= 0 else -1)
    y0 = y * scale * (1 if b >= 0 else -1)
    return x0, y0


def diophantine_all_solutions(
    a: int, b: int, c: int, n: int = 2
) -> list[tuple[int, int]]:
    """
    Find n integer solutions to a*x + b*y = c.

    General solution: x = x0 + (b/d)*t,  y = y0 - (a/d)*t  for integer t.

    >>> diophantine_all_solutions(10, 6, 14)
    [(-7, 14), (-4, 9)]
    >>> diophantine_all_solutions(10, 6, 14, 4)
    [(-7, 14), (-4, 9), (-1, 4), (2, -1)]
    >>> diophantine_all_solutions(391, 299, -69, 4)
    [(9, -12), (22, -29), (35, -46), (48, -63)]
    """
    x0, y0 = diophantine(a, b, c)
    d = math.gcd(abs(a), abs(b))
    step_x = b // d
    step_y = a // d
    return [(x0 + i * step_x, y0 - i * step_y) for i in range(n)]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
