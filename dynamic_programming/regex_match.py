# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/regex_match.py


def regex_match(text: str, pattern: str) -> bool:
    """
    Regular expression matching with '.' and '*'.

    '.' matches any single character.
    '*' matches zero or more of the preceding element.

    >>> regex_match("aa", "a")
    False
    >>> regex_match("aa", "a*")
    True
    >>> regex_match("ab", ".*")
    True
    >>> regex_match("aab", "c*a*b")
    True
    >>> regex_match("mississippi", "mis*is*p*.")
    False
    >>> regex_match("", "")
    True
    >>> regex_match("", "a*")
    True
    """
    m, n = len(text), len(pattern)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    # Handle patterns like a*, a*b*, etc. matching empty string
    for j in range(2, n + 1):
        if pattern[j - 1] == "*":
            dp[0][j] = dp[0][j - 2]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if pattern[j - 1] == "*":
                # Zero occurrences of preceding element
                dp[i][j] = dp[i][j - 2]
                # One or more occurrences
                if pattern[j - 2] == "." or pattern[j - 2] == text[i - 1]:
                    dp[i][j] = dp[i][j] or dp[i - 1][j]
            elif pattern[j - 1] == "." or pattern[j - 1] == text[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]

    return dp[m][n]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        ("aa", "a", False),
        ("aa", "a*", True),
        ("ab", ".*", True),
        ("aab", "c*a*b", True),
        ("mississippi", "mis*is*p*.", False),
        ("", "", True),
        ("", "a*", True),
    ]
    for text, pattern, expected in cases:
        result = regex_match(text, pattern)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] regex_match({text!r}, {pattern!r}) = {result}  (expected {expected})")
