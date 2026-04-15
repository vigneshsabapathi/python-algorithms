"""
Perfect Number
==============
A positive integer is a perfect number if it equals the sum of its proper
divisors (excluding itself).

Examples: 6 = 1+2+3, 28 = 1+2+4+7+14, 496, 8128.

https://en.wikipedia.org/wiki/Perfect_number
"""


def perfect(number: int) -> bool:
    """
    Return True if ``number`` is a perfect number.

    >>> perfect(6)
    True
    >>> perfect(28)
    True
    >>> perfect(496)
    True
    >>> perfect(12)
    False
    >>> perfect(1)
    False
    >>> perfect(0)
    False
    >>> perfect(-6)
    False
    """
    if not isinstance(number, int):
        raise ValueError("number must be an int")
    if number <= 1:
        return False
    return sum(i for i in range(1, number // 2 + 1) if number % i == 0) == number


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    for n in (6, 28, 496, 8128, 33550336):
        print(f"{n}: {perfect(n)}")
