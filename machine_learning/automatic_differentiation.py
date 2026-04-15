"""
Automatic Differentiation

Forward-mode automatic differentiation using dual numbers.
Computes exact derivatives without symbolic manipulation or
numerical approximation.

A dual number: a + b*epsilon, where epsilon^2 = 0.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/automatic_differentiation.py
"""

from __future__ import annotations

import math


class DualNumber:
    """
    Dual number for forward-mode automatic differentiation.

    Represents a + b*eps where eps^2 = 0.

    >>> x = DualNumber(3.0, 1.0)  # x = 3, dx/dx = 1
    >>> f = x * x  # f(x) = x^2
    >>> f.real  # f(3)
    9.0
    >>> f.dual  # f'(3) = 2*3 = 6
    6.0

    >>> x = DualNumber(2.0, 1.0)
    >>> f = x * x * x  # f(x) = x^3
    >>> f.dual  # f'(2) = 3*4 = 12
    12.0
    """

    def __init__(self, real: float, dual: float = 0.0) -> None:
        self.real = real
        self.dual = dual

    def __repr__(self) -> str:
        return f"DualNumber({self.real}, {self.dual})"

    def __add__(self, other: DualNumber | float) -> DualNumber:
        if isinstance(other, (int, float)):
            return DualNumber(self.real + other, self.dual)
        return DualNumber(self.real + other.real, self.dual + other.dual)

    def __radd__(self, other: float) -> DualNumber:
        return self.__add__(other)

    def __sub__(self, other: DualNumber | float) -> DualNumber:
        if isinstance(other, (int, float)):
            return DualNumber(self.real - other, self.dual)
        return DualNumber(self.real - other.real, self.dual - other.dual)

    def __rsub__(self, other: float) -> DualNumber:
        return DualNumber(other - self.real, -self.dual)

    def __mul__(self, other: DualNumber | float) -> DualNumber:
        if isinstance(other, (int, float)):
            return DualNumber(self.real * other, self.dual * other)
        # (a + b*eps)(c + d*eps) = ac + (ad + bc)*eps
        return DualNumber(
            self.real * other.real,
            self.real * other.dual + self.dual * other.real,
        )

    def __rmul__(self, other: float) -> DualNumber:
        return self.__mul__(other)

    def __truediv__(self, other: DualNumber | float) -> DualNumber:
        if isinstance(other, (int, float)):
            return DualNumber(self.real / other, self.dual / other)
        # (a + b*eps) / (c + d*eps) = a/c + (bc - ad)/c^2 * eps
        return DualNumber(
            self.real / other.real,
            (self.dual * other.real - self.real * other.dual) / other.real**2,
        )

    def __rtruediv__(self, other: float) -> DualNumber:
        return DualNumber(other, 0.0).__truediv__(self)

    def __pow__(self, n: float) -> DualNumber:
        # d/dx x^n = n * x^(n-1)
        return DualNumber(
            self.real**n,
            n * self.real ** (n - 1) * self.dual,
        )

    def __neg__(self) -> DualNumber:
        return DualNumber(-self.real, -self.dual)


def dual_sin(x: DualNumber) -> DualNumber:
    """
    Sine for dual numbers: d/dx sin(x) = cos(x).

    >>> x = DualNumber(0.0, 1.0)
    >>> result = dual_sin(x)
    >>> abs(result.real - 0.0) < 1e-10
    True
    >>> abs(result.dual - 1.0) < 1e-10
    True
    """
    return DualNumber(math.sin(x.real), math.cos(x.real) * x.dual)


def dual_cos(x: DualNumber) -> DualNumber:
    """
    Cosine for dual numbers: d/dx cos(x) = -sin(x).

    >>> x = DualNumber(0.0, 1.0)
    >>> result = dual_cos(x)
    >>> abs(result.real - 1.0) < 1e-10
    True
    >>> abs(result.dual - 0.0) < 1e-10
    True
    """
    return DualNumber(math.cos(x.real), -math.sin(x.real) * x.dual)


def dual_exp(x: DualNumber) -> DualNumber:
    """
    Exponential for dual numbers: d/dx exp(x) = exp(x).

    >>> x = DualNumber(0.0, 1.0)
    >>> result = dual_exp(x)
    >>> abs(result.real - 1.0) < 1e-10
    True
    >>> abs(result.dual - 1.0) < 1e-10
    True
    """
    exp_val = math.exp(x.real)
    return DualNumber(exp_val, exp_val * x.dual)


def dual_log(x: DualNumber) -> DualNumber:
    """
    Natural logarithm for dual numbers: d/dx ln(x) = 1/x.

    >>> x = DualNumber(1.0, 1.0)
    >>> result = dual_log(x)
    >>> abs(result.real - 0.0) < 1e-10
    True
    >>> abs(result.dual - 1.0) < 1e-10
    True
    """
    return DualNumber(math.log(x.real), x.dual / x.real)


def derivative(f, x: float) -> tuple[float, float]:
    """
    Compute f(x) and f'(x) using automatic differentiation.

    >>> def f(x): return x ** 2 + 3 * x + 1
    >>> val, deriv = derivative(f, 2.0)
    >>> val  # 4 + 6 + 1
    11.0
    >>> deriv  # 2*2 + 3
    7.0
    """
    result = f(DualNumber(x, 1.0))
    if isinstance(result, DualNumber):
        return result.real, result.dual
    return float(result), 0.0


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- Automatic Differentiation Demo ---")

    # f(x) = x^3 - 2x^2 + 5x - 3
    def poly(x):
        return x**3 - 2 * x**2 + 5 * x - 3

    for x_val in [-1.0, 0.0, 1.0, 2.0, 3.0]:
        val, deriv = derivative(poly, x_val)
        # Analytical: f'(x) = 3x^2 - 4x + 5
        analytical = 3 * x_val**2 - 4 * x_val + 5
        print(f"x={x_val:5.1f}: f(x)={val:8.2f}, f'(x)={deriv:8.2f} (analytical={analytical:.2f})")

    # Composition: f(x) = sin(x^2)
    def f_comp(x):
        return dual_sin(x * x)

    val, deriv = derivative(f_comp, 1.0)
    print(f"\nsin(x^2) at x=1: f={val:.6f}, f'={deriv:.6f}")
    print(f"  analytical: f'= 2*cos(1) = {2 * math.cos(1):.6f}")
