"""
Softmax
=======
softmax(x)_i = exp(x_i) / Σ_j exp(x_j), a probability distribution.
"""
import math
from typing import List


def softmax(x: List[float]) -> List[float]:
    """
    >>> r = softmax([1.0, 2.0, 3.0])
    >>> abs(sum(r) - 1.0) < 1e-9
    True
    >>> r[2] > r[1] > r[0]
    True
    >>> softmax([0.0])
    [1.0]
    """
    if not x:
        return []
    m = max(x)  # subtract max for numerical stability
    exps = [math.exp(v - m) for v in x]
    total = sum(exps)
    return [e / total for e in exps]


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(softmax([1, 2, 3]))
    print(softmax([1000, 1001, 1002]))  # stable thanks to max subtraction
