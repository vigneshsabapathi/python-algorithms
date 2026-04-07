def binary_coded_decimal(number: int) -> str:
    """
    Find binary coded decimal (bcd) of integer base 10.
    Each digit of the number is represented by a 4-bit binary.
    Example:
    >>> binary_coded_decimal(-2)
    '0b0000'
    >>> binary_coded_decimal(-1)
    '0b0000'
    >>> binary_coded_decimal(0)
    '0b0000'
    >>> binary_coded_decimal(3)
    '0b0011'
    >>> binary_coded_decimal(2)
    '0b0010'
    >>> binary_coded_decimal(12)
    '0b00010010'
    >>> binary_coded_decimal(987)
    '0b100110000111'
    """
    return "0b" + "".join(
        str(bin(int(digit)))[2:].zfill(4) for digit in str(max(0, number))
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        (-2,  "0b0000"),
        (-1,  "0b0000"),
        (0,   "0b0000"),
        (2,   "0b0010"),
        (3,   "0b0011"),
        (12,  "0b00010010"),
        (987, "0b100110000111"),
    ]
    for n, expected in cases:
        result = binary_coded_decimal(n)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] binary_coded_decimal({n:>4}) = {result!r:<20}  (expected {expected!r})")
