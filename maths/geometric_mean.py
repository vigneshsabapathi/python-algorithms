"""
Geometric mean: nth root of the product of n numbers.
    GM = (x1 * x2 * ... * xn)^(1/n) = exp(mean(log(xi)))

>>> round(geometric_mean([1, 2, 3, 4, 5]), 4)
2.6052
>>> round(geometric_mean([4, 9]), 4)
6.0
>>> round(geometric_mean([2, 8]), 4)
4.0
"""

import math


def geometric_mean(nums: list[float]) -> float:
    """GM via log-sum (numerically stable).

    >>> round(geometric_mean([1, 1, 1]), 4)
    1.0
    """
    if not nums:
        raise ValueError("empty list")
    if any(x <= 0 for x in nums):
        raise ValueError("geometric mean requires positive values")
    return math.exp(sum(math.log(x) for x in nums) / len(nums))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(round(geometric_mean([1, 2, 3, 4, 5]), 4))
