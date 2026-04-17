"""
One-Time Pad Cipher (pseudo-random variant)
https://en.wikipedia.org/wiki/One-time_pad

Each character is encrypted with a unique random key value.
Decryption requires the same key list used during encryption.
"""

import random


class Onepad:
    @staticmethod
    def encrypt(text: str) -> tuple[list[int], list[int]]:
        """
        Encrypt text, returning (ciphertext_list, key_list).

        >>> Onepad().encrypt("")
        ([], [])
        >>> Onepad().encrypt([])
        ([], [])
        >>> random.seed(1)
        >>> Onepad().encrypt(" ")
        ([6969], [69])
        >>> random.seed(1)
        >>> Onepad().encrypt("Hello")
        ([9729, 114756, 4653, 31309, 10492], [69, 292, 33, 131, 61])
        >>> Onepad().encrypt(1)
        Traceback (most recent call last):
            ...
        TypeError: 'int' object is not iterable
        """
        plain = [ord(c) for c in text]
        key: list[int] = []
        cipher: list[int] = []
        for p in plain:
            k = random.randint(1, 300)
            cipher.append((p + k) * k)
            key.append(k)
        return cipher, key

    @staticmethod
    def decrypt(cipher: list[int], key: list[int]) -> str:
        """
        Decrypt ciphertext using the key list.

        >>> Onepad().decrypt([], [])
        ''
        >>> Onepad().decrypt([35], [])
        ''
        >>> Onepad().decrypt([], [35])
        Traceback (most recent call last):
            ...
        IndexError: list index out of range
        >>> random.seed(1)
        >>> Onepad().decrypt([9729, 114756, 4653, 31309, 10492], [69, 292, 33, 131, 61])
        'Hello'
        """
        return "".join(
            chr(int((cipher[i] - key[i] ** 2) / key[i])) for i in range(len(key))
        )


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    c, k = Onepad().encrypt("Hello")
    print("Cipher:", c)
    print("Key:   ", k)
    print("Plain: ", Onepad().decrypt(c, k))
