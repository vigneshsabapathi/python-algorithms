"""
Linear Congruential Generator (LCG) — Simple pseudorandom number generator.

Generates a sequence of pseudorandom numbers using the recurrence:
    X_{n+1} = (a * X_n + c) mod m

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/linear_congruential_generator.py
"""

from __future__ import annotations


class LinearCongruentialGenerator:
    """
    LCG pseudorandom number generator.

    >>> lcg = LinearCongruentialGenerator(seed=42, a=1103515245, c=12345, m=2**31)
    >>> lcg.next()
    1250496027
    >>> lcg.next()
    1116302264
    >>> lcg = LinearCongruentialGenerator(seed=0)
    >>> [lcg.next() for _ in range(3)]
    [12345, 1406932606, 654583775]
    """

    def __init__(
        self,
        seed: int = 0,
        a: int = 1103515245,
        c: int = 12345,
        m: int = 2**31,
    ) -> None:
        self.state = seed
        self.a = a
        self.c = c
        self.m = m

    def next(self) -> int:
        """Generate the next pseudorandom number."""
        self.state = (self.a * self.state + self.c) % self.m
        return self.state

    def generate(self, n: int) -> list[int]:
        """
        Generate n pseudorandom numbers.

        >>> lcg = LinearCongruentialGenerator(seed=7)
        >>> len(lcg.generate(5))
        5
        """
        return [self.next() for _ in range(n)]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
