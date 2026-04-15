# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/min_distance_up_bottom.py


def min_distance(word1: str, word2: str) -> int:
    """
    Minimum edit distance (Levenshtein) using top-down DP with memoization.

    Operations: insert, delete, replace — each costs 1.

    >>> min_distance("horse", "ros")
    3
    >>> min_distance("intention", "execution")
    5
    >>> min_distance("", "abc")
    3
    >>> min_distance("abc", "")
    3
    >>> min_distance("abc", "abc")
    0
    >>> min_distance("kitten", "sitting")
    3
    >>> min_distance("", "")
    0
    """
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dp(i: int, j: int) -> int:
        if i == 0:
            return j
        if j == 0:
            return i
        if word1[i - 1] == word2[j - 1]:
            return dp(i - 1, j - 1)
        return 1 + min(
            dp(i - 1, j),      # delete
            dp(i, j - 1),      # insert
            dp(i - 1, j - 1),  # replace
        )

    result = dp(len(word1), len(word2))
    dp.cache_clear()
    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        ("horse", "ros", 3),
        ("intention", "execution", 5),
        ("", "abc", 3),
        ("abc", "", 3),
        ("abc", "abc", 0),
        ("kitten", "sitting", 3),
    ]
    for w1, w2, expected in cases:
        result = min_distance(w1, w2)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] min_distance({w1!r}, {w2!r}) = {result}  (expected {expected})")
