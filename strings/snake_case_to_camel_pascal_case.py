def snake_to_camel_case(input_str: str, use_pascal: bool = False) -> str:
    """
    Transforms a snake_case given string to camelCase (or PascalCase if indicated)
    (defaults to not use Pascal)

    >>> snake_to_camel_case("some_random_string")
    'someRandomString'

    >>> snake_to_camel_case("some_random_string", use_pascal=True)
    'SomeRandomString'

    >>> snake_to_camel_case("some_random_string_with_numbers_123")
    'someRandomStringWithNumbers123'

    >>> snake_to_camel_case("some_random_string_with_numbers_123", use_pascal=True)
    'SomeRandomStringWithNumbers123'

    >>> snake_to_camel_case(123)
    Traceback (most recent call last):
        ...
    ValueError: Expected string as input, found <class 'int'>

    >>> snake_to_camel_case("some_string", use_pascal="True")
    Traceback (most recent call last):
        ...
    ValueError: Expected boolean as use_pascal parameter, found <class 'str'>
    """

    if not isinstance(input_str, str):
        msg = f"Expected string as input, found {type(input_str)}"
        raise ValueError(msg)
    if not isinstance(use_pascal, bool):
        msg = f"Expected boolean as use_pascal parameter, found {type(use_pascal)}"
        raise ValueError(msg)

    # Split on underscore to get individual words
    words = input_str.split("_")

    # PascalCase: capitalize from index 0; camelCase: capitalize from index 1
    start_index = 0 if use_pascal else 1

    words_to_capitalize = words[start_index:]

    # Capitalize only the first character of each word, preserve the rest
    capitalized_words = [word[0].upper() + word[1:] for word in words_to_capitalize]

    # camelCase keeps the first word as-is; PascalCase has no initial word
    initial_word = "" if use_pascal else words[0]

    return "".join([initial_word, *capitalized_words])


if __name__ == "__main__":
    from doctest import testmod

    testmod()
