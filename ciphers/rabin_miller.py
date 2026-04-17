"""
Rabin-Miller Primality Test

A probabilistic primality test used as the basis for RSA key generation.
The test runs k rounds; each round has a 1/4 chance of a false positive,
so 5 rounds gives a false-positive probability < 1/1024.

https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test
"""

import random


def rabin_miller(num: int) -> bool:
    """
    Return True if num is probably prime (probabilistic).

    >>> rabin_miller(7)
    True
    >>> rabin_miller(9)
    False
    >>> rabin_miller(11)
    True
    """
    s = num - 1
    t = 0
    while s % 2 == 0:
        s //= 2
        t += 1

    for _ in range(5):  # 5 witness rounds
        a = random.randrange(2, num - 1)
        v = pow(a, s, num)
        if v != 1:
            i = 0
            while v != (num - 1):
                if i == t - 1:
                    return False
                i += 1
                v = (v * v) % num
    return True


def is_prime(num: int) -> bool:
    """
    Return True if num is prime, using trial division for small primes
    then Rabin-Miller for larger candidates.

    >>> is_prime(2)
    True
    >>> is_prime(1)
    False
    >>> is_prime(97)
    True
    >>> is_prime(100)
    False
    >>> is_prime(982451653)
    True
    """
    if num < 2:
        return False

    low_primes = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
        71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149,
        151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
        233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313,
        317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
        419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499,
        503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601,
        607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691,
        701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809,
        811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907,
        911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997,
    ]

    if num in low_primes:
        return True
    for prime in low_primes:
        if num % prime == 0:
            return False

    return rabin_miller(num)


def generate_large_prime(keysize: int = 1024) -> int:
    """
    Generate a large random prime of approximately keysize bits.

    >>> import random; random.seed(0)
    >>> p = generate_large_prime(8)
    >>> is_prime(p)
    True
    """
    while True:
        num = random.randrange(2 ** (keysize - 1), 2**keysize)
        if is_prime(num):
            return num


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    p = generate_large_prime(16)
    print(f"Prime: {p}, is_prime: {is_prime(p)}")
