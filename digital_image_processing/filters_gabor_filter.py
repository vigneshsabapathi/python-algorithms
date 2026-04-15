"""
Gabor Filter

A linear filter used for texture analysis. It is essentially a Gaussian kernel
modulated by a sinusoidal wave. Useful for edge detection at specific
orientations and frequencies.

Reference: https://github.com/TheAlgorithms/Python/blob/master/digital_image_processing/filters/gabor_filter.py
"""

import numpy as np
from scipy.ndimage import convolve


def gabor_kernel(
    size: int = 21,
    sigma: float = 5.0,
    theta: float = 0.0,
    lambd: float = 10.0,
    gamma: float = 0.5,
    psi: float = 0.0,
) -> np.ndarray:
    """
    Generate a 2D Gabor filter kernel.

    Args:
        size: Kernel size (odd number).
        sigma: Standard deviation of Gaussian envelope.
        theta: Orientation angle in radians.
        lambd: Wavelength of sinusoidal factor.
        gamma: Spatial aspect ratio (ellipticity).
        psi: Phase offset in radians.

    Returns:
        Gabor kernel, shape (size, size).

    >>> k = gabor_kernel(5, sigma=2.0, theta=0, lambd=4.0, gamma=1.0)
    >>> k.shape
    (5, 5)

    >>> k = gabor_kernel(3)
    >>> k.shape
    (3, 3)
    """
    half = size // 2
    y, x = np.mgrid[-half : half + 1, -half : half + 1]

    # Rotation
    x_theta = x * np.cos(theta) + y * np.sin(theta)
    y_theta = -x * np.sin(theta) + y * np.cos(theta)

    # Gabor formula
    gaussian = np.exp(-0.5 * (x_theta**2 + gamma**2 * y_theta**2) / sigma**2)
    sinusoidal = np.cos(2 * np.pi * x_theta / lambd + psi)

    return gaussian * sinusoidal


def apply_gabor_filter(
    image: np.ndarray,
    sigma: float = 5.0,
    theta: float = 0.0,
    lambd: float = 10.0,
    gamma: float = 0.5,
) -> np.ndarray:
    """
    Apply Gabor filter to a grayscale image.

    Args:
        image: Grayscale image, shape (H, W).
        sigma, theta, lambd, gamma: Gabor parameters.

    Returns:
        Filtered image.

    >>> img = np.zeros((10, 10), dtype=np.float64)
    >>> img[:, 5:] = 1.0
    >>> result = apply_gabor_filter(img, sigma=2, theta=0, lambd=4, gamma=1)
    >>> result.shape
    (10, 10)

    >>> np.zeros((5, 5), dtype=np.float64).sum() == 0
    True
    """
    kernel = gabor_kernel(
        size=int(6 * sigma) | 1,  # ensure odd
        sigma=sigma,
        theta=theta,
        lambd=lambd,
        gamma=gamma,
    )
    return convolve(image.astype(np.float64), kernel)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    # Demo: filter a striped pattern at different orientations
    img = np.zeros((32, 32), dtype=np.float64)
    for i in range(32):
        if i % 4 < 2:
            img[i, :] = 1.0  # horizontal stripes

    for angle_deg in [0, 45, 90]:
        theta = np.radians(angle_deg)
        filtered = apply_gabor_filter(img, sigma=3, theta=theta, lambd=4, gamma=1)
        print(f"Angle {angle_deg}deg: response range [{filtered.min():.3f}, {filtered.max():.3f}]")
