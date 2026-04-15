"""
Multiplicative Persistence
==========================
Count the number of times you must multiply digits of ``n`` until a single
digit is obtained.

    39 -> 27 -> 14 -> 4   (persistence 3)
"""


def persistence(num: int) -> int:
    """
    >>> persistence(39)
    3
    >>> persistence(999)
    4
    >>> persistence(4)
    0
    >>> persistence(25)
    2
    >>> persistence(0)
    0
    """
    if num < 0:
        raise ValueError("num must be non-negative")
    steps = 0
    while num >= 10:
        product = 1
        for d in str(num):
            product *= int(d)
        num = product
        steps += 1
    return steps


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    for n in (39, 999, 77, 277777788888899):
        print(f"persistence({n}) = {persistence(n)}")
