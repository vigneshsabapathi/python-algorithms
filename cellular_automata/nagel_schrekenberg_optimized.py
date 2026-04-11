"""
Nagel-Schreckenberg Traffic Model - Optimized Variants with Benchmark
https://en.wikipedia.org/wiki/Nagel%E2%80%93Schreckenberg_model

Variant 1: list_based   - Pure Python lists, per-car loop
Variant 2: numpy_based  - NumPy arrays for vectorized speed updates
Variant 3: dict_based   - Sparse dict representation (car_index -> speed)
"""

from __future__ import annotations

import time
from random import random, seed as set_seed

import numpy as np


# ---- Variant 1: List-based ----
def simulate_list(
    highway: list[int], steps: int, probability: float, max_speed: int
) -> list[list[int]]:
    """
    Pure list-based simulation.

    >>> set_seed(0)
    >>> simulate_list([0, -1, -1, 0, -1, -1], 2, 0.0, 2)
    [[0, -1, -1, 0, -1, -1], [-1, 1, -1, -1, 1, -1], [-1, -1, 1, -1, -1, 1]]
    """
    n = len(highway)
    history = [highway[:]]

    for _ in range(steps):
        current = history[-1]
        new_speeds = [-1] * n

        for i in range(n):
            if current[i] == -1:
                continue
            # Find distance to next car
            dist = 0
            for d in range(1, n):
                idx = (i + d) % n
                if current[idx] != -1:
                    break
                dist += 1

            speed = min(current[i] + 1, max_speed)  # Accelerate
            speed = min(speed, dist - 1) if dist > 0 else 0  # Slow for gap
            if random() < probability:
                speed = max(speed - 1, 0)             # Random slowdown
            new_speeds[i] = speed

        # Move cars
        next_state = [-1] * n
        for i in range(n):
            if new_speeds[i] != -1:
                next_state[(i + new_speeds[i]) % n] = new_speeds[i]
        history.append(next_state)

    return history


# ---- Variant 2: NumPy-based ----
def simulate_numpy(
    highway: list[int], steps: int, probability: float, max_speed: int
) -> list[list[int]]:
    """
    NumPy-based simulation. Uses arrays for speed calculations.

    >>> set_seed(0)
    >>> simulate_numpy([0, -1, -1, 0, -1, -1], 2, 0.0, 2)
    [[0, -1, -1, 0, -1, -1], [-1, 1, -1, -1, 1, -1], [-1, -1, 1, -1, -1, 1]]
    """
    n = len(highway)
    current = np.array(highway, dtype=np.int8)
    history = [highway[:]]

    for _ in range(steps):
        car_mask = current != -1
        car_indices = np.where(car_mask)[0]

        new_speeds = np.full(n, -1, dtype=np.int8)

        for i in car_indices:
            # Distance to next car
            dist = 0
            for d in range(1, n):
                if current[(i + d) % n] != -1:
                    break
                dist += 1

            speed = min(int(current[i]) + 1, max_speed)
            speed = min(speed, dist - 1) if dist > 0 else 0
            if random() < probability:
                speed = max(speed - 1, 0)
            new_speeds[i] = speed

        # Move
        next_state = np.full(n, -1, dtype=np.int8)
        for i in car_indices:
            if new_speeds[i] != -1:
                next_state[(i + new_speeds[i]) % n] = new_speeds[i]

        current = next_state
        history.append(current.tolist())

    return history


# ---- Variant 3: Dict-based (sparse) ----
def simulate_dict(
    highway: list[int], steps: int, probability: float, max_speed: int
) -> list[list[int]]:
    """
    Sparse dict-based simulation. Only stores cars, not empty cells.
    Best for low-density highways.

    >>> set_seed(0)
    >>> simulate_dict([0, -1, -1, 0, -1, -1], 2, 0.0, 2)
    [[0, -1, -1, 0, -1, -1], [-1, 1, -1, -1, 1, -1], [-1, -1, 1, -1, -1, 1]]
    """
    n = len(highway)
    # Convert to dict: position -> speed
    cars = {i: highway[i] for i in range(n) if highway[i] != -1}
    history = [highway[:]]

    for _ in range(steps):
        sorted_positions = sorted(cars.keys())
        num_cars = len(sorted_positions)
        new_cars: dict[int, int] = {}

        for idx, pos in enumerate(sorted_positions):
            # Distance to next car (circular), minus 1 for safety
            next_pos = sorted_positions[(idx + 1) % num_cars]
            if next_pos > pos:
                gap = next_pos - pos - 1
            else:
                gap = (n - pos - 1) + next_pos
            dn = gap - 1  # Safety: can't occupy cell right before next car

            speed = min(cars[pos] + 1, max_speed)
            speed = min(speed, max(dn, 0))
            if random() < probability:
                speed = max(speed - 1, 0)

            new_pos = (pos + speed) % n
            new_cars[new_pos] = speed

        cars = new_cars
        state = [-1] * n
        for p, s in cars.items():
            state[p] = s
        history.append(state)

    return history


# ---- Benchmark ----
def benchmark(
    cells: int = 1000, density: int = 5, steps: int = 500,
    probability: float = 0.3, max_speed: int = 5
) -> None:
    """Run all three variants and compare performance."""
    # Build initial highway
    highway = [-1] * cells
    for i in range(0, cells, density):
        highway[i] = 0

    print(f"Nagel-Schreckenberg Benchmark")
    print(f"Cells: {cells}, Car spacing: {density}, Steps: {steps}, P: {probability}")
    print("=" * 55)

    set_seed(42)
    start = time.perf_counter()
    h1 = simulate_list(highway[:], steps, probability, max_speed)
    t1 = time.perf_counter() - start

    set_seed(42)
    start = time.perf_counter()
    h2 = simulate_numpy(highway[:], steps, probability, max_speed)
    t2 = time.perf_counter() - start

    set_seed(42)
    start = time.perf_counter()
    h3 = simulate_dict(highway[:], steps, probability, max_speed)
    t3 = time.perf_counter() - start

    print(f"{'Variant':<25} {'Time (s)':<12} {'Speedup'}")
    print("-" * 55)
    print(f"{'1. list_based':<25} {t1:<12.4f}")
    print(f"{'2. numpy_based':<25} {t2:<12.4f} {t1/t2:.1f}x")
    print(f"{'3. dict_based':<25} {t3:<12.4f} {t1/t3:.1f}x")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
