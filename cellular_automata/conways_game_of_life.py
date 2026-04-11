"""
Conway's Game of Life implemented in Python.
https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

Rules:
1. Any live cell with 2 or 3 live neighbours survives.
2. Any dead cell with exactly 3 live neighbours becomes alive.
3. All other live cells die; all other dead cells stay dead.

>>> new_generation(BLINKER)
[[0, 0, 0], [1, 1, 1], [0, 0, 0]]
>>> new_generation([[0, 0, 0], [1, 1, 1], [0, 0, 0]])
[[0, 1, 0], [0, 1, 0], [0, 1, 0]]
"""

from __future__ import annotations

# Classic patterns
GLIDER = [
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

BLINKER = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]

BLOCK = [[1, 1], [1, 1]]  # Still life


def count_neighbours(cells: list[list[int]], row: int, col: int) -> int:
    """
    Count the number of live neighbours for a cell at (row, col).

    >>> count_neighbours([[0, 1, 0], [0, 1, 0], [0, 1, 0]], 1, 1)
    2
    >>> count_neighbours([[1, 1, 1], [1, 0, 1], [1, 1, 1]], 1, 1)
    8
    >>> count_neighbours([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 0, 0)
    0
    """
    rows, cols = len(cells), len(cells[0])
    count = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            if 0 <= r < rows and 0 <= c < cols:
                count += cells[r][c]
    return count


def new_generation(cells: list[list[int]]) -> list[list[int]]:
    """
    Generates the next generation for a given state of Conway's Game of Life.

    >>> new_generation(BLINKER)
    [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
    >>> new_generation(BLOCK)
    [[1, 1], [1, 1]]
    >>> new_generation([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    """
    rows, cols = len(cells), len(cells[0])
    next_gen = []
    for i in range(rows):
        row = []
        for j in range(cols):
            neighbours = count_neighbours(cells, i, j)
            alive = cells[i][j] == 1
            if (alive and 2 <= neighbours <= 3) or (not alive and neighbours == 3):
                row.append(1)
            else:
                row.append(0)
        next_gen.append(row)
    return next_gen


def run_simulation(cells: list[list[int]], generations: int) -> list[list[list[int]]]:
    """
    Run the Game of Life for a given number of generations.

    >>> states = run_simulation(BLINKER, 2)
    >>> len(states)
    3
    >>> states[0]
    [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
    >>> states[1]
    [[0, 0, 0], [1, 1, 1], [0, 0, 0]]
    >>> states[2]
    [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
    """
    history = [cells]
    current = cells
    for _ in range(generations):
        current = new_generation(current)
        history.append(current)
    return history


def grid_to_string(cells: list[list[int]]) -> str:
    """
    Convert a grid to a printable string representation.

    >>> print(grid_to_string(BLINKER))
    .#.
    .#.
    .#.
    """
    return "\n".join("".join("#" if c else "." for c in row) for row in cells)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print("Conway's Game of Life - Glider (5 generations)")
    print("=" * 40)
    states = run_simulation(GLIDER, 4)
    for i, state in enumerate(states):
        print(f"\nGeneration {i}:")
        print(grid_to_string(state))
