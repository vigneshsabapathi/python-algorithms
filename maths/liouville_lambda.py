"""
Liouville function λ(n) = (-1)^Ω(n), where Ω(n) counts prime factors with multiplicity.
λ(1) = 1.

>>> liouville(1)
1
>>> liouville(2)
-1
>>> liouville(4)
1
>>> liouville(12)
-1
>>> [liouville(i) for i in range(1, 11)]
[1, -1, -1, 1, -1, 1, -1, -1, 1, 1]
"""


def big_omega(n: int) -> int:
    """Count prime factors with multiplicity."""
    count = 0
    i = 2
    while i * i <= n:
        while n % i == 0:
            n //= i
            count += 1
        i += 1
    if n > 1:
        count += 1
    return count


def liouville(n: int) -> int:
    """λ(n) = (-1)^Ω(n).

    >>> liouville(6)
    1
    """
    if n < 1:
        raise ValueError("n must be positive")
    return 1 if big_omega(n) % 2 == 0 else -1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print([liouville(i) for i in range(1, 11)])
