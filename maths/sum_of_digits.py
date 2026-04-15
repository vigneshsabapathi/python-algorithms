"""
Sum of Digits
=============
Return the sum of the decimal digits of |n|.
"""


def sum_of_digits(n: int) -> int:
    """
    >>> sum_of_digits(123)
    6
    >>> sum_of_digits(0)
    0
    >>> sum_of_digits(-45)
    9
    >>> sum_of_digits(99999)
    45
    """
    n = abs(n)
    s = 0
    while n:
        s += n % 10
        n //= 10
    return s


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    for n in (0, 7, 123, 99999, -45, 2**30):
        print(f"sum_of_digits({n}) = {sum_of_digits(n)}")
