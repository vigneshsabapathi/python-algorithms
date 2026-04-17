"""
Porta Cipher (Bifid-like reciprocal cipher)

Each key letter selects a row from a 26-row, 2-column table. The cipher
swaps a plaintext letter with its counterpart in the other column of the
same row. Both encrypt and decrypt use the same operation (reciprocal).

https://en.wikipedia.org/wiki/Porta_cipher
"""

# Each entry: (top_half_alphabet, bottom_half_shifted)
ALPHABET: dict[str, tuple[str, str]] = {
    "A": ("ABCDEFGHIJKLM", "NOPQRSTUVWXYZ"),
    "B": ("ABCDEFGHIJKLM", "NOPQRSTUVWXYZ"),
    "C": ("ABCDEFGHIJKLM", "ZNOPQRSTUVWXY"),
    "D": ("ABCDEFGHIJKLM", "ZNOPQRSTUVWXY"),
    "E": ("ABCDEFGHIJKLM", "YZNOPQRSTUVWX"),
    "F": ("ABCDEFGHIJKLM", "YZNOPQRSTUVWX"),
    "G": ("ABCDEFGHIJKLM", "XYZNOPQRSTUVW"),
    "H": ("ABCDEFGHIJKLM", "XYZNOPQRSTUVW"),
    "I": ("ABCDEFGHIJKLM", "WXYZNOPQRSTUV"),
    "J": ("ABCDEFGHIJKLM", "WXYZNOPQRSTUV"),
    "K": ("ABCDEFGHIJKLM", "VWXYZNOPQRSTU"),
    "L": ("ABCDEFGHIJKLM", "VWXYZNOPQRSTU"),
    "M": ("ABCDEFGHIJKLM", "UVWXYZNOPQRST"),
    "N": ("ABCDEFGHIJKLM", "UVWXYZNOPQRST"),
    "O": ("ABCDEFGHIJKLM", "TUVWXYZNOPQRS"),
    "P": ("ABCDEFGHIJKLM", "TUVWXYZNOPQRS"),
    "Q": ("ABCDEFGHIJKLM", "STUVWXYZNOPQR"),
    "R": ("ABCDEFGHIJKLM", "STUVWXYZNOPQR"),
    "S": ("ABCDEFGHIJKLM", "RSTUVWXYZNOPQ"),
    "T": ("ABCDEFGHIJKLM", "RSTUVWXYZNOPQ"),
    "U": ("ABCDEFGHIJKLM", "QRSTUVWXYZNOP"),
    "V": ("ABCDEFGHIJKLM", "QRSTUVWXYZNOP"),
    "W": ("ABCDEFGHIJKLM", "PQRSTUVWXYZNO"),
    "X": ("ABCDEFGHIJKLM", "PQRSTUVWXYZNO"),
    "Y": ("ABCDEFGHIJKLM", "OPQRSTUVWXYZN"),
    "Z": ("ABCDEFGHIJKLM", "OPQRSTUVWXYZN"),
}


def generate_table(key: str) -> list[tuple[str, str]]:
    """
    Build the cipher table rows for each character in the key.

    >>> generate_table('marvin')  # doctest: +NORMALIZE_WHITESPACE
    [('ABCDEFGHIJKLM', 'UVWXYZNOPQRST'), ('ABCDEFGHIJKLM', 'NOPQRSTUVWXYZ'),
     ('ABCDEFGHIJKLM', 'STUVWXYZNOPQR'), ('ABCDEFGHIJKLM', 'QRSTUVWXYZNOP'),
     ('ABCDEFGHIJKLM', 'WXYZNOPQRSTUV'), ('ABCDEFGHIJKLM', 'UVWXYZNOPQRST')]
    """
    return [ALPHABET[char] for char in key.upper()]


def get_position(table_row: tuple[str, str], char: str) -> tuple[int, int]:
    """
    Return (row_index, col_index) of char in the table row.
    row_index 0 = top half, 1 = bottom half.

    >>> get_position(generate_table('marvin')[0], 'M')
    (0, 12)
    """
    row = 0 if char in table_row[0] else 1
    col = table_row[row].index(char)
    return row, col


def get_opponent(table_row: tuple[str, str], char: str) -> str:
    """
    Return the character in the opposite half at the same column.

    >>> get_opponent(generate_table('marvin')[0], 'M')
    'T'
    """
    row, col = get_position(table_row, char.upper())
    if row == 1:
        return table_row[0][col]
    return table_row[1][col]


def encrypt(key: str, words: str) -> str:
    """
    Encrypt using the Porta cipher (reciprocal — same as decrypt).

    >>> encrypt('marvin', 'jessica')
    'QRACRWU'
    """
    cipher = ""
    table = generate_table(key)
    for i, char in enumerate(words.upper()):
        cipher += get_opponent(table[i % len(table)], char)
    return cipher


def decrypt(key: str, words: str) -> str:
    """
    Decrypt using the Porta cipher (same operation as encrypt).

    >>> decrypt('marvin', 'QRACRWU')
    'JESSICA'
    """
    return encrypt(key, words)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    key = "marvin"
    text = "jessica"
    enc = encrypt(key, text)
    print(f"Encrypted: {enc}")
    print(f"Decrypted: {decrypt(key, enc)}")
