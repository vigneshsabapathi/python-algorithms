"""
Magic Diamond Pattern — Print a diamond shape with numbers.

Creates a diamond pattern using number sequences, commonly asked in
pattern printing interview questions.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/magicdiamondpattern.py
"""

from __future__ import annotations


def magic_diamond(n: int) -> str:
    """
    Generate a magic diamond pattern of size n.

    >>> print(magic_diamond(3))
      1
     2 2
    3 3 3
     2 2
      1
    >>> print(magic_diamond(1))
    1
    >>> print(magic_diamond(2))
     1
    2 2
     1
    """
    if n <= 0:
        return ""

    lines: list[str] = []

    # Upper half including middle
    for i in range(1, n + 1):
        spaces = " " * (n - i)
        nums = " ".join(str(i) for _ in range(i))
        lines.append(spaces + nums)

    # Lower half (mirror of upper, excluding middle)
    for i in range(n - 1, 0, -1):
        spaces = " " * (n - i)
        nums = " ".join(str(i) for _ in range(i))
        lines.append(spaces + nums)

    return "\n".join(lines)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
