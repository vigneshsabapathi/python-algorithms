"""
RSA Key Generator (pure Python)
================================
Generates RSA public/private key pairs using Rabin-Miller primality testing
and the extended Euclidean algorithm for modular inverse.

https://en.wikipedia.org/wiki/RSA_(cryptosystem)
"""

import math
import random

from ciphers.rabin_miller import generate_large_prime


def find_mod_inverse(a: int, m: int) -> int:
    """
    Return x such that (a * x) % m == 1 (extended Euclidean algorithm).

    >>> find_mod_inverse(17, 3120)
    2753
    >>> find_mod_inverse(3, 40)
    27
    """
    if math.gcd(a, m) != 1:
        raise ValueError(f"{a} and {m} are not coprime")
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        u1, u2, u3, v1, v2, v3 = v1, v2, v3, u1 - q * v1, u2 - q * v2, u3 - q * v3
    return u1 % m


def generate_key(
    key_size: int,
) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Generate an RSA public/private key pair of *key_size* bits each prime.

    Returns ((n, e), (n, d)) where (n, e) is the public key.

    >>> random.seed(0)
    >>> public_key, private_key = generate_key(8)
    >>> public_key
    (26569, 239)
    >>> private_key
    (26569, 2855)
    """
    p = generate_large_prime(key_size)
    q = generate_large_prime(key_size)
    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        e = random.randrange(2 ** (key_size - 1), 2**key_size)
        if math.gcd(e, phi) == 1:
            break

    d = find_mod_inverse(e, phi)
    return (n, e), (n, d)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    pub, priv = generate_key(16)
    print(f"Public key : {pub}")
    print(f"Private key: {priv}")
