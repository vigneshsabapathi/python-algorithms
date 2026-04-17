"""
Hill Cipher — a polygraphic substitution cipher using linear algebra.

Encrypts blocks of text by multiplying a numerical vector (derived from the
plaintext) by an NxN key matrix mod 36 (A-Z + 0-9). Decryption uses the
modular inverse of the key matrix.

Constraint: gcd(det(key_matrix), 36) must equal 1.

References:
    https://en.wikipedia.org/wiki/Hill_cipher
"""

import string
from math import gcd

import numpy as np


class HillCipher:
    """
    Hill Cipher implementation over a 36-character alphabet (A-Z, 0-9).

    >>> import numpy as np
    >>> key = np.array([[2, 5], [1, 6]])
    >>> hc = HillCipher(key)
    >>> hc.encrypt("hello world")
    '85FF4CFIB3'
    >>> hc.decrypt(hc.encrypt("hello world"))
    'HELLOWORLD'
    """

    key_string = string.ascii_uppercase + string.digits
    modulus = np.vectorize(lambda x: x % 36)
    to_int = np.vectorize(round)

    def __init__(self, encrypt_key: np.ndarray) -> None:
        self.encrypt_key = self.modulus(encrypt_key)
        self.check_determinant()
        self.break_key = encrypt_key.shape[0]

    def replace_letters(self, letter: str) -> int:
        return self.key_string.index(letter)

    def replace_digits(self, num: int) -> str:
        return self.key_string[int(num)]

    def check_determinant(self) -> None:
        """Raise ValueError if the key matrix determinant is not coprime with 36."""
        det = round(np.linalg.det(self.encrypt_key))
        if det < 0:
            det = det % len(self.key_string)
        if gcd(det, len(self.key_string)) != 1:
            raise ValueError(
                f"determinant modular {len(self.key_string)} of encryption key ({det}) "
                f"is not coprime w.r.t {len(self.key_string)}. Try another key."
            )

    def process_text(self, text: str) -> str:
        """
        Filter to alphanumeric chars and pad to a multiple of break_key.

        >>> import numpy as np
        >>> key = np.array([[2, 5], [1, 6]])
        >>> HillCipher(key).process_text("Hello World!")
        'HELLOWORLD'
        """
        chars = [ch for ch in text.upper() if ch in self.key_string]
        last = chars[-1]
        while len(chars) % self.break_key != 0:
            chars.append(last)
        return "".join(chars)

    def encrypt(self, text: str) -> str:
        """
        Encrypt text using the Hill cipher key matrix.

        >>> import numpy as np
        >>> key = np.array([[2, 5], [1, 6]])
        >>> HillCipher(key).encrypt("hello world")
        '85FF4CFIB3'
        """
        text = self.process_text(text.upper())
        encrypted = ""
        for i in range(0, len(text) - self.break_key + 1, self.break_key):
            batch = text[i : i + self.break_key]
            vec = np.array([[self.replace_letters(ch)] for ch in batch])
            result = self.modulus(self.encrypt_key.dot(vec)).T.tolist()[0]
            encrypted += "".join(self.replace_digits(num) for num in result)
        return encrypted

    def make_decrypt_key(self) -> np.ndarray:
        """Compute the modular inverse of the encryption key matrix."""
        det = round(np.linalg.det(self.encrypt_key))
        if det < 0:
            det = det % len(self.key_string)
        det_inv = None
        for i in range(len(self.key_string)):
            if (det * i) % len(self.key_string) == 1:
                det_inv = i
                break
        inv_key = (
            det_inv
            * np.linalg.det(self.encrypt_key)
            * np.linalg.inv(self.encrypt_key)
        )
        return self.to_int(self.modulus(inv_key))

    def decrypt(self, text: str) -> str:
        """
        Decrypt Hill-cipher text using the inverse key matrix.

        >>> import numpy as np
        >>> key = np.array([[2, 5], [1, 6]])
        >>> HillCipher(key).decrypt('85FF4CFIB3')
        'HELLOWORLD'
        """
        decrypt_key = self.make_decrypt_key()
        text = self.process_text(text.upper())
        decrypted = ""
        for i in range(0, len(text) - self.break_key + 1, self.break_key):
            batch = text[i : i + self.break_key]
            vec = np.array([[self.replace_letters(ch)] for ch in batch])
            result = self.modulus(decrypt_key.dot(vec)).T.tolist()[0]
            decrypted += "".join(self.replace_digits(num) for num in result)
        return decrypted


if __name__ == "__main__":
    import doctest
    doctest.testmod()
