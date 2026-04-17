"""
Shuffled Shift Cipher
======================
A Caesar-cipher variant that shuffles the reference character list using
unique characters from a passcode as pivot points, then computes a numeric
shift from the passcode's alternating-sign ASCII sum.

Brute-force is made impractical: 97 printable characters yield 97! possible
shuffled lists, and each has 26 possible shift offsets.
"""

from __future__ import annotations

import random
import string


class ShuffledShiftCipher:
    """
    >>> ssc = ShuffledShiftCipher('4PYIXyqeQZr44')
    >>> ssc.encrypt('Hello, this is a modified Caesar cipher')
    "d>**-1z6&'5z'5z:z+-='$'>=zp:>5:#z<'.&>#"
    >>> ssc.decrypt("d>**-1z6&'5z'5z:z+-='$'>=zp:>5:#z<'.&>#")
    'Hello, this is a modified Caesar cipher'
    """

    def __init__(self, passcode: str | None = None) -> None:
        self.__passcode = passcode or self.__passcode_creator()
        self.__key_list = self.__make_key_list()
        self.__shift_key = self.__make_shift_key()

    def __str__(self) -> str:
        return "".join(self.__passcode)

    def __neg_pos(self, iterlist: list[int]) -> list[int]:
        for i in range(1, len(iterlist), 2):
            iterlist[i] *= -1
        return iterlist

    def __passcode_creator(self) -> list[str]:
        choices = string.ascii_letters + string.digits
        return [random.choice(choices) for _ in range(random.randint(10, 20))]

    def __make_key_list(self) -> list[str]:
        key_list_options = (
            string.ascii_letters + string.digits + string.punctuation + " \t\n"
        )
        keys_l: list[str] = []
        breakpoints = sorted(set(self.__passcode))
        temp_list: list[str] = []
        for i in key_list_options:
            temp_list.append(i)
            if i in breakpoints or i == key_list_options[-1]:
                keys_l.extend(temp_list[::-1])
                temp_list.clear()
        return keys_l

    def __make_shift_key(self) -> int:
        num = sum(self.__neg_pos([ord(x) for x in self.__passcode]))
        return num if num > 0 else len(self.__passcode)

    def encrypt(self, plaintext: str) -> str:
        """
        Shift each character forward in the shuffled key list.

        >>> ssc = ShuffledShiftCipher('4PYIXyqeQZr44')
        >>> ssc.encrypt('Hello, this is a modified Caesar cipher')
        "d>**-1z6&'5z'5z:z+-='$'>=zp:>5:#z<'.&>#"
        """
        encoded_message = ""
        for i in plaintext:
            position = self.__key_list.index(i)
            encoded_message += self.__key_list[
                (position + self.__shift_key) % len(self.__key_list)
            ]
        return encoded_message

    def decrypt(self, encoded_message: str) -> str:
        """
        Shift each character backward in the shuffled key list.

        >>> ssc = ShuffledShiftCipher('4PYIXyqeQZr44')
        >>> ssc.decrypt("d>**-1z6&'5z'5z:z+-='$'>=zp:>5:#z<'.&>#")
        'Hello, this is a modified Caesar cipher'
        """
        decoded_message = ""
        for i in encoded_message:
            position = self.__key_list.index(i)
            decoded_message += self.__key_list[
                (position - self.__shift_key) % -len(self.__key_list)
            ]
        return decoded_message


def test_end_to_end(msg: str = "Hello, this is a modified Caesar cipher") -> str:
    """
    >>> test_end_to_end()
    'Hello, this is a modified Caesar cipher'
    """
    cip1 = ShuffledShiftCipher()
    return cip1.decrypt(cip1.encrypt(msg))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(test_end_to_end())
