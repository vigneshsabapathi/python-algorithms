"""
RSA Prime Factorization

Given the RSA parameters d (private exponent), e (public exponent), and n
(modulus), recover the two prime factors p and q such that p * q = n.

Algorithm follows the randomized method from:
  https://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf  (page 3)
  https://www.di-mgt.com.au/rsa_factorize_n.html
"""

from __future__ import annotations

import math
import random


def rsafactor(d: int, e: int, n: int) -> list[int]:
    """
    Return the two prime factors [p, q] of n given d and e.

    >>> rsafactor(3, 16971, 25777)
    [149, 173]
    >>> rsafactor(7331, 11, 27233)
    [113, 241]
    >>> rsafactor(4021, 13, 17711)
    [89, 199]
    """
    k = d * e - 1
    p = 0
    q = 0
    while p == 0:
        g = random.randint(2, n - 1)
        t = k
        while True:
            if t % 2 == 0:
                t //= 2
                x = pow(g, t, n)
                y = math.gcd(x - 1, n)
                if x > 1 and y > 1:
                    p = y
                    q = n // y
                    break
            else:
                break  # t odd — pick a new g
    return sorted([p, q])


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(rsafactor(3, 16971, 25777))
