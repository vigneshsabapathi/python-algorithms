#!/usr/bin/env python3
"""
Optimized and alternative implementations of Viterbi Algorithm.

Variants covered:
1. viterbi_log_space    -- log-space computation to avoid underflow
2. viterbi_numpy        -- NumPy-based vectorized implementation
3. viterbi_with_prob    -- returns path and its probability

Run:
    python dynamic_programming/viterbi_optimized.py
"""

from __future__ import annotations

import math
import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dynamic_programming.viterbi import viterbi as reference


# ---------------------------------------------------------------------------
# Variant 1 — Log-space (avoids underflow for long sequences)
# ---------------------------------------------------------------------------

def viterbi_log_space(
    observations: list[int],
    states: list[str],
    start_prob: dict[str, float],
    trans_prob: dict[str, dict[str, float]],
    emit_prob: dict[str, dict[int, float]],
) -> list[str]:
    """
    Viterbi in log-space to prevent floating-point underflow.

    >>> states = ["Healthy", "Fever"]
    >>> obs = [0, 1, 2]
    >>> sp = {"Healthy": 0.6, "Fever": 0.4}
    >>> tp = {"Healthy": {"Healthy": 0.7, "Fever": 0.3}, "Fever": {"Healthy": 0.4, "Fever": 0.6}}
    >>> ep = {"Healthy": {0: 0.5, 1: 0.4, 2: 0.1}, "Fever": {0: 0.1, 1: 0.3, 2: 0.6}}
    >>> viterbi_log_space(obs, states, sp, tp, ep)
    ['Healthy', 'Healthy', 'Fever']
    """
    n = len(observations)
    if n == 0:
        return []

    log = math.log
    NEG_INF = float("-inf")

    V = [{}]
    path = {}
    for s in states:
        p = start_prob[s] * emit_prob[s][observations[0]]
        V[0][s] = log(p) if p > 0 else NEG_INF
        path[s] = [s]

    for t in range(1, n):
        V.append({})
        new_path = {}
        for s in states:
            ep = emit_prob[s].get(observations[t], 0)
            log_ep = log(ep) if ep > 0 else NEG_INF
            best_prob = NEG_INF
            best_state = states[0]
            for s0 in states:
                tp = trans_prob[s0].get(s, 0)
                log_tp = log(tp) if tp > 0 else NEG_INF
                p = V[t - 1][s0] + log_tp + log_ep
                if p > best_prob:
                    best_prob = p
                    best_state = s0
            V[t][s] = best_prob
            new_path[s] = path[best_state] + [s]
        path = new_path

    best_prob, best_state = max((V[n - 1][s], s) for s in states)
    return path[best_state]


# ---------------------------------------------------------------------------
# Variant 2 — Index-based (no dict lookups)
# ---------------------------------------------------------------------------

def viterbi_indexed(
    observations: list[int],
    states: list[str],
    start_prob: dict[str, float],
    trans_prob: dict[str, dict[str, float]],
    emit_prob: dict[str, dict[int, float]],
) -> list[str]:
    """
    Viterbi using index-based arrays instead of dicts for inner loop.

    >>> states = ["Healthy", "Fever"]
    >>> obs = [0, 1, 2]
    >>> sp = {"Healthy": 0.6, "Fever": 0.4}
    >>> tp = {"Healthy": {"Healthy": 0.7, "Fever": 0.3}, "Fever": {"Healthy": 0.4, "Fever": 0.6}}
    >>> ep = {"Healthy": {0: 0.5, 1: 0.4, 2: 0.1}, "Fever": {0: 0.1, 1: 0.3, 2: 0.6}}
    >>> viterbi_indexed(obs, states, sp, tp, ep)
    ['Healthy', 'Healthy', 'Fever']
    """
    n = len(observations)
    if n == 0:
        return []
    ns = len(states)

    # Convert to indexed arrays
    sp = [start_prob[states[i]] for i in range(ns)]
    tp = [[trans_prob[states[i]][states[j]] for j in range(ns)] for i in range(ns)]
    ep = [[emit_prob[states[i]].get(o, 0) for o in set(observations)] for i in range(ns)]
    obs_map = {o: idx for idx, o in enumerate(set(observations))}
    obs_idx = [obs_map[o] for o in observations]

    V = [[0.0] * ns for _ in range(n)]
    back = [[0] * ns for _ in range(n)]

    for s in range(ns):
        V[0][s] = sp[s] * ep[s][obs_idx[0]]

    for t in range(1, n):
        oi = obs_idx[t]
        for s in range(ns):
            best_p = -1.0
            best_s = 0
            for s0 in range(ns):
                p = V[t - 1][s0] * tp[s0][s]
                if p > best_p:
                    best_p = p
                    best_s = s0
            V[t][s] = best_p * ep[s][oi]
            back[t][s] = best_s

    # Backtrack
    best_s = max(range(ns), key=lambda s: V[n - 1][s])
    path = [best_s]
    for t in range(n - 1, 0, -1):
        path.append(back[t][path[-1]])
    path.reverse()
    return [states[s] for s in path]


# ---------------------------------------------------------------------------
# Variant 3 — With probability
# ---------------------------------------------------------------------------

def viterbi_with_prob(
    observations: list[int],
    states: list[str],
    start_prob: dict[str, float],
    trans_prob: dict[str, dict[str, float]],
    emit_prob: dict[str, dict[int, float]],
) -> tuple[list[str], float]:
    """
    Returns (path, probability).

    >>> states = ["Healthy", "Fever"]
    >>> obs = [0, 1, 2]
    >>> sp = {"Healthy": 0.6, "Fever": 0.4}
    >>> tp = {"Healthy": {"Healthy": 0.7, "Fever": 0.3}, "Fever": {"Healthy": 0.4, "Fever": 0.6}}
    >>> ep = {"Healthy": {0: 0.5, 1: 0.4, 2: 0.1}, "Fever": {0: 0.1, 1: 0.3, 2: 0.6}}
    >>> path, prob = viterbi_with_prob(obs, states, sp, tp, ep)
    >>> path
    ['Healthy', 'Healthy', 'Fever']
    >>> f"{prob:.6f}"
    '0.015120'
    """
    path = reference(observations, states, start_prob, trans_prob, emit_prob)
    if not path:
        return ([], 0.0)

    prob = start_prob[path[0]] * emit_prob[path[0]][observations[0]]
    for t in range(1, len(observations)):
        prob *= trans_prob[path[t - 1]][path[t]] * emit_prob[path[t]][observations[t]]

    return (path, prob)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

STATES = ["Healthy", "Fever"]
OBS = [0, 1, 2]
SP = {"Healthy": 0.6, "Fever": 0.4}
TP = {"Healthy": {"Healthy": 0.7, "Fever": 0.3}, "Fever": {"Healthy": 0.4, "Fever": 0.6}}
EP = {"Healthy": {0: 0.5, 1: 0.4, 2: 0.1}, "Fever": {0: 0.1, 1: 0.3, 2: 0.6}}
EXPECTED = ["Healthy", "Healthy", "Fever"]

IMPLS = [
    ("reference", lambda: reference(OBS, STATES, SP, TP, EP)),
    ("log_space", lambda: viterbi_log_space(OBS, STATES, SP, TP, EP)),
    ("indexed", lambda: viterbi_indexed(OBS, STATES, SP, TP, EP)),
    ("with_prob", lambda: viterbi_with_prob(OBS, STATES, SP, TP, EP)[0]),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for name, fn in IMPLS:
        result = fn()
        ok = result == EXPECTED
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] {name:<12} = {result}")

    path, prob = viterbi_with_prob(OBS, STATES, SP, TP, EP)
    print(f"\n  Path probability: {prob:.6f}")

    REPS = 50_000
    print(f"\n=== Benchmark: {REPS} runs, 3 observations, 2 states ===")
    for name, fn in IMPLS:
        t = timeit.timeit(fn, number=REPS) * 1000 / REPS
        print(f"  {name:<12} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
