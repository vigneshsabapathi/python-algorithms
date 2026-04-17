"""
Bifid Cipher — a fractionating transposition cipher using a 5x5 Polybius square.

The letter 'j' is merged with 'i'. Encryption splits each letter's row/column
coordinates, concatenates all rows then all columns, and recombines into pairs.

References:
    https://en.wikipedia.org/wiki/Bifid_cipher
    https://www.braingle.com/brainteasers/codes/bifid.php
"""

import numpy as np

SQUARE = [
    ["a", "b", "c", "d", "e"],
    ["f", "g", "h", "i", "k"],
    ["l", "m", "n", "o", "p"],
    ["q", "r", "s", "t", "u"],
    ["v", "w", "x", "y", "z"],
]


class BifidCipher:
    def __init__(self) -> None:
        self.SQUARE = np.array(SQUARE)

    def letter_to_numbers(self, letter: str) -> np.ndarray:
        """
        Return the (row, col) pair for a letter in the Polybius square.

        >>> np.array_equal(BifidCipher().letter_to_numbers('a'), [1, 1])
        True
        >>> np.array_equal(BifidCipher().letter_to_numbers('u'), [4, 5])
        True
        """
        index1, index2 = np.where(letter == self.SQUARE)
        return np.concatenate([index1 + 1, index2 + 1])

    def numbers_to_letter(self, index1: int, index2: int) -> str:
        """
        Return the letter at position (index1, index2) in the Polybius square.

        >>> BifidCipher().numbers_to_letter(4, 5) == 'u'
        True
        >>> BifidCipher().numbers_to_letter(1, 1) == 'a'
        True
        """
        return self.SQUARE[index1 - 1, index2 - 1]

    def encode(self, message: str) -> str:
        """
        Encode a message using the Bifid cipher.

        >>> BifidCipher().encode('testmessage') == 'qtltbdxrxlk'
        True
        >>> BifidCipher().encode('Test Message') == 'qtltbdxrxlk'
        True
        >>> BifidCipher().encode('test j') == BifidCipher().encode('test i')
        True
        """
        message = message.lower().replace(" ", "").replace("j", "i")

        first_step = np.empty((2, len(message)))
        for idx, letter in enumerate(message):
            numbers = self.letter_to_numbers(letter)
            first_step[0, idx] = numbers[0]
            first_step[1, idx] = numbers[1]

        second_step = first_step.reshape(2 * len(message))
        encoded_message = ""
        for i in range(len(message)):
            index1 = int(second_step[i * 2])
            index2 = int(second_step[i * 2 + 1])
            encoded_message += self.numbers_to_letter(index1, index2)
        return encoded_message

    def decode(self, message: str) -> str:
        """
        Decode a Bifid-encoded message.

        >>> BifidCipher().decode('qtltbdxrxlk') == 'testmessage'
        True
        """
        message = message.lower().replace(" ", "")
        first_step = np.empty(2 * len(message))
        for idx, letter in enumerate(message):
            numbers = self.letter_to_numbers(letter)
            first_step[idx * 2] = numbers[0]
            first_step[idx * 2 + 1] = numbers[1]

        second_step = first_step.reshape((2, len(message)))
        decoded_message = ""
        for i in range(len(message)):
            index1 = int(second_step[0, i])
            index2 = int(second_step[1, i])
            decoded_message += self.numbers_to_letter(index1, index2)
        return decoded_message


if __name__ == "__main__":
    import doctest
    doctest.testmod()
