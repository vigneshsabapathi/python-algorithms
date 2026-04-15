"""
Monte Carlo estimation of π: sample random points in the unit square and
count how many fall inside the quarter unit circle. The ratio → π/4.

>>> import random
>>> random.seed(42)
>>> p = estimate_pi(10_000)
>>> 3.0 < p < 3.3
True
"""

import random


def estimate_pi(samples: int) -> float:
    """Return π estimate using `samples` random points.

    >>> random.seed(1)
    >>> result = estimate_pi(100_000)
    >>> 3.0 < result < 3.3
    True
    """
    hits = 0
    for _ in range(samples):
        x, y = random.random(), random.random()
        if x * x + y * y <= 1.0:
            hits += 1
    return 4.0 * hits / samples


def estimate_integral(fn, a: float, b: float, samples: int) -> float:
    """Estimate ∫_a^b fn(x) dx by mean-value Monte Carlo."""
    total = 0.0
    for _ in range(samples):
        x = random.uniform(a, b)
        total += fn(x)
    return (b - a) * total / samples


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    random.seed(0)
    print(estimate_pi(100_000))
