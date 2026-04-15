"""
Longest Common Substring

Given two strings, find the longest substring (contiguous) present in both.

Unlike subsequence, a substring must be continuous.

Example: "abcdef" and "xabded" -> "ab" (or "de", both length 2)

>>> longest_common_substring("abcdef", "bcd")
'bcd'
>>> longest_common_substring("abcdef", "xabded")
'ab'
>>> longest_common_substring("GeeksforGeeks", "GeeksQuiz")
'Geeks'
>>> longest_common_substring("", "")
''
>>> longest_common_substring("a", "a")
'a'
>>> longest_common_substring(1, 1)
Traceback (most recent call last):
    ...
ValueError: longest_common_substring() takes two strings for inputs
"""


def longest_common_substring(text1: str, text2: str) -> str:
    """
    Find the longest common substring using bottom-up DP.

    O(m*n) time and space where m, n are string lengths.

    >>> longest_common_substring("abcdef", "bcd")
    'bcd'
    >>> longest_common_substring("zxabcdezy", "yzabcdezx")
    'abcdez'
    >>> longest_common_substring("abcdxyz", "xyzabcd")
    'abcd'
    >>> longest_common_substring(1, 1)
    Traceback (most recent call last):
        ...
    ValueError: longest_common_substring() takes two strings for inputs
    """
    if not (isinstance(text1, str) and isinstance(text2, str)):
        raise ValueError("longest_common_substring() takes two strings for inputs")

    if not text1 or not text2:
        return ""

    text1_length = len(text1)
    text2_length = len(text2)

    dp = [[0] * (text2_length + 1) for _ in range(text1_length + 1)]
    end_pos = 0
    max_length = 0

    for i in range(1, text1_length + 1):
        for j in range(1, text2_length + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
                if dp[i][j] > max_length:
                    end_pos = i
                    max_length = dp[i][j]

    return text1[end_pos - max_length: end_pos]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    tests = [
        ("abcdef", "bcd"),
        ("abcdef", "xabded"),
        ("GeeksforGeeks", "GeeksQuiz"),
        ("abcdxyz", "xyzabcd"),
        ("zxabcdezy", "yzabcdezx"),
    ]
    for a, b in tests:
        result = longest_common_substring(a, b)
        print(f"  LCS_substring({a!r}, {b!r}) = {result!r}")
