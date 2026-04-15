"""
Longest Common Subsequence (LCS) — LeetCode 1143

Given two strings, find the length of the longest subsequence present in both.
A subsequence appears in the same relative order but not necessarily contiguously.

Example: "abc", "abg" are subsequences of "abcdefgh".

Returns both the length and the actual subsequence.

>>> longest_common_subsequence("programming", "gaming")
(6, 'gaming')
>>> longest_common_subsequence("physics", "smartphone")
(2, 'ph')
>>> longest_common_subsequence("", "abc")
(0, '')
>>> longest_common_subsequence("abc", "abc")
(3, 'abc')
>>> longest_common_subsequence("abcdef", "ace")
(3, 'ace')
"""


def longest_common_subsequence(x: str, y: str) -> tuple[int, str]:
    """
    Find the longest common subsequence of strings x and y.

    Returns (length, subsequence_string).

    >>> longest_common_subsequence("programming", "gaming")
    (6, 'gaming')
    >>> longest_common_subsequence("computer", "food")
    (1, 'o')
    >>> longest_common_subsequence("", "")
    (0, '')
    >>> longest_common_subsequence("ABCD", "ACBD")
    (3, 'ABD')
    """
    assert x is not None
    assert y is not None

    m = len(x)
    n = len(y)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = 1 if x[i - 1] == y[j - 1] else 0
            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1] + match)

    # Reconstruct the subsequence
    seq = ""
    i, j = m, n
    while i > 0 and j > 0:
        match = 1 if x[i - 1] == y[j - 1] else 0
        if dp[i][j] == dp[i - 1][j - 1] + match:
            if match == 1:
                seq = x[i - 1] + seq
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i - 1][j]:
            i -= 1
        else:
            j -= 1

    return dp[m][n], seq


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    tests = [
        ("AGGTAB", "GXTXAYB"),
        ("programming", "gaming"),
        ("abcdef", "ace"),
        ("abc", "def"),
    ]
    for a, b in tests:
        ln, subseq = longest_common_subsequence(a, b)
        print(f"  LCS({a!r}, {b!r}) = len={ln}, seq={subseq!r}")
