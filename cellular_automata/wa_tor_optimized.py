"""
Wa-Tor Predator-Prey Simulation - Optimized Variants with Benchmark
https://en.wikipedia.org/wiki/Wa-Tor

Variant 1: oop_based      - Object-oriented with Entity class per cell
Variant 2: numpy_grid     - NumPy arrays (type, energy, repro stored separately)
Variant 3: dict_sparse    - Sparse dict storing only occupied cells
"""

from __future__ import annotations

import time
from random import randint, random, seed as set_seed, shuffle

import numpy as np

# Constants
PREY_REPRO = 5
PRED_ENERGY = 15
PRED_FOOD = 5
PRED_REPRO = 20


# ---- Variant 1: OOP-based ----
class _Entity:
    __slots__ = ("prey", "row", "col", "repro", "energy", "alive")

    def __init__(self, prey: bool, row: int, col: int) -> None:
        self.prey = prey
        self.row = row
        self.col = col
        self.repro = PREY_REPRO if prey else PRED_REPRO
        self.energy = 0 if prey else PRED_ENERGY
        self.alive = True


def run_oop(
    width: int, height: int, prey_count: int, pred_count: int, steps: int
) -> list[tuple[int, int]]:
    """
    OOP-based simulation. Returns list of (prey_count, pred_count) per step.

    >>> set_seed(42)
    >>> h = run_oop(10, 10, 5, 3, 5)
    >>> len(h)
    5
    >>> all(isinstance(t, tuple) for t in h)
    True
    """
    grid: list[list[_Entity | None]] = [[None] * width for _ in range(height)]

    def add(prey: bool) -> None:
        while True:
            r, c = randint(0, height - 1), randint(0, width - 1)
            if grid[r][c] is None:
                grid[r][c] = _Entity(prey, r, c)
                return

    for _ in range(prey_count):
        add(True)
    for _ in range(pred_count):
        add(False)

    def adj(r: int, c: int) -> list[tuple[int, int]]:
        return [
            (nr, nc) for nr, nc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
            if 0 <= nr < height and 0 <= nc < width
        ]

    history = []
    for _ in range(steps):
        entities = [e for row in grid for e in row if e is not None]
        shuffle(entities)
        for e in entities:
            if not e.alive:
                continue
            nbrs = adj(e.row, e.col)
            shuffle(nbrs)

            if e.prey:
                # Move to empty
                for nr, nc in nbrs:
                    if grid[nr][nc] is None:
                        grid[nr][nc] = e
                        grid[e.row][e.col] = None
                        old_r, old_c = e.row, e.col
                        e.row, e.col = nr, nc
                        e.repro -= 1
                        if e.repro <= 0:
                            grid[old_r][old_c] = _Entity(True, old_r, old_c)
                            e.repro = PREY_REPRO
                        break
            else:
                if e.energy <= 0:
                    grid[e.row][e.col] = None
                    e.alive = False
                    continue
                # Try eat prey
                prey_nbrs = [(nr, nc) for nr, nc in nbrs
                             if grid[nr][nc] is not None and grid[nr][nc].prey]
                if prey_nbrs:
                    pr, pc = prey_nbrs[0]
                    grid[pr][pc].alive = False
                    grid[e.row][e.col] = None
                    grid[pr][pc] = e
                    e.row, e.col = pr, pc
                    e.energy += PRED_FOOD
                else:
                    for nr, nc in nbrs:
                        if grid[nr][nc] is None:
                            grid[nr][nc] = e
                            grid[e.row][e.col] = None
                            old_r, old_c = e.row, e.col
                            e.row, e.col = nr, nc
                            e.repro -= 1
                            if e.repro <= 0:
                                grid[old_r][old_c] = _Entity(False, old_r, old_c)
                                e.repro = PRED_REPRO
                            break
                e.energy -= 1

        ents = [e for row in grid for e in row if e is not None]
        pc = sum(1 for e in ents if e.prey)
        history.append((pc, len(ents) - pc))
    return history


# ---- Variant 2: NumPy grid ----
# Cell types: 0=empty, 1=prey, 2=predator
def run_numpy(
    width: int, height: int, prey_count: int, pred_count: int, steps: int
) -> list[tuple[int, int]]:
    """
    NumPy arrays store cell type, energy, and reproduction timer.
    Returns list of (prey_count, pred_count) per step.

    >>> set_seed(42)
    >>> h = run_numpy(10, 10, 5, 3, 5)
    >>> len(h)
    5
    """
    cell_type = np.zeros((height, width), dtype=np.int8)
    energy = np.zeros((height, width), dtype=np.int16)
    repro = np.zeros((height, width), dtype=np.int16)

    def add(ctype: int) -> None:
        while True:
            r, c = randint(0, height - 1), randint(0, width - 1)
            if cell_type[r, c] == 0:
                cell_type[r, c] = ctype
                energy[r, c] = PRED_ENERGY if ctype == 2 else 0
                repro[r, c] = PREY_REPRO if ctype == 1 else PRED_REPRO
                return

    for _ in range(prey_count):
        add(1)
    for _ in range(pred_count):
        add(2)

    def adj(r: int, c: int) -> list[tuple[int, int]]:
        return [
            (nr, nc) for nr, nc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
            if 0 <= nr < height and 0 <= nc < width
        ]

    history = []
    for _ in range(steps):
        coords = list(zip(*np.where(cell_type > 0)))
        shuffle(coords)
        for r, c in coords:
            ct = cell_type[r, c]
            if ct == 0:
                continue
            nbrs = adj(r, c)
            shuffle(nbrs)

            if ct == 1:  # prey
                for nr, nc in nbrs:
                    if cell_type[nr, nc] == 0:
                        cell_type[nr, nc] = 1
                        repro[nr, nc] = repro[r, c] - 1
                        if repro[r, c] <= 1:
                            cell_type[r, c] = 1
                            repro[r, c] = PREY_REPRO
                            repro[nr, nc] = PREY_REPRO
                        else:
                            cell_type[r, c] = 0
                        break
            else:  # predator
                if energy[r, c] <= 0:
                    cell_type[r, c] = 0
                    continue
                prey_nbrs = [(nr, nc) for nr, nc in nbrs if cell_type[nr][nc] == 1]
                if prey_nbrs:
                    pr, pc_ = prey_nbrs[0]
                    cell_type[pr, pc_] = 2
                    energy[pr, pc_] = energy[r, c] + PRED_FOOD - 1
                    repro[pr, pc_] = repro[r, c]
                    cell_type[r, c] = 0
                else:
                    for nr, nc in nbrs:
                        if cell_type[nr, nc] == 0:
                            cell_type[nr, nc] = 2
                            energy[nr, nc] = energy[r, c] - 1
                            repro[nr, nc] = repro[r, c] - 1
                            if repro[r, c] <= 1:
                                cell_type[r, c] = 2
                                energy[r, c] = PRED_ENERGY
                                repro[r, c] = PRED_REPRO
                                repro[nr, nc] = PRED_REPRO
                            else:
                                cell_type[r, c] = 0
                            break
                    else:
                        energy[r, c] -= 1

        pc = int((cell_type == 1).sum())
        dc = int((cell_type == 2).sum())
        history.append((pc, dc))
    return history


# ---- Variant 3: Dict sparse ----
def run_dict(
    width: int, height: int, prey_count: int, pred_count: int, steps: int
) -> list[tuple[int, int]]:
    """
    Sparse dict: only occupied cells stored.
    Good for low-density planets.
    Returns list of (prey_count, pred_count) per step.

    >>> set_seed(42)
    >>> h = run_dict(10, 10, 5, 3, 5)
    >>> len(h)
    5
    """
    # Dict: (row, col) -> (is_prey, energy, repro)
    cells: dict[tuple[int, int], tuple[bool, int, int]] = {}

    def add(prey: bool) -> None:
        while True:
            r, c = randint(0, height - 1), randint(0, width - 1)
            if (r, c) not in cells:
                cells[(r, c)] = (prey, 0 if prey else PRED_ENERGY,
                                 PREY_REPRO if prey else PRED_REPRO)
                return

    for _ in range(prey_count):
        add(True)
    for _ in range(pred_count):
        add(False)

    def adj(r: int, c: int) -> list[tuple[int, int]]:
        return [
            (nr, nc) for nr, nc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
            if 0 <= nr < height and 0 <= nc < width
        ]

    history = []
    for _ in range(steps):
        positions = list(cells.keys())
        shuffle(positions)
        for pos in positions:
            if pos not in cells:
                continue
            is_prey, en, rp = cells[pos]
            r, c = pos
            nbrs = adj(r, c)
            shuffle(nbrs)

            if is_prey:
                for nr, nc in nbrs:
                    if (nr, nc) not in cells:
                        rp -= 1
                        if rp <= 0:
                            cells[(nr, nc)] = (True, 0, PREY_REPRO)
                            cells[pos] = (True, 0, PREY_REPRO)
                        else:
                            cells[(nr, nc)] = (True, 0, rp)
                            del cells[pos]
                        break
            else:
                if en <= 0:
                    del cells[pos]
                    continue
                prey_n = [(nr, nc) for nr, nc in nbrs if (nr, nc) in cells and cells[(nr, nc)][0]]
                if prey_n:
                    pr, pc_ = prey_n[0]
                    cells[(pr, pc_)] = (False, en + PRED_FOOD - 1, rp)
                    del cells[pos]
                else:
                    for nr, nc in nbrs:
                        if (nr, nc) not in cells:
                            rp -= 1
                            if rp <= 0:
                                cells[(nr, nc)] = (False, en - 1, PRED_REPRO)
                                cells[pos] = (False, PRED_ENERGY, PRED_REPRO)
                            else:
                                cells[(nr, nc)] = (False, en - 1, rp)
                                del cells[pos]
                            break
                    else:
                        cells[pos] = (False, en - 1, rp)

        pc = sum(1 for v in cells.values() if v[0])
        history.append((pc, len(cells) - pc))
    return history


# ---- Benchmark ----
def benchmark(
    width: int = 30, height: int = 30,
    prey: int = 50, pred: int = 20, steps: int = 100
) -> None:
    """Run all three variants and compare."""
    print(f"Wa-Tor Simulation Benchmark")
    print(f"Grid: {width}x{height}, Prey: {prey}, Predators: {pred}, Steps: {steps}")
    print("=" * 55)

    set_seed(42)
    start = time.perf_counter()
    h1 = run_oop(width, height, prey, pred, steps)
    t1 = time.perf_counter() - start

    set_seed(42)
    start = time.perf_counter()
    h2 = run_numpy(width, height, prey, pred, steps)
    t2 = time.perf_counter() - start

    set_seed(42)
    start = time.perf_counter()
    h3 = run_dict(width, height, prey, pred, steps)
    t3 = time.perf_counter() - start

    print(f"{'Variant':<25} {'Time (s)':<12} {'Final prey':<12} {'Final pred':<12} {'Speedup'}")
    print("-" * 65)
    print(f"{'1. oop_based':<25} {t1:<12.4f} {h1[-1][0]:<12} {h1[-1][1]:<12}")
    print(f"{'2. numpy_grid':<25} {t2:<12.4f} {h2[-1][0]:<12} {h2[-1][1]:<12} {t1/t2:.1f}x")
    print(f"{'3. dict_sparse':<25} {t3:<12.4f} {h3[-1][0]:<12} {h3[-1][1]:<12} {t1/t3:.1f}x")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
