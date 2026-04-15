"""
Sum of Harmonic Series
======================
H_n = 1 + 1/2 + 1/3 + ... + 1/n.
"""
import math


def harmonic_sum(n: int) -> float:
    """
    >>> round(harmonic_sum(1), 6)
    1.0
    >>> round(harmonic_sum(2), 6)
    1.5
    >>> round(harmonic_sum(10), 6)
    2.928968
    """
    if n < 1:
        raise ValueError("n must be >= 1")
    s = 0.0
    for k in range(1, n + 1):
        s += 1.0 / k
    return s


def harmonic_approx(n: int) -> float:
    """
    Asymptotic approximation: H_n ~ ln(n) + gamma + 1/(2n).

    >>> round(harmonic_approx(1000), 4)
    7.4855
    """
    GAMMA = 0.5772156649015329
    return math.log(n) + GAMMA + 1.0 / (2 * n) - 1.0 / (12 * n * n)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    for n in (1, 10, 100, 1000):
        print(f"H_{n} = {harmonic_sum(n):.6f}  approx = {harmonic_approx(n):.6f}")
