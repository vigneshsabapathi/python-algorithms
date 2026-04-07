def binary_count_setbits(a: int) -> int:
    """
    Take in 1 integer, return a number that is
    the number of 1's in binary representation of that number.

    >>> binary_count_setbits(25)
    3
    >>> binary_count_setbits(36)
    2
    >>> binary_count_setbits(16)
    1
    >>> binary_count_setbits(58)
    4
    >>> binary_count_setbits(4294967295)
    32
    >>> binary_count_setbits(0)
    0
    >>> binary_count_setbits(-10)
    Traceback (most recent call last):
        ...
    ValueError: Input value must be a positive integer
    >>> binary_count_setbits(0.8)
    Traceback (most recent call last):
        ...
    TypeError: Input value must be a 'int' type
    >>> binary_count_setbits("0")
    Traceback (most recent call last):
        ...
    TypeError: '<' not supported between instances of 'str' and 'int'
    """
    if a < 0:
        raise ValueError("Input value must be a positive integer")
    elif isinstance(a, float):
        raise TypeError("Input value must be a 'int' type")
    return bin(a).count("1")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        (25,         3),
        (36,         2),
        (16,         1),
        (58,         4),
        (4294967295, 32),
        (0,          0),
    ]
    for n, expected in cases:
        result = binary_count_setbits(n)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] binary_count_setbits({n}) = {result}  (expected {expected})")
