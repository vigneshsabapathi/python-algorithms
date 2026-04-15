"""
Time Series Forecasting

Implements simple forecasting methods: moving average, exponential
smoothing, and linear trend extrapolation.

Reference: https://github.com/TheAlgorithms/Python/blob/master/machine_learning/forecasting/run.py
"""

import numpy as np


def moving_average(data: list[float], window: int = 3) -> list[float]:
    """
    Simple moving average forecast.

    >>> moving_average([1, 2, 3, 4, 5], window=3)
    [2.0, 3.0, 4.0]
    >>> moving_average([10, 20, 30], window=2)
    [15.0, 25.0]
    """
    result = []
    for i in range(len(data) - window + 1):
        avg = sum(data[i : i + window]) / window
        result.append(avg)
    return result


def exponential_smoothing(
    data: list[float], alpha: float = 0.3
) -> list[float]:
    """
    Simple exponential smoothing.

    S_t = alpha * x_t + (1 - alpha) * S_{t-1}

    >>> result = exponential_smoothing([10, 20, 30, 40, 50], alpha=0.5)
    >>> len(result) == 5
    True
    >>> result[0]
    10.0
    """
    smoothed = [float(data[0])]
    for i in range(1, len(data)):
        s = alpha * data[i] + (1 - alpha) * smoothed[-1]
        smoothed.append(s)
    return smoothed


def double_exponential_smoothing(
    data: list[float], alpha: float = 0.3, beta: float = 0.1
) -> list[float]:
    """
    Double exponential smoothing (Holt's method) for data with trend.

    >>> result = double_exponential_smoothing([10, 20, 30, 40, 50], 0.5, 0.3)
    >>> len(result) == 5
    True
    """
    level = float(data[0])
    trend = float(data[1] - data[0])
    result = [level]

    for i in range(1, len(data)):
        new_level = alpha * data[i] + (1 - alpha) * (level + trend)
        new_trend = beta * (new_level - level) + (1 - beta) * trend
        level = new_level
        trend = new_trend
        result.append(level + trend)

    return result


def linear_trend_forecast(
    data: list[float], n_forecast: int = 5
) -> list[float]:
    """
    Forecast using linear trend extrapolation.

    >>> linear_trend_forecast([2, 4, 6, 8, 10], n_forecast=3)
    [12.0, 14.0, 16.0]
    """
    n = len(data)
    x = np.arange(n)
    y = np.array(data)

    # Linear regression: y = mx + b
    x_mean = np.mean(x)
    y_mean = np.mean(y)
    m = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
    b = y_mean - m * x_mean

    forecasts = []
    for i in range(n, n + n_forecast):
        forecasts.append(float(m * i + b))
    return forecasts


def mean_absolute_error_forecast(
    actual: list[float], predicted: list[float]
) -> float:
    """
    MAE for forecast evaluation.

    >>> mean_absolute_error_forecast([1, 2, 3], [1.5, 2.5, 2.5])
    0.5
    """
    return sum(abs(a - p) for a, p in zip(actual, predicted)) / len(actual)


def interquartile_range_forecast(data: list[float]) -> tuple[float, float]:
    """
    Return IQR-based forecast bounds.

    >>> lo, hi = interquartile_range_forecast([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    >>> lo < hi
    True
    """
    arr = np.array(data)
    q1 = float(np.percentile(arr, 25))
    q3 = float(np.percentile(arr, 75))
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- Forecasting Demo ---")
    # Sample time series: monthly sales
    data = [112, 118, 132, 129, 121, 135, 148, 148, 136, 119, 104, 118,
            115, 126, 141, 135, 125, 149, 170, 170, 158, 133, 114, 140]

    print(f"Data points: {len(data)}")
    print(f"Data: {data}")

    # Moving average
    ma = moving_average(data, window=3)
    print(f"\nMoving Average (w=3, last 5): {[round(x, 1) for x in ma[-5:]]}")

    # Exponential smoothing
    es = exponential_smoothing(data, alpha=0.3)
    print(f"Exp Smoothing (a=0.3, last 5): {[round(x, 1) for x in es[-5:]]}")

    # Double exponential
    des = double_exponential_smoothing(data, alpha=0.3, beta=0.1)
    print(f"Double Exp (last 5): {[round(x, 1) for x in des[-5:]]}")

    # Linear trend forecast
    forecast = linear_trend_forecast(data, n_forecast=3)
    print(f"\nLinear trend forecast (next 3): {[round(x, 1) for x in forecast]}")

    # Evaluation
    train, test = data[:18], data[18:]
    pred = exponential_smoothing(data[:18], 0.3)[-len(test):]
    if len(pred) < len(test):
        pred = exponential_smoothing(data, 0.3)[18:]
    print(f"Test MAE: {mean_absolute_error_forecast(test[:len(pred)], pred[:len(test)]):.2f}")
