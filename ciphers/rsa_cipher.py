"""
RSA Cipher (Pure Python)

Implements RSA encryption and decryption on text messages by converting
each block of ASCII bytes to a large integer and applying modular
exponentiation.

  Encrypt: C = M^e mod n
  Decrypt: M = C^d mod n

The key is a tuple (n, e) for encryption or (n, d) for decryption.

https://en.wikipedia.org/wiki/RSA_(cryptosystem)
"""

DEFAULT_BLOCK_SIZE = 128
BYTE_SIZE = 256


def get_blocks_from_text(
    message: str, block_size: int = DEFAULT_BLOCK_SIZE
) -> list[int]:
    """
    Convert a message string to a list of block integers.

    >>> get_blocks_from_text("Hello", block_size=5)
    [478560413000]
    """
    message_bytes = message.encode("ascii")
    block_ints = []
    for block_start in range(0, len(message_bytes), block_size):
        block_int = 0
        for i in range(block_start, min(block_start + block_size, len(message_bytes))):
            block_int += message_bytes[i] * (BYTE_SIZE ** (i % block_size))
        block_ints.append(block_int)
    return block_ints


def get_text_from_blocks(
    block_ints: list[int],
    message_length: int,
    block_size: int = DEFAULT_BLOCK_SIZE,
) -> str:
    """
    Convert block integers back to the original message string.

    >>> get_text_from_blocks([478560413000], 5, block_size=5)
    'Hello'
    """
    message: list[str] = []
    for block_int in block_ints:
        block_message: list[str] = []
        for i in range(block_size - 1, -1, -1):
            if len(message) + i < message_length:
                ascii_number = block_int // (BYTE_SIZE**i)
                block_int = block_int % (BYTE_SIZE**i)
                block_message.insert(0, chr(ascii_number))
        message.extend(block_message)
    return "".join(message)


def encrypt_message(
    message: str,
    key: tuple[int, int],
    block_size: int = DEFAULT_BLOCK_SIZE,
) -> list[int]:
    """
    Encrypt a message with an RSA public key (n, e).

    >>> n = 323; e = 5; d = 173   # p=17, q=19 textbook example
    >>> enc = encrypt_message("Hi", (n, e), block_size=1)
    >>> decrypt_message(enc, len("Hi"), (n, d), block_size=1)
    'Hi'
    """
    n, e = key
    return [pow(block, e, n) for block in get_blocks_from_text(message, block_size)]


def decrypt_message(
    encrypted_blocks: list[int],
    message_length: int,
    key: tuple[int, int],
    block_size: int = DEFAULT_BLOCK_SIZE,
) -> str:
    """
    Decrypt a list of RSA-encrypted blocks with private key (n, d).

    >>> n = 323; e = 5; d = 173   # p=17, q=19 textbook example
    >>> enc = encrypt_message("Hi", (n, e), block_size=1)
    >>> decrypt_message(enc, len("Hi"), (n, d), block_size=1)
    'Hi'
    """
    n, d = key
    decrypted_blocks = [pow(block, d, n) for block in encrypted_blocks]
    return get_text_from_blocks(decrypted_blocks, message_length, block_size)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    # Small demo key (NOT secure — for illustration only)
    n, e, d = 2537, 13, 937
    msg = "Hello RSA"
    enc = encrypt_message(msg, (n, e), block_size=2)
    dec = decrypt_message(enc, len(msg), (n, d), block_size=2)
    print(f"Original : {msg}")
    print(f"Encrypted: {enc}")
    print(f"Decrypted: {dec}")
