def lower(word: str) -> str:
    """
    Will convert the entire string to lowercase letters

    >>> lower("wow")
    'wow'
    >>> lower("HellZo")
    'hellzo'
    >>> lower("WHAT")
    'what'
    >>> lower("wh[]32")
    'wh[]32'
    >>> lower("whAT")
    'what'
    """
    # ASCII distance between 'A' (65) and 'a' (97) is exactly 32.
    # Adding 32 to any uppercase letter's ordinal gives its lowercase equivalent.
    # Guard "A" <= char <= "Z" ensures digits, symbols, and already-lowercase
    # letters are passed through unchanged.
    return "".join(chr(ord(char) + 32) if "A" <= char <= "Z" else char for char in word)


if __name__ == "__main__":
    from doctest import testmod

    testmod()
