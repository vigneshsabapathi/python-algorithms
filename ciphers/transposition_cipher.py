"""
Transposition (Columnar) Cipher
=================================
Writes the plaintext column-by-column into *key* columns, then reads across
each column to produce the ciphertext.

https://en.wikipedia.org/wiki/Transposition_cipher
"""

import math


def encrypt_message(key: int, message: str) -> str:
    """
    Encrypt *message* by distributing characters across *key* columns.

    >>> encrypt_message(6, 'Harshil Darji')
    'Hlia rDsahrij'
    >>> encrypt_message(3, 'HELLO')
    'HLEOL'
    """
    cipher_text = [""] * key
    for col in range(key):
        pointer = col
        while pointer < len(message):
            cipher_text[col] += message[pointer]
            pointer += key
    return "".join(cipher_text)


def decrypt_message(key: int, message: str) -> str:
    """
    Decrypt a message that was encrypted with *key* columns.

    >>> decrypt_message(6, 'Hlia rDsahrij')
    'Harshil Darji'
    >>> decrypt_message(3, 'HLEOL')
    'HELLO'
    """
    num_cols = math.ceil(len(message) / key)
    num_rows = key
    num_shaded_boxes = (num_cols * num_rows) - len(message)
    plain_text = [""] * num_cols
    col = 0
    row = 0
    for symbol in message:
        plain_text[col] += symbol
        col += 1
        if (col == num_cols) or (
            col == num_cols - 1 and row >= num_rows - num_shaded_boxes
        ):
            col = 0
            row += 1
    return "".join(plain_text)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    key = 6
    msg = "Harshil Darji"
    enc = encrypt_message(key, msg)
    print(f"Encrypted: {enc}")
    print(f"Decrypted: {decrypt_message(key, enc)}")
