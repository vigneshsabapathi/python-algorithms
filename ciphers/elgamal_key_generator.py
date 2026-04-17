"""
ElGamal Key Generator — asymmetric key generation for the ElGamal cryptosystem.

Generates a public/private key pair:
  - Public key:  (key_size, e1, e2, p)  where e2 = e1^d mod p
  - Private key: (key_size, d)

Uses Miller-Rabin primality testing and primitive root generation.

References:
    https://en.wikipedia.org/wiki/ElGamal_encryption
    Handbook of Applied Cryptography, Algorithm 4.80
"""

from __future__ import annotations

import random

from ciphers.deterministic_miller_rabin import miller_rabin


def _is_prime(n: int) -> bool:
    """Thin wrapper around miller_rabin for clarity."""
    return miller_rabin(n, allow_probable=True)


def _generate_prime(key_size: int) -> int:
    """
    Generate a random prime of approximately key_size bits.

    >>> p = _generate_prime(16)
    >>> _is_prime(p)
    True
    """
    while True:
        candidate = random.getrandbits(key_size) | 1  # ensure odd
        if candidate >= 2 ** (key_size - 1) and _is_prime(candidate):
            return candidate


def primitive_root(p: int) -> int:
    """
    Return a primitive root modulo prime p.

    Uses the heuristic from Handbook of Applied Cryptography §4.80:
    pick random g and verify g^((p-1)/q) != 1 mod p for each prime factor q of p-1.

    >>> g = primitive_root(7)
    >>> g in (3, 5)
    True
    >>> g = primitive_root(11)
    >>> g in (2, 6, 7, 8)
    True
    """
    if p == 2:
        return 1
    p_minus_1 = p - 1
    # Find prime factors of p-1
    factors: list[int] = []
    temp = p_minus_1
    d = 2
    while d * d <= temp:
        if temp % d == 0:
            factors.append(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        factors.append(temp)

    while True:
        g = random.randint(2, p - 1)
        if all(pow(g, p_minus_1 // factor, p) != 1 for factor in factors):
            return g


def generate_key(key_size: int) -> tuple[tuple, tuple]:
    """
    Generate an ElGamal key pair of the given bit size.

    Returns (public_key, private_key) where:
      public_key  = (key_size, e1, e2, p)
      private_key = (key_size, d)

    >>> pub, priv = generate_key(64)
    >>> pub[0] == 64
    True
    >>> priv[0] == 64
    True
    >>> pub[3] > 0   # p is a large prime
    True
    """
    p = _generate_prime(key_size)
    e1 = primitive_root(p)
    d = random.randint(3, p - 2)      # private key must be > 2
    e2 = pow(e1, d, p)
    public_key = (key_size, e1, e2, p)
    private_key = (key_size, d)
    return public_key, private_key


if __name__ == "__main__":
    import doctest
    doctest.testmod()
