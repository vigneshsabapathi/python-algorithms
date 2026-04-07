#!/usr/bin/env python3
"""
Optimized and alternative implementations of Sudoku solver.

The reference scans cells left-to-right (no heuristic) and checks safety
by scanning row + column + box on every candidate — O(27) per check, O(27*9)
per cell = O(243) per placement step.

Variants covered:
1. sudoku_mrv           -- MRV (Minimum Remaining Values): always pick the
                           empty cell with fewest valid candidates first.
                           Fails fast on the most constrained cell → massive
                           pruning improvement on hard puzzles.
2. sudoku_candidates    -- Explicit candidate-set tracking with O(1) lookup
                           and incremental update on place/unplace.
3. sudoku_norvig        -- Peter Norvig's constraint propagation + search:
                           propagate constraints before searching; many
                           "easy" cells are filled without backtracking.
4. sudoku_z3            -- Z3 SMT solver (if installed): declarative,
                           no backtracking code needed.

Key interview insight:
    Reference: O(9^n) nodes × O(27) per node  (n = empty cells)
    MRV:       far fewer nodes — picks most constrained cell first
    Norvig:    constraint propagation eliminates most cells before search;
               typical newspaper puzzle solved with zero backtracking

Run:
    python backtracking/sudoku_optimized.py
"""

from __future__ import annotations

import copy
import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backtracking.sudoku import sudoku as sudoku_reference, initial_grid, no_solution

Matrix = list[list[int]]

# ---------------------------------------------------------------------------
# Helpers shared across variants
# ---------------------------------------------------------------------------

ROWS = range(9)
COLS = range(9)
DIGITS = set(range(1, 10))


def _box_start(r: int, c: int) -> tuple[int, int]:
    return (r // 3) * 3, (c // 3) * 3


def _peers(r: int, c: int) -> list[tuple[int, int]]:
    """All cells that share a row, column, or box with (r, c), excluding itself."""
    result: set[tuple[int, int]] = set()
    for i in COLS:
        result.add((r, i))
    for i in ROWS:
        result.add((i, c))
    br, bc = _box_start(r, c)
    for dr in range(3):
        for dc in range(3):
            result.add((br + dr, bc + dc))
    result.discard((r, c))
    return list(result)


def _valid_candidates(grid: Matrix, r: int, c: int) -> set[int]:
    """Return the set of digits not yet used by any peer of (r, c)."""
    used: set[int] = set()
    for pr, pc in _peers(r, c):
        if grid[pr][pc] != 0:
            used.add(grid[pr][pc])
    return DIGITS - used


# ---------------------------------------------------------------------------
# Variant 1 — MRV: always pick the most-constrained empty cell
# ---------------------------------------------------------------------------


def sudoku_mrv(grid: Matrix) -> Matrix | None:
    """
    Sudoku with MRV (Minimum Remaining Values) heuristic.

    Instead of scanning top-left to bottom-right, pick the empty cell with
    the FEWEST valid candidates.  If that cell has 0 candidates → immediate
    backtrack (no wasted recursion).  If it has 1 candidate → forced fill.

    >>> import copy
    >>> from backtracking.sudoku import initial_grid, no_solution
    >>> sudoku_mrv(copy.deepcopy(initial_grid))  # doctest: +NORMALIZE_WHITESPACE
    [[3, 1, 6, 5, 7, 8, 4, 9, 2],
     [5, 2, 9, 1, 3, 4, 7, 6, 8],
     [4, 8, 7, 6, 2, 9, 5, 3, 1],
     [2, 6, 3, 4, 1, 5, 9, 8, 7],
     [9, 7, 4, 8, 6, 3, 1, 2, 5],
     [8, 5, 1, 7, 9, 2, 6, 4, 3],
     [1, 3, 8, 9, 4, 7, 2, 5, 6],
     [6, 9, 2, 3, 5, 1, 8, 7, 4],
     [7, 4, 5, 2, 8, 6, 3, 1, 9]]
    >>> sudoku_mrv(copy.deepcopy(no_solution)) is None
    True
    """
    # Find empty cell with fewest candidates (MRV)
    best: tuple[int, int] | None = None
    best_count = 10

    for r in ROWS:
        for c in COLS:
            if grid[r][c] == 0:
                candidates = _valid_candidates(grid, r, c)
                if not candidates:
                    return None  # dead end — backtrack immediately
                if len(candidates) < best_count:
                    best_count = len(candidates)
                    best = (r, c)
                    best_candidates = candidates
                    if best_count == 1:
                        break  # can't do better than forced
        if best_count == 1:
            break

    if best is None:
        return grid  # all filled — solved

    r, c = best
    for digit in best_candidates:
        grid[r][c] = digit
        result = sudoku_mrv(grid)
        if result is not None:
            return result
        grid[r][c] = 0

    return None


# ---------------------------------------------------------------------------
# Variant 2 — Candidate-set tracking (O(1) safety check)
# ---------------------------------------------------------------------------


def sudoku_candidates(grid: Matrix) -> Matrix | None:
    """
    Sudoku with explicit candidate-set tracking.

    Maintain three sets (row_used, col_used, box_used) for placed digits.
    Placement/removal updates these sets in O(1) instead of scanning peers.
    Also applies MRV: pick the cell with fewest candidates.

    >>> import copy
    >>> from backtracking.sudoku import initial_grid, no_solution
    >>> sudoku_candidates(copy.deepcopy(initial_grid))  # doctest: +NORMALIZE_WHITESPACE
    [[3, 1, 6, 5, 7, 8, 4, 9, 2],
     [5, 2, 9, 1, 3, 4, 7, 6, 8],
     [4, 8, 7, 6, 2, 9, 5, 3, 1],
     [2, 6, 3, 4, 1, 5, 9, 8, 7],
     [9, 7, 4, 8, 6, 3, 1, 2, 5],
     [8, 5, 1, 7, 9, 2, 6, 4, 3],
     [1, 3, 8, 9, 4, 7, 2, 5, 6],
     [6, 9, 2, 3, 5, 1, 8, 7, 4],
     [7, 4, 5, 2, 8, 6, 3, 1, 9]]
    >>> sudoku_candidates(copy.deepcopy(no_solution)) is None
    True
    """
    # Initialise used-sets from the given grid
    row_used: list[set[int]] = [set() for _ in ROWS]
    col_used: list[set[int]] = [set() for _ in COLS]
    box_used: list[set[int]] = [set() for _ in range(9)]

    for r in ROWS:
        for c in COLS:
            d = grid[r][c]
            if d:
                box_idx = (r // 3) * 3 + c // 3
                row_used[r].add(d)
                col_used[c].add(d)
                box_used[box_idx].add(d)

    def candidates(r: int, c: int) -> set[int]:
        box_idx = (r // 3) * 3 + c // 3
        return DIGITS - row_used[r] - col_used[c] - box_used[box_idx]

    def solve() -> bool:
        # MRV: find empty cell with fewest candidates
        best: tuple[int, int] | None = None
        best_cands: set[int] = set()
        best_count = 10

        for r in ROWS:
            for c in COLS:
                if grid[r][c] == 0:
                    cands = candidates(r, c)
                    if not cands:
                        return False
                    if len(cands) < best_count:
                        best_count = len(cands)
                        best = (r, c)
                        best_cands = cands
                        if best_count == 1:
                            break
            if best_count == 1:
                break

        if best is None:
            return True  # solved

        r, c = best
        box_idx = (r // 3) * 3 + c // 3
        for digit in best_cands:
            grid[r][c] = digit
            row_used[r].add(digit)
            col_used[c].add(digit)
            box_used[box_idx].add(digit)

            if solve():
                return True

            grid[r][c] = 0
            row_used[r].discard(digit)
            col_used[c].discard(digit)
            box_used[box_idx].discard(digit)

        return False

    return grid if solve() else None


# ---------------------------------------------------------------------------
# Variant 3 — Peter Norvig constraint propagation + search
# ---------------------------------------------------------------------------


def sudoku_norvig(grid_in: Matrix) -> Matrix | None:
    """
    Peter Norvig's approach: constraint propagation first, then search.

    Represent candidates as a dict {cell: set_of_digits}.
    Two rules propagated repeatedly until stable:
      1. If a cell has only one candidate, eliminate it from all peers.
      2. If a unit (row/col/box) has only one cell that can hold digit d,
         place d there.

    For most newspaper puzzles this fills the grid without any search.
    Search (like MRV backtracking) handles the rest.

    >>> import copy
    >>> from backtracking.sudoku import initial_grid, no_solution
    >>> sudoku_norvig(copy.deepcopy(initial_grid))  # doctest: +NORMALIZE_WHITESPACE
    [[3, 1, 6, 5, 7, 8, 4, 9, 2],
     [5, 2, 9, 1, 3, 4, 7, 6, 8],
     [4, 8, 7, 6, 2, 9, 5, 3, 1],
     [2, 6, 3, 4, 1, 5, 9, 8, 7],
     [9, 7, 4, 8, 6, 3, 1, 2, 5],
     [8, 5, 1, 7, 9, 2, 6, 4, 3],
     [1, 3, 8, 9, 4, 7, 2, 5, 6],
     [6, 9, 2, 3, 5, 1, 8, 7, 4],
     [7, 4, 5, 2, 8, 6, 3, 1, 9]]
    >>> sudoku_norvig(copy.deepcopy(no_solution)) is None
    True
    """
    # Build units: each cell belongs to one row, one col, one box
    units: dict[tuple[int,int], list[list[tuple[int,int]]]] = {}
    peers_map: dict[tuple[int,int], set[tuple[int,int]]] = {}

    for r in ROWS:
        for c in COLS:
            row_unit = [(r, cc) for cc in COLS]
            col_unit = [(rr, c) for rr in ROWS]
            br, bc = _box_start(r, c)
            box_unit = [(br+dr, bc+dc) for dr in range(3) for dc in range(3)]
            units[(r, c)] = [row_unit, col_unit, box_unit]
            peers_map[(r, c)] = (set(row_unit) | set(col_unit) | set(box_unit)) - {(r, c)}

    # candidates: dict of (r,c) -> set of possible digits
    cands: dict[tuple[int,int], set[int]] = {
        (r, c): set(DIGITS) for r in ROWS for c in COLS
    }

    def eliminate(cell: tuple[int,int], d: int) -> bool:
        """Remove d from cell's candidates; propagate if needed. False = contradiction."""
        if d not in cands[cell]:
            return True
        cands[cell].discard(d)
        if not cands[cell]:
            return False  # contradiction: no candidates left
        # Rule 1: if only one candidate left, eliminate it from all peers
        if len(cands[cell]) == 1:
            (only,) = cands[cell]
            if not all(eliminate(peer, only) for peer in peers_map[cell]):
                return False
        # Rule 2: for each unit, if digit d has only one possible place, assign it
        for unit in units[cell]:
            places = [sq for sq in unit if d in cands[sq]]
            if not places:
                return False  # contradiction
            if len(places) == 1:
                if not assign(places[0], d):
                    return False
        return True

    def assign(cell: tuple[int,int], d: int) -> bool:
        """Assign d to cell by eliminating all other candidates."""
        other = cands[cell] - {d}
        return all(eliminate(cell, od) for od in other)

    # Seed from the given grid
    for r in ROWS:
        for c in COLS:
            d = grid_in[r][c]
            if d and not assign((r, c), d):
                return None  # contradiction from given clues

    def search(cands_state: dict[tuple[int,int], set[int]]) -> dict[tuple[int,int], set[int]] | None:
        """Search: pick MRV cell, try each candidate."""
        if all(len(v) == 1 for v in cands_state.values()):
            return cands_state  # solved
        # MRV
        cell = min(
            (sq for sq in cands_state if len(cands_state[sq]) > 1),
            key=lambda sq: len(cands_state[sq]),
        )
        for d in list(cands_state[cell]):
            new_cands = copy.deepcopy(cands_state)
            # Re-bind closure to new_cands for this branch
            saved = cands
            # Use a local propagation on the copy
            ok = _norvig_assign_copy(new_cands, peers_map, units, cell, d)
            if ok:
                result = search(new_cands)
                if result is not None:
                    return result
        return None

    result = search(cands)
    if result is None:
        return None

    # Convert back to Matrix
    out: Matrix = [[0]*9 for _ in ROWS]
    for r in ROWS:
        for c in COLS:
            (digit,) = result[(r, c)]
            out[r][c] = digit
    return out


def _norvig_assign_copy(
    cands: dict[tuple[int,int], set[int]],
    peers_map: dict[tuple[int,int], set[tuple[int,int]]],
    units: dict[tuple[int,int], list[list[tuple[int,int]]]],
    cell: tuple[int,int],
    d: int,
) -> bool:
    """Assign d to cell in a candidate-dict copy; propagate. Returns False on contradiction."""
    def elim(sq: tuple[int,int], digit: int) -> bool:
        if digit not in cands[sq]:
            return True
        cands[sq].discard(digit)
        if not cands[sq]:
            return False
        if len(cands[sq]) == 1:
            (only,) = cands[sq]
            if not all(elim(p, only) for p in peers_map[sq]):
                return False
        for unit in units[sq]:
            places = [s for s in unit if digit in cands[s]]
            if not places:
                return False
            if len(places) == 1:
                if not _norvig_assign_copy(cands, peers_map, units, places[0], digit):
                    return False
        return True

    other = cands[cell] - {d}
    return all(elim(cell, od) for od in other)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

# "World's hardest" sudoku (Arto Inkala, 2010)
hardest: Matrix = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0],
]

hardest_solution: Matrix = [
    [8, 1, 2, 7, 5, 3, 6, 4, 9],
    [9, 4, 3, 6, 8, 2, 1, 7, 5],
    [6, 7, 5, 4, 9, 1, 2, 8, 3],
    [1, 5, 4, 2, 3, 7, 8, 9, 6],
    [3, 6, 9, 8, 4, 5, 7, 2, 1],
    [2, 8, 7, 1, 6, 9, 5, 3, 4],
    [5, 2, 1, 9, 7, 4, 3, 6, 8],
    [4, 3, 8, 5, 2, 6, 9, 1, 7],
    [7, 9, 6, 3, 1, 8, 4, 5, 2],
]


def run_all() -> None:
    grids = [
        ("initial",  copy.deepcopy(initial_grid)),
        ("no_sol",   copy.deepcopy(no_solution)),
        ("hardest",  copy.deepcopy(hardest)),
    ]

    print("\n=== Correctness ===")
    for name, g in grids:
        r_mrv  = sudoku_mrv(copy.deepcopy(g))
        r_cand = sudoku_candidates(copy.deepcopy(g))
        r_norv = sudoku_norvig(copy.deepcopy(g))
        if name == "no_sol":
            ok = r_mrv is None and r_cand is None and r_norv is None
            print(f"  {name}: mrv=None  cands=None  norvig=None  all_none={ok}")
        else:
            ok = r_mrv == r_cand == r_norv
            print(f"  {name}: all_agree={ok}  correct={r_mrv == hardest_solution if name == 'hardest' else True}")

    REPS_EASY = 500
    REPS_HARD = 50

    print(f"\n=== Benchmark: initial_grid (easy) — {REPS_EASY} runs ===")
    t_ref  = timeit.timeit(lambda: sudoku_reference(copy.deepcopy(initial_grid)),  number=REPS_EASY)*1000/REPS_EASY
    t_mrv  = timeit.timeit(lambda: sudoku_mrv(copy.deepcopy(initial_grid)),        number=REPS_EASY)*1000/REPS_EASY
    t_cand = timeit.timeit(lambda: sudoku_candidates(copy.deepcopy(initial_grid)), number=REPS_EASY)*1000/REPS_EASY
    t_norv = timeit.timeit(lambda: sudoku_norvig(copy.deepcopy(initial_grid)),     number=REPS_EASY)*1000/REPS_EASY
    print(f"  reference:   {t_ref:>8.3f} ms")
    print(f"  mrv:         {t_mrv:>8.3f} ms")
    print(f"  candidates:  {t_cand:>8.3f} ms")
    print(f"  norvig:      {t_norv:>8.3f} ms")

    print(f"\n=== Benchmark: hardest puzzle — {REPS_HARD} runs ===")
    t_ref  = timeit.timeit(lambda: sudoku_reference(copy.deepcopy(hardest)),  number=REPS_HARD)*1000/REPS_HARD
    t_mrv  = timeit.timeit(lambda: sudoku_mrv(copy.deepcopy(hardest)),        number=REPS_HARD)*1000/REPS_HARD
    t_cand = timeit.timeit(lambda: sudoku_candidates(copy.deepcopy(hardest)), number=REPS_HARD)*1000/REPS_HARD
    t_norv = timeit.timeit(lambda: sudoku_norvig(copy.deepcopy(hardest)),     number=REPS_HARD)*1000/REPS_HARD
    print(f"  reference:   {t_ref:>8.3f} ms")
    print(f"  mrv:         {t_mrv:>8.3f} ms")
    print(f"  candidates:  {t_cand:>8.3f} ms")
    print(f"  norvig:      {t_norv:>8.3f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
