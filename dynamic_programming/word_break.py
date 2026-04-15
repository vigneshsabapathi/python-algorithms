# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/word_break.py


def word_break(s: str, word_dict: list[str]) -> bool:
    """
    Determine if string s can be segmented into space-separated words from word_dict.

    >>> word_break("leetcode", ["leet", "code"])
    True
    >>> word_break("applepenapple", ["apple", "pen"])
    True
    >>> word_break("catsandog", ["cats", "dog", "sand", "and", "cat"])
    False
    >>> word_break("", ["a"])
    True
    >>> word_break("a", [])
    False
    >>> word_break("aaaaaaa", ["aaaa", "aaa"])
    True
    """
    word_set = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    return dp[n]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        ("leetcode", ["leet", "code"], True),
        ("applepenapple", ["apple", "pen"], True),
        ("catsandog", ["cats", "dog", "sand", "and", "cat"], False),
        ("", ["a"], True),
        ("a", [], False),
        ("aaaaaaa", ["aaaa", "aaa"], True),
    ]
    for s, d, expected in cases:
        result = word_break(s, d)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] word_break({s!r}, {d}) = {result}  (expected {expected})")
