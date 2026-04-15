"""
Canny Edge Detection

Multi-stage edge detection algorithm:
1. Gaussian blur to reduce noise
2. Gradient computation (Sobel operators)
3. Non-maximum suppression (thin edges)
4. Double thresholding (classify strong/weak edges)
5. Hysteresis edge tracking (connect weak edges to strong ones)

Reference: https://github.com/TheAlgorithms/Python/blob/master/digital_image_processing/edge_detection/canny.py
"""

import numpy as np
from scipy.ndimage import convolve


def gaussian_kernel(size: int = 5, sigma: float = 1.4) -> np.ndarray:
    """
    Generate a 2D Gaussian kernel.

    >>> k = gaussian_kernel(3, 1.0)
    >>> k.shape
    (3, 3)
    >>> abs(k.sum() - 1.0) < 1e-10
    True
    """
    ax = np.arange(size) - size // 2
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    return kernel / kernel.sum()


def sobel_gradients(image: np.ndarray) -> tuple:
    """
    Compute gradient magnitude and direction using Sobel operators.

    >>> img = np.array([[0, 0, 0], [0, 255, 0], [0, 0, 0]], dtype=np.float64)
    >>> mag, angle = sobel_gradients(img)
    >>> mag.shape
    (3, 3)
    """
    kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float64)
    ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype=np.float64)

    gx = convolve(image, kx)
    gy = convolve(image, ky)

    magnitude = np.hypot(gx, gy)
    direction = np.arctan2(gy, gx)
    return magnitude, direction


def non_max_suppression(magnitude: np.ndarray, direction: np.ndarray) -> np.ndarray:
    """
    Thin edges by keeping only local maxima along gradient direction.

    >>> mag = np.array([[10, 20, 10], [10, 30, 10], [10, 20, 10]], dtype=np.float64)
    >>> angle = np.zeros((3, 3))
    >>> result = non_max_suppression(mag, angle)
    >>> result[1, 1] > 0
    True
    """
    h, w = magnitude.shape
    output = np.zeros_like(magnitude)
    angle = direction * 180.0 / np.pi
    angle[angle < 0] += 180

    for i in range(1, h - 1):
        for j in range(1, w - 1):
            q, r = 255.0, 255.0

            # Angle 0 (horizontal edge, compare left-right)
            if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                q = magnitude[i, j + 1]
                r = magnitude[i, j - 1]
            # Angle 45
            elif 22.5 <= angle[i, j] < 67.5:
                q = magnitude[i + 1, j - 1]
                r = magnitude[i - 1, j + 1]
            # Angle 90 (vertical edge, compare up-down)
            elif 67.5 <= angle[i, j] < 112.5:
                q = magnitude[i + 1, j]
                r = magnitude[i - 1, j]
            # Angle 135
            elif 112.5 <= angle[i, j] < 157.5:
                q = magnitude[i - 1, j - 1]
                r = magnitude[i + 1, j + 1]

            if magnitude[i, j] >= q and magnitude[i, j] >= r:
                output[i, j] = magnitude[i, j]

    return output


def double_threshold(
    image: np.ndarray, low_ratio: float = 0.05, high_ratio: float = 0.15
) -> tuple:
    """
    Classify pixels as strong, weak, or non-edges.

    >>> img = np.array([[10, 50, 200], [5, 100, 150], [0, 30, 250]], dtype=np.float64)
    >>> result, weak, strong = double_threshold(img, 0.1, 0.3)
    >>> strong
    255
    """
    high_threshold = image.max() * high_ratio
    low_threshold = high_threshold * low_ratio

    strong = 255
    weak = 50

    result = np.zeros_like(image, dtype=np.uint8)
    result[image >= high_threshold] = strong
    result[(image >= low_threshold) & (image < high_threshold)] = weak

    return result, weak, strong


def hysteresis(image: np.ndarray, weak: int = 50, strong: int = 255) -> np.ndarray:
    """
    Connect weak edges to strong edges via 8-connectivity.

    >>> img = np.array([[0, 0, 0], [0, 50, 255], [0, 0, 0]], dtype=np.uint8)
    >>> result = hysteresis(img, 50, 255)
    >>> result[1, 1]
    255
    """
    h, w = image.shape
    output = image.copy()

    for i in range(1, h - 1):
        for j in range(1, w - 1):
            if output[i, j] == weak:
                # Check 8-connected neighbors for strong edge
                neighborhood = output[i - 1 : i + 2, j - 1 : j + 2]
                if strong in neighborhood:
                    output[i, j] = strong
                else:
                    output[i, j] = 0

    return output


def canny_edge_detection(
    image: np.ndarray,
    kernel_size: int = 5,
    sigma: float = 1.4,
    low_ratio: float = 0.05,
    high_ratio: float = 0.15,
) -> np.ndarray:
    """
    Full Canny edge detection pipeline.

    Args:
        image: Grayscale image, shape (H, W), dtype uint8.
        kernel_size: Gaussian kernel size.
        sigma: Gaussian sigma.
        low_ratio: Low threshold ratio for double thresholding.
        high_ratio: High threshold ratio.

    Returns:
        Binary edge map, dtype uint8.

    >>> img = np.zeros((10, 10), dtype=np.uint8)
    >>> img[3:7, 3:7] = 255
    >>> edges = canny_edge_detection(img)
    >>> edges.shape
    (10, 10)
    >>> edges.dtype
    dtype('uint8')
    """
    # Step 1: Gaussian blur
    kernel = gaussian_kernel(kernel_size, sigma)
    blurred = convolve(image.astype(np.float64), kernel)

    # Step 2: Gradient computation
    magnitude, direction = sobel_gradients(blurred)

    # Step 3: Non-maximum suppression
    thinned = non_max_suppression(magnitude, direction)

    # Step 4: Double thresholding
    thresholded, weak, strong = double_threshold(thinned, low_ratio, high_ratio)

    # Step 5: Hysteresis
    edges = hysteresis(thresholded, weak, strong)

    return edges


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    # Demo: detect edges on a synthetic image with a bright square
    img = np.zeros((20, 20), dtype=np.uint8)
    img[5:15, 5:15] = 200
    edges = canny_edge_detection(img)
    print(f"\nInput: 20x20 with bright square")
    print(f"Edge pixels found: {np.sum(edges > 0)}")
    print(f"Edge map unique values: {np.unique(edges)}")
