"""
Vernam Cipher (repeating-key XOR on alphabet)
==============================================
Each plaintext letter's 0-based index (A=0 … Z=25) is added to the
corresponding key-letter index modulo 26; decryption subtracts.

https://en.wikipedia.org/wiki/Vernam_cipher
"""


def vernam_encrypt(plaintext: str, key: str) -> str:
    """
    Encrypt uppercase *plaintext* with *key* (repeats if shorter).

    >>> vernam_encrypt("HELLO", "KEY")
    'RIJVS'
    >>> vernam_encrypt("A", "A")
    'A'
    >>> vernam_encrypt("Z", "A")
    'Z'
    """
    ciphertext = ""
    for i, ch in enumerate(plaintext):
        ct = (ord(ch) - 65 + ord(key[i % len(key)]) - 65) % 26
        ciphertext += chr(65 + ct)
    return ciphertext


def vernam_decrypt(ciphertext: str, key: str) -> str:
    """
    Decrypt *ciphertext* produced by vernam_encrypt with the same *key*.

    >>> vernam_decrypt("RIJVS", "KEY")
    'HELLO'
    >>> vernam_decrypt("A", "A")
    'A'
    """
    plaintext = ""
    for i, ch in enumerate(ciphertext):
        ct = (ord(ch) - ord(key[i % len(key)])) % 26
        plaintext += chr(65 + ct)
    return plaintext


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    plaintext = "HELLO"
    key = "KEY"
    enc = vernam_encrypt(plaintext, key)
    dec = vernam_decrypt(enc, key)
    print(f"Plaintext : {plaintext}")
    print(f"Encrypted : {enc}")
    print(f"Decrypted : {dec}")
