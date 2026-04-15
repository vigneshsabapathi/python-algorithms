"""
Hexadecimal to Binary Conversion

Convert a hexadecimal (base-16) string to its binary (base-2) representation.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/hex_to_bin.py
"""


def hex_to_bin(hex_string: str) -> str:
    """
    Convert a hexadecimal string to binary string.

    >>> hex_to_bin("FF")
    '11111111'
    >>> hex_to_bin("0")
    '0'
    >>> hex_to_bin("1A")
    '11010'
    >>> hex_to_bin("CA")
    '11001010'
    >>> hex_to_bin("")
    Traceback (most recent call last):
        ...
    ValueError: Empty string is not a valid hexadecimal
    >>> hex_to_bin("ZZ")
    Traceback (most recent call last):
        ...
    ValueError: Invalid hexadecimal string
    """
    if not hex_string:
        raise ValueError("Empty string is not a valid hexadecimal")

    hex_string = hex_string.upper().lstrip("0X")
    if not hex_string:
        return "0"

    valid = set("0123456789ABCDEF")
    if not all(c in valid for c in hex_string):
        raise ValueError("Invalid hexadecimal string")

    hex_to_bin_map = {
        "0": "0000", "1": "0001", "2": "0010", "3": "0011",
        "4": "0100", "5": "0101", "6": "0110", "7": "0111",
        "8": "1000", "9": "1001", "A": "1010", "B": "1011",
        "C": "1100", "D": "1101", "E": "1110", "F": "1111",
    }

    binary = "".join(hex_to_bin_map[c] for c in hex_string)
    return binary.lstrip("0") or "0"


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    test_cases = ["FF", "0", "1A", "CA", "10", "FFFF"]
    for h in test_cases:
        print(f"  hex_to_bin('{h}') = {hex_to_bin(h)}")
