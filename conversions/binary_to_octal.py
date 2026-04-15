"""
Binary to Octal Conversion

Convert a binary (base-2) string to its octal (base-8) representation.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/binary_to_octal.py
"""


def binary_to_octal(binary_string: str) -> str:
    """
    Convert a binary string to octal.

    >>> binary_to_octal("101")
    '0o5'
    >>> binary_to_octal("1111")
    '0o17'
    >>> binary_to_octal("1000")
    '0o10'
    >>> binary_to_octal("0")
    '0o0'
    >>> binary_to_octal("")
    Traceback (most recent call last):
        ...
    ValueError: Empty string is not a valid binary number
    >>> binary_to_octal("2")
    Traceback (most recent call last):
        ...
    ValueError: Non-binary value was passed to the function
    """
    if not binary_string:
        raise ValueError("Empty string is not a valid binary number")
    if not all(char in "01" for char in binary_string):
        raise ValueError("Non-binary value was passed to the function")

    # Pad to multiple of 3
    padded = binary_string.zfill((len(binary_string) + 2) // 3 * 3)

    octal_digits = []
    for i in range(0, len(padded), 3):
        group = padded[i : i + 3]
        octal_digits.append(str(int(group, 2)))

    octal_string = "".join(octal_digits).lstrip("0") or "0"
    return "0o" + octal_string


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    test_cases = ["101", "1111", "1000", "11001010", "0", "111"]
    for binary in test_cases:
        print(f"  binary_to_octal('{binary}') = {binary_to_octal(binary)}")
