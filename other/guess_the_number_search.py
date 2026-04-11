"""
Guess the Number Search — Binary search based number guessing game.

Implements both interactive and automated versions of the number guessing game
where binary search is used to find a secret number efficiently.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/guess_the_number_search.py
"""

from __future__ import annotations

import random


def guess_the_number(
    low: int, high: int, secret: int | None = None
) -> tuple[int, int]:
    """
    Find a secret number in [low, high] using binary search.

    Returns (secret_number, number_of_guesses).

    >>> guess_the_number(1, 100, 42)
    (42, 7)
    >>> guess_the_number(1, 100, 1)
    (1, 6)
    >>> guess_the_number(1, 100, 100)
    (100, 7)
    >>> guess_the_number(1, 1, 1)
    (1, 1)
    >>> guess_the_number(50, 60, 55)
    (55, 1)
    """
    if secret is None:
        secret = random.randint(low, high)

    guesses = 0
    lo, hi = low, high

    while lo <= hi:
        guesses += 1
        mid = (lo + hi) // 2
        if mid == secret:
            return secret, guesses
        elif mid < secret:
            lo = mid + 1
        else:
            hi = mid - 1

    return secret, guesses  # Should not reach here for valid input


if __name__ == "__main__":
    import doctest

    doctest.testmod()
