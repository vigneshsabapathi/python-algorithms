def pig_latin(word: str) -> str:
    """Compute the piglatin of a given string.

    https://en.wikipedia.org/wiki/Pig_Latin

    Usage examples:
    >>> pig_latin("pig")
    'igpay'
    >>> pig_latin("latin")
    'atinlay'
    >>> pig_latin("banana")
    'ananabay'
    >>> pig_latin("friends")
    'iendsfray'
    >>> pig_latin("smile")
    'ilesmay'
    >>> pig_latin("string")
    'ingstray'
    >>> pig_latin("eat")
    'eatway'
    >>> pig_latin("omelet")
    'omeletway'
    >>> pig_latin("are")
    'areway'
    >>> pig_latin(" ")
    ''
    >>> pig_latin(None)
    ''
    """
    # Guard: return empty string for None or whitespace-only input
    if not (word or "").strip():
        return ""

    word = word.lower()

    if word[0] in "aeiou":
        # Vowel rule: word starts with a vowel → append "way"
        return f"{word}way"

    # Consonant rule: find the first vowel, move the leading consonant cluster
    # to the end, then append "ay"
    for i, char in enumerate(word):  # noqa: B007
        if char in "aeiou":
            break

    # word[i:] = from first vowel onward, word[:i] = consonant cluster
    return f"{word[i:]}{word[:i]}ay"


if __name__ == "__main__":
    print(f"{pig_latin('friends') = }")
    word = input("Enter a word: ")
    print(f"{pig_latin(word) = }")
