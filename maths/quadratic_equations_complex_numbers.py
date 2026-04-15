"""
Quadratic Equation Solver (complex roots)
=========================================
Solve ax² + bx + c = 0 with complex coefficients/roots via quadratic formula.
"""
import cmath
from typing import Tuple


def quadratic_roots(a: complex, b: complex, c: complex) -> Tuple[complex, complex]:
    """
    >>> quadratic_roots(1, -3, 2)
    ((2+0j), (1+0j))
    >>> quadratic_roots(1, 0, 1)
    (1j, -1j)
    >>> quadratic_roots(1, 2, 1)
    ((-1+0j), (-1+0j))
    """
    if a == 0:
        raise ValueError("a must be non-zero for a quadratic equation")
    d = cmath.sqrt(b * b - 4 * a * c)
    return (-b + d) / (2 * a), (-b - d) / (2 * a)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    for coeffs in [(1, -3, 2), (1, 0, 1), (1, 2, 5)]:
        r = quadratic_roots(*coeffs)
        print(f"{coeffs} -> {r}")
