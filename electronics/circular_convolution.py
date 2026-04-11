#!/usr/bin/env python3
"""
Circular Convolution — cyclic convolution using matrix method.

Reference: https://en.wikipedia.org/wiki/Circular_convolution

Run:
    python -m doctest electronics/circular_convolution.py -v
"""

import doctest
from collections import deque

import numpy as np


class CircularConvolution:
    """
    Stores two signals and performs circular convolution via matrix multiplication.
    """

    def __init__(self) -> None:
        self.first_signal = [2, 1, 2, -1]
        self.second_signal = [1, 2, 3, 4]

    def circular_convolution(self) -> list[float]:
        """
        Perform circular convolution of first_signal and second_signal.

        >>> convolution = CircularConvolution()
        >>> convolution.circular_convolution()
        [10.0, 10.0, 6.0, 14.0]

        >>> convolution.first_signal = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6]
        >>> convolution.second_signal = [0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5]
        >>> convolution.circular_convolution()
        [5.2, 6.0, 6.48, 6.64, 6.48, 6.0, 5.2, 4.08]

        >>> convolution.first_signal = [-1, 1, 2, -2]
        >>> convolution.second_signal = [0.5, 1, -1, 2, 0.75]
        >>> convolution.circular_convolution()
        [6.25, -3.0, 1.5, -2.0, -2.75]

        >>> convolution.first_signal = [1, -1, 2, 3, -1]
        >>> convolution.second_signal = [1, 2, 3]
        >>> convolution.circular_convolution()
        [8.0, -2.0, 3.0, 4.0, 11.0]
        """
        length_first_signal = len(self.first_signal)
        length_second_signal = len(self.second_signal)
        max_length = max(length_first_signal, length_second_signal)

        matrix = [[0] * max_length for i in range(max_length)]

        if length_first_signal < length_second_signal:
            self.first_signal += [0] * (max_length - length_first_signal)
        elif length_first_signal > length_second_signal:
            self.second_signal += [0] * (max_length - length_second_signal)

        for i in range(max_length):
            rotated_signal = deque(self.second_signal)
            rotated_signal.rotate(i)
            for j, item in enumerate(rotated_signal):
                matrix[i][j] += item

        final_signal = np.matmul(np.transpose(matrix), np.transpose(self.first_signal))
        return [float(round(i, 2)) for i in final_signal]


if __name__ == "__main__":
    doctest.testmod()
