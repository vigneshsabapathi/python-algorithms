"""
Data Transformations for Machine Learning

Normalization, standardization, and feature scaling techniques.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/data_transformations.py
"""

import numpy as np


def normalize(data: np.ndarray) -> np.ndarray:
    """
    Min-Max normalization to [0, 1] range.

    x_norm = (x - x_min) / (x_max - x_min)

    >>> normalize(np.array([1, 2, 3, 4, 5], dtype=float))
    array([0.  , 0.25, 0.5 , 0.75, 1.  ])
    >>> normalize(np.array([5, 5, 5], dtype=float))
    array([0., 0., 0.])
    """
    x_min = np.min(data)
    x_max = np.max(data)
    if x_max - x_min == 0:
        return np.zeros_like(data)
    return (data - x_min) / (x_max - x_min)


def standardize(data: np.ndarray) -> np.ndarray:
    """
    Z-score standardization (mean=0, std=1).

    z = (x - mean) / std

    >>> result = standardize(np.array([1, 2, 3, 4, 5], dtype=float))
    >>> round(float(np.mean(result)), 10)
    0.0
    >>> round(float(np.std(result)), 10)
    1.0
    """
    mean = np.mean(data)
    std = np.std(data)
    if std == 0:
        return np.zeros_like(data)
    return (data - mean) / std


def log_transform(data: np.ndarray) -> np.ndarray:
    """
    Log transformation: log(1 + x). Useful for skewed distributions.

    >>> log_transform(np.array([0, 1, 2, 3], dtype=float))
    array([0.        , 0.69314718, 1.09861229, 1.38629436])
    """
    return np.log1p(data)


def sigmoid(data: np.ndarray) -> np.ndarray:
    """
    Sigmoid transformation: maps values to (0, 1).

    sigma(x) = 1 / (1 + exp(-x))

    >>> sigmoid(np.array([0.0]))
    array([0.5])
    >>> sigmoid(np.array([-1000.0]))[0] < 0.01
    True
    >>> sigmoid(np.array([1000.0]))[0] > 0.99
    True
    """
    return 1.0 / (1.0 + np.exp(-data))


def softmax(data: np.ndarray) -> np.ndarray:
    """
    Softmax transformation: maps values to probability distribution.

    softmax(x_i) = exp(x_i) / sum(exp(x_j))

    >>> result = softmax(np.array([1.0, 2.0, 3.0]))
    >>> round(float(np.sum(result)), 10)
    1.0
    >>> result[2] > result[1] > result[0]
    True
    """
    shifted = data - np.max(data)  # numerical stability
    exp_vals = np.exp(shifted)
    return exp_vals / np.sum(exp_vals)


def robust_scale(data: np.ndarray) -> np.ndarray:
    """
    Robust scaling using median and IQR (resistant to outliers).

    x_scaled = (x - median) / IQR

    >>> robust_scale(np.array([1, 2, 3, 4, 100], dtype=float))
    array([-1. , -0.5,  0. ,  0.5, 48.5])
    """
    median = np.median(data)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    if iqr == 0:
        return data - median
    return (data - median) / iqr


def max_abs_scale(data: np.ndarray) -> np.ndarray:
    """
    Scale by maximum absolute value to [-1, 1] range.

    >>> max_abs_scale(np.array([-4, -2, 0, 2, 4], dtype=float))
    array([-1. , -0.5,  0. ,  0.5,  1. ])
    """
    max_abs = np.max(np.abs(data))
    if max_abs == 0:
        return data.copy()
    return data / max_abs


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- Data Transformations Demo ---")
    data = np.array([2.0, 5.0, 10.0, 50.0, 100.0])
    print(f"Original:     {data}")
    print(f"Normalized:   {normalize(data)}")
    print(f"Standardized: {standardize(data)}")
    print(f"Log:          {log_transform(data)}")
    print(f"Sigmoid:      {sigmoid(data)}")
    print(f"Softmax:      {softmax(data)}")
    print(f"Robust:       {robust_scale(data)}")
    print(f"MaxAbs:       {max_abs_scale(data)}")
