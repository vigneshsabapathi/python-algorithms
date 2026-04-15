"""
Polynomial Evaluation (Horner's Method)
=======================================
Evaluate p(x) = a0 + a1*x + a2*x^2 + ... in O(n) using Horner's scheme:
    p(x) = ((... (a_n * x + a_{n-1}) * x + a_{n-2}) * x ... ) * x + a_0
"""
from typing import Sequence


def evaluate_poly(coeffs: Sequence[float], x: float) -> float:
    """
    Evaluate polynomial with ``coeffs`` in ascending order at ``x``.

    >>> evaluate_poly([1, 2, 3], 2)     # 1 + 2*2 + 3*4 = 17
    17
    >>> evaluate_poly([0, 0, 1], 5)     # x^2 at x=5
    25
    >>> evaluate_poly([1, -1, 1, -1], 1)  # 1 - 1 + 1 - 1
    0
    >>> evaluate_poly([], 3)
    0
    """
    result = 0
    for c in reversed(coeffs):
        result = result * x + c
    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(evaluate_poly([1, 2, 3], 2))
    print(evaluate_poly([2, -6, 2, -1], 3))  # -1*27 + 2*9 - 18 + 2 = -25
