"""
Nagel-Schreckenberg traffic model - a cellular automaton for simulating
freeway traffic flow on a single-lane loop highway.
https://en.wikipedia.org/wiki/Nagel%E2%80%93Schreckenberg_model

Each cell is either empty (-1) or contains a car with speed 0..max_speed.

Rules (applied each time step):
1. Acceleration: speed = min(speed + 1, max_speed)
2. Slowing:     speed = min(speed, distance_to_next_car - 1)
3. Randomization: with probability p, speed = max(speed - 1, 0)
4. Movement:    car moves forward by its speed (loop wraps around)

>>> simulate(construct_highway(6, 3, 0), 2, 0, 2)
[[0, -1, -1, 0, -1, -1], [-1, 1, -1, -1, 1, -1], [-1, -1, 1, -1, -1, 1]]
>>> simulate(construct_highway(5, 2, -2), 3, 0, 2)
[[0, -1, 0, -1, 0], [0, -1, 0, -1, -1], [0, -1, -1, 1, -1], [-1, 1, -1, 0, -1]]
"""

from __future__ import annotations

from random import randint, random


def construct_highway(
    number_of_cells: int,
    frequency: int,
    initial_speed: int,
    random_frequency: bool = False,
    random_speed: bool = False,
    max_speed: int = 5,
) -> list[list[int]]:
    """
    Build a highway with cars placed at regular intervals.
    -1 = empty cell, 0..max_speed = car with that speed.

    >>> construct_highway(10, 2, 6)
    [[6, -1, 6, -1, 6, -1, 6, -1, 6, -1]]
    >>> construct_highway(10, 10, 2)
    [[2, -1, -1, -1, -1, -1, -1, -1, -1, -1]]
    >>> construct_highway(6, 3, 0)
    [[0, -1, -1, 0, -1, -1]]
    """
    highway = [[-1] * number_of_cells]
    i = 0
    initial_speed = max(initial_speed, 0)
    while i < number_of_cells:
        highway[0][i] = randint(0, max_speed) if random_speed else initial_speed
        i += randint(1, max_speed * 2) if random_frequency else frequency
    return highway


def get_distance(highway_now: list[int], car_index: int) -> int:
    """
    Get the number of empty cells between the car at car_index and the next
    car ahead (wrapping around the loop).

    >>> get_distance([6, -1, 6, -1, 6], 2)
    1
    >>> get_distance([2, -1, -1, -1, 3, 1, 0, 1, 3, 2], 0)
    3
    >>> get_distance([-1, -1, -1, -1, 2, -1, -1, -1, 3], -1)
    4
    """
    distance = 0
    cells = highway_now[car_index + 1:]
    for cell in cells:
        if cell != -1:
            return distance
        distance += 1
    # Wrap around to the beginning
    return distance + get_distance(highway_now, -1)


def update(highway_now: list[int], probability: float, max_speed: int) -> list[int]:
    """
    Update the speed of all cars on the highway (rules 1-3).

    >>> update([-1, -1, -1, -1, -1, 2, -1, -1, -1, -1, 3], 0.0, 5)
    [-1, -1, -1, -1, -1, 3, -1, -1, -1, -1, 4]
    >>> update([-1, -1, 2, -1, -1, -1, -1, 3], 0.0, 5)
    [-1, -1, 3, -1, -1, -1, -1, 1]
    """
    n = len(highway_now)
    next_highway = [-1] * n

    for i in range(n):
        if highway_now[i] != -1:
            # Rule 1: Acceleration
            speed = min(highway_now[i] + 1, max_speed)
            # Rule 2: Slowing (distance to next car - 1)
            gap = get_distance(highway_now, i) - 1
            speed = min(speed, gap)
            # Rule 3: Randomization
            if random() < probability:
                speed = max(speed - 1, 0)
            next_highway[i] = speed
    return next_highway


def simulate(
    highway: list[list[int]], number_of_updates: int,
    probability: float, max_speed: int
) -> list[list[int]]:
    """
    Simulate the highway for a number of time steps.

    >>> simulate([[-1, 2, -1, -1, -1, 3]], 2, 0.0, 3)
    [[-1, 2, -1, -1, -1, 3], [-1, -1, -1, 2, -1, 0], [1, -1, -1, 0, -1, -1]]
    >>> simulate([[-1, 2, -1, 3]], 4, 0.0, 3)
    [[-1, 2, -1, 3], [-1, 0, -1, 0], [-1, 0, -1, 0], [-1, 0, -1, 0], [-1, 0, -1, 0]]
    """
    n = len(highway[0])

    for i in range(number_of_updates):
        # Update speeds
        new_speeds = update(highway[i], probability, max_speed)
        # Rule 4: Movement
        next_positions = [-1] * n
        for car_idx in range(n):
            speed = new_speeds[car_idx]
            if speed != -1:
                new_pos = (car_idx + speed) % n
                next_positions[new_pos] = speed
        highway.append(next_positions)

    return highway


def highway_to_string(highway: list[int]) -> str:
    """
    Convert highway state to a printable string.

    >>> highway_to_string([2, -1, -1, 0, -1, 3])
    '2..0.3'
    """
    return "".join(str(c) if c >= 0 else "." for c in highway)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print("Nagel-Schreckenberg Traffic Model")
    print("=" * 40)
    highway = construct_highway(30, 5, 0)
    result = simulate(highway, 15, 0.3, 5)
    for step, state in enumerate(result):
        print(f"t={step:>2}: {highway_to_string(state)}")
