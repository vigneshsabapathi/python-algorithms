"""
Joint probability distribution for two discrete random variables.

Given samples (x_i, y_i), estimate P(X=x, Y=y). Then derive marginals and
check independence: P(X,Y) == P(X)·P(Y) for independent variables.

>>> x = [1, 1, 2, 2]
>>> y = [0, 1, 0, 1]
>>> joint, mx, my = joint_distribution(x, y)
>>> round(joint[(1, 0)], 4)
0.25
>>> round(mx[1], 4)
0.5
>>> is_independent(x, y)
True
"""

from collections import Counter


def joint_distribution(xs, ys):
    """Return (joint, marginal_x, marginal_y) as dicts of probabilities."""
    if len(xs) != len(ys):
        raise ValueError("xs and ys must be same length")
    n = len(xs)
    joint_counts = Counter(zip(xs, ys))
    mx_counts = Counter(xs)
    my_counts = Counter(ys)
    joint = {k: v / n for k, v in joint_counts.items()}
    mx = {k: v / n for k, v in mx_counts.items()}
    my = {k: v / n for k, v in my_counts.items()}
    return joint, mx, my


def is_independent(xs, ys, tol: float = 1e-9) -> bool:
    """True if joint equals product of marginals (within tolerance).

    >>> is_independent([1,1,2,2,3,3], [0,1,0,1,0,1])
    True
    """
    joint, mx, my = joint_distribution(xs, ys)
    for x in mx:
        for y in my:
            expected = mx[x] * my[y]
            actual = joint.get((x, y), 0.0)
            if abs(actual - expected) > tol:
                return False
    return True


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    x = [1, 1, 2, 2]
    y = [0, 1, 0, 1]
    print(joint_distribution(x, y))
    print("independent:", is_independent(x, y))
