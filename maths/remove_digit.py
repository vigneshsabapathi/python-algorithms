"""
Remove Digit (LeetCode 2259)
============================
Return the largest number you can obtain by deleting exactly one occurrence of
``digit`` from the decimal representation of ``number``.
"""


def remove_digit(number: str, digit: str) -> str:
    """
    >>> remove_digit("123", "1")
    '23'
    >>> remove_digit("1231", "1")
    '231'
    >>> remove_digit("551", "5")
    '51'
    >>> remove_digit("133235", "3")
    '13325'
    """
    best = ""
    for i, c in enumerate(number):
        if c == digit:
            candidate = number[:i] + number[i + 1 :]
            if candidate > best:
                best = candidate
    return best


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    for s, d in [("123", "1"), ("1231", "1"), ("551", "5"), ("133235", "3")]:
        print(f"remove_digit({s!r}, {d!r}) = {remove_digit(s, d)}")
