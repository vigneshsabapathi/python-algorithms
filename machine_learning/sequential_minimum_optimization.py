"""
Sequential Minimum Optimization (SMO)

Efficient algorithm for training Support Vector Machines.
Solves the SVM dual optimization problem by breaking it into
smallest possible sub-problems (pairs of Lagrange multipliers).

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/sequential_minimum_optimization.py
"""

import numpy as np


class SMO:
    """
    SVM trained with Sequential Minimum Optimization (Platt's algorithm).

    >>> np.random.seed(42)
    >>> X = np.vstack([np.random.randn(20, 2) + [2, 2], np.random.randn(20, 2) + [-2, -2]])
    >>> y = np.array([1]*20 + [-1]*20, dtype=float)
    >>> smo = SMO(C=1.0, tol=0.01, max_passes=20, kernel='linear')
    >>> smo.fit(X, y)
    >>> smo.predict(np.array([[3, 3]]))[0] > 0
    True
    >>> smo.predict(np.array([[-3, -3]]))[0] < 0
    True
    """

    def __init__(
        self,
        C: float = 1.0,
        tol: float = 0.001,
        max_passes: int = 100,
        kernel: str = "linear",
        gamma: float = 0.5,
    ) -> None:
        self.C = C
        self.tol = tol
        self.max_passes = max_passes
        self.kernel_type = kernel
        self.gamma = gamma
        self.alphas: np.ndarray | None = None
        self.b: float = 0.0
        self.x_train: np.ndarray | None = None
        self.y_train: np.ndarray | None = None

    def _kernel(self, x1: np.ndarray, x2: np.ndarray) -> np.ndarray:
        """Compute kernel function."""
        if self.kernel_type == "rbf":
            if x1.ndim == 1:
                x1 = x1.reshape(1, -1)
            if x2.ndim == 1:
                x2 = x2.reshape(1, -1)
            sq_dist = (
                np.sum(x1**2, axis=1, keepdims=True)
                + np.sum(x2**2, axis=1)
                - 2 * x1 @ x2.T
            )
            return np.exp(-self.gamma * sq_dist)
        # Linear kernel
        return x1 @ x2.T if x1.ndim > 1 else np.dot(x1, x2)

    def fit(self, x: np.ndarray, y: np.ndarray) -> None:
        """Train SVM using SMO algorithm."""
        n_samples = x.shape[0]
        self.x_train = x.copy()
        self.y_train = y.copy()
        self.alphas = np.zeros(n_samples)
        self.b = 0.0

        # Precompute kernel matrix
        K = np.zeros((n_samples, n_samples))
        for i in range(n_samples):
            K[i] = self._kernel(x[i:i+1], x).ravel()

        passes = 0
        while passes < self.max_passes:
            num_changed = 0

            for i in range(n_samples):
                Ei = float(
                    np.sum(self.alphas * y * K[i]) + self.b - y[i]
                )

                if (y[i] * Ei < -self.tol and self.alphas[i] < self.C) or \
                   (y[i] * Ei > self.tol and self.alphas[i] > 0):

                    # Select j != i randomly
                    j = i
                    while j == i:
                        j = np.random.randint(n_samples)

                    Ej = float(
                        np.sum(self.alphas * y * K[j]) + self.b - y[j]
                    )

                    old_ai, old_aj = self.alphas[i], self.alphas[j]

                    # Compute bounds L and H
                    if y[i] != y[j]:
                        L = max(0, self.alphas[j] - self.alphas[i])
                        H = min(self.C, self.C + self.alphas[j] - self.alphas[i])
                    else:
                        L = max(0, self.alphas[i] + self.alphas[j] - self.C)
                        H = min(self.C, self.alphas[i] + self.alphas[j])

                    if L >= H:
                        continue

                    eta = 2 * K[i, j] - K[i, i] - K[j, j]
                    if eta >= 0:
                        continue

                    # Update alpha_j
                    self.alphas[j] -= y[j] * (Ei - Ej) / eta
                    self.alphas[j] = np.clip(self.alphas[j], L, H)

                    if abs(self.alphas[j] - old_aj) < 1e-5:
                        continue

                    # Update alpha_i
                    self.alphas[i] += y[i] * y[j] * (old_aj - self.alphas[j])

                    # Update bias
                    b1 = (
                        self.b - Ei
                        - y[i] * (self.alphas[i] - old_ai) * K[i, i]
                        - y[j] * (self.alphas[j] - old_aj) * K[i, j]
                    )
                    b2 = (
                        self.b - Ej
                        - y[i] * (self.alphas[i] - old_ai) * K[i, j]
                        - y[j] * (self.alphas[j] - old_aj) * K[j, j]
                    )

                    if 0 < self.alphas[i] < self.C:
                        self.b = b1
                    elif 0 < self.alphas[j] < self.C:
                        self.b = b2
                    else:
                        self.b = (b1 + b2) / 2

                    num_changed += 1

            if num_changed == 0:
                passes += 1
            else:
                passes = 0

    def decision_function(self, x: np.ndarray) -> np.ndarray:
        """Compute decision function value."""
        if x.ndim == 1:
            x = x.reshape(1, -1)
        K = self._kernel(x, self.x_train)
        return (K @ (self.alphas * self.y_train)) + self.b

    def predict(self, x: np.ndarray) -> np.ndarray:
        """Predict class labels."""
        return np.sign(self.decision_function(x))

    def n_support_vectors(self) -> int:
        """Count support vectors (alphas > 0)."""
        return int(np.sum(self.alphas > 1e-5))


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- SMO Demo ---")
    np.random.seed(42)

    X_pos = np.random.randn(40, 2) + [2, 2]
    X_neg = np.random.randn(40, 2) + [-2, -2]
    X = np.vstack([X_pos, X_neg])
    y = np.array([1.0] * 40 + [-1.0] * 40)

    idx = np.random.permutation(80)
    X, y = X[idx], y[idx]

    smo = SMO(C=1.0, tol=0.01, max_passes=50, kernel="linear")
    smo.fit(X, y)

    preds = smo.predict(X)
    acc = np.mean(preds.ravel() * y > 0)
    print(f"Accuracy: {acc:.4f}")
    print(f"Support vectors: {smo.n_support_vectors()}")
    print(f"Bias: {smo.b:.4f}")
