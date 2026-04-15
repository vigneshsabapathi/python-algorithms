"""
Catalan Numbers using Dynamic Programming.

The Catalan numbers are a sequence of positive integers that appear in many
counting problems in combinatorics:
  - Number of Dyck words of length 2n
  - Number of valid expressions with n pairs of parentheses
  - Number of ways to parenthesize n+1 factors
  - Number of full binary trees with n+1 leaves

Recurrence relation:
  C(0) = C(1) = 1
  C(n) = sum(C(i) * C(n-i-1)) for i = 0 to n-1

Closed form:
  C(n) = (1 / (n+1)) * C(2n, n)

>>> catalan_numbers(5)
[1, 1, 2, 5, 14, 42]
>>> catalan_numbers(2)
[1, 1, 2]
>>> catalan_numbers(0)
[1]
>>> catalan_numbers(-1)
Traceback (most recent call last):
    ...
ValueError: Limit for the Catalan sequence must be >= 0
"""


def catalan_numbers(upper_limit: int) -> list[int]:
    """
    Return a list of Catalan numbers from C(0) through C(upper_limit).

    >>> catalan_numbers(5)
    [1, 1, 2, 5, 14, 42]
    >>> catalan_numbers(2)
    [1, 1, 2]
    >>> catalan_numbers(0)
    [1]
    >>> catalan_numbers(-1)
    Traceback (most recent call last):
        ...
    ValueError: Limit for the Catalan sequence must be >= 0
    """
    if upper_limit < 0:
        raise ValueError("Limit for the Catalan sequence must be >= 0")

    catalan_list = [0] * (upper_limit + 1)
    catalan_list[0] = 1
    if upper_limit > 0:
        catalan_list[1] = 1

    for i in range(2, upper_limit + 1):
        for j in range(i):
            catalan_list[i] += catalan_list[j] * catalan_list[i - j - 1]

    return catalan_list


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    for n in [0, 5, 10, 15]:
        result = catalan_numbers(n)
        print(f"  catalan_numbers({n}) = {result}")
