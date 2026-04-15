"""
Longest Palindromic Subsequence — LeetCode 516

Given a string, find the length of the longest palindromic subsequence.

Key insight: LPS(s) == LCS(s, reverse(s))
This reduces the problem to Longest Common Subsequence.

>>> longest_palindromic_subsequence("bbbab")
4
>>> longest_palindromic_subsequence("bbabcbcab")
7
>>> longest_palindromic_subsequence("a")
1
>>> longest_palindromic_subsequence("abcba")
5
>>> longest_palindromic_subsequence("")
0
"""


def longest_palindromic_subsequence(input_string: str) -> int:
    """
    Return the length of the longest palindromic subsequence.

    Uses DP by computing LCS of the string with its reverse.

    >>> longest_palindromic_subsequence("bbbab")
    4
    >>> longest_palindromic_subsequence("bbabcbcab")
    7
    >>> longest_palindromic_subsequence("cbbd")
    2
    """
    n = len(input_string)
    if n == 0:
        return 0

    rev = input_string[::-1]
    m = len(rev)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if input_string[i - 1] == rev[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[n][m]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    tests = ["bbbab", "bbabcbcab", "abcba", "cbbd", "a", "abcdefgfedcba"]
    for s in tests:
        print(f"  LPS({s!r}) = {longest_palindromic_subsequence(s)}")
