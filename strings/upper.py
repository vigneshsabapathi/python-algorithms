def upper(word: str) -> str:
    """
    Convert an entire string to ASCII uppercase letters by looking for lowercase ASCII
    letters and subtracting 32 from their integer representation to get the uppercase
    letter.

    >>> upper("wow")
    'WOW'
    >>> upper("Hello")
    'HELLO'
    >>> upper("WHAT")
    'WHAT'
    >>> upper("wh[]32")
    'WH[]32'
    """
    return "".join(
        # ASCII distance between 'a' (97) and 'A' (65) is exactly 32,
        # so subtracting 32 from any lowercase letter's ordinal gives its uppercase
        chr(ord(char) - 32) if "a" <= char <= "z" else char
        for char in word
    )


if __name__ == "__main__":
    from doctest import testmod

    testmod()
