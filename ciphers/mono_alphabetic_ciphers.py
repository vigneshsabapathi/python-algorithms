"""
Mono-Alphabetic Substitution Cipher
https://en.wikipedia.org/wiki/Substitution_cipher

Each letter in the plaintext is replaced by a corresponding letter in a custom
key alphabet.  Non-alphabetic characters are preserved unchanged.
"""

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def translate_message(key: str, message: str, mode: str) -> str:
    """
    Core translation using key substitution.

    >>> translate_message("QWERTYUIOPASDFGHJKLZXCVBNM", "Hello World", "encrypt")
    'Itssg Vgksr'
    >>> translate_message("QWERTYUIOPASDFGHJKLZXCVBNM", "Itssg Vgksr", "decrypt")
    'Hello World'
    """
    translated = ""
    chars_a = LETTERS
    chars_b = key.upper()

    if mode == "decrypt":
        chars_a, chars_b = chars_b, chars_a

    for symbol in message:
        if symbol.upper() in chars_a:
            idx = chars_a.index(symbol.upper())
            translated += chars_b[idx].upper() if symbol.isupper() else chars_b[idx].lower()
        else:
            translated += symbol
    return translated


def encrypt_message(key: str, message: str) -> str:
    """
    Encrypt message using the substitution key.

    >>> encrypt_message("QWERTYUIOPASDFGHJKLZXCVBNM", "Hello World")
    'Itssg Vgksr'
    """
    return translate_message(key, message, "encrypt")


def decrypt_message(key: str, message: str) -> str:
    """
    Decrypt message using the substitution key.

    >>> decrypt_message("QWERTYUIOPASDFGHJKLZXCVBNM", "Itssg Vgksr")
    'Hello World'
    """
    return translate_message(key, message, "decrypt")


def check_valid_key(key: str) -> bool:
    """
    Validate that key is a permutation of the 26-letter alphabet.

    >>> check_valid_key("QWERTYUIOPASDFGHJKLZXCVBNM")
    True
    >>> check_valid_key("AAAA")
    False
    """
    return sorted(key.upper()) == sorted(LETTERS)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    key = "LFWOAYUISVKMNXPBDCRJTQEGHZ"
    msg = "Hello World"
    enc = encrypt_message(key, msg)
    print("Encrypted:", enc)
    print("Decrypted:", decrypt_message(key, enc))
