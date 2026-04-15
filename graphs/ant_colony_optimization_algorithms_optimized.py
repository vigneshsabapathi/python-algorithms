"""
Ant Colony Optimization - Optimized Variants with Benchmarks.

Variant 1: Standard ACO (AS - Ant System)
Variant 2: Max-Min ACO (bounds on pheromone levels)
Variant 3: Elitist ACO (extra pheromone for best-so-far ant)

>>> import random
>>> random.seed(42)
>>> cities = [(0,0), (3,4), (6,0), (3,-4)]
>>> path, dist = aco_standard(cities, n_ants=10, n_iter=30, seed=42)
>>> len(path) == 5 and path[0] == path[-1]
True
"""

import math
import random
import time


def _distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def _build_distance_matrix(
    cities: list[tuple[float, float]],
) -> list[list[float]]:
    n = len(cities)
    return [[_distance(cities[i], cities[j]) for j in range(n)] for i in range(n)]


def _select_next(
    current: int,
    visited: set[int],
    pheromone: list[list[float]],
    distances: list[list[float]],
    n: int,
    alpha: float,
    beta: float,
) -> int:
    probs = []
    for j in range(n):
        if j in visited:
            probs.append(0.0)
        else:
            tau = pheromone[current][j] ** alpha
            eta = (1.0 / max(distances[current][j], 1e-10)) ** beta
            probs.append(tau * eta)
    total = sum(probs)
    if total == 0:
        unvisited = [j for j in range(n) if j not in visited]
        return random.choice(unvisited) if unvisited else current
    r = random.random() * total
    cumulative = 0.0
    for j, p in enumerate(probs):
        cumulative += p
        if cumulative >= r:
            return j
    return n - 1


def _tour_distance(tour: list[int], distances: list[list[float]]) -> float:
    return sum(distances[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))


def _construct_tour(
    n: int,
    pheromone: list[list[float]],
    distances: list[list[float]],
    alpha: float,
    beta: float,
) -> tuple[list[int], float]:
    start = random.randint(0, n - 1)
    visited = {start}
    tour = [start]
    for _ in range(n - 1):
        nxt = _select_next(tour[-1], visited, pheromone, distances, n, alpha, beta)
        tour.append(nxt)
        visited.add(nxt)
    tour.append(start)
    return tour, _tour_distance(tour, distances)


# --- Variant 1: Standard ACO ---
def aco_standard(
    cities: list[tuple[float, float]],
    n_ants: int = 20,
    n_iter: int = 100,
    alpha: float = 1.0,
    beta: float = 2.0,
    evaporation: float = 0.5,
    q: float = 100.0,
    seed: int | None = None,
) -> tuple[list[int], float]:
    """
    Standard Ant System.

    >>> random.seed(1)
    >>> p, d = aco_standard([(0,0),(1,1),(2,0)], n_ants=5, n_iter=10, seed=1)
    >>> len(set(p[:-1])) == 3
    True
    """
    if seed is not None:
        random.seed(seed)
    n = len(cities)
    distances = _build_distance_matrix(cities)
    pheromone = [[1.0] * n for _ in range(n)]
    best_tour, best_dist = [], float("inf")

    for _ in range(n_iter):
        tours_dists = [_construct_tour(n, pheromone, distances, alpha, beta) for _ in range(n_ants)]
        for i in range(n):
            for j in range(n):
                pheromone[i][j] *= 1 - evaporation
        for tour, dist in tours_dists:
            deposit = q / dist
            for k in range(len(tour) - 1):
                pheromone[tour[k]][tour[k + 1]] += deposit
                pheromone[tour[k + 1]][tour[k]] += deposit
            if dist < best_dist:
                best_dist = dist
                best_tour = tour[:]
    return best_tour, best_dist


# --- Variant 2: Max-Min ACO ---
def aco_max_min(
    cities: list[tuple[float, float]],
    n_ants: int = 20,
    n_iter: int = 100,
    alpha: float = 1.0,
    beta: float = 2.0,
    evaporation: float = 0.5,
    q: float = 100.0,
    seed: int | None = None,
) -> tuple[list[int], float]:
    """
    Max-Min Ant System: pheromone bounded between tau_min and tau_max.

    >>> random.seed(2)
    >>> p, d = aco_max_min([(0,0),(1,1),(2,0)], n_ants=5, n_iter=10, seed=2)
    >>> len(set(p[:-1])) == 3
    True
    """
    if seed is not None:
        random.seed(seed)
    n = len(cities)
    distances = _build_distance_matrix(cities)
    tau_max = 10.0
    tau_min = 0.1
    pheromone = [[tau_max] * n for _ in range(n)]
    best_tour, best_dist = [], float("inf")

    for _ in range(n_iter):
        tours_dists = [_construct_tour(n, pheromone, distances, alpha, beta) for _ in range(n_ants)]
        # Only the iteration-best deposits pheromone
        iter_best_tour, iter_best_dist = min(tours_dists, key=lambda x: x[1])
        if iter_best_dist < best_dist:
            best_dist = iter_best_dist
            best_tour = iter_best_tour[:]
        for i in range(n):
            for j in range(n):
                pheromone[i][j] *= 1 - evaporation
        deposit = q / best_dist
        for k in range(len(best_tour) - 1):
            pheromone[best_tour[k]][best_tour[k + 1]] += deposit
            pheromone[best_tour[k + 1]][best_tour[k]] += deposit
        # Clamp
        for i in range(n):
            for j in range(n):
                pheromone[i][j] = max(tau_min, min(tau_max, pheromone[i][j]))
    return best_tour, best_dist


# --- Variant 3: Elitist ACO ---
def aco_elitist(
    cities: list[tuple[float, float]],
    n_ants: int = 20,
    n_iter: int = 100,
    alpha: float = 1.0,
    beta: float = 2.0,
    evaporation: float = 0.5,
    q: float = 100.0,
    elite_weight: float = 3.0,
    seed: int | None = None,
) -> tuple[list[int], float]:
    """
    Elitist Ant System: best-so-far ant gets extra pheromone deposit.

    >>> random.seed(3)
    >>> p, d = aco_elitist([(0,0),(1,1),(2,0)], n_ants=5, n_iter=10, seed=3)
    >>> len(set(p[:-1])) == 3
    True
    """
    if seed is not None:
        random.seed(seed)
    n = len(cities)
    distances = _build_distance_matrix(cities)
    pheromone = [[1.0] * n for _ in range(n)]
    best_tour, best_dist = [], float("inf")

    for _ in range(n_iter):
        tours_dists = [_construct_tour(n, pheromone, distances, alpha, beta) for _ in range(n_ants)]
        for i in range(n):
            for j in range(n):
                pheromone[i][j] *= 1 - evaporation
        for tour, dist in tours_dists:
            deposit = q / dist
            for k in range(len(tour) - 1):
                pheromone[tour[k]][tour[k + 1]] += deposit
                pheromone[tour[k + 1]][tour[k]] += deposit
            if dist < best_dist:
                best_dist = dist
                best_tour = tour[:]
        # Elite deposit
        if best_tour:
            elite_deposit = elite_weight * q / best_dist
            for k in range(len(best_tour) - 1):
                pheromone[best_tour[k]][best_tour[k + 1]] += elite_deposit
                pheromone[best_tour[k + 1]][best_tour[k]] += elite_deposit
    return best_tour, best_dist


def benchmark() -> None:
    """Benchmark all ACO variants."""
    random.seed(42)
    cities = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(20)]
    variants = [
        ("Standard ACO", lambda: aco_standard(cities, n_ants=15, n_iter=50, seed=42)),
        ("Max-Min ACO", lambda: aco_max_min(cities, n_ants=15, n_iter=50, seed=42)),
        ("Elitist ACO", lambda: aco_elitist(cities, n_ants=15, n_iter=50, seed=42)),
    ]
    print(f"\nBenchmark: ACO variants on {len(cities)} cities")
    print("-" * 60)
    for name, func in variants:
        t0 = time.perf_counter()
        path, dist = func()
        elapsed = time.perf_counter() - t0
        print(f"{name:<20} distance={dist:<10.2f} time={elapsed*1000:.1f}ms")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
