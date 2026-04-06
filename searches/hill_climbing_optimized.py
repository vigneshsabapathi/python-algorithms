#!/usr/bin/env python3

"""
Optimized and alternative implementations of hill climbing.

Variants covered:
1. hill_climbing_stochastic     — picks a RANDOM improving neighbor instead of
                                  the steepest one; faster per iteration, escapes
                                  some plateaus better
2. hill_climbing_random_restart — runs steepest-ascent multiple times from
                                  random starting points; best practical fix for
                                  local optima
3. scipy_minimize               — scipy.optimize.minimize (Nelder-Mead / BFGS)
                                  as the production-quality baseline

Run benchmarks:
    python searches/hill_climbing_optimized.py
"""

from __future__ import annotations

import math
import random
import timeit
from typing import Callable

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from searches.hill_climbing import SearchProblem, hill_climbing


# ---------------------------------------------------------------------------
# Variant 1 — stochastic hill climbing
# ---------------------------------------------------------------------------


def hill_climbing_stochastic(
    search_prob: SearchProblem,
    find_max: bool = True,
    max_x: float = math.inf,
    min_x: float = -math.inf,
    max_y: float = math.inf,
    min_y: float = -math.inf,
    max_iter: int = 10000,
) -> SearchProblem:
    """
    Stochastic hill climbing: at each step pick a RANDOM improving neighbor
    instead of the steepest one.

    Advantages over steepest-ascent:
    - Each iteration is O(1) instead of O(k) where k=8 neighbors
    - Can escape ridges where steepest-ascent oscillates

    Disadvantage: may take more steps to reach the local optimum.
    """
    current_state = search_prob
    visited: set[SearchProblem] = set()

    for _ in range(max_iter):
        visited.add(current_state)
        current_score = current_state.score()

        improving = []
        for nb in current_state.get_neighbors():
            if nb in visited:
                continue
            if nb.x > max_x or nb.x < min_x or nb.y > max_y or nb.y < min_y:
                continue
            change = nb.score() - current_score
            if (find_max and change > 0) or (not find_max and change < 0):
                improving.append(nb)

        if not improving:
            break
        current_state = random.choice(improving)

    return current_state


# ---------------------------------------------------------------------------
# Variant 2 — random-restart hill climbing
# ---------------------------------------------------------------------------


def hill_climbing_random_restart(
    function_to_optimize: Callable[[float, float], float],
    find_max: bool = True,
    max_x: float = 10.0,
    min_x: float = -10.0,
    max_y: float = 10.0,
    min_y: float = -10.0,
    step_size: float = 1.0,
    restarts: int = 20,
    max_iter_per_restart: int = 1000,
    seed: int | None = None,
) -> SearchProblem:
    """
    Random-restart hill climbing: runs steepest-ascent hill climbing
    `restarts` times from uniformly random starting points and returns
    the best result.

    This is the standard practical fix for local optima — with enough
    restarts it converges to the global optimum in probability.

    Args:
        function_to_optimize: f(x, y) to maximise or minimise.
        find_max: True to maximise, False to minimise.
        max_x, min_x, max_y, min_y: search bounds.
        step_size: step size for each search.
        restarts: number of random restarts.
        max_iter_per_restart: max iterations per single climb.
        seed: random seed for reproducibility.

    Returns:
        The best SearchProblem found across all restarts.
    """
    rng = random.Random(seed)
    best: SearchProblem | None = None

    for _ in range(restarts):
        start_x = rng.uniform(min_x, max_x)
        start_y = rng.uniform(min_y, max_y)
        prob = SearchProblem(start_x, start_y, step_size, function_to_optimize)
        result = hill_climbing(
            prob,
            find_max=find_max,
            max_x=max_x,
            min_x=min_x,
            max_y=max_y,
            min_y=min_y,
            max_iter=max_iter_per_restart,
        )
        if best is None:
            best = result
        elif find_max and result.score() > best.score():
            best = result
        elif not find_max and result.score() < best.score():
            best = result

    return best  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Variant 3 — scipy.optimize baseline
# ---------------------------------------------------------------------------


def scipy_minimize(
    function_to_optimize: Callable[[float, float], float],
    x0: float = 0.0,
    y0: float = 0.0,
    find_max: bool = False,
    method: str = "Nelder-Mead",
) -> tuple[float, float, float]:
    """
    Wraps scipy.optimize.minimize for continuous 2D optimisation.

    Returns (x, y, score) of the found optimum.

    Note: scipy minimises by default; for maximisation we negate the function.
    """
    from scipy.optimize import minimize

    sign = -1 if find_max else 1
    obj = lambda xy: sign * function_to_optimize(xy[0], xy[1])
    res = minimize(obj, [x0, y0], method=method)
    x, y = res.x
    return x, y, function_to_optimize(x, y)


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------


def benchmark() -> None:
    import timeit

    # Test function: bowl — global min at (0,0), global max is unbounded
    def f_bowl(x, y):
        return x**2 + y**2

    # Test function: multi-modal — multiple local minima
    def f_multimodal(x, y):
        return math.sin(x) * math.cos(y) + 0.1 * (x**2 + y**2)

    RESTARTS = 10
    REPS = 20

    print("\n=== Benchmark: find_min of f(x,y)=x^2+y^2 from (5,5) ===")
    prob = SearchProblem(5, 5, 1, f_bowl)

    t1 = timeit.timeit(
        lambda: hill_climbing(SearchProblem(5, 5, 1, f_bowl), find_max=False),
        number=REPS,
    )
    print(f"  steepest-ascent           {t1*1000/REPS:8.3f} ms/run")

    t2 = timeit.timeit(
        lambda: hill_climbing_stochastic(SearchProblem(5, 5, 1, f_bowl), find_max=False),
        number=REPS,
    )
    print(f"  stochastic                {t2*1000/REPS:8.3f} ms/run")

    t3 = timeit.timeit(
        lambda: hill_climbing_random_restart(
            f_bowl, find_max=False, max_x=10, min_x=-10, max_y=10, min_y=-10,
            restarts=RESTARTS, seed=42,
        ),
        number=REPS,
    )
    print(f"  random-restart ({RESTARTS}x)     {t3*1000/REPS:8.3f} ms/run")

    try:
        t4 = timeit.timeit(
            lambda: scipy_minimize(f_bowl, 5, 5, find_max=False),
            number=REPS,
        )
        print(f"  scipy Nelder-Mead         {t4*1000/REPS:8.3f} ms/run")
    except ImportError:
        print("  scipy not installed — skipping")

    print("\n=== Quality check: multimodal f(x,y)=sin(x)*cos(y)+0.1*(x^2+y^2) ===")
    print("  (multiple local minima — random restart should find a better minimum)")
    prob = SearchProblem(3, 3, 0.5, f_multimodal)
    r_steepest = hill_climbing(prob, find_max=False)
    r_restart = hill_climbing_random_restart(
        f_multimodal, find_max=False, max_x=5, min_x=-5, max_y=5, min_y=-5,
        step_size=0.5, restarts=20, seed=0,
    )
    print(f"  steepest-ascent:   {r_steepest}, score={r_steepest.score():.4f}")
    print(f"  random-restart:    {r_restart}, score={r_restart.score():.4f}")
    try:
        sx, sy, ss = scipy_minimize(f_multimodal, 3, 3, find_max=False)
        print(f"  scipy Nelder-Mead: x={sx:.4f} y={sy:.4f} score={ss:.4f}")
    except ImportError:
        pass


if __name__ == "__main__":
    benchmark()
