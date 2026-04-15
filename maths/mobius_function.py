"""
Möbius function μ(n):
    μ(1) = 1
    μ(n) = 0 if n is divisible by a square of a prime
    μ(n) = (-1)^k if n is a product of k distinct primes

>>> mobius(1)
1
>>> mobius(2)
-1
>>> mobius(4)
0
>>> mobius(6)
1
>>> mobius(30)
-1
>>> [mobius(i) for i in range(1, 11)]
[1, -1, -1, 0, -1, 1, -1, 0, 0, 1]
"""


def mobius(n: int) -> int:
    """Compute μ(n) via trial-division factorization.

    >>> mobius(12)
    0
    """
    if n < 1:
        raise ValueError("n must be positive")
    if n == 1:
        return 1
    count = 0
    i = 2
    while i * i <= n:
        if n % i == 0:
            n //= i
            if n % i == 0:
                return 0  # square factor
            count += 1
        i += 1
    if n > 1:
        count += 1
    return -1 if count % 2 else 1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print([mobius(i) for i in range(1, 11)])
