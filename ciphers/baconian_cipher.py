"""
Baconian (Bacon's) Cipher — encodes each letter as a 5-character sequence of
'A' and 'B', e.g. A→AAAAA, B→AAAAB, ..., Z→BABBB.
Spaces are preserved as-is.

References:
    https://en.wikipedia.org/wiki/Bacon%27s_cipher
"""

ENCODE_DICT: dict[str, str] = {
    "a": "AAAAA", "b": "AAAAB", "c": "AAABA", "d": "AAABB", "e": "AABAA",
    "f": "AABAB", "g": "AABBA", "h": "AABBB", "i": "ABAAA", "j": "BBBAA",
    "k": "ABAAB", "l": "ABABA", "m": "ABABB", "n": "ABBAA", "o": "ABBAB",
    "p": "ABBBA", "q": "ABBBB", "r": "BAAAA", "s": "BAAAB", "t": "BAABA",
    "u": "BAABB", "v": "BBBAB", "w": "BABAA", "x": "BABAB", "y": "BABBA",
    "z": "BABBB", " ": " ",
}

DECODE_DICT: dict[str, str] = {v: k for k, v in ENCODE_DICT.items()}


def encode(word: str) -> str:
    """
    Encode a word to Baconian cipher (letters and spaces only).

    >>> encode("hello")
    'AABBBAABAAABABAABABAABBAB'
    >>> encode("hello world")
    'AABBBAABAAABABAABABAABBAB BABAAABBABBAAAAABABAAAABB'
    >>> encode("hello world!")
    Traceback (most recent call last):
        ...
    Exception: encode() accepts only letters of the alphabet and spaces
    """
    encoded = ""
    for letter in word.lower():
        if letter.isalpha() or letter == " ":
            encoded += ENCODE_DICT[letter]
        else:
            raise Exception("encode() accepts only letters of the alphabet and spaces")
    return encoded


def decode(coded: str) -> str:
    """
    Decode a Baconian cipher string back to text.

    >>> decode("AABBBAABAAABABAABABAABBAB BABAAABBABBAAAAABABAAAABB")
    'hello world'
    >>> decode("AABBBAABAAABABAABABAABBAB")
    'hello'
    >>> decode("AABBBAABAAABABAABABAABBAB BABAAABBABBAAAAABABAAAABB!")
    Traceback (most recent call last):
        ...
    Exception: decode() accepts only 'A', 'B' and spaces
    """
    if set(coded) - {"A", "B", " "} != set():
        raise Exception("decode() accepts only 'A', 'B' and spaces")
    decoded = ""
    for word in coded.split():
        while word:
            decoded += DECODE_DICT[word[:5]]
            word = word[5:]
        decoded += " "
    return decoded.strip()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
