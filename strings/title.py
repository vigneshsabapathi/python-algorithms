def to_title_case(word: str) -> str:
    """
    Converts a string to capitalized case, preserving the input as is

    >>> to_title_case("Aakash")
    'Aakash'

    >>> to_title_case("aakash")
    'Aakash'

    >>> to_title_case("AAKASH")
    'Aakash'

    >>> to_title_case("aAkAsH")
    'Aakash'
    """

    # Uppercase the first character if it's a lowercase ASCII letter (subtract 32)
    if "a" <= word[0] <= "z":
        word = chr(ord(word[0]) - 32) + word[1:]

    # Lowercase all remaining characters that are uppercase ASCII letters (add 32)
    for i in range(1, len(word)):
        if "A" <= word[i] <= "Z":
            word = word[:i] + chr(ord(word[i]) + 32) + word[i + 1 :]

    return word


def sentence_to_title_case(input_str: str) -> str:
    """
    Converts a string to title case, preserving the input as is

    >>> sentence_to_title_case("Aakash Giri")
    'Aakash Giri'

    >>> sentence_to_title_case("aakash giri")
    'Aakash Giri'

    >>> sentence_to_title_case("AAKASH GIRI")
    'Aakash Giri'

    >>> sentence_to_title_case("aAkAsH gIrI")
    'Aakash Giri'
    """
    # Split on whitespace, title-case each word, rejoin with spaces
    return " ".join(to_title_case(word) for word in input_str.split())


if __name__ == "__main__":
    from doctest import testmod

    testmod()
