"""
Monte Carlo dice simulation: simulate rolling num_dice dice for num_throws
trials, return the empirical probability distribution of the total.

>>> import random
>>> random.seed(0)
>>> probs = throw_dice(num_throws=10_000, num_dice=2)
>>> len(probs)  # possible sums 2..12
11
>>> abs(sum(probs.values()) - 1.0) < 1e-9
True
"""

import random
from collections import Counter


def throw_dice(num_throws: int, num_dice: int = 2) -> dict:
    """Empirical PMF of the sum of `num_dice` six-sided dice over `num_throws` trials.

    >>> random.seed(7)
    >>> p = throw_dice(1000, 1)
    >>> len(p)
    6
    """
    counts = Counter()
    for _ in range(num_throws):
        total = sum(random.randint(1, 6) for _ in range(num_dice))
        counts[total] += 1
    return {k: v / num_throws for k, v in sorted(counts.items())}


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    random.seed(0)
    p = throw_dice(100_000, 2)
    for k, v in sorted(p.items()):
        print(f"{k:2d}: {v:.4f}")
