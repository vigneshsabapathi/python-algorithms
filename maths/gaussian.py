"""
Gaussian (Normal) probability density function:
    f(x) = (1 / (sigma*sqrt(2*pi))) * exp(-((x-mu)^2) / (2*sigma^2))

>>> round(gaussian(0), 5)
0.39894
>>> round(gaussian(1), 5)
0.24197
>>> round(gaussian(0, mu=5, sigma=2), 5)
0.00876
"""

import math


def gaussian(x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    """Normal PDF at x.

    >>> round(gaussian(2, mu=0, sigma=1), 5)
    0.05399
    """
    coef = 1 / (sigma * math.sqrt(2 * math.pi))
    return coef * math.exp(-0.5 * ((x - mu) / sigma) ** 2)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(round(gaussian(0), 5))
