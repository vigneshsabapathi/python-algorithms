"""
XOR Cipher
===========
XORs each character's ASCII value with an integer key (0-255).
Since XOR is self-inverse, the same operation encrypts and decrypts.

https://en.wikipedia.org/wiki/XOR_cipher
"""

from __future__ import annotations


class XORCipher:
    """
    XOR cipher operating on strings.

    >>> XORCipher().encrypt_string("hallo welt", 1)
    'i`mmn!vdmu'
    >>> XORCipher().decrypt_string("i`mmn!vdmu", 1)
    'hallo welt'
    """

    def __init__(self, key: int = 0) -> None:
        self.__key = key

    def encrypt(self, content: str, key: int) -> list[str]:
        """
        Return encrypted *content* as a list of characters.

        >>> XORCipher().encrypt("", 5)
        []
        >>> XORCipher().encrypt("hallo welt", 1)
        ['i', '`', 'm', 'm', 'n', '!', 'v', 'd', 'm', 'u']
        >>> XORCipher().encrypt("HALLO WELT", 32)
        ['h', 'a', 'l', 'l', 'o', '\\x00', 'w', 'e', 'l', 't']
        >>> XORCipher().encrypt("hallo welt", 256)
        ['h', 'a', 'l', 'l', 'o', ' ', 'w', 'e', 'l', 't']
        """
        assert isinstance(key, int)
        assert isinstance(content, str)
        key = (key or self.__key or 1) % 256
        return [chr(ord(ch) ^ key) for ch in content]

    def decrypt(self, content: str, key: int) -> list[str]:
        """
        Return decrypted *content* as a list of characters (identical to encrypt).

        >>> XORCipher().decrypt("", 5)
        []
        >>> XORCipher().decrypt("hallo welt", 1)
        ['i', '`', 'm', 'm', 'n', '!', 'v', 'd', 'm', 'u']
        >>> XORCipher().decrypt("HALLO WELT", 32)
        ['h', 'a', 'l', 'l', 'o', '\\x00', 'w', 'e', 'l', 't']
        >>> XORCipher().decrypt("hallo welt", 256)
        ['h', 'a', 'l', 'l', 'o', ' ', 'w', 'e', 'l', 't']
        """
        assert isinstance(key, int)
        assert isinstance(content, str)
        key = (key or self.__key or 1) % 256
        return [chr(ord(ch) ^ key) for ch in content]

    def encrypt_string(self, content: str, key: int = 0) -> str:
        """
        Return encrypted *content* as a string.

        >>> XORCipher().encrypt_string("", 5)
        ''
        >>> XORCipher().encrypt_string("hallo welt", 1)
        'i`mmn!vdmu'
        >>> XORCipher().encrypt_string("HALLO WELT", 32)
        'hallo\\x00welt'
        >>> XORCipher().encrypt_string("hallo welt", 256)
        'hallo welt'
        """
        assert isinstance(key, int)
        assert isinstance(content, str)
        key = (key or self.__key or 1) % 256
        return "".join(chr(ord(ch) ^ key) for ch in content)

    def decrypt_string(self, content: str, key: int = 0) -> str:
        """
        Return decrypted *content* as a string (identical to encrypt_string).

        >>> XORCipher().decrypt_string("", 5)
        ''
        >>> XORCipher().decrypt_string("hallo welt", 1)
        'i`mmn!vdmu'
        >>> XORCipher().decrypt_string("HALLO WELT", 32)
        'hallo\\x00welt'
        >>> XORCipher().decrypt_string("hallo welt", 256)
        'hallo welt'
        """
        assert isinstance(key, int)
        assert isinstance(content, str)
        key = (key or self.__key or 1) % 256
        return "".join(chr(ord(ch) ^ key) for ch in content)

    def encrypt_file(self, file: str, key: int = 0) -> bool:
        """Encrypt file contents and write to encrypt.out. Returns True on success."""
        assert isinstance(file, str)
        assert isinstance(key, int)
        key %= 256
        try:
            with open(file) as fin, open("encrypt.out", "w+") as fout:
                for line in fin:
                    fout.write(self.encrypt_string(line, key))
        except OSError:
            return False
        return True

    def decrypt_file(self, file: str, key: int) -> bool:
        """Decrypt file contents and write to decrypt.out. Returns True on success."""
        assert isinstance(file, str)
        assert isinstance(key, int)
        key %= 256
        try:
            with open(file) as fin, open("decrypt.out", "w+") as fout:
                for line in fin:
                    fout.write(self.decrypt_string(line, key))
        except OSError:
            return False
        return True


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    cipher = XORCipher()
    enc = cipher.encrypt_string("Hello, World!", 42)
    print(f"Encrypted: {enc}")
    print(f"Decrypted: {cipher.decrypt_string(enc, 42)}")
