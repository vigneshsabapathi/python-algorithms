# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/wildcard_matching.py


def wildcard_match(text: str, pattern: str) -> bool:
    """
    Wildcard pattern matching with '?' and '*'.

    '?' matches any single character.
    '*' matches any sequence of characters (including empty).

    >>> wildcard_match("aa", "a")
    False
    >>> wildcard_match("aa", "*")
    True
    >>> wildcard_match("cb", "?a")
    False
    >>> wildcard_match("adceb", "*a*b")
    True
    >>> wildcard_match("acdcb", "a*c?b")
    False
    >>> wildcard_match("", "")
    True
    >>> wildcard_match("", "*")
    True
    >>> wildcard_match("abc", "abc")
    True
    """
    m, n = len(text), len(pattern)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    # Pattern starting with * can match empty string
    for j in range(1, n + 1):
        if pattern[j - 1] == "*":
            dp[0][j] = dp[0][j - 1]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if pattern[j - 1] == "*":
                dp[i][j] = dp[i - 1][j] or dp[i][j - 1]
            elif pattern[j - 1] == "?" or pattern[j - 1] == text[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]

    return dp[m][n]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        ("aa", "a", False),
        ("aa", "*", True),
        ("cb", "?a", False),
        ("adceb", "*a*b", True),
        ("acdcb", "a*c?b", False),
        ("", "", True),
        ("", "*", True),
        ("abc", "abc", True),
    ]
    for text, pattern, expected in cases:
        result = wildcard_match(text, pattern)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] wildcard_match({text!r}, {pattern!r}) = {result}  (expected {expected})")
