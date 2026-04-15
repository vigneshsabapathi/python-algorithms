"""
Octal to Binary Conversion

Convert an octal (base-8) string to its binary (base-2) representation.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/octal_to_binary.py
"""


def octal_to_binary(octal_string: str) -> str:
    """
    Convert an octal string to binary string.

    >>> octal_to_binary("5")
    '0b101'
    >>> octal_to_binary("17")
    '0b1111'
    >>> octal_to_binary("10")
    '0b1000'
    >>> octal_to_binary("0")
    '0b0'
    >>> octal_to_binary("377")
    '0b11111111'
    >>> octal_to_binary("")
    Traceback (most recent call last):
        ...
    ValueError: Empty string is not a valid octal number
    >>> octal_to_binary("8")
    Traceback (most recent call last):
        ...
    ValueError: Non-octal value was passed to the function
    """
    if not octal_string:
        raise ValueError("Empty string is not a valid octal number")
    if not all(c in "01234567" for c in octal_string):
        raise ValueError("Non-octal value was passed to the function")

    octal_to_bin_map = {
        "0": "000", "1": "001", "2": "010", "3": "011",
        "4": "100", "5": "101", "6": "110", "7": "111",
    }

    binary = "".join(octal_to_bin_map[c] for c in octal_string)
    binary = binary.lstrip("0") or "0"
    return "0b" + binary


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    test_cases = ["5", "17", "10", "0", "377", "144"]
    for o in test_cases:
        print(f"  octal_to_binary('{o}') = {octal_to_binary(o)}")
