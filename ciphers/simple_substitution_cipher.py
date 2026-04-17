"""
Simple Substitution Cipher
============================
A monoalphabetic cipher where each letter is replaced by the corresponding
letter in a 26-character key string.

https://en.wikipedia.org/wiki/Substitution_cipher
"""

import random

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def check_valid_key(key: str) -> None:
    """
    Raise SystemExit if *key* is not a valid permutation of the 26 letters.

    >>> check_valid_key("LFWOAYUISVKMNXPBDCRJTQEGHZ")
    >>> check_valid_key("AAAA")
    Traceback (most recent call last):
        ...
    SystemExit: Error in the key or symbol set.
    """
    import sys

    if sorted(key.upper()) != sorted(LETTERS):
        sys.exit("Error in the key or symbol set.")


def translate_message(key: str, message: str, mode: str) -> str:
    """
    Core translation used by both encrypt and decrypt.

    >>> translate_message("LFWOAYUISVKMNXPBDCRJTQEGHZ", "Harshil Darji", "encrypt")
    'Ilcrism Olcvs'
    """
    translated = ""
    chars_a = LETTERS
    chars_b = key
    if mode == "decrypt":
        chars_a, chars_b = chars_b, chars_a
    for symbol in message:
        if symbol.upper() in chars_a:
            sym_index = chars_a.find(symbol.upper())
            if symbol.isupper():
                translated += chars_b[sym_index].upper()
            else:
                translated += chars_b[sym_index].lower()
        else:
            translated += symbol
    return translated


def encrypt_message(key: str, message: str) -> str:
    """
    Encrypt *message* using the substitution *key*.

    >>> encrypt_message('LFWOAYUISVKMNXPBDCRJTQEGHZ', 'Harshil Darji')
    'Ilcrism Olcvs'
    """
    return translate_message(key, message, "encrypt")


def decrypt_message(key: str, message: str) -> str:
    """
    Decrypt *message* using the substitution *key*.

    >>> decrypt_message('LFWOAYUISVKMNXPBDCRJTQEGHZ', 'Ilcrism Olcvs')
    'Harshil Darji'
    """
    return translate_message(key, message, "decrypt")


def get_random_key() -> str:
    """
    Return a random valid 26-letter key.

    >>> len(get_random_key()) == 26
    True
    """
    key = list(LETTERS)
    random.shuffle(key)
    return "".join(key)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    key = "LFWOAYUISVKMNXPBDCRJTQEGHZ"
    msg = "Harshil Darji"
    enc = encrypt_message(key, msg)
    print(f"Encrypted: {enc}")
    print(f"Decrypted: {decrypt_message(key, enc)}")
