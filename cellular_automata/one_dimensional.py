"""
One-Dimensional Elementary Cellular Automaton.
https://mathworld.wolfram.com/ElementaryCellularAutomaton.html

Given a rule number (0-255), simulates the 1D cellular automaton.
Each cell's next state is determined by its current state and its
two neighbours, giving 2^3 = 8 possible patterns, encoded as an
8-bit rule number.

Famous examples:
- Rule 30:  chaos from simple initial state
- Rule 90:  Sierpinski triangle
- Rule 110: Turing-complete

>>> format_ruleset(30)
[0, 0, 0, 1, 1, 1, 1, 0]
>>> format_ruleset(90)
[0, 1, 0, 1, 1, 0, 1, 0]
>>> format_ruleset(110)
[0, 1, 1, 0, 1, 1, 1, 0]
"""

from __future__ import annotations


def format_ruleset(rule_number: int) -> list[int]:
    """
    Convert a rule number (0-255) into its 8-bit binary representation
    as a list, MSB first. The index maps to the 3-cell neighbourhood pattern.

    >>> format_ruleset(0)
    [0, 0, 0, 0, 0, 0, 0, 0]
    >>> format_ruleset(255)
    [1, 1, 1, 1, 1, 1, 1, 1]
    >>> format_ruleset(30)
    [0, 0, 0, 1, 1, 1, 1, 0]
    >>> format_ruleset(90)
    [0, 1, 0, 1, 1, 0, 1, 0]
    """
    return [int(c) for c in f"{rule_number:08b}"]


def new_generation(cells: list[int], rule: list[int]) -> list[int]:
    """
    Generate the next row of cells using the given rule.

    The three-cell neighbourhood (left, center, right) is converted to a
    binary number (0-7), then mapped to the rule table.

    >>> new_generation([0, 0, 0, 1, 0, 0, 0], format_ruleset(30))
    [0, 0, 1, 1, 1, 0, 0]
    >>> new_generation([0, 0, 1, 1, 1, 0, 0], format_ruleset(30))
    [0, 1, 1, 0, 0, 1, 0]
    >>> new_generation([0, 0, 0, 1, 0, 0, 0], format_ruleset(90))
    [0, 0, 1, 0, 1, 0, 0]
    """
    population = len(cells)
    next_gen = []
    for i in range(population):
        left = 0 if i == 0 else cells[i - 1]
        center = cells[i]
        right = 0 if i == population - 1 else cells[i + 1]
        # Convert 3-bit neighbourhood to index (7 - pattern for MSB-first)
        pattern = 7 - int(f"{left}{center}{right}", 2)
        next_gen.append(rule[pattern])
    return next_gen


def run_automaton(
    rule_number: int, width: int = 31, generations: int = 15
) -> list[list[int]]:
    """
    Run a 1D cellular automaton for the given number of generations.
    Starts with a single cell in the center.

    >>> cells = run_automaton(90, width=7, generations=3)
    >>> len(cells)
    4
    >>> cells[0]
    [0, 0, 0, 1, 0, 0, 0]
    >>> cells[1]
    [0, 0, 1, 0, 1, 0, 0]
    """
    # Initialize: single active cell in center
    cells = [[0] * width]
    cells[0][width // 2] = 1

    rule = format_ruleset(rule_number)
    for _ in range(generations):
        cells.append(new_generation(cells[-1], rule))
    return cells


def cells_to_string(cells: list[list[int]]) -> str:
    """
    Convert the automaton state to a printable string.

    >>> print(cells_to_string([[0, 1, 0], [1, 1, 1]]))
    .#.
    ###
    """
    return "\n".join("".join("#" if c else "." for c in row) for row in cells)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    for rule_num in [30, 90, 110]:
        print(f"\nRule {rule_num}:")
        print("=" * 31)
        cells = run_automaton(rule_num, width=31, generations=15)
        print(cells_to_string(cells))
