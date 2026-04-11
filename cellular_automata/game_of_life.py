"""
Conway's Game of Life - NumPy-based implementation
https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

This variant uses NumPy for the grid and neighbourhood slicing, making it
more idiomatic for numerical computation than the pure-list approach in
conways_game_of_life.py.

Rules:
1. Any live cell with fewer than 2 live neighbours dies (under-population).
2. Any live cell with 2 or 3 live neighbours lives on.
3. Any live cell with more than 3 live neighbours dies (over-population).
4. Any dead cell with exactly 3 live neighbours becomes alive (reproduction).

>>> import numpy as np
>>> blinker = np.array([[False, True, False],
...                     [False, True, False],
...                     [False, True, False]])
>>> run(blinker).tolist()
[[False, False, False], [True, True, True], [False, False, False]]
"""

from __future__ import annotations

import numpy as np


def create_canvas(size: int) -> np.ndarray:
    """
    Create a square canvas (grid) of given size, initialized to all dead.

    >>> create_canvas(3).tolist()
    [[False, False, False], [False, False, False], [False, False, False]]
    >>> create_canvas(1).shape
    (1, 1)
    """
    return np.zeros((size, size), dtype=bool)


def seed_random(canvas: np.ndarray, density: float = 0.5) -> np.ndarray:
    """
    Randomly seed a canvas with live cells.

    >>> import numpy as np
    >>> np.random.seed(42)
    >>> c = seed_random(create_canvas(3), density=0.5)
    >>> c.dtype
    dtype('bool')
    >>> c.shape
    (3, 3)
    """
    return np.random.random(canvas.shape) < density


def judge_point(cell: bool, neighbours: np.ndarray) -> bool:
    """
    Apply Game of Life rules to a single cell given its neighbourhood.

    :param cell: Current state of the cell (True=alive, False=dead)
    :param neighbours: 2D array slice of the neighbourhood (including the cell)

    >>> import numpy as np
    >>> judge_point(True, np.array([[False, True, False],
    ...                             [False, True, True],
    ...                             [False, False, False]]))
    True
    >>> judge_point(True, np.array([[True, True, True],
    ...                             [True, True, True],
    ...                             [True, True, True]]))
    False
    >>> judge_point(False, np.array([[True, True, False],
    ...                              [False, False, True],
    ...                              [False, False, False]]))
    True
    """
    alive_count = int(np.sum(neighbours)) - int(cell)
    if cell:
        return 2 <= alive_count <= 3
    return alive_count == 3


def run(canvas: np.ndarray) -> np.ndarray:
    """
    Advance the Game of Life by one generation using NumPy slicing.

    >>> import numpy as np
    >>> blinker = np.array([[False, True, False],
    ...                     [False, True, False],
    ...                     [False, True, False]])
    >>> run(blinker).tolist()
    [[False, False, False], [True, True, True], [False, False, False]]

    >>> block = np.array([[True, True], [True, True]])
    >>> run(block).tolist()
    [[True, True], [True, True]]

    >>> empty = np.zeros((3, 3), dtype=bool)
    >>> run(empty).tolist()
    [[False, False, False], [False, False, False], [False, False, False]]
    """
    rows, cols = canvas.shape
    next_gen = np.zeros_like(canvas)
    for r in range(rows):
        for c in range(cols):
            # Neighbourhood slice (handles boundary by clamping)
            r_start, r_end = max(0, r - 1), min(rows, r + 2)
            c_start, c_end = max(0, c - 1), min(cols, c + 2)
            neighbours = canvas[r_start:r_end, c_start:c_end]
            next_gen[r][c] = judge_point(canvas[r][c], neighbours)
    return next_gen


def run_simulation(canvas: np.ndarray, generations: int) -> list[np.ndarray]:
    """
    Run the Game of Life for multiple generations.

    >>> import numpy as np
    >>> blinker = np.array([[False, True, False],
    ...                     [False, True, False],
    ...                     [False, True, False]])
    >>> states = run_simulation(blinker, 2)
    >>> len(states)
    3
    >>> states[2].tolist() == blinker.tolist()
    True
    """
    history = [canvas.copy()]
    current = canvas
    for _ in range(generations):
        current = run(current)
        history.append(current.copy())
    return history


def grid_to_string(canvas: np.ndarray) -> str:
    """
    Convert a boolean grid to printable string.

    >>> import numpy as np
    >>> print(grid_to_string(np.array([[True, False], [False, True]])))
    #.
    .#
    """
    return "\n".join("".join("#" if c else "." for c in row) for row in canvas)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print("Game of Life - NumPy Implementation")
    print("=" * 40)
    np.random.seed(42)
    canvas = seed_random(create_canvas(6), density=0.3)
    print(f"Initial ({int(canvas.sum())} alive):")
    print(grid_to_string(canvas))
    for gen in range(1, 4):
        canvas = run(canvas)
        print(f"\nGeneration {gen} ({int(canvas.sum())} alive):")
        print(grid_to_string(canvas))
