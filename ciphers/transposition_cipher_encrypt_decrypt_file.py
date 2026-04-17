"""
Transposition Cipher — File Encrypt/Decrypt
=============================================
Applies the columnar transposition cipher to the contents of a file.
This module exposes the core logic as plain functions; actual file I/O
is wrapped so it can be skipped in tests.

https://en.wikipedia.org/wiki/Transposition_cipher
"""

import math
import time


# ---------------------------------------------------------------------------
# Pure transposition logic (duplicated here so the module is self-contained)
# ---------------------------------------------------------------------------

def encrypt_message(key: int, message: str) -> str:
    """
    Encrypt *message* using columnar transposition with *key* columns.

    >>> encrypt_message(6, 'Harshil Darji')
    'Hlia rDsahrij'
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
    Decrypt a columnar-transposition ciphertext back to plaintext.

    >>> decrypt_message(6, 'Hlia rDsahrij')
    'Harshil Darji'
    """
    num_cols = math.ceil(len(message) / key)
    num_rows = key
    num_shaded = (num_cols * num_rows) - len(message)
    plain_text = [""] * num_cols
    col = row = 0
    for symbol in message:
        plain_text[col] += symbol
        col += 1
        if col == num_cols or (col == num_cols - 1 and row >= num_rows - num_shaded):
            col = 0
            row += 1
    return "".join(plain_text)


# ---------------------------------------------------------------------------
# File-level wrappers (file I/O doctests are skipped per project convention)
# ---------------------------------------------------------------------------

def encrypt_file(input_path: str, output_path: str, key: int) -> float:
    """
    Read *input_path*, encrypt its content, write to *output_path*.

    Returns elapsed seconds.

    >>> encrypt_file("missing.txt", "out.txt", 5)  # doctest: +SKIP
    """
    start = time.time()
    with open(input_path) as f:
        content = f.read()
    translated = encrypt_message(key, content)
    with open(output_path, "w") as f:
        f.write(translated)
    return round(time.time() - start, 4)


def decrypt_file(input_path: str, output_path: str, key: int) -> float:
    """
    Read *input_path*, decrypt its content, write to *output_path*.

    Returns elapsed seconds.

    >>> decrypt_file("missing.txt", "out.txt", 5)  # doctest: +SKIP
    """
    start = time.time()
    with open(input_path) as f:
        content = f.read()
    translated = decrypt_message(key, content)
    with open(output_path, "w") as f:
        f.write(translated)
    return round(time.time() - start, 4)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    # Demo without actual files
    key = 6
    msg = "Prehistoric men lived in caves and hunted mammoths."
    enc = encrypt_message(key, msg)
    dec = decrypt_message(key, enc)
    print(f"Encrypted: {enc}")
    print(f"Decrypted: {dec}")
