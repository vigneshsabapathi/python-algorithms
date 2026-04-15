"""
Fermat's Little Theorem:
    If p is prime and gcd(a, p) == 1, then a^(p-1) ≡ 1 (mod p).
Equivalently, a^p ≡ a (mod p) for any integer a.

Used for modular inverse when p is prime: a^(-1) ≡ a^(p-2) (mod p).

>>> fermat_little_theorem(2, 7)
1
>>> fermat_little_theorem(3, 11)
1
>>> modular_inverse(3, 11)
4
>>> (3 * 4) % 11
1
"""


def fermat_little_theorem(a: int, p: int) -> int:
    """Return a^(p-1) mod p. Should be 1 if p is prime and gcd(a,p)=1.

    >>> fermat_little_theorem(5, 13)
    1
    """
    return pow(a, p - 1, p)


def modular_inverse(a: int, p: int) -> int:
    """Modular inverse via Fermat's Little Theorem (p must be prime).

    >>> modular_inverse(7, 13)
    2
    >>> (7 * 2) % 13
    1
    """
    return pow(a, p - 2, p)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(fermat_little_theorem(2, 7))
    print(modular_inverse(3, 11))
