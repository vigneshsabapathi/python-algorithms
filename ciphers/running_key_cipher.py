"""
Running Key Cipher
==================
A variant of the Vigenère cipher where the key is a long passage of text
(e.g., a book excerpt) rather than a short repeating keyword.

https://en.wikipedia.org/wiki/Running_key_cipher
"""


def running_key_encrypt(key: str, plaintext: str) -> str:
    """
    Encrypt *plaintext* using the running key *key*.

    Spaces are stripped and the result is uppercase.

    >>> running_key_encrypt("How does the duck know that? said Victor", "DEFEND THIS")
    'KSBHBHLAPW'
    >>> running_key_encrypt("KEY", "ABC")
    'KFA'
    """
    plaintext = plaintext.replace(" ", "").upper()
    key = key.replace(" ", "").upper()
    key_length = len(key)
    ord_a = ord("A")
    return "".join(
        chr(((ord(ch) - ord_a + ord(key[i % key_length]) - ord_a) % 26) + ord_a)
        for i, ch in enumerate(plaintext)
    )


def running_key_decrypt(key: str, ciphertext: str) -> str:
    """
    Decrypt *ciphertext* using the running key *key*.

    >>> running_key_decrypt("How does the duck know that? said Victor", "KSBHBHLAPW")
    'DEFENDTHIS'
    >>> running_key_decrypt("KEY", "KFA")
    'ABC'
    """
    ciphertext = ciphertext.replace(" ", "").upper()
    key = key.replace(" ", "").upper()
    key_length = len(key)
    ord_a = ord("A")
    return "".join(
        chr(((ord(ch) - ord_a - (ord(key[i % key_length]) - ord_a)) % 26) + ord_a)
        for i, ch in enumerate(ciphertext)
    )


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    key = "How does the duck know that? said Victor"
    plaintext = "DEFEND THIS"
    enc = running_key_encrypt(key, plaintext)
    dec = running_key_decrypt(key, enc)
    print(f"Encrypted: {enc}")
    print(f"Decrypted: {dec}")
