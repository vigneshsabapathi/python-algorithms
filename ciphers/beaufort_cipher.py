"""
Beaufort Cipher — a reciprocal polyalphabetic substitution cipher.

Encryption: C[i] = (key[i] - P[i]) mod 26
Decryption: same operation (the cipher is its own inverse).

Unlike Vigenère where E(x) = (P + K) mod 26, Beaufort uses (K - P) mod 26,
making it self-reciprocal (encrypting ciphertext with the same key recovers
the plaintext).

References:
    https://en.wikipedia.org/wiki/Beaufort_cipher
"""

from string import ascii_uppercase

# Build forward and reverse lookup tables
DICT1 = {char: i for i, char in enumerate(ascii_uppercase)}
DICT2 = dict(enumerate(ascii_uppercase))


def generate_key(message: str, key: str) -> str:
    """
    Repeat/trim the key cyclically to match the length of the message
    (spaces in the message are excluded from key alignment).

    >>> generate_key("THE GERMAN ATTACK", "SECRET")
    'SECRETSECRETSECRE'
    """
    x = len(message)
    i = 0
    while True:
        if x == i:
            i = 0
        if len(key) == len(message):
            break
        key += key[i]
        i += 1
    return key


def cipher_text(message: str, key_new: str) -> str:
    """
    Encrypt message: each letter shifted by (plaintext - key) mod 26.

    >>> cipher_text("THE GERMAN ATTACK", "SECRETSECRETSECRE")
    'BDC PAYUWL JPAIYI'
    """
    result = ""
    i = 0
    for letter in message:
        if letter == " ":
            result += " "
        else:
            x = (DICT1[letter] - DICT1[key_new[i]]) % 26
            i += 1
            result += DICT2[x]
    return result


def original_text(cipher: str, key_new: str) -> str:
    """
    Decrypt: shift each letter by (key + cipher) mod 26.

    >>> original_text("BDC PAYUWL JPAIYI", "SECRETSECRETSECRE")
    'THE GERMAN ATTACK'
    """
    or_txt = ""
    i = 0
    for letter in cipher:
        if letter == " ":
            or_txt += " "
        else:
            x = (DICT1[letter] + DICT1[key_new[i]] + 26) % 26
            i += 1
            or_txt += DICT2[x]
    return or_txt


if __name__ == "__main__":
    import doctest
    doctest.testmod()
