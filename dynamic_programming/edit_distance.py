"""
Edit Distance (Levenshtein Distance) — LeetCode 72

Given two strings, find the minimum number of operations to convert one into
the other. Permitted operations: insert, delete, replace.

Classic DP problem with both top-down and bottom-up solutions.

>>> EditDistance().min_dist_top_down("intention", "execution")
5
>>> EditDistance().min_dist_bottom_up("intention", "execution")
5
>>> EditDistance().min_dist_top_down("", "")
0
>>> EditDistance().min_dist_bottom_up("kitten", "sitting")
3
"""


class EditDistance:
    """
    Solver for the edit distance problem with both top-down and bottom-up DP.

    >>> solver = EditDistance()
    >>> solver.min_dist_top_down("horse", "ros")
    3
    >>> solver.min_dist_bottom_up("horse", "ros")
    3
    """

    def __init__(self) -> None:
        self.word1 = ""
        self.word2 = ""
        self.dp: list[list[int]] = []

    def __min_dist_top_down_dp(self, m: int, n: int) -> int:
        if m == -1:
            return n + 1
        elif n == -1:
            return m + 1
        elif self.dp[m][n] > -1:
            return self.dp[m][n]
        else:
            if self.word1[m] == self.word2[n]:
                self.dp[m][n] = self.__min_dist_top_down_dp(m - 1, n - 1)
            else:
                insert = self.__min_dist_top_down_dp(m, n - 1)
                delete = self.__min_dist_top_down_dp(m - 1, n)
                replace = self.__min_dist_top_down_dp(m - 1, n - 1)
                self.dp[m][n] = 1 + min(insert, delete, replace)
            return self.dp[m][n]

    def min_dist_top_down(self, word1: str, word2: str) -> int:
        """
        Top-down (recursive with memoization) edit distance.

        >>> EditDistance().min_dist_top_down("intention", "execution")
        5
        >>> EditDistance().min_dist_top_down("intention", "")
        9
        >>> EditDistance().min_dist_top_down("", "")
        0
        """
        self.word1 = word1
        self.word2 = word2
        self.dp = [[-1 for _ in range(len(word2))] for _ in range(len(word1))]
        return self.__min_dist_top_down_dp(len(word1) - 1, len(word2) - 1)

    def min_dist_bottom_up(self, word1: str, word2: str) -> int:
        """
        Bottom-up (tabulation) edit distance.

        >>> EditDistance().min_dist_bottom_up("intention", "execution")
        5
        >>> EditDistance().min_dist_bottom_up("intention", "")
        9
        >>> EditDistance().min_dist_bottom_up("", "")
        0
        """
        self.word1 = word1
        self.word2 = word2
        m = len(word1)
        n = len(word2)
        self.dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0:
                    self.dp[i][j] = j
                elif j == 0:
                    self.dp[i][j] = i
                elif word1[i - 1] == word2[j - 1]:
                    self.dp[i][j] = self.dp[i - 1][j - 1]
                else:
                    insert = self.dp[i][j - 1]
                    delete = self.dp[i - 1][j]
                    replace = self.dp[i - 1][j - 1]
                    self.dp[i][j] = 1 + min(insert, delete, replace)
        return self.dp[m][n]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    solver = EditDistance()
    tests = [
        ("intention", "execution", 5),
        ("kitten", "sitting", 3),
        ("horse", "ros", 3),
        ("", "", 0),
        ("abc", "", 3),
    ]
    for w1, w2, expected in tests:
        td = solver.min_dist_top_down(w1, w2)
        bu = solver.min_dist_bottom_up(w1, w2)
        tag = "OK" if td == expected == bu else "FAIL"
        print(f"  [{tag}] edit_distance({w1!r}, {w2!r}) = top_down:{td}, bottom_up:{bu}  (expected {expected})")
