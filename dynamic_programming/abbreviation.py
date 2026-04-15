"""
Abbreviation (HackerRank)

https://www.hackerrank.com/challenges/abbr/problem

You can perform the following operations on string `a`:
  1. Capitalize zero or more of a's lowercase letters at some index i.
  2. Delete all of the remaining lowercase letters.

Determine if it's possible to make string `a` equal to string `b`.

Example:
  a = "daBcd", b = "ABC"
  daBcd -> capitalize a and c -> dABCd -> remove d's -> ABC  =>  True

>>> abbr("daBcd", "ABC")
True
>>> abbr("dBcd", "ABC")
False
>>> abbr("ABc", "ABC")
True
>>> abbr("ABC", "ABC")
True
>>> abbr("abc", "ABC")
True
>>> abbr("abcd", "ABC")
True
>>> abbr("ABcd", "BCD")
False
>>> abbr("", "")
True
>>> abbr("a", "")
True
>>> abbr("", "A")
False
>>> abbr("A", "")
False
"""


def abbr(a: str, b: str) -> bool:
    """
    Determine if string a can be transformed into string b by:
      1. Capitalizing some lowercase letters
      2. Deleting remaining lowercase letters

    Uses bottom-up DP. dp[i][j] = True means first i chars of a can form first j chars of b.

    >>> abbr("daBcd", "ABC")
    True
    >>> abbr("dBcd", "ABC")
    False
    >>> abbr("ABc", "ABC")
    True
    >>> abbr("", "")
    True
    """
    n = len(a)
    m = len(b)
    dp = [[False for _ in range(m + 1)] for _ in range(n + 1)]
    dp[0][0] = True
    for i in range(n):
        for j in range(m + 1):
            if dp[i][j]:
                # Option 1: capitalize a[i] if it matches b[j]
                if j < m and a[i].upper() == b[j]:
                    dp[i + 1][j + 1] = True
                # Option 2: delete a[i] (only if it's lowercase)
                if a[i].islower():
                    dp[i + 1][j] = True
    return dp[n][m]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    # Live demo
    tests = [
        ("daBcd", "ABC", True),
        ("dBcd", "ABC", False),
        ("ABc", "ABC", True),
        ("abc", "ABC", True),
        ("ABcd", "BCD", False),
        ("", "", True),
    ]
    for a, b, expected in tests:
        result = abbr(a, b)
        tag = "OK" if result == expected else "FAIL"
        print(f"  [{tag}] abbr({a!r}, {b!r}) = {result}  (expected {expected})")
