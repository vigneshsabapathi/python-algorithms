# Created by susmith98

from collections import Counter
from timeit import timeit

# Problem Description:
# Check if characters of the given string can be rearranged to form a palindrome.
# Counter is faster for long strings and non-Counter is faster for short strings.


def can_string_be_rearranged_as_palindrome_counter(
    input_str: str = "",
) -> bool:
    """
    A Palindrome is a String that reads the same forward as it does backwards.
    Examples of Palindromes mom, dad, malayalam
    >>> can_string_be_rearranged_as_palindrome_counter("Momo")
    True
    >>> can_string_be_rearranged_as_palindrome_counter("Mother")
    False
    >>> can_string_be_rearranged_as_palindrome_counter("Father")
    False
    >>> can_string_be_rearranged_as_palindrome_counter("A man a plan a canal Panama")
    True
    """
    return sum(c % 2 for c in Counter(input_str.replace(" ", "").lower()).values()) < 2


def can_string_be_rearranged_as_palindrome(input_str: str = "") -> bool:
    """
    A Palindrome is a String that reads the same forward as it does backwards.
    Examples of Palindromes mom, dad, malayalam
    >>> can_string_be_rearranged_as_palindrome("Momo")
    True
    >>> can_string_be_rearranged_as_palindrome("Mother")
    False
    >>> can_string_be_rearranged_as_palindrome("Father")
    False
    >>> can_string_be_rearranged_as_palindrome("A man a plan a canal Panama")
    True
    """
    if len(input_str) == 0:
        return True
    lower_case_input_str = input_str.replace(" ", "").lower()
    # character_freq_dict: Stores the frequency of every character in the input string
    character_freq_dict: dict[str, int] = {}

    for character in lower_case_input_str:
        character_freq_dict[character] = character_freq_dict.get(character, 0) + 1

    # Even-length palindrome: every char appears an even number of times.
    # Odd-length palindrome: exactly one char appears an odd number of times.
    # If more than 1 char has an odd count, rearranging as a palindrome is impossible.
    odd_char = 0
    for character_count in character_freq_dict.values():
        if character_count % 2:
            odd_char += 1
    return not odd_char > 1


if __name__ == "__main__":
    from doctest import testmod

    testmod()

    examples = [
        "Momo",
        "Mother",
        "A man a plan a canal Panama",
        "racecar",
    ]
    for s in examples:
        status = can_string_be_rearranged_as_palindrome_counter(s)
        print(f"{s!r} can {'': <3}{'not ' if not status else ''}be rearranged as a palindrome")
