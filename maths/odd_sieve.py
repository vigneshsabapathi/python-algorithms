"""
Odd sieve: Sieve of Eratosthenes that skips even numbers (except 2).
Halves memory and roughly halves time.

>>> odd_sieve(10)
[2, 3, 5, 7]
>>> odd_sieve(30)
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
>>> odd_sieve(2)
[2]
>>> odd_sieve(1)
[]
"""


def odd_sieve(n: int) -> list[int]:
    """All primes ≤ n using an odd-only sieve.

    >>> odd_sieve(20)
    [2, 3, 5, 7, 11, 13, 17, 19]
    """
    if n < 2:
        return []
    if n == 2:
        return [2]
    # index i represents odd number 2*i + 3; i in [0, size)
    size = (n - 1) // 2  # odd numbers from 3 up to (n if odd else n-1)
    sieve = [True] * size
    i = 0
    while (2 * i + 3) ** 2 <= n:
        if sieve[i]:
            p = 2 * i + 3
            start = (p * p - 3) // 2
            for j in range(start, size, p):
                sieve[j] = False
        i += 1
    primes = [2]
    for i in range(size):
        if sieve[i]:
            primes.append(2 * i + 3)
    return primes


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(odd_sieve(30))
