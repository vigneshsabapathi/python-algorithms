"""
Fractionated Morse Cipher.

Converts plaintext to Morse code (using 'x' as letter separator), then groups
the Morse characters into trigrams. Each trigram maps to a letter via a
key-derived substitution table, mixing letters across word boundaries.

References:
    http://practicalcryptography.com/ciphers/fractionated-morse-cipher/
"""

import string

MORSE_CODE_DICT: dict[str, str] = {
    "A": ".-",   "B": "-...", "C": "-.-.", "D": "-..",  "E": ".",
    "F": "..-.", "G": "--.",  "H": "....", "I": "..",   "J": ".---",
    "K": "-.-",  "L": ".-..", "M": "--",   "N": "-.",   "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.",  "S": "...",  "T": "-",
    "U": "..-",  "V": "...-", "W": ".--",  "X": "-..-", "Y": "-.--",
    "Z": "--..",  " ": "",
}

# All 27 possible trigrams of {'.', '-', 'x'}
MORSE_COMBINATIONS: list[str] = [
    "...", "..-", "..x", ".-.", ".--", ".-x", ".x.", ".x-", ".xx",
    "-..", "-.-", "-.x", "--.", "---", "--x", "-x.", "-x-", "-xx",
    "x..", "x.-", "x.x", "x-.", "x--", "x-x", "xx.", "xx-", "xxx",
]

REVERSE_MORSE: dict[str, str] = {v: k for k, v in MORSE_CODE_DICT.items()}


def encode_to_morse(plaintext: str) -> str:
    """
    Convert plaintext to Morse code with 'x' as letter separator.

    >>> encode_to_morse("defend the east")
    '-..x.x..-.x.x-.x-..xx-x....x.xx.x.-x...x-'
    """
    return "x".join(MORSE_CODE_DICT.get(ch.upper(), "") for ch in plaintext)


def encrypt_fractionated_morse(plaintext: str, key: str) -> str:
    """
    Encrypt plaintext using the Fractionated Morse Cipher.

    >>> encrypt_fractionated_morse("defend the east", "Roundtable")
    'ESOAVVLJRSSTRX'
    """
    morse_code = encode_to_morse(plaintext)
    key = key.upper() + string.ascii_uppercase
    key = "".join(sorted(set(key), key=key.find))

    # Pad Morse code to a multiple of 3 with 'x'
    padding_length = (-len(morse_code)) % 3
    morse_code += "x" * padding_length

    trigram_to_letter = {v: k for k, v in zip(key, MORSE_COMBINATIONS)}
    trigram_to_letter["xxx"] = ""

    encrypted = "".join(
        trigram_to_letter[morse_code[i : i + 3]]
        for i in range(0, len(morse_code), 3)
    )
    return encrypted


def decrypt_fractionated_morse(ciphertext: str, key: str) -> str:
    """
    Decrypt a Fractionated Morse Cipher ciphertext.

    >>> decrypt_fractionated_morse("ESOAVVLJRSSTRX", "Roundtable")
    'DEFEND THE EAST'
    """
    key = key.upper() + string.ascii_uppercase
    key = "".join(sorted(set(key), key=key.find))

    letter_to_trigram = dict(zip(key, MORSE_COMBINATIONS))
    morse_code = "".join(letter_to_trigram.get(ch, "") for ch in ciphertext)
    decrypted = "".join(
        REVERSE_MORSE[code] for code in morse_code.split("x")
    ).strip()
    return decrypted


if __name__ == "__main__":
    import doctest
    doctest.testmod()
