"""
Gradient Descent Optimization

Implements batch, stochastic, and mini-batch gradient descent
for function minimization.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/gradient_descent.py
"""

import numpy as np


def batch_gradient_descent(
    x: np.ndarray,
    y: np.ndarray,
    learning_rate: float = 0.01,
    n_iterations: int = 1000,
) -> tuple[np.ndarray, float, list[float]]:
    """
    Batch Gradient Descent for linear regression (y = Xw + b).

    Returns (weights, bias, cost_history).

    >>> x = np.array([[1], [2], [3]], dtype=float)
    >>> y = np.array([2, 4, 6], dtype=float)
    >>> w, b, costs = batch_gradient_descent(x, y, 0.1, 500)
    >>> abs(float(w[0]) - 2.0) < 0.1
    True
    """
    n_samples, n_features = x.shape
    weights = np.zeros(n_features)
    bias = 0.0
    cost_history = []

    for _ in range(n_iterations):
        y_pred = x @ weights + bias
        error = y_pred - y

        dw = (1 / n_samples) * (x.T @ error)
        db = (1 / n_samples) * np.sum(error)

        weights -= learning_rate * dw
        bias -= learning_rate * db

        cost = (1 / (2 * n_samples)) * np.sum(error**2)
        cost_history.append(cost)

    return weights, bias, cost_history


def stochastic_gradient_descent(
    x: np.ndarray,
    y: np.ndarray,
    learning_rate: float = 0.01,
    n_iterations: int = 100,
    seed: int | None = None,
) -> tuple[np.ndarray, float, list[float]]:
    """
    Stochastic Gradient Descent - updates weights for each sample.

    Returns (weights, bias, cost_history).

    >>> np.random.seed(42)
    >>> x = np.array([[1], [2], [3], [4]], dtype=float)
    >>> y = np.array([2, 4, 6, 8], dtype=float)
    >>> w, b, costs = stochastic_gradient_descent(x, y, 0.01, 200, seed=42)
    >>> abs(float(w[0]) - 2.0) < 0.5
    True
    """
    if seed is not None:
        np.random.seed(seed)
    n_samples, n_features = x.shape
    weights = np.zeros(n_features)
    bias = 0.0
    cost_history = []

    for _ in range(n_iterations):
        indices = np.random.permutation(n_samples)
        epoch_cost = 0.0
        for i in indices:
            xi = x[i : i + 1]
            yi = y[i]
            y_pred = float(xi @ weights + bias)
            error = y_pred - yi

            weights -= learning_rate * error * xi.ravel()
            bias -= learning_rate * error

            epoch_cost += 0.5 * error**2
        cost_history.append(epoch_cost / n_samples)

    return weights, bias, cost_history


def mini_batch_gradient_descent(
    x: np.ndarray,
    y: np.ndarray,
    learning_rate: float = 0.01,
    n_iterations: int = 100,
    batch_size: int = 32,
    seed: int | None = None,
) -> tuple[np.ndarray, float, list[float]]:
    """
    Mini-Batch Gradient Descent - compromise between batch and SGD.

    Returns (weights, bias, cost_history).

    >>> np.random.seed(42)
    >>> x = np.array([[1], [2], [3], [4], [5], [6]], dtype=float)
    >>> y = np.array([2, 4, 6, 8, 10, 12], dtype=float)
    >>> w, b, costs = mini_batch_gradient_descent(x, y, 0.01, 300, 2, seed=42)
    >>> abs(float(w[0]) - 2.0) < 0.5
    True
    """
    if seed is not None:
        np.random.seed(seed)
    n_samples, n_features = x.shape
    weights = np.zeros(n_features)
    bias = 0.0
    cost_history = []

    for _ in range(n_iterations):
        indices = np.random.permutation(n_samples)
        epoch_cost = 0.0
        n_batches = 0

        for start in range(0, n_samples, batch_size):
            end = min(start + batch_size, n_samples)
            batch_idx = indices[start:end]
            x_batch = x[batch_idx]
            y_batch = y[batch_idx]

            y_pred = x_batch @ weights + bias
            error = y_pred - y_batch
            bs = len(y_batch)

            dw = (1 / bs) * (x_batch.T @ error)
            db = (1 / bs) * np.sum(error)

            weights -= learning_rate * dw
            bias -= learning_rate * db

            epoch_cost += (1 / (2 * bs)) * np.sum(error**2)
            n_batches += 1

        cost_history.append(epoch_cost / n_batches)

    return weights, bias, cost_history


def gradient_descent_function_minimization(
    gradient_fn,
    x0: np.ndarray,
    learning_rate: float = 0.01,
    n_iterations: int = 1000,
    tolerance: float = 1e-8,
) -> tuple[np.ndarray, list[np.ndarray]]:
    """
    General gradient descent for minimizing any differentiable function.

    Args:
        gradient_fn: function that computes gradient at point x
        x0: starting point
        learning_rate: step size
        n_iterations: max iterations
        tolerance: convergence threshold

    Returns (optimal_x, history).

    >>> # Minimize f(x) = x^2, gradient = 2x
    >>> x_opt, hist = gradient_descent_function_minimization(lambda x: 2*x, np.array([5.0]), 0.1, 100)
    >>> abs(float(x_opt[0])) < 0.01
    True
    """
    x = x0.copy()
    history = [x.copy()]

    for _ in range(n_iterations):
        grad = gradient_fn(x)
        x -= learning_rate * grad
        history.append(x.copy())
        if np.linalg.norm(grad) < tolerance:
            break

    return x, history


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- Gradient Descent Demo ---")
    np.random.seed(42)
    X = np.random.rand(50, 1) * 10
    y = 3 * X.ravel() + 7 + np.random.randn(50) * 0.5

    for name, fn in [
        ("Batch", lambda: batch_gradient_descent(X, y, 0.01, 500)),
        ("SGD", lambda: stochastic_gradient_descent(X, y, 0.001, 100, seed=42)),
        ("MiniBatch", lambda: mini_batch_gradient_descent(X, y, 0.01, 200, 16, seed=42)),
    ]:
        w, b, costs = fn()
        print(f"{name:10s}: w={w[0]:.4f}, b={b:.4f}, final_cost={costs[-1]:.4f}")

    # Function minimization: f(x,y) = (x-3)^2 + (y+1)^2
    grad_fn = lambda p: np.array([2 * (p[0] - 3), 2 * (p[1] + 1)])
    x_opt, _ = gradient_descent_function_minimization(grad_fn, np.array([0.0, 0.0]), 0.1, 500)
    print(f"\nMinimize (x-3)^2 + (y+1)^2: optimal = ({x_opt[0]:.4f}, {x_opt[1]:.4f})")
