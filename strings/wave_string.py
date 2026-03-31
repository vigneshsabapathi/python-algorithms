def wave(txt: str) -> list:
    """
    Returns a so called 'wave' of a given string
    >>> wave('cat')
    ['Cat', 'cAt', 'caT']
    >>> wave('one')
    ['One', 'oNe', 'onE']
    >>> wave('book')
    ['Book', 'bOok', 'boOk', 'booK']
    """

    return [
        txt[:a] + txt[a].upper() + txt[a + 1 :]  # capitalize only the char at index a
        for a in range(len(txt))
        if txt[a].isalpha()  # skip non-alpha characters (digits, spaces, punctuation)
    ]


if __name__ == "__main__":
    __import__("doctest").testmod()
