"""
Binary to Hexadecimal Conversion

Convert a binary (base-2) string to its hexadecimal (base-16) representation.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/binary_to_hexadecimal.py
"""


def binary_to_hexadecimal(binary_string: str) -> str:
    """
    Convert a binary string to hexadecimal.

    >>> binary_to_hexadecimal("101")
    '0x5'
    >>> binary_to_hexadecimal("1111")
    '0xF'
    >>> binary_to_hexadecimal("10000")
    '0x10'
    >>> binary_to_hexadecimal("11001010")
    '0xCA'
    >>> binary_to_hexadecimal("0")
    '0x0'
    >>> binary_to_hexadecimal("")
    Traceback (most recent call last):
        ...
    ValueError: Empty string is not a valid binary number
    >>> binary_to_hexadecimal("abc")
    Traceback (most recent call last):
        ...
    ValueError: Non-binary value was passed to the function
    """
    if not binary_string:
        raise ValueError("Empty string is not a valid binary number")
    if not all(char in "01" for char in binary_string):
        raise ValueError("Non-binary value was passed to the function")

    # Pad to multiple of 4
    padded = binary_string.zfill((len(binary_string) + 3) // 4 * 4)

    hex_map = {
        "0000": "0", "0001": "1", "0010": "2", "0011": "3",
        "0100": "4", "0101": "5", "0110": "6", "0111": "7",
        "1000": "8", "1001": "9", "1010": "A", "1011": "B",
        "1100": "C", "1101": "D", "1110": "E", "1111": "F",
    }

    hex_digits = []
    for i in range(0, len(padded), 4):
        group = padded[i : i + 4]
        hex_digits.append(hex_map[group])

    hex_string = "".join(hex_digits).lstrip("0") or "0"
    return "0x" + hex_string


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    test_cases = ["101", "1111", "10000", "11001010", "0", "11111111"]
    for binary in test_cases:
        print(f"  binary_to_hexadecimal('{binary}') = {binary_to_hexadecimal(binary)}")
