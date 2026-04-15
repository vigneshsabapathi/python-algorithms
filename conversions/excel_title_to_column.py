"""
Excel Title to Column Number

Convert Excel column titles (A, B, ..., Z, AA, AB, ...) to column numbers.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/excel_title_to_column.py
"""


def excel_title_to_column(title: str) -> int:
    """
    Convert an Excel column title to its corresponding column number.

    >>> excel_title_to_column("A")
    1
    >>> excel_title_to_column("B")
    2
    >>> excel_title_to_column("Z")
    26
    >>> excel_title_to_column("AA")
    27
    >>> excel_title_to_column("AZ")
    52
    >>> excel_title_to_column("ZY")
    701
    >>> excel_title_to_column("")
    Traceback (most recent call last):
        ...
    ValueError: Title cannot be empty
    >>> excel_title_to_column("1A")
    Traceback (most recent call last):
        ...
    ValueError: Invalid character in title: 1
    """
    if not title:
        raise ValueError("Title cannot be empty")

    result = 0
    for char in title.upper():
        if not char.isalpha():
            raise ValueError(f"Invalid character in title: {char}")
        result = result * 26 + (ord(char) - ord("A") + 1)
    return result


def column_to_excel_title(column: int) -> str:
    """
    Convert a column number to its Excel column title.

    >>> column_to_excel_title(1)
    'A'
    >>> column_to_excel_title(26)
    'Z'
    >>> column_to_excel_title(27)
    'AA'
    >>> column_to_excel_title(52)
    'AZ'
    >>> column_to_excel_title(701)
    'ZY'
    >>> column_to_excel_title(0)
    Traceback (most recent call last):
        ...
    ValueError: Column number must be positive
    """
    if column <= 0:
        raise ValueError("Column number must be positive")

    result = []
    while column > 0:
        column -= 1
        result.append(chr(column % 26 + ord("A")))
        column //= 26
    return "".join(reversed(result))


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    test_cases = ["A", "B", "Z", "AA", "AZ", "ZY", "AAA"]
    for title in test_cases:
        col = excel_title_to_column(title)
        back = column_to_excel_title(col)
        print(f"  '{title}' -> {col} -> '{back}'")
