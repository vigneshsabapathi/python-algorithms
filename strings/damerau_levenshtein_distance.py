"""
Implementation of the Damerau-Levenshtein distance algorithm.

Measures the minimum number of single-character edits (insertions, deletions,
substitutions, and adjacent transpositions) to change one string into another.

Note: This implements the Optimal String Alignment (OSA) variant — a restriction
of the true Damerau-Levenshtein distance that does not allow a substring to be
edited more than once. See damerau_levenshtein_optimized.py for the true variant.

More information:
https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
"""


def damerau_levenshtein_distance(first_string: str, second_string: str) -> int:
    """
    Returns the OSA edit distance between two strings.
    Operations: insert, delete, substitute, transpose adjacent characters.

    >>> damerau_levenshtein_distance("cat", "cut")
    1
    >>> damerau_levenshtein_distance("kitten", "sitting")
    3
    >>> damerau_levenshtein_distance("hello", "world")
    4
    >>> damerau_levenshtein_distance("book", "back")
    2
    >>> damerau_levenshtein_distance("container", "containment")
    3
    >>> damerau_levenshtein_distance("", "")
    0
    >>> damerau_levenshtein_distance("abc", "")
    3
    >>> damerau_levenshtein_distance("", "abc")
    3
    >>> damerau_levenshtein_distance("ab", "ba")
    1
    """
    # DP matrix: rows = first_string chars, cols = second_string chars
    # dp_matrix[i][j] = edit distance between first_string[:i] and second_string[:j]
    dp_matrix = [[0] * (len(second_string) + 1) for _ in range(len(first_string) + 1)]

    # Base cases: transforming prefix to/from empty string costs i/j deletions/insertions
    for i in range(len(first_string) + 1):
        dp_matrix[i][0] = i
    for j in range(len(second_string) + 1):
        dp_matrix[0][j] = j

    for i, first_char in enumerate(first_string, start=1):
        for j, second_char in enumerate(second_string, start=1):
            cost = int(first_char != second_char)  # 0 if same, 1 if different

            dp_matrix[i][j] = min(
                dp_matrix[i - 1][j] + 1,        # deletion from first_string
                dp_matrix[i][j - 1] + 1,        # insertion into first_string
                dp_matrix[i - 1][j - 1] + cost, # substitution (or no-op if same)
            )

            # Transposition: swap adjacent characters (OSA check)
            if (
                i > 1
                and j > 1
                and first_string[i - 1] == second_string[j - 2]
                and first_string[i - 2] == second_string[j - 1]
            ):
                dp_matrix[i][j] = min(dp_matrix[i][j], dp_matrix[i - 2][j - 2] + cost)

    return dp_matrix[-1][-1]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
