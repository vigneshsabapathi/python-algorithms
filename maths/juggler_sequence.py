"""
Juggler sequence: a[0] = n.
    a[k+1] = floor(a[k]^(1/2))    if a[k] is even
    a[k+1] = floor(a[k]^(3/2))    if a[k] is odd
Conjectured to always reach 1.

>>> juggler_sequence(9)
[9, 27, 140, 11, 36, 6, 2, 1]
>>> juggler_sequence(1)
[1]
>>> juggler_sequence(2)
[2, 1]
"""

import math


def juggler_sequence(n: int) -> list[int]:
    """Generate sequence until it hits 1.

    >>> juggler_sequence(4)
    [4, 2, 1]
    """
    if n < 1:
        raise ValueError("n must be positive")
    seq = [n]
    while n != 1:
        if n % 2 == 0:
            n = math.isqrt(n)
        else:
            n = math.isqrt(n * n * n)
        seq.append(n)
    return seq


def juggler_length(n: int) -> int:
    """Number of steps to reach 1 (length of sequence - 1).

    >>> juggler_length(9)
    7
    """
    return len(juggler_sequence(n)) - 1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(juggler_sequence(9))
