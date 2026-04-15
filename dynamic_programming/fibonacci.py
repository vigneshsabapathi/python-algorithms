"""
Fibonacci Sequence using Dynamic Programming (Iterative Tabulation).

Builds the sequence incrementally, storing all computed values.
The Fibonacci class caches values so repeated calls are efficient.

>>> Fibonacci().get(10)
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
>>> Fibonacci().get(5)
[0, 1, 1, 2, 3]
>>> Fibonacci().get(1)
[0]
"""


class Fibonacci:
    """
    Fibonacci sequence generator with memoization.

    >>> f = Fibonacci()
    >>> f.get(10)
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    >>> f.get(5)
    [0, 1, 1, 2, 3]
    """

    def __init__(self) -> None:
        self.sequence = [0, 1]

    def get(self, index: int) -> list:
        """
        Get the first `index` Fibonacci numbers.
        Calculates missing values as needed.

        >>> Fibonacci().get(10)
        [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        >>> Fibonacci().get(5)
        [0, 1, 1, 2, 3]
        """
        if (difference := index - (len(self.sequence) - 2)) >= 1:
            for _ in range(difference):
                self.sequence.append(self.sequence[-1] + self.sequence[-2])
        return self.sequence[:index]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    fib = Fibonacci()
    for n in [1, 5, 10, 15, 20]:
        print(f"  Fibonacci().get({n}) = {fib.get(n)}")
