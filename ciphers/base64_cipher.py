"""
Base64 Encoding and Decoding (RFC 4648).

Converts bytes to a Base64 string using A-Z, a-z, 0-9, +, /
with '=' padding to align output to multiples of 4 characters.

References:
    https://en.wikipedia.org/wiki/Base64
    https://datatracker.ietf.org/doc/html/rfc4648
"""

B64_CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def base64_encode(data: bytes) -> bytes:
    """
    Encode bytes to Base64 per RFC 4648.

    >>> from base64 import b64encode
    >>> a = b"This pull request is part of Hacktoberfest20!"
    >>> b = b"https://tools.ietf.org/html/rfc4648"
    >>> c = b"A"
    >>> base64_encode(a) == b64encode(a)
    True
    >>> base64_encode(b) == b64encode(b)
    True
    >>> base64_encode(c) == b64encode(c)
    True
    >>> base64_encode("abc")
    Traceback (most recent call last):
      ...
    TypeError: a bytes-like object is required, not 'str'
    """
    if not isinstance(data, bytes):
        msg = f"a bytes-like object is required, not '{data.__class__.__name__}'"
        raise TypeError(msg)

    binary_stream = "".join(bin(byte)[2:].zfill(8) for byte in data)

    padding_needed = len(binary_stream) % 6 != 0

    if padding_needed:
        padding = b"=" * ((6 - len(binary_stream) % 6) // 2)
        binary_stream += "0" * (6 - len(binary_stream) % 6)
    else:
        padding = b""

    return (
        "".join(
            B64_CHARSET[int(binary_stream[index : index + 6], 2)]
            for index in range(0, len(binary_stream), 6)
        ).encode()
        + padding
    )


def base64_decode(encoded_data: str) -> bytes:
    """
    Decode a Base64 string back to bytes per RFC 4648.

    >>> from base64 import b64decode
    >>> a = "VGhpcyBwdWxsIHJlcXVlc3QgaXMgcGFydCBvZiBIYWNrdG9iZXJmZXN0MjAh"
    >>> b = "aHR0cHM6Ly90b29scy5pZXRmLm9yZy9odG1sL3JmYzQ2NDg="
    >>> c = "QQ=="
    >>> base64_decode(a) == b64decode(a)
    True
    >>> base64_decode(b) == b64decode(b)
    True
    >>> base64_decode(c) == b64decode(c)
    True
    >>> base64_decode("abc")
    Traceback (most recent call last):
      ...
    AssertionError: Incorrect padding
    """
    if not isinstance(encoded_data, (bytes, str)):
        msg = (
            "argument should be a bytes-like object or ASCII string, "
            f"not '{encoded_data.__class__.__name__}'"
        )
        raise TypeError(msg)

    if isinstance(encoded_data, bytes):
        try:
            encoded_data = encoded_data.decode("utf-8")
        except UnicodeDecodeError:
            raise ValueError("base64 encoded data should only contain ASCII characters")

    padding = encoded_data.count("=")

    if padding:
        assert all(char in B64_CHARSET for char in encoded_data[:-padding]), (
            "Invalid base64 character(s) found."
        )
    else:
        assert all(char in B64_CHARSET for char in encoded_data), (
            "Invalid base64 character(s) found."
        )

    assert len(encoded_data) % 4 == 0 and padding < 3, "Incorrect padding"

    if padding:
        encoded_data = encoded_data[:-padding]
        binary_stream = "".join(
            bin(B64_CHARSET.index(char))[2:].zfill(6) for char in encoded_data
        )[: -padding * 2]
    else:
        binary_stream = "".join(
            bin(B64_CHARSET.index(char))[2:].zfill(6) for char in encoded_data
        )

    data = [
        int(binary_stream[index : index + 8], 2)
        for index in range(0, len(binary_stream), 8)
    ]

    return bytes(data)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
