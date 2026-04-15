"""
Estimate Pi with Monte Carlo
============================
Sample uniform points in the unit square; the fraction that fall inside the
quarter-circle of radius 1 converges to pi/4.
"""
import random


def estimate_pi(samples: int = 100_000, seed: int | None = 42) -> float:
    """
    >>> round(estimate_pi(10_000, seed=1), 1)
    3.1
    >>> 3.0 < estimate_pi(50_000, seed=123) < 3.3
    True
    """
    if samples <= 0:
        raise ValueError("samples must be positive")
    rng = random.Random(seed)
    inside = 0
    for _ in range(samples):
        x = rng.random()
        y = rng.random()
        if x * x + y * y <= 1.0:
            inside += 1
    return 4.0 * inside / samples


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    for n in (1_000, 10_000, 100_000, 1_000_000):
        print(f"samples={n:>8}: pi ~= {estimate_pi(n):.6f}")
