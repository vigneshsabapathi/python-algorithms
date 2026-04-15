"""
Ant Colony Optimization (ACO) for the Travelling Salesman Problem.

Ants deposit pheromones on edges. Future ants prefer edges with more pheromone,
converging on good solutions. Combines pheromone trails (exploitation) with
random exploration.

Reference: https://github.com/TheAlgorithms/Python/blob/master/graphs/ant_colony_optimization_algorithms.py

>>> import random
>>> random.seed(42)
>>> cities = [(0, 0), (1, 5), (5, 2), (6, 6), (8, 3)]
>>> aco = AntColonyOptimization(cities, n_ants=10, n_iterations=50, seed=42)
>>> best_path, best_distance = aco.solve()
>>> len(best_path) == len(cities) + 1
True
>>> best_path[0] == best_path[-1]
True
>>> best_distance < 25.0
True
"""

import math
import random


class AntColonyOptimization:
    """
    ACO algorithm for TSP.

    >>> random.seed(0)
    >>> cities = [(0, 0), (3, 4), (6, 0)]
    >>> aco = AntColonyOptimization(cities, n_ants=5, n_iterations=20, seed=0)
    >>> path, dist = aco.solve()
    >>> len(set(path[:-1])) == 3
    True
    """

    def __init__(
        self,
        cities: list[tuple[float, float]],
        n_ants: int = 20,
        n_iterations: int = 100,
        alpha: float = 1.0,
        beta: float = 2.0,
        evaporation: float = 0.5,
        q: float = 100.0,
        seed: int | None = None,
    ) -> None:
        if seed is not None:
            random.seed(seed)
        self.cities = cities
        self.n = len(cities)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha  # pheromone importance
        self.beta = beta  # distance importance
        self.evaporation = evaporation
        self.q = q  # pheromone deposit factor

        # Precompute distances
        self.distances = [
            [self._distance(cities[i], cities[j]) for j in range(self.n)]
            for i in range(self.n)
        ]
        # Initialize pheromone
        self.pheromone = [[1.0] * self.n for _ in range(self.n)]

    @staticmethod
    def _distance(a: tuple[float, float], b: tuple[float, float]) -> float:
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    def _select_next(self, current: int, visited: set[int]) -> int:
        probabilities = []
        for j in range(self.n):
            if j in visited:
                probabilities.append(0.0)
            else:
                tau = self.pheromone[current][j] ** self.alpha
                eta = (1.0 / max(self.distances[current][j], 1e-10)) ** self.beta
                probabilities.append(tau * eta)

        total = sum(probabilities)
        if total == 0:
            # All visited
            unvisited = [j for j in range(self.n) if j not in visited]
            return random.choice(unvisited) if unvisited else current

        r = random.random() * total
        cumulative = 0.0
        for j, p in enumerate(probabilities):
            cumulative += p
            if cumulative >= r:
                return j
        return self.n - 1

    def _tour_distance(self, tour: list[int]) -> float:
        return sum(
            self.distances[tour[i]][tour[i + 1]] for i in range(len(tour) - 1)
        )

    def solve(self) -> tuple[list[int], float]:
        """
        Run ACO and return (best_tour, best_distance).
        Tour is a list of city indices starting and ending at the same city.
        """
        best_tour: list[int] = []
        best_distance = float("inf")

        for _ in range(self.n_iterations):
            all_tours: list[list[int]] = []
            all_distances: list[float] = []

            for _ in range(self.n_ants):
                start = random.randint(0, self.n - 1)
                visited = {start}
                tour = [start]

                for _ in range(self.n - 1):
                    next_city = self._select_next(tour[-1], visited)
                    tour.append(next_city)
                    visited.add(next_city)

                tour.append(start)  # return to start
                dist = self._tour_distance(tour)
                all_tours.append(tour)
                all_distances.append(dist)

                if dist < best_distance:
                    best_distance = dist
                    best_tour = tour[:]

            # Evaporate pheromone
            for i in range(self.n):
                for j in range(self.n):
                    self.pheromone[i][j] *= 1 - self.evaporation

            # Deposit new pheromone
            for tour, dist in zip(all_tours, all_distances):
                deposit = self.q / dist
                for k in range(len(tour) - 1):
                    i, j = tour[k], tour[k + 1]
                    self.pheromone[i][j] += deposit
                    self.pheromone[j][i] += deposit

        return best_tour, best_distance


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    cities = [(0, 0), (1, 5), (5, 2), (6, 6), (8, 3)]
    aco = AntColonyOptimization(cities, n_ants=20, n_iterations=100, seed=42)
    best_path, best_dist = aco.solve()
    print(f"Cities: {cities}")
    print(f"Best path: {best_path}")
    print(f"Best distance: {best_dist:.2f}")
