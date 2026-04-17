"""
Playfair Cipher
https://en.wikipedia.org/wiki/Playfair_cipher

Digraph substitution cipher using a 5x5 key table (I and J share a cell).
"""

import itertools
import string
from collections.abc import Generator, Iterable


def chunker(seq: Iterable[str], size: int) -> Generator[tuple[str, ...], None, None]:
    """Yield successive tuples of *size* from *seq*."""
    it = iter(seq)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            return
        yield chunk


def prepare_input(dirty: str) -> str:
    """
    Upper-case, keep only letters (I=J), and split repeated digraph chars with X.

    >>> prepare_input("Hello")
    'HELXLO'
    >>> prepare_input("balloon")
    'BALXLOXONX'
    """
    dirty = "".join(c.upper() for c in dirty if c in string.ascii_letters)
    clean = ""

    if len(dirty) < 2:
        return dirty

    for i in range(len(dirty) - 1):
        clean += dirty[i]
        if dirty[i] == dirty[i + 1]:
            clean += "X"

    clean += dirty[-1]

    if len(clean) % 2:
        clean += "X"

    return clean


def generate_table(key: str) -> list[str]:
    """
    Build the 25-character Playfair table from *key* (I/J share a slot).

    >>> generate_table("MONARCHY")[:8]
    ['M', 'O', 'N', 'A', 'R', 'C', 'H', 'Y']
    """
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # no J
    table: list[str] = []
    for char in key.upper():
        if char not in table and char in alphabet:
            table.append(char)
    for char in alphabet:
        if char not in table:
            table.append(char)
    return table


def encode(plaintext: str, key: str) -> str:
    """
    Encode plaintext with the Playfair cipher.

    >>> encode("Hello", "MONARCHY")
    'CFSUPM'
    >>> encode("attack on the left flank", "EMERGENCY")
    'DQZSBYFSDZFMFNLOHFDRSG'
    >>> encode("Sorry!", "SPECIAL")
    'AVXETX'
    """
    table = generate_table(key)
    plaintext = prepare_input(plaintext)
    ciphertext = ""

    for char1, char2 in chunker(plaintext, 2):
        row1, col1 = divmod(table.index(char1), 5)
        row2, col2 = divmod(table.index(char2), 5)

        if row1 == row2:
            ciphertext += table[row1 * 5 + (col1 + 1) % 5]
            ciphertext += table[row2 * 5 + (col2 + 1) % 5]
        elif col1 == col2:
            ciphertext += table[((row1 + 1) % 5) * 5 + col1]
            ciphertext += table[((row2 + 1) % 5) * 5 + col2]
        else:
            ciphertext += table[row1 * 5 + col2]
            ciphertext += table[row2 * 5 + col1]

    return ciphertext


def decode(ciphertext: str, key: str) -> str:
    """
    Decode a Playfair-encoded string.

    >>> decode("BMZFAZRZDH", "HAZARD")
    'FIREHAZARD'
    >>> decode("HNBWBPQT", "AUTOMOBILE")
    'DRIVINGX'
    >>> decode("CFSUPM", "MONARCHY")
    'HELXLO'
    """
    table = generate_table(key)
    plaintext = ""

    for char1, char2 in chunker(ciphertext, 2):
        row1, col1 = divmod(table.index(char1), 5)
        row2, col2 = divmod(table.index(char2), 5)

        if row1 == row2:
            plaintext += table[row1 * 5 + (col1 - 1) % 5]
            plaintext += table[row2 * 5 + (col2 - 1) % 5]
        elif col1 == col2:
            plaintext += table[((row1 - 1) % 5) * 5 + col1]
            plaintext += table[((row2 - 1) % 5) * 5 + col2]
        else:
            plaintext += table[row1 * 5 + col2]
            plaintext += table[row2 * 5 + col1]

    return plaintext


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    enc = encode("BYE AND THANKS", "GREETING")
    print("Encoded:", enc)
    print("Decoded:", decode(enc, "GREETING"))
