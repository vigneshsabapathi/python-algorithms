"""
Trifid Cipher
=============
A fractionating transposition cipher: each letter maps to a 3-digit trigram;
trigrams within each period are arranged vertically then read horizontally;
the resulting sequence is decoded back to letters.

https://en.wikipedia.org/wiki/Trifid_cipher
"""

from __future__ import annotations

# fmt: off
TEST_CHARACTER_TO_NUMBER = {
    "A": "111", "B": "112", "C": "113", "D": "121", "E": "122", "F": "123", "G": "131",
    "H": "132", "I": "133", "J": "211", "K": "212", "L": "213", "M": "221", "N": "222",
    "O": "223", "P": "231", "Q": "232", "R": "233", "S": "311", "T": "312", "U": "313",
    "V": "321", "W": "322", "X": "323", "Y": "331", "Z": "332", "+": "333",
}
# fmt: on

TEST_NUMBER_TO_CHARACTER = {val: key for key, val in TEST_CHARACTER_TO_NUMBER.items()}


def _encrypt_part(message_part: str, character_to_number: dict[str, str]) -> str:
    """
    Arrange trigram values of each letter vertically, then join horizontally.

    >>> _encrypt_part('ASK', TEST_CHARACTER_TO_NUMBER)
    '132111112'
    """
    one, two, three = "", "", ""
    for each in (character_to_number[c] for c in message_part):
        one += each[0]
        two += each[1]
        three += each[2]
    return one + two + three


def _decrypt_part(
    message_part: str, character_to_number: dict[str, str]
) -> tuple[str, str, str]:
    """
    Convert letters to trigrams, join, split into three equal groups.

    >>> _decrypt_part('ABCDE', TEST_CHARACTER_TO_NUMBER)
    ('11111', '21131', '21122')
    """
    joined = "".join(character_to_number[c] for c in message_part)
    size = len(message_part)
    result = [joined[i * size : (i + 1) * size] for i in range(3)]
    return result[0], result[1], result[2]


def _prepare(
    message: str, alphabet: str
) -> tuple[str, str, dict[str, str], dict[str, str]]:
    """
    Validate and prepare message and alphabet; return conversion dicts.

    >>> test = _prepare('I aM a BOy','abCdeFghijkLmnopqrStuVwxYZ+')
    >>> expected = ('IAMABOY', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ+',
    ...             TEST_CHARACTER_TO_NUMBER, TEST_NUMBER_TO_CHARACTER)
    >>> test == expected
    True

    >>> _prepare('I aM a BOy','abCdeFghijkLmnopqrStuVw')
    Traceback (most recent call last):
        ...
    KeyError: 'Length of alphabet has to be 27.'

    >>> _prepare('am i a boy?','abCdeFghijkLmnopqrStuVwxYZ+')
    Traceback (most recent call last):
        ...
    ValueError: Each message character has to be included in alphabet!

    >>> _prepare(500,'abCdeFghijkLmnopqrStuVwxYZ+')
    Traceback (most recent call last):
        ...
    AttributeError: 'int' object has no attribute 'replace'
    """
    alphabet = alphabet.replace(" ", "").upper()
    message = message.replace(" ", "").upper()
    if len(alphabet) != 27:
        raise KeyError("Length of alphabet has to be 27.")
    if any(c not in alphabet for c in message):
        raise ValueError("Each message character has to be included in alphabet!")
    character_to_number = dict(zip(alphabet, TEST_CHARACTER_TO_NUMBER.values()))
    number_to_character = {v: k for k, v in character_to_number.items()}
    return message, alphabet, character_to_number, number_to_character


def encrypt_message(
    message: str,
    alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ.",
    period: int = 5,
) -> str:
    """
    Encrypt *message* using the Trifid cipher.

    >>> encrypt_message('I am a boy')
    'BCDGBQY'
    >>> encrypt_message(' ')
    ''
    >>> encrypt_message('   aide toi le c  iel      ta id  era    ',
    ...     'FELIXMARDSTBCGHJKNOPQUVWYZ+', 5)
    'FMJFVOISSUFTFPUFEQQC'
    """
    message, alphabet, character_to_number, number_to_character = _prepare(
        message, alphabet
    )
    encrypted_numeric = ""
    for i in range(0, len(message) + 1, period):
        encrypted_numeric += _encrypt_part(message[i : i + period], character_to_number)
    encrypted = ""
    for i in range(0, len(encrypted_numeric), 3):
        encrypted += number_to_character[encrypted_numeric[i : i + 3]]
    return encrypted


def decrypt_message(
    message: str,
    alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ.",
    period: int = 5,
) -> str:
    """
    Decrypt a Trifid-encrypted *message*.

    >>> decrypt_message('BCDGBQY')
    'IAMABOY'
    >>> decrypt_message('FMJFVOISSUFTFPUFEQQC', 'FELIXMARDSTBCGHJKNOPQUVWYZ+', 5)
    'AIDETOILECIELTAIDERA'
    """
    message, alphabet, character_to_number, number_to_character = _prepare(
        message, alphabet
    )
    decrypted_numeric: list[str] = []
    for i in range(0, len(message), period):
        a, b, c = _decrypt_part(message[i : i + period], character_to_number)
        for j in range(len(a)):
            decrypted_numeric.append(a[j] + b[j] + c[j])
    return "".join(number_to_character[each] for each in decrypted_numeric)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    msg = "DEFEND THE EAST WALL OF THE CASTLE."
    key_alpha = "EPSDUCVWYM.ZLKXNBTFGORIJHAQ"
    enc = encrypt_message(msg, key_alpha)
    dec = decrypt_message(enc, key_alpha)
    print(f"Encrypted: {enc}")
    print(f"Decrypted: {dec}")
