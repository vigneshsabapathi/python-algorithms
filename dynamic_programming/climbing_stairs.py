"""
Climbing Stairs (LeetCode 70)

You are climbing a staircase with n steps. Each time you can climb 1 or 2 steps.
How many distinct ways can you climb to the top?

This is equivalent to computing the (n+1)-th Fibonacci number.

>>> climb_stairs(1)
1
>>> climb_stairs(2)
2
>>> climb_stairs(3)
3
>>> climb_stairs(5)
8
>>> climb_stairs(10)
89
>>> climb_stairs(-1)
Traceback (most recent call last):
    ...
AssertionError: number_of_steps needs to be positive integer, your input -1
"""


def climb_stairs(number_of_steps: int) -> int:
    """
    Return the number of distinct ways to climb a staircase of n steps,
    where each time you can climb 1 or 2 steps.

    Uses O(1) space with two rolling variables.

    >>> climb_stairs(3)
    3
    >>> climb_stairs(1)
    1
    >>> climb_stairs(10)
    89
    >>> climb_stairs(-7)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    AssertionError: number_of_steps needs to be positive integer, your input -7
    """
    assert isinstance(number_of_steps, int) and number_of_steps > 0, (
        f"number_of_steps needs to be positive integer, your input {number_of_steps}"
    )
    if number_of_steps == 1:
        return 1
    previous, current = 1, 1
    for _ in range(number_of_steps - 1):
        current, previous = current + previous, current
    return current


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    for n in [1, 2, 3, 5, 10, 20, 30]:
        print(f"  climb_stairs({n}) = {climb_stairs(n)}")
