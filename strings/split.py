def split(string: str, separator: str = " ") -> list:
    """
    Will split the string up into all the values separated by the separator
    (defaults to spaces)

    >>> split("apple#banana#cherry#orange",separator='#')
    ['apple', 'banana', 'cherry', 'orange']

    >>> split("Hello there")
    ['Hello', 'there']

    >>> split("11/22/63",separator = '/')
    ['11', '22', '63']

    >>> split("12:43:39",separator = ":")
    ['12', '43', '39']

    >>> split(";abbb;;c;", separator=';')
    ['', 'abbb', '', 'c', '']
    """

    split_words = []
    last_index = 0  # start of the current token

    for index, char in enumerate(string):
        if char == separator:
            # Found a separator — slice from last_index up to (not including) this char
            split_words.append(string[last_index:index])
            last_index = index + 1  # next token starts after the separator

        if index + 1 == len(string):
            # End of string — append whatever remains after the last separator
            split_words.append(string[last_index: index + 1])

    return split_words


if __name__ == "__main__":
    from doctest import testmod

    testmod()
