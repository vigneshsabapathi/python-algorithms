#!/usr/bin/env python3
"""
Optimized and alternative implementations of Minimax.

The reference minimax explores the ENTIRE game tree — O(b^d) nodes where
b = branching factor, d = depth.  These variants reduce that cost:

1. minimax_alphabeta     -- Alpha-Beta pruning: same result, up to O(b^(d/2))
                            nodes in the best case (perfect move ordering).
2. minimax_alphabeta_ids -- Alpha-Beta + Iterative Deepening (IDS): depth-first
                            search repeated at increasing depths; enables a
                            time-limited search and improves move ordering.
3. minimax_negamax       -- Negamax formulation: cleaner code, same result.
                            Collapses max/min into a single sign flip.
4. best_move             -- Wrapper returning the actual best move index,
                            not just the score.

Key interview insight:
    Pure minimax:   O(b^d) nodes
    Alpha-beta:     O(b^(d/2)) best case (perfect ordering) → same depth, sqrt nodes
                    O(b^d)     worst case (reverse ordering)
    In practice:    ~O(b^(3d/4)) with random ordering — roughly halves depth searchable
    For chess (b≈35, d=6): minimax=1.8B nodes; alpha-beta≈~58M best case.

Run:
    python backtracking/minimax_optimized.py
"""

from __future__ import annotations

import math
import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backtracking.minimax import minimax


# ---------------------------------------------------------------------------
# Variant 1 — Alpha-Beta Pruning
# ---------------------------------------------------------------------------


def minimax_alphabeta(
    depth: int,
    node_index: int,
    is_max: bool,
    scores: list[int],
    height: float,
    alpha: int = -math.inf,
    beta: int = math.inf,
) -> int:
    """
    Minimax with Alpha-Beta pruning.

    alpha: best score the maximizer can guarantee so far (lower bound)
    beta:  best score the minimizer can guarantee so far (upper bound)

    A branch is pruned when alpha >= beta:
    - Maximizer finds a move better than beta → minimizer would never allow it → prune
    - Minimizer finds a move worse than alpha → maximizer would never allow it → prune

    Produces identical results to plain minimax.

    >>> import math
    >>> scores = [90, 23, 6, 33, 21, 65, 123, 34423]
    >>> height = math.log(len(scores), 2)
    >>> minimax_alphabeta(0, 0, True, scores, height)
    65
    >>> scores = [3, 5, 2, 9, 12, 5, 23, 23]
    >>> height = math.log(len(scores), 2)
    >>> minimax_alphabeta(0, 0, True, scores, height)
    12
    >>> minimax_alphabeta(0, 0, False, scores, height)
    3
    """
    if depth == height:
        return scores[node_index]

    if is_max:
        best = -math.inf
        for i in range(2):
            val = minimax_alphabeta(
                depth + 1, node_index * 2 + i, False, scores, height, alpha, beta
            )
            best = max(best, val)
            alpha = max(alpha, best)
            if alpha >= beta:
                break  # beta cut-off: minimizer won't allow this
        return best
    else:
        best = math.inf
        for i in range(2):
            val = minimax_alphabeta(
                depth + 1, node_index * 2 + i, True, scores, height, alpha, beta
            )
            best = min(best, val)
            beta = min(beta, best)
            if alpha >= beta:
                break  # alpha cut-off: maximizer won't allow this
        return best


# ---------------------------------------------------------------------------
# Variant 2 — Negamax (cleaner formulation of minimax)
# ---------------------------------------------------------------------------


def minimax_negamax(
    depth: int,
    node_index: int,
    scores: list[int],
    height: float,
    alpha: int = -math.inf,
    beta: int = math.inf,
    color: int = 1,
) -> int:
    """
    Negamax with Alpha-Beta: unifies max/min into a single recursive form.

    Instead of alternating is_max, negate the score and swap the perspective
    on every call.  color = +1 for maximizer, -1 for minimizer.

    Produces identical results to plain minimax (from maximizer's perspective).

    >>> import math
    >>> scores = [90, 23, 6, 33, 21, 65, 123, 34423]
    >>> height = math.log(len(scores), 2)
    >>> minimax_negamax(0, 0, scores, height)
    65
    >>> scores = [3, 5, 2, 9, 12, 5, 23, 23]
    >>> height = math.log(len(scores), 2)
    >>> minimax_negamax(0, 0, scores, height)
    12
    """
    if depth == height:
        return color * scores[node_index]

    best = -math.inf
    for i in range(2):
        val = -minimax_negamax(
            depth + 1, node_index * 2 + i, scores, height, -beta, -alpha, -color
        )
        best = max(best, val)
        alpha = max(alpha, best)
        if alpha >= beta:
            break
    return best


# ---------------------------------------------------------------------------
# Variant 3 — Alpha-Beta + Iterative Deepening (IDS)
# ---------------------------------------------------------------------------


def minimax_alphabeta_ids(
    scores: list[int],
    max_depth: int,
    is_max: bool = True,
) -> tuple[int, int]:
    """
    Alpha-Beta with Iterative Deepening Search (IDS).

    Searches depth 1, 2, ..., max_depth in succession.  Each depth is a
    complete alpha-beta search.  Benefits:
    - Shallowest result available immediately (for time-limited search)
    - Shallower searches improve move ordering for deeper ones
    - Total cost dominated by the last (deepest) iteration: O(b^d)

    Returns (optimal_score, nodes_visited_at_final_depth).

    >>> import math
    >>> scores = [90, 23, 6, 33, 21, 65, 123, 34423]
    >>> score, _ = minimax_alphabeta_ids(scores, int(math.log(len(scores), 2)))
    >>> score
    65
    >>> scores = [3, 5, 2, 9, 12, 5, 23, 23]
    >>> score, _ = minimax_alphabeta_ids(scores, int(math.log(len(scores), 2)))
    >>> score
    12
    """
    height = math.log(len(scores), 2)
    nodes_visited = 0
    best_score = 0

    for d in range(1, max_depth + 1):
        partial_height = min(d, height)
        counter = [0]

        def _ab(dep: int, idx: int, is_mx: bool, a: float, b: float) -> int:
            counter[0] += 1
            if dep == partial_height:
                return scores[idx]
            if is_mx:
                best = -math.inf
                for i in range(2):
                    val = _ab(dep + 1, idx * 2 + i, False, a, b)
                    best = max(best, val)
                    a = max(a, best)
                    if a >= b:
                        break
                return best
            else:
                best = math.inf
                for i in range(2):
                    val = _ab(dep + 1, idx * 2 + i, True, a, b)
                    best = min(best, val)
                    b = min(b, best)
                    if a >= b:
                        break
                return best

        best_score = _ab(0, 0, is_max, -math.inf, math.inf)
        nodes_visited = counter[0]

    return best_score, nodes_visited


# ---------------------------------------------------------------------------
# Variant 4 — best_move: return move index, not just score
# ---------------------------------------------------------------------------


def best_move(
    scores: list[int],
    is_max: bool = True,
) -> tuple[int, int]:
    """
    Return the (best_score, best_child_index) from the root's children.
    Uses alpha-beta internally.

    >>> scores = [90, 23, 6, 33, 21, 65, 123, 34423]
    >>> best_move(scores)
    (65, 1)

    >>> scores = [3, 5, 2, 9, 12, 5, 23, 23]
    >>> best_move(scores)
    (12, 1)
    """
    height = math.log(len(scores), 2)
    best_val = -math.inf if is_max else math.inf
    best_idx = 0

    for child in range(2):
        val = minimax_alphabeta(1, child, not is_max, scores, height)
        if is_max and val > best_val:
            best_val, best_idx = val, child
        elif not is_max and val < best_val:
            best_val, best_idx = val, child

    return best_val, best_idx


# ---------------------------------------------------------------------------
# Node-count instrumentation: measure pruning efficiency
# ---------------------------------------------------------------------------


def count_nodes_minimax(
    depth: int, node_index: int, is_max: bool, scores: list[int], height: float
) -> tuple[int, int]:
    """Return (score, nodes_visited) for plain minimax."""
    if depth == height:
        return scores[node_index], 1
    results = [
        count_nodes_minimax(depth + 1, node_index * 2 + i, not is_max, scores, height)
        for i in range(2)
    ]
    scores_only = [r[0] for r in results]
    total_nodes = sum(r[1] for r in results) + 1
    score = max(scores_only) if is_max else min(scores_only)
    return score, total_nodes


def count_nodes_alphabeta(
    depth: int,
    node_index: int,
    is_max: bool,
    scores: list[int],
    height: float,
    alpha: float = -math.inf,
    beta: float = math.inf,
) -> tuple[int, int]:
    """Return (score, nodes_visited) for alpha-beta."""
    if depth == height:
        return scores[node_index], 1
    counter = [0]

    if is_max:
        best = -math.inf
        for i in range(2):
            val, n = count_nodes_alphabeta(
                depth + 1, node_index * 2 + i, False, scores, height, alpha, beta
            )
            counter[0] += n
            best = max(best, val)
            alpha = max(alpha, best)
            if alpha >= beta:
                break
    else:
        best = math.inf
        for i in range(2):
            val, n = count_nodes_alphabeta(
                depth + 1, node_index * 2 + i, True, scores, height, alpha, beta
            )
            counter[0] += n
            best = min(best, val)
            beta = min(beta, best)
            if alpha >= beta:
                break

    return best, counter[0] + 1


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------


def run_all() -> None:
    import random
    random.seed(42)

    test_cases: list[tuple[str, list[int]]] = [
        ("reference", [90, 23, 6, 33, 21, 65, 123, 34423]),
        ("second",    [3, 5, 2, 9, 12, 5, 23, 23]),
    ]

    print("\n=== Correctness ===")
    for name, scores in test_cases:
        h = math.log(len(scores), 2)
        r0 = minimax(0, 0, True, scores, h)
        r1 = minimax_alphabeta(0, 0, True, scores, h)
        r2 = minimax_negamax(0, 0, scores, h)
        r3, _ = minimax_alphabeta_ids(scores, int(h))
        bm, bi = best_move(scores)
        ok = r0 == r1 == r2 == r3 == bm
        print(f"  {name}: score={r0}  ab={r1}  negamax={r2}  ids={r3}  "
              f"best_move=({bm}, child={bi})  match={ok}")

    print("\n=== Pruning efficiency (nodes visited) ===")
    print(f"  {'depth':>6}  {'leaves':>8}  {'minimax':>10}  {'alpha-beta':>12}  "
          f"{'pruned%':>9}")
    for d in [3, 4, 5, 6, 7, 8]:
        n_leaves = 2 ** d
        scores_rand = [random.randint(0, 1000) for _ in range(n_leaves)]
        h = float(d)
        _, mm_nodes = count_nodes_minimax(0, 0, True, scores_rand, h)
        _, ab_nodes = count_nodes_alphabeta(0, 0, True, scores_rand, h)
        pruned_pct = 100 * (1 - ab_nodes / mm_nodes)
        print(f"  {d:>6}  {n_leaves:>8}  {mm_nodes:>10}  {ab_nodes:>12}  "
              f"{pruned_pct:>8.1f}%")

    REPS = 5000
    scores_bench = [90, 23, 6, 33, 21, 65, 123, 34423]
    h_bench = math.log(len(scores_bench), 2)

    print(f"\n=== Benchmark ({REPS} runs each, depth=3) ===")
    t0 = timeit.timeit(
        lambda: minimax(0, 0, True, scores_bench, h_bench), number=REPS
    ) * 1e6 / REPS
    t1 = timeit.timeit(
        lambda: minimax_alphabeta(0, 0, True, scores_bench, h_bench), number=REPS
    ) * 1e6 / REPS
    t2 = timeit.timeit(
        lambda: minimax_negamax(0, 0, scores_bench, h_bench), number=REPS
    ) * 1e6 / REPS
    t3 = timeit.timeit(
        lambda: minimax_alphabeta_ids(scores_bench, int(h_bench)), number=REPS
    ) * 1e6 / REPS
    print(f"  minimax:      {t0:>8.2f} us")
    print(f"  alpha-beta:   {t1:>8.2f} us")
    print(f"  negamax:      {t2:>8.2f} us")
    print(f"  ids:          {t3:>8.2f} us")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
