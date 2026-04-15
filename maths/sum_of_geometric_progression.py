"""
Sum of Geometric Progression
============================
S_n = a (1 - r^n) / (1 - r) for r != 1, else S_n = n * a.
"""


def geometric_sum(a: float, r: float, n: int) -> float:
    """
    >>> geometric_sum(1, 2, 10)  # 1+2+4+...+512 = 1023
    1023.0
    >>> geometric_sum(3, 1, 4)   # 3+3+3+3 = 12
    12.0
    >>> geometric_sum(1, 0.5, 4) # 1+0.5+0.25+0.125 = 1.875
    1.875
    >>> abs(geometric_sum(1, 2, 0)) < 1e-9
    True
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if r == 1:
        return float(a * n)
    return float(a * (1 - r**n) / (1 - r))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(geometric_sum(1, 2, 20))   # 2^20 - 1 = 1048575
    print(geometric_sum(1, 0.5, 50)) # converges to 2
