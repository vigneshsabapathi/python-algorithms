"""
Karatsuba multiplication: O(n^log2(3)) ≈ O(n^1.585) recursive algorithm.
Splits each number into high/low halves and uses 3 sub-multiplications
instead of 4.

>>> karatsuba(0, 5)
0
>>> karatsuba(1234, 5678)
7006652
>>> karatsuba(10, 20)
200
>>> karatsuba(99999, 99999)
9999800001
"""


def karatsuba(x: int, y: int) -> int:
    """Recursive Karatsuba multiplication.

    >>> karatsuba(1234567, 7654321)
    9449772114007
    """
    if x < 10 or y < 10:
        return x * y
    n = max(len(str(x)), len(str(y)))
    m = n // 2
    power = 10**m
    high_x, low_x = divmod(x, power)
    high_y, low_y = divmod(y, power)
    z0 = karatsuba(low_x, low_y)
    z2 = karatsuba(high_x, high_y)
    z1 = karatsuba(low_x + high_x, low_y + high_y) - z0 - z2
    return z2 * 10 ** (2 * m) + z1 * 10**m + z0


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(karatsuba(1234, 5678))
