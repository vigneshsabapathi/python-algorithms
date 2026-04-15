"""
Scoring Functions for Machine Learning Model Evaluation

Metrics for evaluating classification and regression models:
accuracy, precision, recall, F1, R-squared, etc.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/scoring_functions.py
"""

import numpy as np


def accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Classification accuracy = correct predictions / total predictions.

    >>> accuracy(np.array([1, 0, 1, 1]), np.array([1, 0, 0, 1]))
    0.75
    >>> accuracy(np.array([1, 1, 1]), np.array([1, 1, 1]))
    1.0
    """
    return float(np.sum(y_true == y_pred) / len(y_true))


def precision(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Precision = TP / (TP + FP). Measures exactness.

    >>> precision(np.array([1, 0, 1, 1, 0]), np.array([1, 1, 1, 0, 0]))
    0.6666666666666666
    >>> precision(np.array([1, 1]), np.array([1, 1]))
    1.0
    """
    true_positive = np.sum((y_true == 1) & (y_pred == 1))
    false_positive = np.sum((y_true == 0) & (y_pred == 1))
    if true_positive + false_positive == 0:
        return 0.0
    return float(true_positive / (true_positive + false_positive))


def recall(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Recall = TP / (TP + FN). Measures completeness.

    >>> recall(np.array([1, 0, 1, 1, 0]), np.array([1, 1, 1, 0, 0]))
    0.6666666666666666
    >>> recall(np.array([1, 1, 1]), np.array([1, 1, 1]))
    1.0
    """
    true_positive = np.sum((y_true == 1) & (y_pred == 1))
    false_negative = np.sum((y_true == 1) & (y_pred == 0))
    if true_positive + false_negative == 0:
        return 0.0
    return float(true_positive / (true_positive + false_negative))


def f1_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    F1 Score = 2 * (precision * recall) / (precision + recall).
    Harmonic mean of precision and recall.

    >>> f1_score(np.array([1, 0, 1, 1, 0]), np.array([1, 1, 1, 0, 0]))
    0.6666666666666666
    >>> f1_score(np.array([1, 1]), np.array([1, 1]))
    1.0
    """
    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    if p + r == 0:
        return 0.0
    return float(2 * p * r / (p + r))


def r_squared(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    R-squared (coefficient of determination) for regression.

    R^2 = 1 - SS_res / SS_tot
    where SS_res = sum((y_true - y_pred)^2), SS_tot = sum((y_true - mean(y_true))^2)

    >>> r_squared(np.array([1, 2, 3, 4, 5]), np.array([1, 2, 3, 4, 5]))
    1.0
    >>> r_squared(np.array([1, 2, 3]), np.array([2, 2, 2]))
    0.0
    """
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    if ss_tot == 0:
        return 1.0 if ss_res == 0 else 0.0
    return float(1 - ss_res / ss_tot)


def mean_absolute_percentage_error(
    y_true: np.ndarray, y_pred: np.ndarray
) -> float:
    """
    MAPE = (1/n) * sum(|y_true - y_pred| / |y_true|) * 100

    >>> round(mean_absolute_percentage_error(np.array([100, 200]), np.array([110, 190])), 1)
    7.5
    """
    mask = y_true != 0
    return float(np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100)


def confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """
    Compute confusion matrix components for binary classification.

    >>> cm = confusion_matrix(np.array([1, 0, 1, 1, 0]), np.array([1, 1, 1, 0, 0]))
    >>> cm['tp'], cm['fp'], cm['fn'], cm['tn']
    (2, 1, 1, 1)
    """
    tp = int(np.sum((y_true == 1) & (y_pred == 1)))
    fp = int(np.sum((y_true == 0) & (y_pred == 1)))
    fn = int(np.sum((y_true == 1) & (y_pred == 0)))
    tn = int(np.sum((y_true == 0) & (y_pred == 0)))
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- Scoring Functions Demo ---")
    y_true = np.array([1, 0, 1, 1, 0, 1, 0, 0, 1, 1])
    y_pred = np.array([1, 0, 1, 0, 0, 1, 1, 0, 0, 1])

    print(f"y_true: {y_true}")
    print(f"y_pred: {y_pred}")
    print(f"Accuracy:  {accuracy(y_true, y_pred):.4f}")
    print(f"Precision: {precision(y_true, y_pred):.4f}")
    print(f"Recall:    {recall(y_true, y_pred):.4f}")
    print(f"F1 Score:  {f1_score(y_true, y_pred):.4f}")
    print(f"Confusion: {confusion_matrix(y_true, y_pred)}")

    # Regression
    y_reg = np.array([3.0, -0.5, 2.0, 7.0])
    y_hat = np.array([2.5, 0.0, 2.0, 8.0])
    print(f"\nR-squared: {r_squared(y_reg, y_hat):.4f}")
