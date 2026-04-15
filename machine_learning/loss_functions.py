"""
Loss Functions for Machine Learning

Common loss functions used in training machine learning models.
Includes MSE, MAE, Binary Cross-Entropy, Hinge Loss, Huber Loss, and Log-Cosh Loss.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/loss_functions.py
"""

import numpy as np


def mean_squared_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Mean Squared Error (MSE) loss.

    MSE = (1/n) * sum((y_true - y_pred)^2)

    >>> mean_squared_error(np.array([1, 2, 3]), np.array([1, 2, 3]))
    0.0
    >>> mean_squared_error(np.array([1, 2, 3]), np.array([2, 3, 4]))
    1.0
    >>> mean_squared_error(np.array([0]), np.array([5]))
    25.0
    """
    return float(np.mean((y_true - y_pred) ** 2))


def mean_absolute_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Mean Absolute Error (MAE) loss.

    MAE = (1/n) * sum(|y_true - y_pred|)

    >>> mean_absolute_error(np.array([1, 2, 3]), np.array([1, 2, 3]))
    0.0
    >>> mean_absolute_error(np.array([1, 2, 3]), np.array([2, 3, 4]))
    1.0
    >>> mean_absolute_error(np.array([0]), np.array([5]))
    5.0
    """
    return float(np.mean(np.abs(y_true - y_pred)))


def binary_cross_entropy(
    y_true: np.ndarray, y_pred: np.ndarray, epsilon: float = 1e-15
) -> float:
    """
    Binary Cross-Entropy loss.

    BCE = -(1/n) * sum(y_true * log(y_pred) + (1 - y_true) * log(1 - y_pred))

    >>> round(binary_cross_entropy(np.array([1, 0, 1]), np.array([0.9, 0.1, 0.8])), 4)
    0.1446
    >>> binary_cross_entropy(np.array([1, 1]), np.array([1.0, 1.0])) < 1e-10
    True
    """
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return float(
        -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
    )


def hinge_loss(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Hinge Loss for SVM-style classification.

    Labels should be -1 or +1.
    Hinge = (1/n) * sum(max(0, 1 - y_true * y_pred))

    >>> round(hinge_loss(np.array([1, -1, 1]), np.array([0.8, -0.5, 1.2])), 4)
    0.2333
    >>> hinge_loss(np.array([1, -1]), np.array([2.0, -2.0]))
    0.0
    """
    return float(np.mean(np.maximum(0, 1 - y_true * y_pred)))


def huber_loss(
    y_true: np.ndarray, y_pred: np.ndarray, delta: float = 1.0
) -> float:
    """
    Huber Loss - combination of MSE and MAE, robust to outliers.

    L = 0.5 * (y_true - y_pred)^2           if |y_true - y_pred| <= delta
    L = delta * |y_true - y_pred| - 0.5 * delta^2   otherwise

    >>> huber_loss(np.array([1, 2, 3]), np.array([1, 2, 3]))
    0.0
    >>> huber_loss(np.array([1.0]), np.array([1.5]), delta=1.0)
    0.125
    >>> huber_loss(np.array([1.0]), np.array([3.0]), delta=1.0)
    1.5
    """
    error = y_true - y_pred
    is_small = np.abs(error) <= delta
    squared_loss = 0.5 * error**2
    linear_loss = delta * np.abs(error) - 0.5 * delta**2
    return float(np.mean(np.where(is_small, squared_loss, linear_loss)))


def log_cosh_loss(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Log-Cosh Loss - smooth approximation of MAE.

    L = (1/n) * sum(log(cosh(y_pred - y_true)))

    >>> log_cosh_loss(np.array([1, 2, 3]), np.array([1, 2, 3]))
    0.0
    >>> round(log_cosh_loss(np.array([0.0]), np.array([1.0])), 4)
    0.4338
    """
    error = y_pred - y_true
    return float(np.mean(np.log(np.cosh(error))))


def categorical_cross_entropy(
    y_true: np.ndarray, y_pred: np.ndarray, epsilon: float = 1e-15
) -> float:
    """
    Categorical Cross-Entropy for multi-class classification.

    y_true: one-hot encoded true labels (n_samples, n_classes)
    y_pred: predicted probabilities (n_samples, n_classes)

    >>> y_t = np.array([[1, 0, 0], [0, 1, 0]])
    >>> y_p = np.array([[0.9, 0.05, 0.05], [0.1, 0.8, 0.1]])
    >>> round(categorical_cross_entropy(y_t, y_p), 4)
    0.1643
    """
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return float(-np.mean(np.sum(y_true * np.log(y_pred), axis=1)))


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    # Live demo
    print("\n--- Loss Functions Demo ---")
    y_true = np.array([1.0, 0.0, 1.0, 0.0, 1.0])
    y_pred_good = np.array([0.9, 0.1, 0.8, 0.2, 0.95])
    y_pred_bad = np.array([0.5, 0.5, 0.5, 0.5, 0.5])

    print(f"y_true:      {y_true}")
    print(f"y_pred_good: {y_pred_good}")
    print(f"y_pred_bad:  {y_pred_bad}")
    print()

    for name, fn in [
        ("MSE", mean_squared_error),
        ("MAE", mean_absolute_error),
        ("BCE", binary_cross_entropy),
    ]:
        good_loss = fn(y_true, y_pred_good)
        bad_loss = fn(y_true, y_pred_bad)
        print(f"{name}: good={good_loss:.4f}, bad={bad_loss:.4f}")

    # Regression losses
    y_reg = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    y_hat = np.array([1.1, 2.3, 2.8, 4.5, 4.7])
    print(f"\nRegression: y={y_reg}, y_hat={y_hat}")
    print(f"Huber Loss:    {huber_loss(y_reg, y_hat):.4f}")
    print(f"Log-Cosh Loss: {log_cosh_loss(y_reg, y_hat):.4f}")
