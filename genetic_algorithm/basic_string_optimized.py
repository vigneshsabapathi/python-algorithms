"""
Basic String GA -- Optimized Variants
======================================
Four implementations compared:

1. **Standard GA** -- classic evaluate/select/crossover/mutate loop
2. **NumPy-vectorized GA** -- fitness computed via vectorized char arrays
3. **Tournament Selection GA** -- k-tournament instead of rank-based selection
4. **Roulette-Wheel Selection GA** -- fitness-proportionate selection

All share the same crossover & mutation logic for a fair comparison.

Usage:
    python basic_string_optimized.py          # run benchmark
"""

from __future__ import annotations

import random
import time
from typing import Callable

import numpy as np

# ---------------------------------------------------------------------------
# Hyperparameters (shared across all variants)
# ---------------------------------------------------------------------------
N_POPULATION: int = 200
N_SELECTED: int = 50
MUTATION_PROBABILITY: float = 0.4


# ===================================================================
# Shared helpers
# ===================================================================

def _crossover(p1: str, p2: str) -> tuple[str, str]:
    """Single-point crossover.

    >>> random.seed(42)
    >>> _crossover("123456", "abcdef")
    ('12345f', 'abcde6')
    """
    pt = random.randint(0, len(p1) - 1)
    return (p1[:pt] + p2[pt:], p2[:pt] + p1[pt:])


def _mutate(child: str, genes: list[str]) -> str:
    """Random single-gene mutation.

    >>> random.seed(123)
    >>> _mutate("123456", list("ABCDEF"))
    '12345A'
    """
    chars = list(child)
    if random.random() < MUTATION_PROBABILITY:
        chars[random.randint(0, len(child)) - 1] = random.choice(genes)
    return "".join(chars)


# ===================================================================
# Variant 1 -- Standard GA  (rank-based selection)
# ===================================================================

def ga_standard(
    target: str, genes: list[str], *, seed: int = 42
) -> tuple[int, int, str]:
    """Classic GA with rank-based selection.

    >>> result = ga_standard("Hi", list("HGIiFghijklm "), seed=0)
    >>> result[2]
    'Hi'
    """
    random.seed(seed)
    population = [
        "".join(random.choice(genes) for _ in range(len(target)))
        for _ in range(N_POPULATION)
    ]
    generation = total = 0

    while True:
        generation += 1
        total += len(population)
        scored = sorted(
            ((s, sum(a == b for a, b in zip(s, target))) for s in population),
            key=lambda x: x[1],
            reverse=True,
        )
        if scored[0][0] == target:
            return generation, total, scored[0][0]

        # Elitism -- keep top third
        elites = [s for s, _ in scored[: N_POPULATION // 3]]
        norm = [(s, sc / len(target)) for s, sc in scored]

        new_pop: list[str] = list(elites)
        for i in range(min(N_SELECTED, len(norm))):
            n_children = min(int(norm[i][1] * 100) + 1, 10)
            for _ in range(n_children):
                p2 = norm[random.randint(0, min(N_SELECTED, len(norm) - 1))][0]
                c1, c2 = _crossover(norm[i][0], p2)
                new_pop.extend((_mutate(c1, genes), _mutate(c2, genes)))
                if len(new_pop) > N_POPULATION:
                    break
            if len(new_pop) > N_POPULATION:
                break
        population = new_pop


# ===================================================================
# Variant 2 -- NumPy-vectorized fitness
# ===================================================================

def ga_numpy(
    target: str, genes: list[str], *, seed: int = 42
) -> tuple[int, int, str]:
    """GA with NumPy-vectorized fitness evaluation.

    >>> result = ga_numpy("Hi", list("HGIiFghijklm "), seed=0)
    >>> result[2]
    'Hi'
    """
    random.seed(seed)
    np.random.seed(seed)
    target_arr = np.array(list(target))

    population = [
        "".join(random.choice(genes) for _ in range(len(target)))
        for _ in range(N_POPULATION)
    ]
    generation = total = 0

    while True:
        generation += 1
        total += len(population)

        # Vectorized fitness -- build 2-D char array, compare row-wise
        pop_arr = np.array([list(s) for s in population])
        scores = (pop_arr == target_arr).sum(axis=1)
        order = np.argsort(-scores)

        best_idx = order[0]
        if population[best_idx] == target:
            return generation, total, population[best_idx]

        # Selection & reproduction (still Python -- crossover is string-based)
        elites = [population[i] for i in order[: N_POPULATION // 3]]
        norm = [
            (population[order[i]], scores[order[i]] / len(target))
            for i in range(len(order))
        ]
        new_pop: list[str] = list(elites)
        for i in range(min(N_SELECTED, len(norm))):
            n_children = min(int(norm[i][1] * 100) + 1, 10)
            for _ in range(n_children):
                p2 = norm[random.randint(0, min(N_SELECTED, len(norm) - 1))][0]
                c1, c2 = _crossover(norm[i][0], p2)
                new_pop.extend((_mutate(c1, genes), _mutate(c2, genes)))
                if len(new_pop) > N_POPULATION:
                    break
            if len(new_pop) > N_POPULATION:
                break
        population = new_pop


# ===================================================================
# Variant 3 -- Tournament Selection
# ===================================================================

def ga_tournament(
    target: str,
    genes: list[str],
    *,
    seed: int = 42,
    k: int = 5,
) -> tuple[int, int, str]:
    """GA using k-tournament selection instead of rank-based.

    In each tournament, *k* random individuals compete; the fittest wins
    and becomes a parent.  This adds selection pressure while preserving
    diversity better than pure rank selection.

    >>> result = ga_tournament("Hi", list("HGIiFghijklm "), seed=0)
    >>> result[2]
    'Hi'
    """
    random.seed(seed)
    population = [
        "".join(random.choice(genes) for _ in range(len(target)))
        for _ in range(N_POPULATION)
    ]
    generation = total = 0

    def _fitness(individual: str) -> int:
        return sum(a == b for a, b in zip(individual, target))

    def _tournament(pop: list[str]) -> str:
        contestants = random.sample(pop, min(k, len(pop)))
        return max(contestants, key=_fitness)

    while True:
        generation += 1
        total += len(population)

        scored = sorted(
            ((s, _fitness(s)) for s in population),
            key=lambda x: x[1],
            reverse=True,
        )
        if scored[0][0] == target:
            return generation, total, scored[0][0]

        # Elitism
        elites = [s for s, _ in scored[: N_POPULATION // 3]]
        new_pop: list[str] = list(elites)

        while len(new_pop) < N_POPULATION:
            p1 = _tournament(population)
            p2 = _tournament(population)
            c1, c2 = _crossover(p1, p2)
            new_pop.append(_mutate(c1, genes))
            if len(new_pop) < N_POPULATION:
                new_pop.append(_mutate(c2, genes))
        population = new_pop


# ===================================================================
# Variant 4 -- Roulette-Wheel (fitness-proportionate) Selection
# ===================================================================

def ga_roulette(
    target: str, genes: list[str], *, seed: int = 42
) -> tuple[int, int, str]:
    """GA with roulette-wheel (fitness-proportionate) selection.

    Each individual's chance of being selected as a parent is proportional
    to its fitness score, giving a softer selection pressure than rank or
    tournament methods.

    >>> result = ga_roulette("Hi", list("HGIiFghijklm "), seed=0)
    >>> result[2]
    'Hi'
    """
    random.seed(seed)
    population = [
        "".join(random.choice(genes) for _ in range(len(target)))
        for _ in range(N_POPULATION)
    ]
    generation = total = 0

    def _fitness(individual: str) -> float:
        return sum(a == b for a, b in zip(individual, target)) + 1e-6  # avoid zero

    while True:
        generation += 1
        total += len(population)

        fitnesses = [_fitness(s) for s in population]
        best_idx = max(range(len(population)), key=lambda i: fitnesses[i])
        if population[best_idx] == target:
            return generation, total, population[best_idx]

        total_fit = sum(fitnesses)
        weights = [f / total_fit for f in fitnesses]

        # Elitism
        ranked = sorted(range(len(population)), key=lambda i: fitnesses[i], reverse=True)
        elites = [population[i] for i in ranked[: N_POPULATION // 3]]
        new_pop: list[str] = list(elites)

        while len(new_pop) < N_POPULATION:
            p1 = random.choices(population, weights=weights, k=1)[0]
            p2 = random.choices(population, weights=weights, k=1)[0]
            c1, c2 = _crossover(p1, p2)
            new_pop.append(_mutate(c1, genes))
            if len(new_pop) < N_POPULATION:
                new_pop.append(_mutate(c2, genes))
        population = new_pop


# ===================================================================
# Benchmark
# ===================================================================

def benchmark(
    target: str = "Hello World!",
    genes: list[str] | None = None,
    seed: int = 42,
    runs: int = 5,
) -> None:
    """Compare all four GA variants on the same target string.

    >>> benchmark("Hi", list("HGIiFghijklm "), seed=0, runs=1)  # doctest: +NORMALIZE_WHITESPACE
    ... # doctest: +ELLIPSIS
    === Genetic Algorithm Benchmark ===
    Target: 'Hi' | Gene pool size: 13 | Runs: 1
    ...
    """
    if genes is None:
        genes = list(
            " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!.,;?+-"
        )

    variants: list[tuple[str, Callable[..., tuple[int, int, str]]]] = [
        ("Standard GA (rank)",    ga_standard),
        ("NumPy-vectorized",      ga_numpy),
        ("Tournament (k=5)",      ga_tournament),
        ("Roulette-wheel",        ga_roulette),
    ]

    print(f"=== Genetic Algorithm Benchmark ===")
    print(f"Target: {target!r} | Gene pool size: {len(genes)} | Runs: {runs}")
    print(f"{'Variant':<25} {'Gens':>6} {'Pop':>10} {'Time (ms)':>10}")
    print("-" * 55)

    for name, func in variants:
        times, gens, pops = [], [], []
        for r in range(runs):
            run_seed = seed + r
            t0 = time.perf_counter()
            gen, pop, result = func(target, genes, seed=run_seed)
            elapsed = (time.perf_counter() - t0) * 1000
            assert result == target, f"{name} failed to converge (got {result!r})"
            times.append(elapsed)
            gens.append(gen)
            pops.append(pop)
        avg_t = sum(times) / len(times)
        avg_g = sum(gens) / len(gens)
        avg_p = sum(pops) / len(pops)
        print(f"{name:<25} {avg_g:>6.1f} {avg_p:>10.0f} {avg_t:>10.2f}")


if __name__ == "__main__":
    benchmark()
