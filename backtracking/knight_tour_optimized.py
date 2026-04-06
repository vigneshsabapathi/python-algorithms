"""
Knight Tour — Optimized implementations.

Variants:
1. Warnsdorff's Rule (greedy heuristic — O(n^2), near-instant)
2. Warnsdorff + Backtracking fallback (guaranteed solution)
3. Closed Knight Tour (returns to start)

Reference: https://en.wikipedia.org/wiki/Knight%27s_tour#Warnsdorff%27s_rule
"""

from __future__ import annotations

# All 8 L-shaped knight moves
KNIGHT_MOVES = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1),
]


def _on_board(y: int, x: int, n: int) -> bool:
    return 0 <= y < n and 0 <= x < n


def _unvisited_neighbors(
    y: int, x: int, n: int, board: list[list[int]]
) -> list[tuple[int, int]]:
    return [
        (y + dy, x + dx)
        for dy, dx in KNIGHT_MOVES
        if _on_board(y + dy, x + dx, n) and board[y + dy][x + dx] == 0
    ]


# ── Variant 1: Warnsdorff's Rule (pure greedy) ──────────────────────────


def _warnsdorff_key(
    p: tuple[int, int], n: int, board: list[list[int]]
) -> tuple[int, float]:
    """Sort key: (degree, -distance_from_center). Fewer moves first;
    ties broken by farthest from center (keeps knight near edges)."""
    degree = len(_unvisited_neighbors(p[0], p[1], n, board))
    center = (n - 1) / 2
    dist = (p[0] - center) ** 2 + (p[1] - center) ** 2
    return (degree, -dist)


def warnsdorff_tour(n: int, start: tuple[int, int] = (0, 0)) -> list[list[int]]:
    """
    Solve knight tour using Warnsdorff's heuristic: always move to the
    square with the fewest onward moves. Ties broken by farthest-from-center.
    Runs in O(n^2) — near-instant even for 100x100 boards.

    >>> warnsdorff_tour(1)
    [[1]]
    >>> warnsdorff_tour(5)[0][0]
    1
    >>> len(warnsdorff_tour(8))
    8
    """
    if n < 1:
        raise ValueError("Board size must be >= 1")
    if n == 1:
        return [[1]]

    board = [[0] * n for _ in range(n)]
    y, x = start
    board[y][x] = 1

    for step in range(2, n * n + 1):
        neighbors = _unvisited_neighbors(y, x, n, board)
        if not neighbors:
            msg = f"Warnsdorff heuristic stuck on board of size {n}"
            raise ValueError(msg)
        y, x = min(neighbors, key=lambda p: _warnsdorff_key(p, n, board))
        board[y][x] = step

    return board


# ── Variant 2: Warnsdorff + Backtracking (guaranteed) ───────────────────


def warnsdorff_backtrack(n: int, start: tuple[int, int] = (0, 0)) -> list[list[int]]:
    """
    Warnsdorff-ordered backtracking. Ties in degree are broken via DFS.
    Guaranteed to find a tour when one exists.

    >>> warnsdorff_backtrack(1)
    [[1]]
    >>> warnsdorff_backtrack(5)[0][0]
    1
    """
    if n < 1:
        raise ValueError("Board size must be >= 1")
    if n == 1:
        return [[1]]

    board = [[0] * n for _ in range(n)]
    board[start[0]][start[1]] = 1

    def solve(y: int, x: int, step: int) -> bool:
        if step == n * n:
            return True
        neighbors = _unvisited_neighbors(y, x, n, board)
        neighbors.sort(key=lambda p: _warnsdorff_key(p, n, board))
        for ny, nx in neighbors:
            board[ny][nx] = step + 1
            if solve(ny, nx, step + 1):
                return True
            board[ny][nx] = 0
        return False

    if solve(start[0], start[1], 1):
        return board

    msg = f"Knight tour not possible on board of size {n}"
    raise ValueError(msg)


# ── Variant 3: Closed Knight Tour (multi-start Warnsdorff) ────────────────


def closed_knight_tour(n: int) -> list[list[int]]:
    """
    Find a closed (re-entrant) knight tour where the last position is a
    knight's jump away from the starting square.

    Strategy: try Warnsdorff greedy from every starting cell. Since
    Warnsdorff runs in O(n^2), trying all n^2 starts is still O(n^4)
    worst-case but finishes quickly for practical sizes (up to ~30).

    >>> len(closed_knight_tour(6))
    6
    >>> len(closed_knight_tour(8))
    8
    """
    if n < 1:
        raise ValueError("Board size must be >= 1")
    if n == 1:
        return [[1]]

    for sy in range(n):
        for sx in range(n):
            board = [[0] * n for _ in range(n)]
            y, x = sy, sx
            board[y][x] = 1

            for step in range(2, n * n + 1):
                neighbors = _unvisited_neighbors(y, x, n, board)
                if not neighbors:
                    break
                y, x = min(neighbors, key=lambda p: _warnsdorff_key(p, n, board))
                board[y][x] = step
            else:
                # Tour complete — check if last cell connects to start
                if (sy - y, sx - x) in [(dy, dx) for dy, dx in KNIGHT_MOVES]:
                    return board

    msg = f"Closed knight tour not found for board of size {n}"
    raise ValueError(msg)


if __name__ == "__main__":
    import time

    sizes = [5, 6, 7, 8]
    print("=== Warnsdorff's Rule (greedy) ===")
    for n in sizes:
        t = time.perf_counter()
        board = warnsdorff_tour(n)
        print(f"  {n}x{n}: {time.perf_counter() - t:.6f}s")

    print("\n=== Warnsdorff + Backtracking ===")
    for n in sizes:
        t = time.perf_counter()
        board = warnsdorff_backtrack(n)
        print(f"  {n}x{n}: {time.perf_counter() - t:.6f}s")

    print("\n=== Closed Knight Tour ===")
    for n in [6, 8]:
        t = time.perf_counter()
        board = closed_knight_tour(n)
        elapsed = time.perf_counter() - t
        print(f"  {n}x{n}: {elapsed:.4f}s")
        for row in board:
            print("   ", row)

    # Run doctests
    import doctest
    doctest.testmod()
