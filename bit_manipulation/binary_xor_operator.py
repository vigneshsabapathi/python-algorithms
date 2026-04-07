# https://www.tutorialspoint.com/python3/bitwise_operators_example.htm


def binary_xor(a: int, b: int) -> str:
    """
    Take in 2 integers, convert them to binary,
    return a binary number that is the
    result of a binary xor operation on the integers provided.

    >>> binary_xor(25, 32)
    '0b111001'
    >>> binary_xor(37, 50)
    '0b010111'
    >>> binary_xor(21, 30)
    '0b01011'
    >>> binary_xor(58, 73)
    '0b1110011'
    >>> binary_xor(0, 255)
    '0b11111111'
    >>> binary_xor(256, 256)
    '0b000000000'
    >>> binary_xor(0, -1)
    Traceback (most recent call last):
        ...
    ValueError: the value of both inputs must be positive
    >>> binary_xor(0, 1.1)
    Traceback (most recent call last):
        ...
    TypeError: 'float' object cannot be interpreted as an integer
    >>> binary_xor("0", "1")
    Traceback (most recent call last):
        ...
    TypeError: '<' not supported between instances of 'str' and 'int'
    """
    if a < 0 or b < 0:
        raise ValueError("the value of both inputs must be positive")

    a_binary = str(bin(a))[2:]  # remove the leading "0b"
    b_binary = str(bin(b))[2:]  # remove the leading "0b"

    max_len = max(len(a_binary), len(b_binary))

    return "0b" + "".join(
        str(int(char_a != char_b))
        for char_a, char_b in zip(a_binary.zfill(max_len), b_binary.zfill(max_len))
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        (25,  32,  "0b111001"),
        (37,  50,  "0b010111"),
        (21,  30,  "0b01011"),
        (58,  73,  "0b1110011"),
        (0,   255, "0b11111111"),
        (256, 256, "0b000000000"),
    ]
    for a, b, expected in cases:
        result = binary_xor(a, b)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] binary_xor({a}, {b}) = {result!r}  (expected {expected!r})")
