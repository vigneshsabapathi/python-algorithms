"""
Gronsfeld Cipher — a variant of the Vigenère cipher that uses a numeric key.

Each digit d in the key shifts the corresponding plaintext letter by d positions
in the alphabet. Only alphabetic characters are shifted; others are preserved.
The key cycles through the message.

References:
    https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher#Variants
"""

from string import ascii_uppercase


def gronsfeld(text: str, key: str) -> str:
    """
    Encrypt (or decrypt with negative offsets) using the Gronsfeld cipher.

    >>> gronsfeld('hello', '412')
    'LFNPP'
    >>> gronsfeld('hello', '123')
    'IGOMQ'
    >>> gronsfeld('', '123')
    ''
    >>> gronsfeld('yes, ¥€$ - _!@#%?', '0')
    'YES, ¥€$ - _!@#%?'
    >>> gronsfeld('yes, ¥€$ - _!@#%?', '01')
    'YFS, ¥€$ - _!@#%?'
    >>> gronsfeld('yes, ¥€$ - _!@#%?', '012')
    'YFU, ¥€$ - _!@#%?'
    >>> gronsfeld('yes, ¥€$ - _!@#%?', '')
    Traceback (most recent call last):
      ...
    ZeroDivisionError: integer modulo by zero
    """
    ascii_len = len(ascii_uppercase)
    key_len = len(key)
    encrypted_text = ""
    keys = [int(ch) for ch in key]
    upper_text = text.upper()

    for i, char in enumerate(upper_text):
        if char in ascii_uppercase:
            new_pos = (ascii_uppercase.index(char) + keys[i % key_len]) % ascii_len
            encrypted_text += ascii_uppercase[new_pos]
        else:
            encrypted_text += char
    return encrypted_text


if __name__ == "__main__":
    import doctest
    doctest.testmod()
