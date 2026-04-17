"""
Atbash Cipher — a substitution cipher where A↔Z, B↔Y, etc.
Works for both upper and lowercase; non-letters pass through unchanged.

References:
    https://en.wikipedia.org/wiki/Atbash
"""

import string


def atbash(sequence: str) -> str:
    """
    Encode/decode a string using the Atbash cipher.
    Atbash is its own inverse: atbash(atbash(s)) == s.

    >>> atbash("ABCDEFG")
    'ZYXWVUT'
    >>> atbash("aW;;123BX")
    'zD;;123YC'
    >>> atbash("Hello, World!")
    'Svool, Dliow!'
    >>> atbash("")
    ''
    """
    letters = string.ascii_letters
    letters_reversed = string.ascii_lowercase[::-1] + string.ascii_uppercase[::-1]
    return "".join(
        letters_reversed[letters.index(c)] if c in letters else c for c in sequence
    )


def atbash_slow(sequence: str) -> str:
    """
    Atbash cipher — character-by-character ord() approach (slower reference).

    >>> atbash_slow("ABCDEFG")
    'ZYXWVUT'
    >>> atbash_slow("aW;;123BX")
    'zD;;123YC'
    """
    output = ""
    for ch in sequence:
        code = ord(ch)
        if 65 <= code <= 90:          # uppercase A-Z
            output += chr(155 - code)
        elif 97 <= code <= 122:        # lowercase a-z
            output += chr(219 - code)
        else:
            output += ch
    return output


if __name__ == "__main__":
    import doctest
    doctest.testmod()
