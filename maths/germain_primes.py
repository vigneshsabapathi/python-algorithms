"""
Sophie Germain prime: a prime p such that 2p+1 is also prime.
Examples: 2 (→5), 3 (→7), 5 (→11), 11 (→23), 23 (→47), 29 (→59)...

>>> is_germain_prime(11)
True
>>> is_germain_prime(7)
False
>>> germain_primes_up_to(30)
[2, 3, 5, 11, 23, 29]
"""


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def is_germain_prime(p: int) -> bool:
    """True if p and 2p+1 are both prime.

    >>> is_germain_prime(23)
    True
    """
    return is_prime(p) and is_prime(2 * p + 1)


def germain_primes_up_to(limit: int) -> list[int]:
    """All Germain primes <= limit."""
    return [p for p in range(2, limit + 1) if is_germain_prime(p)]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(germain_primes_up_to(30))
