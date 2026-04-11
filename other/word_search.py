"""
Word Search — Find if a word exists in a 2D grid of characters.

The word can be constructed from letters of sequentially adjacent cells
(horizontally or vertically). Each cell may only be used once.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/word_search.py
"""

from __future__ import annotations


def word_search(board: list[list[str]], word: str) -> bool:
    """
    Check if word exists in the board using DFS backtracking.

    >>> board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']]
    >>> word_search(board, "ABCCED")
    True
    >>> word_search(board, "SEE")
    True
    >>> word_search(board, "ABCB")
    False
    >>> word_search([], "A")
    False
    >>> word_search([['A']], "A")
    True
    >>> word_search([['A']], "B")
    False
    """
    if not board or not board[0] or not word:
        return False

    rows, cols = len(board), len(board[0])

    def dfs(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True
        if (
            r < 0
            or r >= rows
            or c < 0
            or c >= cols
            or board[r][c] != word[idx]
        ):
            return False

        # Mark as visited
        temp = board[r][c]
        board[r][c] = "#"

        found = (
            dfs(r + 1, c, idx + 1)
            or dfs(r - 1, c, idx + 1)
            or dfs(r, c + 1, idx + 1)
            or dfs(r, c - 1, idx + 1)
        )

        # Restore
        board[r][c] = temp
        return found

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0] and dfs(r, c, 0):
                return True

    return False


if __name__ == "__main__":
    import doctest

    doctest.testmod()
