"""
Polybius Square Cipher

A Polybius square maps each letter to a pair of numbers (row, col) based on
its position in a 5x5 grid. 'J' is mapped to 'I'.

https://www.braingle.com/brainteasers/codes/polybius.php
"""

SQUARE = [
    ["a", "b", "c", "d", "e"],
    ["f", "g", "h", "i", "k"],
    ["l", "m", "n", "o", "p"],
    ["q", "r", "s", "t", "u"],
    ["v", "w", "x", "y", "z"],
]


def letter_to_numbers(letter: str) -> tuple[int, int]:
    """
    Return (row, col) (1-indexed) for the given letter.

    >>> letter_to_numbers('a')
    (1, 1)
    >>> letter_to_numbers('u')
    (4, 5)
    >>> letter_to_numbers('z')
    (5, 5)
    """
    for r, row in enumerate(SQUARE):
        if letter in row:
            return (r + 1, row.index(letter) + 1)
    raise ValueError(f"Letter '{letter}' not found in Polybius square")


def numbers_to_letter(index1: int, index2: int) -> str:
    """
    Return the letter at position [index1, index2] (1-indexed).

    >>> numbers_to_letter(4, 5)
    'u'
    >>> numbers_to_letter(1, 1)
    'a'
    """
    return SQUARE[index1 - 1][index2 - 1]


def encode(message: str) -> str:
    """
    Encode a message using the Polybius square.

    >>> encode("test message")
    '44154344 32154343112215'
    >>> encode("Test Message")
    '44154344 32154343112215'
    """
    message = message.lower().replace("j", "i")
    encoded_message = ""
    for letter in message:
        if letter != " ":
            r, c = letter_to_numbers(letter)
            encoded_message += str(r) + str(c)
        else:
            encoded_message += " "
    return encoded_message


def decode(message: str) -> str:
    """
    Decode a Polybius-encoded message.

    >>> decode("44154344 32154343112215")
    'test message'
    >>> decode("4415434432154343112215")
    'testmessage'
    """
    message = message.replace(" ", "  ")
    decoded_message = ""
    for i in range(len(message) // 2):
        if message[i * 2] != " ":
            r = int(message[i * 2])
            c = int(message[i * 2 + 1])
            decoded_message += numbers_to_letter(r, c)
        else:
            decoded_message += " "
    return decoded_message


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(encode("Hello World"))
    print(decode(encode("hello world")))
