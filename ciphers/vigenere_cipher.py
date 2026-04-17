"""
Vigenère Cipher
================
A polyalphabetic substitution cipher that applies a Caesar-cipher shift to
each letter using successive letters of a repeating keyword.

https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher
"""

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def translate_message(key: str, message: str, mode: str) -> str:
    """
    Core translation shared by encrypt and decrypt.

    >>> translate_message('HDarji', 'This is Harshil Darji from Dharmaj.', 'encrypt')
    'Akij ra Odrjqqs Gaisq muod Mphumrs.'
    """
    translated: list[str] = []
    key_index = 0
    key = key.upper()
    for symbol in message:
        num = LETTERS.find(symbol.upper())
        if num != -1:
            if mode == "encrypt":
                num += LETTERS.find(key[key_index])
            elif mode == "decrypt":
                num -= LETTERS.find(key[key_index])
            num %= len(LETTERS)
            translated.append(LETTERS[num] if symbol.isupper() else LETTERS[num].lower())
            key_index = (key_index + 1) % len(key)
        else:
            translated.append(symbol)
    return "".join(translated)


def encrypt_message(key: str, message: str) -> str:
    """
    Encrypt *message* with the Vigenère cipher using *key*.

    >>> encrypt_message('HDarji', 'This is Harshil Darji from Dharmaj.')
    'Akij ra Odrjqqs Gaisq muod Mphumrs.'
    >>> encrypt_message('KEY', 'HELLO')
    'RIJVS'
    """
    return translate_message(key, message, "encrypt")


def decrypt_message(key: str, message: str) -> str:
    """
    Decrypt *message* that was encrypted with Vigenère and *key*.

    >>> decrypt_message('HDarji', 'Akij ra Odrjqqs Gaisq muod Mphumrs.')
    'This is Harshil Darji from Dharmaj.'
    >>> decrypt_message('KEY', 'RIJVS')
    'HELLO'
    """
    return translate_message(key, message, "decrypt")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    key = "HDarji"
    msg = "This is Harshil Darji from Dharmaj."
    enc = encrypt_message(key, msg)
    print(f"Encrypted: {enc}")
    print(f"Decrypted: {decrypt_message(key, enc)}")
