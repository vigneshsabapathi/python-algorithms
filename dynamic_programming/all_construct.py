"""
All Construct — List all ways a target string can be constructed from a word bank.

Given a target string and a list of substrings (word_bank), return all possible
combinations of words that can be concatenated to form the target.

Uses tabulation (bottom-up DP) to build solutions from left to right.

>>> all_construct("hello", ["he", "l", "o"])
[['he', 'l', 'l', 'o']]
>>> all_construct("purple", ["purp", "p", "ur", "le", "purpl"])
[['purp', 'le'], ['p', 'ur', 'p', 'le']]
>>> all_construct("", ["a", "b"])
[[]]
>>> all_construct("abc", ["x", "y"])
[]
>>> all_construct("abcdef", ["ab", "abc", "cd", "def", "abcd", "ef"])
[['abc', 'def'], ['abcd', 'ef'], ['ab', 'cd', 'ef']]
"""

from __future__ import annotations


def all_construct(target: str, word_bank: list[str] | None = None) -> list[list[str]]:
    """
    Return all ways to construct `target` from words in `word_bank`.

    Uses bottom-up tabulation: table[i] holds a list of all ways to
    construct target[:i] from the word bank.

    >>> all_construct("hello", ["he", "l", "o"])
    [['he', 'l', 'l', 'o']]
    >>> all_construct("purple", ["purp", "p", "ur", "le", "purpl"])
    [['purp', 'le'], ['p', 'ur', 'p', 'le']]
    """
    word_bank = word_bank or []
    table_size = len(target) + 1

    table: list[list[list[str]]] = [[] for _ in range(table_size)]
    table[0] = [[]]  # empty string has one combination: the empty list

    for i in range(table_size):
        if table[i] != []:
            for word in word_bank:
                if target[i: i + len(word)] == word:
                    new_combinations = [[word, *way] for way in table[i]]
                    table[i + len(word)] += new_combinations

    # Combinations are built left-to-right but stored in reverse order; reverse them
    for combination in table[len(target)]:
        combination.reverse()

    return table[len(target)]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    tests = [
        ("hello", ["he", "l", "o"]),
        ("purple", ["purp", "p", "ur", "le", "purpl"]),
        ("jwajalapa", ["jwa", "j", "w", "a", "la", "lapa"]),
        ("", ["a", "b"]),
        ("abc", ["x", "y"]),
    ]
    for target, words in tests:
        result = all_construct(target, words)
        print(f"  all_construct({target!r}, {words}) = {result}")
