"""
IIR (Infinite Impulse Response) Filter — N-Order Digital Biquad Filter

An IIR filter uses both feedforward (b) and feedback (a) coefficients to produce
output that depends on current/past inputs AND past outputs. Unlike FIR filters,
the impulse response is theoretically infinite.

Transfer function:
    H(z) = (b0 + b1*z^-1 + b2*z^-2 + ... + bk*z^-k) /
           (a0 + a1*z^-1 + a2*z^-2 + ... + ak*z^-k)

Difference equation:
    y[n] = (1/a0) * (b0*x[n] + b1*x[n-1] + ... + bk*x[n-k]
                     - a1*y[n-1] - a2*y[n-2] - ... - ak*y[n-k])

Reference: https://en.wikipedia.org/wiki/Digital_biquad_filter
TheAlgorithms source: https://github.com/TheAlgorithms/Python/blob/master/audio_filters/iir_filter.py
"""

from __future__ import annotations


class IIRFilter:
    r"""
    N-Order IIR filter.
    Assumes working with float samples normalized on [-1, 1].

    Based on the 2nd-order biquad from Wikipedia, generalized to N-order.

    >>> filt = IIRFilter(2)
    >>> filt.order
    2
    >>> len(filt.a_coeffs)
    3
    >>> len(filt.b_coeffs)
    3

    >>> filt = IIRFilter(0)
    Traceback (most recent call last):
        ...
    ValueError: Filter order must be a positive integer, got 0

    >>> filt = IIRFilter(-1)
    Traceback (most recent call last):
        ...
    ValueError: Filter order must be a positive integer, got -1
    """

    def __init__(self, order: int) -> None:
        if order < 1:
            raise ValueError(
                f"Filter order must be a positive integer, got {order}"
            )
        self.order = order

        # a0 ... ak — denominator (feedback) coefficients
        self.a_coeffs: list[float] = [1.0] + [0.0] * order
        # b0 ... bk — numerator (feedforward) coefficients
        self.b_coeffs: list[float] = [1.0] + [0.0] * order

        # x[n-1] ... x[n-k] — input delay line
        self.input_history: list[float] = [0.0] * self.order
        # y[n-1] ... y[n-k] — output delay line
        self.output_history: list[float] = [0.0] * self.order

    def set_coefficients(
        self, a_coeffs: list[float], b_coeffs: list[float]
    ) -> None:
        """
        Set the filter coefficients. Both lists should be of size (order + 1).
        If a_coeffs has only `order` elements, a0=1.0 is prepended automatically.

        Compatible with scipy.signal filter design functions.

        >>> filt = IIRFilter(2)
        >>> filt.set_coefficients([1.0, -1.8, 0.81], [0.0025, 0.005, 0.0025])
        >>> filt.a_coeffs
        [1.0, -1.8, 0.81]
        >>> filt.b_coeffs
        [0.0025, 0.005, 0.0025]

        >>> filt = IIRFilter(2)
        >>> filt.set_coefficients([-1.8, 0.81], [0.0025, 0.005, 0.0025])
        >>> filt.a_coeffs
        [1.0, -1.8, 0.81]

        >>> filt = IIRFilter(2)
        >>> filt.set_coefficients([1.0, 2.0, 3.0, 4.0], [0.1, 0.2, 0.3])
        Traceback (most recent call last):
            ...
        ValueError: Expected a_coeffs to have 3 elements for 2-order filter, got 4

        >>> filt = IIRFilter(2)
        >>> filt.set_coefficients([1.0, 0.5, 0.5], [0.1])
        Traceback (most recent call last):
            ...
        ValueError: Expected b_coeffs to have 3 elements for 2-order filter, got 1
        """
        if len(a_coeffs) == self.order:
            a_coeffs = [1.0, *a_coeffs]

        if len(a_coeffs) != self.order + 1:
            raise ValueError(
                f"Expected a_coeffs to have {self.order + 1} elements "
                f"for {self.order}-order filter, got {len(a_coeffs)}"
            )

        if len(b_coeffs) != self.order + 1:
            raise ValueError(
                f"Expected b_coeffs to have {self.order + 1} elements "
                f"for {self.order}-order filter, got {len(b_coeffs)}"
            )

        self.a_coeffs = a_coeffs
        self.b_coeffs = b_coeffs

    def process(self, sample: float) -> float:
        """
        Process a single input sample through the filter, producing y[n].

        >>> filt = IIRFilter(2)
        >>> filt.process(0)
        0.0

        >>> filt = IIRFilter(1)
        >>> filt.set_coefficients([1.0, 0.0], [1.0, 0.0])
        >>> filt.process(0.5)
        0.5
        >>> filt.process(0.0)
        0.0

        >>> filt = IIRFilter(1)
        >>> filt.set_coefficients([1.0, -0.5], [1.0, 0.0])
        >>> round(filt.process(1.0), 6)
        1.0
        >>> round(filt.process(0.0), 6)
        0.5
        >>> round(filt.process(0.0), 6)
        0.25
        """
        result = 0.0

        # Accumulate delayed input and output terms (indices 1..order)
        for i in range(1, self.order + 1):
            result += (
                self.b_coeffs[i] * self.input_history[i - 1]
                - self.a_coeffs[i] * self.output_history[i - 1]
            )

        # Add current input and normalize by a0
        result = (result + self.b_coeffs[0] * sample) / self.a_coeffs[0]

        # Shift delay lines
        self.input_history[1:] = self.input_history[:-1]
        self.output_history[1:] = self.output_history[:-1]

        self.input_history[0] = sample
        self.output_history[0] = result

        return result

    def reset(self) -> None:
        """
        Reset filter state (clear delay lines).

        >>> filt = IIRFilter(2)
        >>> filt.process(1.0)
        1.0
        >>> filt.reset()
        >>> filt.input_history
        [0.0, 0.0]
        >>> filt.output_history
        [0.0, 0.0]
        """
        self.input_history = [0.0] * self.order
        self.output_history = [0.0] * self.order

    def process_sequence(self, samples: list[float]) -> list[float]:
        """
        Process a sequence of samples through the filter.

        >>> filt = IIRFilter(1)
        >>> filt.set_coefficients([1.0, 0.0], [0.5, 0.5])
        >>> filt.process_sequence([1.0, 0.0, 0.0])
        [0.5, 0.5, 0.0]
        """
        return [self.process(s) for s in samples]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
