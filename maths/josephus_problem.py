"""
Josephus problem: n people in a circle, every k-th is eliminated.
Return the position (0-indexed) of the last survivor.

Recurrence: J(1)=0, J(n) = (J(n-1) + k) mod n.

>>> josephus(1, 3)
0
>>> josephus(7, 3)
3
>>> josephus(10, 2)
4
>>> josephus_recursive(7, 3)
3
"""


def josephus(n: int, k: int) -> int:
    """Iterative O(n) solution.

    >>> josephus(41, 3)
    30
    """
    if n < 1 or k < 1:
        raise ValueError("n and k must be positive")
    survivor = 0
    for i in range(2, n + 1):
        survivor = (survivor + k) % i
    return survivor


def josephus_recursive(n: int, k: int) -> int:
    """Recursive (classic definition).

    >>> josephus_recursive(10, 2)
    4
    """
    if n == 1:
        return 0
    return (josephus_recursive(n - 1, k) + k) % n


def josephus_simulation(n: int, k: int) -> int:
    """Direct simulation with a list — O(n·k).

    >>> josephus_simulation(7, 3)
    3
    """
    people = list(range(n))
    idx = 0
    while len(people) > 1:
        idx = (idx + k - 1) % len(people)
        people.pop(idx)
    return people[0]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(josephus(7, 3))
