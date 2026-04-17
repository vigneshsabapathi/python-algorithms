"""
Mixed Keyword Cipher
https://en.wikipedia.org/wiki/Substitution_cipher#Keyword_cipher

Builds a shifted alphabet from the keyword, arranges it in rows, then reads
columns top-to-bottom to create the cipher mapping.
"""

from string import ascii_uppercase


def mixed_keyword(
    keyword: str, plaintext: str, verbose: bool = False, alphabet: str = ascii_uppercase
) -> str:
    """
    Encrypt plaintext using a mixed keyword cipher.

    The keyword characters (deduplicated) form the first row; remaining
    alphabet letters fill subsequent rows.  The mapping is then read
    column-by-column (top to bottom, left to right).

    >>> mixed_keyword("college", "UNIVERSITY", False)
    'XKJGUFMJST'

    >>> mixed_keyword("college", "UNIVERSITY", True)  # doctest: +NORMALIZE_WHITESPACE
    {'A': 'C', 'B': 'A', 'C': 'I', 'D': 'P', 'E': 'U', 'F': 'Z', 'G': 'O', 'H': 'B',
     'I': 'J', 'J': 'Q', 'K': 'V', 'L': 'L', 'M': 'D', 'N': 'K', 'O': 'R', 'P': 'W',
     'Q': 'E', 'R': 'F', 'S': 'M', 'T': 'S', 'U': 'X', 'V': 'G', 'W': 'H', 'X': 'N',
     'Y': 'T', 'Z': 'Y'}
    'XKJGUFMJST'

    >>> mixed_keyword("hello", "HELLO")
    'EQRRL'

    >>> mixed_keyword("a", "ABC")
    'ABC'
    """
    keyword = keyword.upper()
    plaintext = plaintext.upper()
    alphabet_set = set(alphabet)

    # Unique characters in keyword (order-preserving)
    unique_chars: list[str] = []
    for char in keyword:
        if char in alphabet_set and char not in unique_chars:
            unique_chars.append(char)

    num_cols = len(unique_chars)

    # Shifted alphabet: keyword letters first, then remaining
    shifted = unique_chars + [c for c in alphabet if c not in unique_chars]

    # Split into rows of width num_cols
    rows = [shifted[k: k + num_cols] for k in range(0, 26, num_cols)]

    # Build mapping by reading columns top-to-bottom
    mapping: dict[str, str] = {}
    letter_index = 0
    for col in range(num_cols):
        for row in rows:
            if len(row) <= col:
                break
            mapping[alphabet[letter_index]] = row[col]
            letter_index += 1

    if verbose:
        print(mapping)

    return "".join(mapping.get(char, char) for char in plaintext)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print(mixed_keyword("college", "UNIVERSITY"))
