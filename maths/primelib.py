"""
Prime Library (primelib)
========================
Small collection of prime-number utilities: primality, factorization,
totient, primes-in-range, GCD/LCM.
"""
import math
from typing import List


def is_prime(n: int) -> bool:
    """
    >>> is_prime(2), is_prime(7), is_prime(10)
    (True, True, False)
    """
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    r = math.isqrt(n)
    for i in range(3, r + 1, 2):
        if n % i == 0:
            return False
    return True


def primes_in_range(lo: int, hi: int) -> List[int]:
    """
    >>> primes_in_range(10, 30)
    [11, 13, 17, 19, 23, 29]
    """
    return [k for k in range(max(2, lo), hi + 1) if is_prime(k)]


def prime_factors(n: int) -> List[int]:
    """
    >>> prime_factors(60)
    [2, 2, 3, 5]
    """
    out = []
    while n % 2 == 0:
        out.append(2); n //= 2
    i = 3
    while i * i <= n:
        while n % i == 0:
            out.append(i); n //= i
        i += 2
    if n > 1:
        out.append(n)
    return out


def greatest_prime_factor(n: int) -> int:
    """
    >>> greatest_prime_factor(60)
    5
    """
    return prime_factors(n)[-1]


def smallest_prime_factor(n: int) -> int:
    """
    >>> smallest_prime_factor(60)
    2
    """
    return prime_factors(n)[0]


def gcd(a: int, b: int) -> int:
    """
    >>> gcd(12, 18)
    6
    """
    while b:
        a, b = b, a % b
    return abs(a)


def lcm(a: int, b: int) -> int:
    """
    >>> lcm(4, 6)
    12
    """
    return abs(a * b) // gcd(a, b) if a and b else 0


def euler_totient(n: int) -> int:
    """
    >>> euler_totient(9)
    6
    >>> euler_totient(10)
    4
    """
    result = n
    for p in set(prime_factors(n)):
        result -= result // p
    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(primes_in_range(1, 30))
    print("phi(36) =", euler_totient(36))
    print("gcd(48, 180) =", gcd(48, 180))
    print("lcm(6, 8) =", lcm(6, 8))
