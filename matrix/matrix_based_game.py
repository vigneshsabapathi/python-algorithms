"""

Task:
Implement a matrix-based game where players select positions to remove
connected elements of the same type. After removal, gravity is simulated
and empty columns shift left. Score is calculated based on elements removed.

Implementation notes: Uses DFS to find connected same-colored elements.
Score formula: count * (count + 1) / 2. Gravity moves elements down within
columns. Empty columns shift left.

Reference: https://github.com/TheAlgorithms/Python/blob/master/matrix/matrix_based_game.py
"""


def find_repeat(
    matrix_g: list[list[str]], row: int, column: int, size: int
) -> set[tuple[int, int]]:
    """
    Find all connected elements of the same type from a given position using DFS.

    >>> find_repeat([['A', 'B', 'A'], ['A', 'B', 'A'], ['A', 'A', 'A']], 0, 0, 3)
    {(1, 2), (2, 1), (0, 0), (2, 0), (0, 2), (2, 2), (1, 0)}
    >>> find_repeat([['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']], 1, 1, 3)
    set()
    """
    column = size - 1 - column
    visited = set()
    repeated = set()

    if (color := matrix_g[column][row]) != "-":

        def dfs(row_n: int, column_n: int) -> None:
            if row_n < 0 or row_n >= size or column_n < 0 or column_n >= size:
                return
            if (row_n, column_n) in visited:
                return
            visited.add((row_n, column_n))
            if matrix_g[row_n][column_n] == color:
                repeated.add((row_n, column_n))
                dfs(row_n - 1, column_n)
                dfs(row_n + 1, column_n)
                dfs(row_n, column_n - 1)
                dfs(row_n, column_n + 1)

        dfs(column, row)

    return repeated


def increment_score(count: int) -> int:
    """
    Calculate score for a move based on elements removed.

    >>> increment_score(3)
    6
    >>> increment_score(0)
    0
    >>> increment_score(1)
    1
    """
    return int(count * (count + 1) / 2)


def move_x(matrix_g: list[list[str]], column: int, size: int) -> list[list[str]]:
    """
    Simulate gravity in a specific column (elements fall down).

    >>> move_x([['-', 'A'], ['-', '-'], ['-', 'C']], 1, 2)
    [['-', '-'], ['-', 'A'], ['-', 'C']]
    """
    new_list = []
    for row in range(size):
        if matrix_g[row][column] != "-":
            new_list.append(matrix_g[row][column])
        else:
            new_list.insert(0, matrix_g[row][column])
    for row in range(size):
        matrix_g[row][column] = new_list[row]
    return matrix_g


def move_y(matrix_g: list[list[str]], size: int) -> list[list[str]]:
    """
    Shift columns leftward when an entire column becomes empty.

    >>> move_y([['-', 'A'], ['-', '-'], ['-', 'C']], 2)
    [['A', '-'], ['-', '-'], ['-', 'C']]
    """
    empty_columns = []
    for column in range(size - 1, -1, -1):
        if all(matrix_g[row][column] == "-" for row in range(size)):
            empty_columns.append(column)

    for column in empty_columns:
        for col in range(column + 1, size):
            for row in range(size):
                matrix_g[row][col - 1] = matrix_g[row][col]
        for row in range(size):
            matrix_g[row][-1] = "-"

    return matrix_g


def play(
    matrix_g: list[list[str]], pos_x: int, pos_y: int, size: int
) -> tuple[list[list[str]], int]:
    """
    Process a single move: find connected, remove, apply gravity, shift columns.

    >>> play([['R', 'G'], ['R', 'G']], 0, 0, 2)
    ([['G', '-'], ['G', '-']], 3)
    """
    same_colors = find_repeat(matrix_g, pos_x, pos_y, size)

    if len(same_colors) != 0:
        for pos in same_colors:
            matrix_g[pos[0]][pos[1]] = "-"
        for column in range(size):
            matrix_g = move_x(matrix_g, column, size)
        matrix_g = move_y(matrix_g, size)

    return (matrix_g, increment_score(len(same_colors)))


def process_game(size: int, matrix: list[str], moves: list[tuple[int, int]]) -> int:
    """
    Process the full game: apply all moves and return total score.

    >>> process_game(3, ['aaa', 'bbb', 'ccc'], [(0, 0)])
    6
    """
    game_matrix = [list(row) for row in matrix]
    total_score = 0

    for move in moves:
        pos_x, pos_y = move
        game_matrix, score = play(game_matrix, pos_x, pos_y, size)
        total_score += score

    return total_score


if __name__ == "__main__":
    import doctest

    doctest.testmod()
