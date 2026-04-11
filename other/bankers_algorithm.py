"""
Banker's Algorithm — Deadlock avoidance algorithm for resource allocation.

Determines whether a system is in a safe state and finds a safe sequence
of process execution that avoids deadlock.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/bankers_algorithm.py
"""

from __future__ import annotations


def bankers_algorithm(
    allocation: list[list[int]],
    max_need: list[list[int]],
    available: list[int],
) -> list[int] | None:
    """
    Find a safe execution sequence using the Banker's algorithm.

    Args:
        allocation: Current allocation matrix (processes x resources)
        max_need: Maximum need matrix (processes x resources)
        available: Available resources vector

    Returns:
        Safe sequence as list of process indices, or None if no safe state.

    >>> bankers_algorithm(
    ...     [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]],
    ...     [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]],
    ...     [3, 3, 2],
    ... )
    [1, 3, 0, 2, 4]
    >>> bankers_algorithm(
    ...     [[0, 1, 0], [2, 0, 0]],
    ...     [[7, 5, 3], [3, 2, 2]],
    ...     [0, 0, 0],
    ... ) is None
    True
    >>> bankers_algorithm([[1]], [[1]], [0])
    [0]
    """
    n_processes = len(allocation)
    n_resources = len(available)

    # Calculate need matrix: need[i][j] = max_need[i][j] - allocation[i][j]
    need = [
        [max_need[i][j] - allocation[i][j] for j in range(n_resources)]
        for i in range(n_processes)
    ]

    work = available[:]
    finished = [False] * n_processes
    safe_sequence: list[int] = []

    while len(safe_sequence) < n_processes:
        found = False
        for i in range(n_processes):
            if not finished[i] and all(
                need[i][j] <= work[j] for j in range(n_resources)
            ):
                # Process i can finish — release its resources
                for j in range(n_resources):
                    work[j] += allocation[i][j]
                finished[i] = True
                safe_sequence.append(i)
                found = True
                break

        if not found:
            return None  # No safe sequence exists

    return safe_sequence


if __name__ == "__main__":
    import doctest

    doctest.testmod()
