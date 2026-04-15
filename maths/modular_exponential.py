"""
Modular exponentiation: compute base^exp mod m in O(log exp).

>>> modular_exp(2, 10, 1000)
24
>>> modular_exp(5, 0, 7)
1
>>> modular_exp(3, 1000000, 1000000007)
64935414
"""


def modular_exp(base: int, exp: int, mod: int) -> int:
    """Binary exponentiation.

    >>> modular_exp(7, 13, 19)
    7
    """
    if mod == 1:
        return 0
    if exp < 0:
        raise ValueError("negative exponent not supported; use modular inverse first")
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod
    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(modular_exp(2, 10, 1000))
