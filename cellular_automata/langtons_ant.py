"""
Langton's Ant - a two-dimensional cellular automaton with simple rules
that produces emergent complex behavior.
https://en.wikipedia.org/wiki/Langton%27s_ant

Rules:
1. On a white square: turn 90 deg clockwise, flip color, move forward.
2. On a black square: turn 90 deg counter-clockwise, flip color, move forward.

After ~10,000 steps the ant creates an emergent "highway" pattern.

>>> la = LangtonsAnt(5, 5)
>>> la.board[2][2]
True
>>> la.step()
True
>>> la.ant_position
(2, 3)
>>> la.board[2][2]
False
"""

from __future__ import annotations


class LangtonsAnt:
    """
    Represents Langton's Ant on a 2D grid.

    True = white, False = black.
    Direction: 0=Up, 1=Right, 2=Down, 3=Left

    >>> la = LangtonsAnt(3, 3)
    >>> la.board
    [[True, True, True], [True, True, True], [True, True, True]]
    >>> la.ant_position
    (1, 1)
    """

    DIRECTIONS = {
        0: (-1, 0),  # Up
        1: (0, 1),   # Right
        2: (1, 0),   # Down
        3: (0, -1),  # Left
    }

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        # True = white, False = black
        self.board: list[list[bool]] = [[True] * width for _ in range(height)]
        self.ant_position: tuple[int, int] = (height // 2, width // 2)
        self.ant_direction: int = 0  # Start facing up

    def step(self) -> bool:
        """
        Perform one step of Langton's Ant.
        Returns False if the ant moves out of bounds.

        >>> la = LangtonsAnt(5, 5)
        >>> la.step()
        True
        >>> la.ant_position
        (2, 3)
        >>> la.board[2][2]
        False
        >>> la.step()
        True
        >>> la.ant_position
        (3, 3)
        >>> la.board[2][3]
        False
        """
        x, y = self.ant_position

        # Turn based on current square color
        if self.board[x][y]:
            # White -> turn clockwise
            self.ant_direction = (self.ant_direction + 1) % 4
        else:
            # Black -> turn counter-clockwise
            self.ant_direction = (self.ant_direction - 1) % 4

        # Flip the color
        self.board[x][y] = not self.board[x][y]

        # Move forward
        dx, dy = self.DIRECTIONS[self.ant_direction]
        new_x, new_y = x + dx, y + dy

        # Check bounds
        if not (0 <= new_x < self.height and 0 <= new_y < self.width):
            return False

        self.ant_position = (new_x, new_y)
        return True

    def run(self, steps: int) -> int:
        """
        Run the ant for a given number of steps.
        Returns the number of steps actually completed.

        >>> la = LangtonsAnt(20, 20)
        >>> la.run(100)
        100
        >>> la = LangtonsAnt(3, 3)
        >>> la.run(1000) < 1000  # will go out of bounds
        True
        """
        for i in range(steps):
            if not self.step():
                return i
        return steps

    def count_black(self) -> int:
        """
        Count the number of black (False) cells.

        >>> la = LangtonsAnt(5, 5)
        >>> la.count_black()
        0
        >>> la.step()
        True
        >>> la.count_black()
        1
        """
        return sum(1 for row in self.board for cell in row if not cell)

    def board_to_string(self) -> str:
        """
        Convert the board to a printable string.
        '.' = white, '#' = black, 'A' = ant position.

        >>> la = LangtonsAnt(3, 3)
        >>> la.board_to_string()
        '...\\n.A.\\n...'
        """
        lines = []
        for r in range(self.height):
            row_str = ""
            for c in range(self.width):
                if (r, c) == self.ant_position:
                    row_str += "A"
                elif self.board[r][c]:
                    row_str += "."
                else:
                    row_str += "#"
            lines.append(row_str)
        return "\n".join(lines)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print("Langton's Ant Simulation")
    print("=" * 40)

    la = LangtonsAnt(21, 21)
    milestones = [0, 50, 100, 200]
    current_step = 0

    for target in milestones:
        la.run(target - current_step)
        current_step = target
        print(f"\nStep {target} (black cells: {la.count_black()}):")
        print(la.board_to_string())
