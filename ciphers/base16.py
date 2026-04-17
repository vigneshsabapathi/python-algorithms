"""
Base16 (Hexadecimal) Encoding and Decoding.

Converts bytes to uppercase hexadecimal strings and back.
Follows RFC 3548 section 6: only uppercase hex digits are valid.

References:
    https://www.ietf.org/rfc/rfc3548.txt
    https://en.wikipedia.org/wiki/Hexadecimal
"""


def base16_encode(data: bytes) -> str:
    """
    Encode bytes to an uppercase hexadecimal string.

    >>> base16_encode(b'Hello World!')
    '48656C6C6F20576F726C6421'
    >>> base16_encode(b'HELLO WORLD!')
    '48454C4C4F20574F524C4421'
    >>> base16_encode(b'')
    ''
    """
    return "".join(hex(byte)[2:].zfill(2).upper() for byte in data)


def base16_decode(data: str) -> bytes:
    """
    Decode an uppercase hexadecimal string to bytes.

    >>> base16_decode('48656C6C6F20576F726C6421')
    b'Hello World!'
    >>> base16_decode('48454C4C4F20574F524C4421')
    b'HELLO WORLD!'
    >>> base16_decode('')
    b''
    >>> base16_decode('486')
    Traceback (most recent call last):
        ...
    ValueError: Base16 encoded data is invalid:
    Data does not have an even number of hex digits.
    >>> base16_decode('48656c6c6f20576f726c6421')
    Traceback (most recent call last):
        ...
    ValueError: Base16 encoded data is invalid:
    Data is not uppercase hex or it contains invalid characters.
    """
    if len(data) % 2 != 0:
        raise ValueError(
            "Base16 encoded data is invalid:\n"
            "Data does not have an even number of hex digits."
        )
    if not set(data) <= set("0123456789ABCDEF"):
        raise ValueError(
            "Base16 encoded data is invalid:\n"
            "Data is not uppercase hex or it contains invalid characters."
        )
    return bytes(int(data[i] + data[i + 1], 16) for i in range(0, len(data), 2))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
