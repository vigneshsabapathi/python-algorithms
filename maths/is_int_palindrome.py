"""
Integer palindrome check: reads the same forward and backward.

>>> is_int_palindrome(121)
True
>>> is_int_palindrome(-121)
False
>>> is_int_palindrome(10)
False
>>> is_int_palindrome(0)
True
>>> is_int_palindrome(1221)
True
"""


def is_int_palindrome(num: int) -> bool:
    """O(log n) — reverse half the digits.

    >>> is_int_palindrome(12321)
    True
    """
    if num < 0 or (num % 10 == 0 and num != 0):
        return False
    reversed_half = 0
    while num > reversed_half:
        reversed_half = reversed_half * 10 + num % 10
        num //= 10
    return num == reversed_half or num == reversed_half // 10


def is_int_palindrome_str(num: int) -> bool:
    """String reversal approach."""
    if num < 0:
        return False
    s = str(num)
    return s == s[::-1]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(is_int_palindrome(12321))
