# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/palindrome_partitioning.py


def min_palindrome_partitions(s: str) -> int:
    """
    Find the minimum number of cuts needed to partition a string
    such that every substring is a palindrome.

    >>> min_palindrome_partitions("aab")
    1
    >>> min_palindrome_partitions("a")
    0
    >>> min_palindrome_partitions("ab")
    1
    >>> min_palindrome_partitions("aba")
    0
    >>> min_palindrome_partitions("abcba")
    0
    >>> min_palindrome_partitions("abcd")
    3
    >>> min_palindrome_partitions("")
    0
    """
    n = len(s)
    if n <= 1:
        return 0

    # is_pal[i][j] = True if s[i..j] is a palindrome
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n):
        is_pal[i][i] = True
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if length == 2:
                is_pal[i][j] = (s[i] == s[j])
            else:
                is_pal[i][j] = (s[i] == s[j]) and is_pal[i + 1][j - 1]

    # cuts[i] = min cuts for s[0..i]
    cuts = list(range(n))  # worst case: cut before every char
    for i in range(n):
        if is_pal[0][i]:
            cuts[i] = 0
        else:
            for j in range(i):
                if is_pal[j + 1][i]:
                    cuts[i] = min(cuts[i], cuts[j] + 1)

    return cuts[n - 1]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        ("aab", 1), ("a", 0), ("ab", 1), ("aba", 0),
        ("abcba", 0), ("abcd", 3), ("", 0),
    ]
    for s, expected in cases:
        result = min_palindrome_partitions(s)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] min_palindrome_partitions({s!r}) = {result}  (expected {expected})")
