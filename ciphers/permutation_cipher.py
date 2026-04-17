"""
Permutation (Transposition) Cipher
https://www.nku.edu/~christensen/1402%20permutation%20ciphers.pdf

Divides the message into fixed-size blocks and rearranges characters within each
block according to a permutation key.
"""

import random


def generate_valid_block_size(message_length: int) -> int:
    """
    Return a random divisor of message_length (between 2 and message_length).

    >>> random.seed(1)
    >>> generate_valid_block_size(12)
    3
    """
    sizes = [s for s in range(2, message_length + 1) if message_length % s == 0]
    return random.choice(sizes)


def generate_permutation_key(block_size: int) -> list[int]:
    """
    Return a random permutation of 0..block_size-1.

    >>> random.seed(0)
    >>> generate_permutation_key(4)
    [2, 0, 1, 3]
    """
    digits = list(range(block_size))
    random.shuffle(digits)
    return digits


def encrypt(
    message: str,
    key: list[int] | None = None,
    block_size: int | None = None,
) -> tuple[str, list[int]]:
    """
    Encrypt message by permuting characters within each block.

    Returns (encrypted_message, key).

    >>> encrypted, key = encrypt("HELLOWORLD", key=[1, 0], block_size=2)
    >>> encrypted
    'EHLLWORODL'
    >>> decrypt(encrypted, key)
    'HELLOWORLD'
    """
    message = message.upper()
    length = len(message)

    if key is None or block_size is None:
        block_size = generate_valid_block_size(length)
        key = generate_permutation_key(block_size)

    encrypted = ""
    for i in range(0, length, block_size):
        block = message[i: i + block_size]
        encrypted += "".join(block[j] for j in key)
    return encrypted, key


def decrypt(encrypted_message: str, key: list[int]) -> str:
    """
    Decrypt a permutation-encrypted message.

    >>> decrypt("EHLLWORODL", [1, 0])
    'HELLOWORLD'
    """
    key_length = len(key)
    decrypted = ""
    for i in range(0, len(encrypted_message), key_length):
        block = encrypted_message[i: i + key_length]
        original: list[str] = [""] * key_length
        for j, pos in enumerate(key):
            original[pos] = block[j]
        decrypted += "".join(original)
    return decrypted


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    msg = "HELLO WORLD"
    enc, k = encrypt(msg)
    print("Encrypted:", enc)
    print("Decrypted:", decrypt(enc, k))
