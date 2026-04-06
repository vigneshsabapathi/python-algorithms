# https://en.wikipedia.org/wiki/Simulated_annealing
import math
import random
from typing import Any

from .hill_climbing import SearchProblem


def simulated_annealing(
    search_prob,
    find_max: bool = True,
    max_x: float = math.inf,
    min_x: float = -math.inf,
    max_y: float = math.inf,
    min_y: float = -math.inf,
    visualization: bool = False,
    start_temperate: float = 100,
    rate_of_decrease: float = 0.01,
    threshold_temp: float = 1,
) -> Any:
    """
    Implementation of the simulated annealing algorithm. We start with a given state,
    find all its neighbors. Pick a random neighbor, if that neighbor improves the
    solution, we move in that direction, if that neighbor does not improve the solution,
    we generate a random real number between 0 and 1, if the number is within a certain
    range (calculated using temperature) we move in that direction, else we pick
    another neighbor randomly and repeat the process.

    Args:
        search_prob: The search state at the start.
        find_max: If True, the algorithm should find the maximum else the minimum.
        max_x, min_x, max_y, min_y: the maximum and minimum bounds of x and y.
        visualization: If True, a matplotlib graph is displayed.
        start_temperate: the initial temperature of the system when the program starts.
        rate_of_decrease: the rate at which the temperature decreases in each iteration.
        threshold_temp: the threshold temperature below which we end the search
    Returns a search state having the maximum (or minimum) score.

    >>> def f(x, y): return -(x**2 + y**2)
    >>> prob = SearchProblem(x=5, y=5, step_size=1, function_to_optimize=f)
    >>> result = simulated_annealing(prob, find_max=True, max_x=10, min_x=-10,
    ...                              max_y=10, min_y=-10, start_temperate=100,
    ...                              rate_of_decrease=0.01, threshold_temp=1)
    >>> result.score() <= 0
    True
    """
    search_end = False
    current_state = search_prob
    current_temp = start_temperate
    scores = []
    iterations = 0
    best_state = None

    while not search_end:
        current_score = current_state.score()
        if best_state is None or current_score > best_state.score():
            best_state = current_state
        scores.append(current_score)
        iterations += 1
        next_state = None
        neighbors = current_state.get_neighbors()
        while (
            next_state is None and neighbors
        ):  # till we do not find a neighbor that we can move to
            index = random.randint(0, len(neighbors) - 1)  # picking a random neighbor
            picked_neighbor = neighbors.pop(index)
            change = picked_neighbor.score() - current_score

            if (
                picked_neighbor.x > max_x
                or picked_neighbor.x < min_x
                or picked_neighbor.y > max_y
                or picked_neighbor.y < min_y
            ):
                continue  # neighbor outside our bounds

            if not find_max:
                change = change * -1  # in case we are finding minimum
            if change > 0:  # improves the solution
                next_state = picked_neighbor
            else:
                probability = (math.e) ** (
                    change / current_temp
                )  # probability generation function
                if random.random() < probability:  # random number within probability
                    next_state = picked_neighbor
        current_temp = current_temp - (current_temp * rate_of_decrease)

        if current_temp < threshold_temp or next_state is None:
            # temperature below threshold, or could not find a suitable neighbor
            search_end = True
        else:
            current_state = next_state

    if visualization:
        from matplotlib import pyplot as plt

        plt.plot(range(iterations), scores)
        plt.xlabel("Iterations")
        plt.ylabel("Function values")
        plt.show()
    return best_state


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    def test_f1(x, y):
        return (x**2) + (y**2)

    # starting the problem with initial coordinates (12, 47)
    prob = SearchProblem(x=12, y=47, step_size=1, function_to_optimize=test_f1)
    local_min = simulated_annealing(
        prob, find_max=False, max_x=100, min_x=5, max_y=50, min_y=-5
    )
    print(
        "The minimum score for f(x, y) = x^2 + y^2 with the domain 100 > x > 5 "
        f"and 50 > y > -5 found via simulated annealing: {local_min.score()}"
    )

    # starting the problem with initial coordinates (12, 47)
    prob = SearchProblem(x=12, y=47, step_size=1, function_to_optimize=test_f1)
    local_max = simulated_annealing(
        prob, find_max=True, max_x=100, min_x=5, max_y=50, min_y=-5
    )
    print(
        "The maximum score for f(x, y) = x^2 + y^2 with the domain 100 > x > 5 "
        f"and 50 > y > -5 found via simulated annealing: {local_max.score()}"
    )

    def test_f2(x, y):
        return (3 * x**2) - (6 * y)

    prob = SearchProblem(x=3, y=4, step_size=1, function_to_optimize=test_f2)
    local_min2 = simulated_annealing(prob, find_max=False)
    print(
        "The minimum score for f(x, y) = 3*x^2 - 6*y found via simulated annealing: "
        f"{local_min2.score()}"
    )

    prob = SearchProblem(x=3, y=4, step_size=1, function_to_optimize=test_f2)
    local_max2 = simulated_annealing(prob, find_max=True)
    print(
        "The maximum score for f(x, y) = 3*x^2 - 6*y found via simulated annealing: "
        f"{local_max2.score()}"
    )
