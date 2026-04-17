"""
Diffie-Hellman Key Exchange — find_primitive helper.

find_primitive(modulus) returns the smallest primitive root modulo `modulus`.
A primitive root r generates all non-zero residues via r^0, r^1, ..., r^(m-2).

The full Diffie-Hellman exchange:
  - Both parties agree on prime q and primitive root g.
  - A picks private key a, publishes g^a mod q.
  - B picks private key b, publishes g^b mod q.
  - Shared secret: (g^b)^a mod q == (g^a)^b mod q.

References:
    https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange
"""

from __future__ import annotations


def find_primitive(modulus: int) -> int | None:
    """
    Return the smallest primitive root modulo `modulus`, or None if none exists.

    >>> find_primitive(7)
    3
    >>> find_primitive(11)
    2
    >>> find_primitive(8) is None
    True
    >>> find_primitive(13)
    2
    """
    for r in range(1, modulus):
        residues = []
        for x in range(modulus - 1):
            val = pow(r, x, modulus)
            if val in residues:
                break
            residues.append(val)
        else:
            return r
    return None


if __name__ == "__main__":
    import doctest
    doctest.testmod()
