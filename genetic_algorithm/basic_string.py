"""
Basic String Genetic Algorithm
==============================
Evolves a random population of strings toward a target string using the
four canonical phases of a genetic algorithm:

    1. **Evaluation** -- score each individual by counting characters that
       match the target at the same position.
    2. **Selection** -- keep the top performers; higher-fitness individuals
       produce more offspring.
    3. **Crossover** -- single-point crossover combines two parents into
       two children.
    4. **Mutation** -- with a given probability, swap one random character
       for another from the gene pool.

Reference: https://en.wikipedia.org/wiki/Genetic_algorithm
Source:    TheAlgorithms/Python  (adapted with doctests & reproducibility)
"""

from __future__ import annotations

import random

# ---------------------------------------------------------------------------
# Hyperparameters
# ---------------------------------------------------------------------------
N_POPULATION: int = 200          # max population size per generation
N_SELECTED: int = 50             # parents kept each generation (must be < N_POPULATION)
MUTATION_PROBABILITY: float = 0.4  # chance a child mutates one gene


# ---------------------------------------------------------------------------
# Core GA operators
# ---------------------------------------------------------------------------

def evaluate(item: str, target: str) -> tuple[str, float]:
    """Return *(item, score)* where *score* counts positional character matches.

    >>> evaluate("Helxo Worlx", "Hello World")
    ('Helxo Worlx', 9.0)
    >>> evaluate("abcdef", "abcdef")
    ('abcdef', 6.0)
    >>> evaluate("xxxxxx", "abcdef")
    ('xxxxxx', 0.0)
    """
    score = sum(1 for i, ch in enumerate(item) if ch == target[i])
    return (item, float(score))


def crossover(parent_1: str, parent_2: str) -> tuple[str, str]:
    """Single-point crossover -- slice two parents at a random index and swap tails.

    >>> random.seed(42)
    >>> crossover("123456", "abcdef")
    ('12345f', 'abcde6')
    >>> random.seed(0)
    >>> crossover("AAAA", "BBBB")
    ('AAAB', 'BBBA')
    """
    point = random.randint(0, len(parent_1) - 1)
    child_1 = parent_1[:point] + parent_2[point:]
    child_2 = parent_2[:point] + parent_1[point:]
    return (child_1, child_2)


def mutate(child: str, genes: list[str]) -> str:
    """With probability *MUTATION_PROBABILITY*, replace one random gene.

    >>> random.seed(123)
    >>> mutate("123456", list("ABCDEF"))
    '12345A'
    >>> random.seed(0)
    >>> mutate("abcd", list("XY"))        # mutation may or may not trigger
    'abcd'
    """
    child_list = list(child)
    if random.uniform(0, 1) < MUTATION_PROBABILITY:
        child_list[random.randint(0, len(child)) - 1] = random.choice(genes)
    return "".join(child_list)


def select(
    parent_1: tuple[str, float],
    population_score: list[tuple[str, float]],
    genes: list[str],
) -> list[str]:
    """Generate children from *parent_1* crossed with random partners.

    Higher-fitness parents produce proportionally more offspring (up to 10 pairs).

    >>> random.seed(42)
    >>> parent = ("ABCDEF", 5.0)
    >>> scores = [("ghijkl", 3.0), ("mnopqr", 4.0), ("stuvwx", 2.0)]
    >>> children = select(parent, scores, list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    >>> all(isinstance(c, str) and len(c) == 6 for c in children)
    True
    """
    pop: list[str] = []
    child_n = min(int(parent_1[1] * 100) + 1, 10)
    for _ in range(child_n):
        parent_2 = population_score[random.randint(0, min(N_SELECTED, len(population_score) - 1))][0]
        c1, c2 = crossover(parent_1[0], parent_2)
        pop.append(mutate(c1, genes))
        pop.append(mutate(c2, genes))
    return pop


# ---------------------------------------------------------------------------
# Main evolution loop
# ---------------------------------------------------------------------------

def basic(target: str, genes: list[str], debug: bool = True) -> tuple[int, int, str]:
    """Run the GA until the *target* string is evolved from *genes*.

    Returns *(generation, total_population_evaluated, best_string)*.

    >>> from string import ascii_lowercase
    >>> random.seed(42)
    >>> gen, pop, result = basic("abc", list(ascii_lowercase), debug=False)
    >>> result
    'abc'
    >>> gen >= 1
    True

    Target must only contain characters present in *genes*:

    >>> basic("xyz", list("ab"), debug=False)
    Traceback (most recent call last):
        ...
    ValueError: ['x', 'y', 'z'] is not in genes list, evolution cannot converge
    """
    if N_POPULATION < N_SELECTED:
        raise ValueError(
            f"{N_POPULATION} must be bigger than {N_SELECTED}"
        )

    # Validate that the target can actually be assembled from the gene pool.
    missing = sorted({ch for ch in target if ch not in genes})
    if missing:
        raise ValueError(
            f"{missing} is not in genes list, evolution cannot converge"
        )

    # Random initial population
    population = [
        "".join(random.choice(genes) for _ in range(len(target)))
        for _ in range(N_POPULATION)
    ]

    generation = 0
    total_population = 0

    while True:
        generation += 1
        total_population += len(population)

        # --- Evaluation ---
        population_score = [evaluate(item, target) for item in population]
        population_score.sort(key=lambda x: x[1], reverse=True)

        # Perfect match?
        if population_score[0][0] == target:
            return (generation, total_population, population_score[0][0])

        # Progress log every 10 generations
        if debug and generation % 10 == 0:
            print(
                f"\nGeneration: {generation}"
                f"\nTotal Population: {total_population}"
                f"\nBest score: {population_score[0][1]}"
                f"\nBest string: {population_score[0][0]}"
            )

        # --- Selection & Reproduction ---
        # Keep top third as elites
        elites = population[: N_POPULATION // 3]
        population.clear()
        population.extend(elites)

        # Normalise scores to [0, 1]
        norm_scores = [
            (item, score / len(target)) for item, score in population_score
        ]

        for i in range(N_SELECTED):
            population.extend(select(norm_scores[i], norm_scores, genes))
            if len(population) > N_POPULATION:
                break


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    random.seed(42)  # reproducible demo

    target_str = "Hello World!"
    genes_list = list(
        " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!.,;?+-"
    )

    generation, population, result = basic(target_str, genes_list)
    print(
        f"\nGeneration: {generation}"
        f"\nTotal Population: {population}"
        f"\nTarget: {result}"
    )
