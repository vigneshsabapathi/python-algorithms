"""
LSTM Prediction (Pure NumPy Implementation)

Long Short-Term Memory network for sequence prediction.
Implements forward pass with forget, input, and output gates.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/lstm/lstm_prediction.py
"""

import numpy as np


def sigmoid(x: np.ndarray) -> np.ndarray:
    """Sigmoid activation."""
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))


def tanh(x: np.ndarray) -> np.ndarray:
    """Tanh activation."""
    return np.tanh(x)


class LSTMCell:
    """
    Single LSTM cell.

    >>> np.random.seed(42)
    >>> cell = LSTMCell(input_size=3, hidden_size=4, seed=42)
    >>> x = np.random.randn(3)
    >>> h_prev = np.zeros(4)
    >>> c_prev = np.zeros(4)
    >>> h, c = cell.forward(x, h_prev, c_prev)
    >>> h.shape
    (4,)
    >>> c.shape
    (4,)
    """

    def __init__(self, input_size: int, hidden_size: int, seed: int = 42) -> None:
        rng = np.random.RandomState(seed)
        n = input_size + hidden_size
        scale = np.sqrt(2.0 / n)

        # Gates: forget, input, candidate, output
        self.Wf = rng.randn(n, hidden_size) * scale
        self.bf = np.zeros(hidden_size)

        self.Wi = rng.randn(n, hidden_size) * scale
        self.bi = np.zeros(hidden_size)

        self.Wc = rng.randn(n, hidden_size) * scale
        self.bc = np.zeros(hidden_size)

        self.Wo = rng.randn(n, hidden_size) * scale
        self.bo = np.zeros(hidden_size)

    def forward(
        self, x: np.ndarray, h_prev: np.ndarray, c_prev: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        LSTM forward pass for one time step.

        f_t = sigmoid(W_f . [h_{t-1}, x_t] + b_f)   # forget gate
        i_t = sigmoid(W_i . [h_{t-1}, x_t] + b_i)   # input gate
        c~_t = tanh(W_c . [h_{t-1}, x_t] + b_c)     # candidate
        c_t = f_t * c_{t-1} + i_t * c~_t             # cell state
        o_t = sigmoid(W_o . [h_{t-1}, x_t] + b_o)    # output gate
        h_t = o_t * tanh(c_t)                         # hidden state
        """
        combined = np.concatenate([h_prev, x])

        f = sigmoid(combined @ self.Wf + self.bf)
        i = sigmoid(combined @ self.Wi + self.bi)
        c_candidate = tanh(combined @ self.Wc + self.bc)
        o = sigmoid(combined @ self.Wo + self.bo)

        c = f * c_prev + i * c_candidate
        h = o * tanh(c)

        return h, c


class LSTM:
    """
    LSTM network for sequence prediction.

    >>> np.random.seed(42)
    >>> lstm = LSTM(input_size=1, hidden_size=8, output_size=1, seed=42)
    >>> seq = np.array([[0.1], [0.2], [0.3], [0.4], [0.5]])
    >>> output = lstm.forward_sequence(seq)
    >>> output.shape
    (5, 1)
    """

    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        output_size: int,
        seed: int = 42,
    ) -> None:
        self.hidden_size = hidden_size
        self.cell = LSTMCell(input_size, hidden_size, seed)

        rng = np.random.RandomState(seed + 1)
        self.Wy = rng.randn(hidden_size, output_size) * np.sqrt(2.0 / hidden_size)
        self.by = np.zeros(output_size)

    def forward_sequence(self, x_seq: np.ndarray) -> np.ndarray:
        """
        Process a sequence through LSTM.

        Args:
            x_seq: shape (seq_length, input_size)

        Returns:
            outputs: shape (seq_length, output_size)
        """
        seq_length = x_seq.shape[0]
        h = np.zeros(self.hidden_size)
        c = np.zeros(self.hidden_size)
        outputs = []

        for t in range(seq_length):
            h, c = self.cell.forward(x_seq[t], h, c)
            y = h @ self.Wy + self.by
            outputs.append(y)

        return np.array(outputs)

    def predict_next(self, x_seq: np.ndarray) -> np.ndarray:
        """Predict next value given input sequence."""
        outputs = self.forward_sequence(x_seq)
        return outputs[-1]


def create_sequences(
    data: np.ndarray, seq_length: int
) -> tuple[np.ndarray, np.ndarray]:
    """
    Create input/target sequences for training.

    >>> data = np.array([1, 2, 3, 4, 5], dtype=float)
    >>> X, y = create_sequences(data.reshape(-1, 1), 3)
    >>> X.shape
    (2, 3, 1)
    >>> y.shape
    (2, 1)
    """
    xs, ys = [], []
    for i in range(len(data) - seq_length):
        xs.append(data[i : i + seq_length])
        ys.append(data[i + seq_length])
    return np.array(xs), np.array(ys)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- LSTM Prediction Demo ---")
    np.random.seed(42)

    # Generate sine wave sequence
    t = np.linspace(0, 4 * np.pi, 100)
    data = np.sin(t).reshape(-1, 1)

    # Create sequences
    seq_len = 10
    X, y = create_sequences(data, seq_len)
    print(f"Data shape: {data.shape}")
    print(f"Sequences: X={X.shape}, y={y.shape}")

    # Forward pass demo
    lstm = LSTM(input_size=1, hidden_size=16, output_size=1, seed=42)

    # Predict on first few sequences
    for i in range(5):
        pred = lstm.predict_next(X[i])
        print(f"  Seq {i}: predicted={pred[0]:.4f}, actual={y[i][0]:.4f}")

    # Full sequence prediction
    all_preds = []
    for i in range(len(X)):
        pred = lstm.predict_next(X[i])
        all_preds.append(pred[0])
    all_preds = np.array(all_preds)
    print(f"\nPrediction MSE (untrained): {np.mean((all_preds - y.ravel()) ** 2):.4f}")
    print("Note: This is an untrained network - MSE is high. Training requires backprop through time.")
