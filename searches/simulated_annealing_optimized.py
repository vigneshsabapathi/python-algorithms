#!/usr/bin/env python3

"""
Optimized and alternative implementations of Simulated Annealing.

Bug fix in this file:
    The reference implementation's best_state tracking always picks the state
    with the highest score regardless of find_max. When find_max=False (finding
    minimum), best_state should track the state with the LOWEST score.

Variants covered:
1. simulated_annealing_fixed      — original algorithm with best_state bug fixed
2. simulated_annealing_exp_cool   — exponential (multiplicative) cooling schedule
                                    (more principled than additive-fraction cooling)
3. scipy_dual_annealing           — scipy.optimize.dual_annealing (production SA)

Run:
    python searches/simulated_annealing_optimized.py
"""

from __future__ import annotations

import math
import random
import timeit
from typing import Callable

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from searches.hill_climbing import SearchProblem
from searches.simulated_annealing import simulated_annealing


# ---------------------------------------------------------------------------
# Variant 1 — fixed SA (best_state bug corrected)
# ---------------------------------------------------------------------------


def simulated_annealing_fixed(
    search_prob: SearchProblem,
    find_max: bool = True,
    max_x: float = math.inf,
    min_x: float = -math.inf,
    max_y: float = math.inf,
    min_y: float = -math.inf,
    start_temp: float = 100.0,
    cooling_rate: float = 0.01,
    threshold_temp: float = 1.0,
) -> SearchProblem:
    """
    Simulated annealing with the best_state tracking bug fixed.

    Bug in original: best_state was updated with `current_score > best_state.score()`
    unconditionally, which always tracks the MAX regardless of find_max.

    Fix: use find_max to decide whether to keep the higher or lower score.

    Cooling schedule: geometric — temp *= (1 - cooling_rate) each iteration.
    This is equivalent to the original `temp -= temp * rate`.

    Args:
        search_prob: starting state.
        find_max: True to find maximum, False for minimum.
        max_x, min_x, max_y, min_y: search bounds.
        start_temp: initial temperature.
        cooling_rate: fraction by which temp is reduced each step.
        threshold_temp: stop when temp falls below this.

    Returns:
        The best SearchProblem state seen during the search.
    """
    current_state = search_prob
    current_temp = start_temp
    best_state: SearchProblem | None = None

    while True:
        current_score = current_state.score()

        # FIX: track best seen state correctly for both find_max and find_min
        if best_state is None:
            best_state = current_state
        elif find_max and current_score > best_state.score():
            best_state = current_state
        elif not find_max and current_score < best_state.score():
            best_state = current_state

        neighbors = current_state.get_neighbors()
        next_state: SearchProblem | None = None

        while next_state is None and neighbors:
            idx = random.randint(0, len(neighbors) - 1)
            candidate = neighbors.pop(idx)

            if (
                candidate.x > max_x
                or candidate.x < min_x
                or candidate.y > max_y
                or candidate.y < min_y
            ):
                continue

            delta = candidate.score() - current_score
            if not find_max:
                delta = -delta  # flip: positive delta = improvement for minimisation

            if delta > 0:
                next_state = candidate
            else:
                probability = math.exp(delta / current_temp)
                if random.random() < probability:
                    next_state = candidate

        current_temp *= 1 - cooling_rate

        if current_temp < threshold_temp or next_state is None:
            break
        current_state = next_state

    return best_state  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Variant 2 — exponential cooling (time-based)
# ---------------------------------------------------------------------------


def simulated_annealing_exp_cool(
    search_prob: SearchProblem,
    find_max: bool = True,
    max_x: float = math.inf,
    min_x: float = -math.inf,
    max_y: float = math.inf,
    min_y: float = -math.inf,
    start_temp: float = 100.0,
    alpha: float = 0.95,
    max_iter: int = 1000,
) -> SearchProblem:
    """
    Simulated annealing with explicit exponential cooling:
        T(k) = T0 * alpha^k   (alpha typically 0.90 – 0.99)

    This makes the temperature schedule independent of iteration timing and
    gives a more principled decay. max_iter controls total steps.

    Args:
        search_prob: starting state.
        find_max: True to maximise, False to minimise.
        max_x, min_x, max_y, min_y: search bounds.
        start_temp: T0.
        alpha: cooling factor per iteration (0 < alpha < 1).
        max_iter: maximum number of iterations.

    Returns:
        Best SearchProblem state seen.
    """
    current_state = search_prob
    best_state = current_state

    for k in range(max_iter):
        current_temp = start_temp * (alpha**k)
        if current_temp < 1e-10:
            break

        current_score = current_state.score()
        if find_max and current_score > best_state.score():
            best_state = current_state
        elif not find_max and current_score < best_state.score():
            best_state = current_state

        neighbors = [
            nb
            for nb in current_state.get_neighbors()
            if min_x <= nb.x <= max_x and min_y <= nb.y <= max_y
        ]
        if not neighbors:
            break

        candidate = random.choice(neighbors)
        delta = candidate.score() - current_score
        if not find_max:
            delta = -delta

        if delta > 0 or random.random() < math.exp(delta / current_temp):
            current_state = candidate

    return best_state


# ---------------------------------------------------------------------------
# Variant 3 — scipy.optimize.dual_annealing
# ---------------------------------------------------------------------------


def scipy_dual_annealing(
    function_to_optimize: Callable[[float, float], float],
    find_max: bool = False,
    min_x: float = -10.0,
    max_x: float = 10.0,
    min_y: float = -10.0,
    max_y: float = 10.0,
    seed: int | None = 42,
) -> tuple[float, float, float]:
    """
    scipy.optimize.dual_annealing — production-quality SA implementation.

    Uses a generalised simulated annealing (Tsallis statistics) combined with
    a local minimizer for the best-of-both-worlds approach.

    Args:
        function_to_optimize: f(x, y).
        find_max: if True, negates the function to convert max→min for scipy.
        min_x, max_x, min_y, max_y: search bounds (required by dual_annealing).
        seed: for reproducibility.

    Returns:
        (x, y, score) of the found optimum.
    """
    from scipy.optimize import dual_annealing

    sign = -1 if find_max else 1
    obj = lambda xy: sign * function_to_optimize(xy[0], xy[1])
    bounds = [(min_x, max_x), (min_y, max_y)]
    result = dual_annealing(obj, bounds, seed=seed)
    x, y = result.x
    return x, y, function_to_optimize(x, y)


# ---------------------------------------------------------------------------
# Benchmark + correctness check
# ---------------------------------------------------------------------------


def run_all() -> None:
    def f_bowl(x: float, y: float) -> float:
        """x^2 + y^2 — global min=0 at (0,0), unbounded max."""
        return x**2 + y**2

    def f_multimodal(x: float, y: float) -> float:
        """Multimodal — multiple local minima."""
        return math.sin(x) * math.cos(y) + 0.1 * (x**2 + y**2)

    REPS = 30
    random.seed(0)

    # -------------------------------------------------------------------
    print("\n=== Bug demonstration: find_min, f=x^2+y^2, bounds x in [5,100] y in [-5,50] ===")
    print("  Optimal min = 25 at (5, 0)\n")

    prob = SearchProblem(x=12, y=47, step_size=1, function_to_optimize=f_bowl)
    orig = simulated_annealing(prob, find_max=False, max_x=100, min_x=5, max_y=50, min_y=-5)
    print(f"  Original SA (buggy best_state): score={orig.score()}")

    prob = SearchProblem(x=12, y=47, step_size=1, function_to_optimize=f_bowl)
    fixed = simulated_annealing_fixed(prob, find_max=False, max_x=100, min_x=5, max_y=50, min_y=-5)
    print(f"  Fixed SA:                       score={fixed.score()}  (should be near 25)")

    # -------------------------------------------------------------------
    print("\n=== Correctness: find_max, f=x^2+y^2, bounds x in [5,100] y in [-5,50] ===")
    print("  Optimal max = 12500 at (100, 50) or (100, -5)\n")

    prob = SearchProblem(x=12, y=47, step_size=1, function_to_optimize=f_bowl)
    orig_max = simulated_annealing(prob, find_max=True, max_x=100, min_x=5, max_y=50, min_y=-5)
    print(f"  Original SA find_max:  score={orig_max.score()}")

    prob = SearchProblem(x=12, y=47, step_size=1, function_to_optimize=f_bowl)
    fixed_max = simulated_annealing_fixed(prob, find_max=True, max_x=100, min_x=5, max_y=50, min_y=-5)
    print(f"  Fixed SA find_max:     score={fixed_max.score()}")

    # -------------------------------------------------------------------
    print("\n=== Multimodal quality: f=sin(x)*cos(y)+0.1*(x^2+y^2), find_min ===")

    prob = SearchProblem(x=3, y=3, step_size=1, function_to_optimize=f_multimodal)
    r_fixed = simulated_annealing_fixed(prob, find_max=False, max_x=10, min_x=-10,
                                         max_y=10, min_y=-10, start_temp=200, cooling_rate=0.005)
    print(f"  SA fixed:              {r_fixed}, score={r_fixed.score():.4f}")

    prob = SearchProblem(x=3, y=3, step_size=1, function_to_optimize=f_multimodal)
    r_exp = simulated_annealing_exp_cool(prob, find_max=False, max_x=10, min_x=-10,
                                          max_y=10, min_y=-10, start_temp=100, alpha=0.97, max_iter=2000)
    print(f"  SA exp cooling:        {r_exp}, score={r_exp.score():.4f}")

    try:
        sx, sy, ss = scipy_dual_annealing(f_multimodal, find_max=False,
                                           min_x=-10, max_x=10, min_y=-10, max_y=10)
        print(f"  scipy dual_annealing:  x={sx:.4f} y={sy:.4f} score={ss:.4f}")
    except ImportError:
        print("  scipy not installed — skipping dual_annealing")

    # -------------------------------------------------------------------
    print("\n=== Benchmark: 30 runs each, find_min f=x^2+y^2, start=(12,47) ===")

    t1 = timeit.timeit(
        lambda: simulated_annealing(
            SearchProblem(12, 47, 1, f_bowl), find_max=False,
            max_x=100, min_x=5, max_y=50, min_y=-5
        ),
        number=REPS,
    )
    print(f"  Original SA (buggy):   {t1*1000/REPS:7.3f} ms/run")

    t2 = timeit.timeit(
        lambda: simulated_annealing_fixed(
            SearchProblem(12, 47, 1, f_bowl), find_max=False,
            max_x=100, min_x=5, max_y=50, min_y=-5
        ),
        number=REPS,
    )
    print(f"  SA fixed:              {t2*1000/REPS:7.3f} ms/run")

    t3 = timeit.timeit(
        lambda: simulated_annealing_exp_cool(
            SearchProblem(12, 47, 1, f_bowl), find_max=False,
            max_x=100, min_x=5, max_y=50, min_y=-5, max_iter=500
        ),
        number=REPS,
    )
    print(f"  SA exp cooling:        {t3*1000/REPS:7.3f} ms/run")

    try:
        t4 = timeit.timeit(
            lambda: scipy_dual_annealing(f_bowl, find_max=False,
                                          min_x=5, max_x=100, min_y=-5, max_y=50),
            number=REPS,
        )
        print(f"  scipy dual_annealing:  {t4*1000/REPS:7.3f} ms/run")
    except ImportError:
        print("  scipy not installed — skipping")


if __name__ == "__main__":
    run_all()
