"""
Trapezoidal Rule
================
Approximate ∫_a^b f(x) dx by partitioning [a, b] into n equal trapezoids.

    I ≈ h/2 · (f(a) + 2·Σ f(x_i) + f(b))    where h = (b-a)/n.
"""
from typing import Callable


def trapezoidal(f: Callable[[float], float], a: float, b: float, n: int = 100) -> float:
    """
    >>> round(trapezoidal(lambda x: x, 0, 1, 100), 6)
    0.5
    >>> round(trapezoidal(lambda x: x*x, 0, 1, 1000), 6)
    0.333333
    >>> round(trapezoidal(lambda x: 1.0, 0, 5, 10), 6)
    5.0
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    h = (b - a) / n
    s = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        s += f(a + i * h)
    return s * h


if __name__ == "__main__":
    import doctest, math

    doctest.testmod()
    print("∫_0^1 x^2 dx ≈", trapezoidal(lambda x: x * x, 0, 1, 1000), "(true 1/3)")
    print("∫_0^pi sin(x) dx ≈", trapezoidal(math.sin, 0, math.pi, 1000), "(true 2)")
