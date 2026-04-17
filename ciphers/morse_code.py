"""
Morse Code Cipher
https://en.wikipedia.org/wiki/Morse_code

Encodes text to Morse code dots/dashes and decodes back.
"""

# fmt: off
MORSE_CODE_DICT = {
    "A": ".-",   "B": "-...", "C": "-.-.", "D": "-..",  "E": ".",    "F": "..-.",
    "G": "--.",  "H": "....", "I": "..",   "J": ".---", "K": "-.-",  "L": ".-..",
    "M": "--",   "N": "-.",   "O": "---",  "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...",  "T": "-",    "U": "..-",  "V": "...-", "W": ".--",  "X": "-..-",
    "Y": "-.--", "Z": "--..", "1": ".----","2": "..---","3": "...--","4": "....-",
    "5": ".....","6": "-.....","7": "--...","8": "---..", "9": "----.", "0": "-----",
    "&": ".-...", "@": ".--.-.", ":": "---...", ",": "--..--", ".": ".-.-.-",
    "'": ".----.", '"': ".-..-.", "?": "..--..", "/": "-..-.", "=": "-...-",
    "+": ".-.-.", "-": "-....-", "(": "-.--.", ")": "-.--.-", "!": "-.-.--",
    " ": "/",
}
# fmt: on

REVERSE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}


def encrypt(message: str) -> str:
    """
    Encode a text message into Morse code.

    >>> encrypt("Sos!")
    '... --- ... -.-.--'
    >>> encrypt("SOS!") == encrypt("sos!")
    True
    >>> encrypt("Hello")
    '.... . .-.. .-.. ---'
    """
    return " ".join(MORSE_CODE_DICT[char] for char in message.upper())


def decrypt(message: str) -> str:
    """
    Decode a Morse code string back to text.

    >>> decrypt('... --- ... -.-.--')
    'SOS!'
    >>> decrypt('.... . .-.. .-.. ---')
    'HELLO'
    """
    return "".join(REVERSE_DICT[token] for token in message.split())


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    msg = "Hello World"
    encoded = encrypt(msg)
    print("Encoded:", encoded)
    print("Decoded:", decrypt(encoded))
