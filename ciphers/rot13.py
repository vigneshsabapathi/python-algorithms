"""
ROT13 Cipher

ROT13 is a special case of the Caesar cipher with a shift of 13.
Because the alphabet has 26 letters, applying ROT13 twice returns
the original text (self-inverse).

https://en.wikipedia.org/wiki/ROT13
"""


def dencrypt(s: str, n: int = 13) -> str:
    """
    Apply a Caesar shift of n to all alphabetical characters in s.
    With n=13 (default) this is ROT13, which is its own inverse.

    >>> msg = "My secret bank account number is 173-52946 so don't tell anyone!!"
    >>> s = dencrypt(msg)
    >>> s
    "Zl frperg onax nppbhag ahzore vf 173-52946 fb qba'g gryy nalbar!!"
    >>> dencrypt(s) == msg
    True
    >>> dencrypt("Hello", 13)
    'Uryyb'
    >>> dencrypt("Uryyb", 13)
    'Hello'
    """
    out = ""
    for c in s:
        if "A" <= c <= "Z":
            out += chr(ord("A") + (ord(c) - ord("A") + n) % 26)
        elif "a" <= c <= "z":
            out += chr(ord("a") + (ord(c) - ord("a") + n) % 26)
        else:
            out += c
    return out


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    s0 = "Hello, World!"
    s1 = dencrypt(s0, 13)
    print(f"ROT13 of '{s0}': {s1}")
    print(f"ROT13 again:     {dencrypt(s1, 13)}")
