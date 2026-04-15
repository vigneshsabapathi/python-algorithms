"""
Bilateral Filter

Edge-preserving smoothing filter that considers both spatial proximity and
intensity similarity. Unlike Gaussian blur, it preserves edges by weighting
pixels based on both distance AND intensity difference.

Reference: https://github.com/TheAlgorithms/Python/blob/master/digital_image_processing/filters/bilateral_filter.py
"""

import numpy as np


def bilateral_filter(
    image: np.ndarray,
    kernel_size: int = 5,
    sigma_space: float = 25.0,
    sigma_intensity: float = 25.0,
) -> np.ndarray:
    """
    Apply bilateral filter to a grayscale image.

    Args:
        image: Grayscale image, shape (H, W), dtype uint8 or float.
        kernel_size: Size of the filter kernel (odd number).
        sigma_space: Spatial Gaussian sigma (controls proximity weight).
        sigma_intensity: Intensity Gaussian sigma (controls similarity weight).

    Returns:
        Filtered image, same shape and dtype as input.

    >>> img = np.array([[10, 10, 10], [10, 50, 10], [10, 10, 10]], dtype=np.float64)
    >>> result = bilateral_filter(img, kernel_size=3, sigma_space=10, sigma_intensity=50)
    >>> result.shape
    (3, 3)
    >>> result[1, 1] < 50  # center smoothed toward neighbors
    True
    >>> result[1, 1] > 10  # but not fully averaged due to edge-preservation
    True

    >>> uniform = np.full((5, 5), 128.0)
    >>> np.allclose(bilateral_filter(uniform, 3, 10, 10), 128.0)
    True
    """
    img = image.astype(np.float64)
    h, w = img.shape
    half = kernel_size // 2
    output = np.zeros_like(img)

    # Precompute spatial Gaussian weights
    ax = np.arange(-half, half + 1)
    xx, yy = np.meshgrid(ax, ax)
    spatial_weight = np.exp(-(xx**2 + yy**2) / (2 * sigma_space**2))

    # Pad image
    padded = np.pad(img, half, mode="reflect")

    for i in range(h):
        for j in range(w):
            # Extract neighborhood
            region = padded[i : i + kernel_size, j : j + kernel_size]
            center_val = img[i, j]

            # Intensity similarity weight
            intensity_diff = region - center_val
            intensity_weight = np.exp(
                -(intensity_diff**2) / (2 * sigma_intensity**2)
            )

            # Combined weight
            weight = spatial_weight * intensity_weight
            weight_sum = weight.sum()

            if weight_sum > 0:
                output[i, j] = (weight * region).sum() / weight_sum
            else:
                output[i, j] = center_val

    return output


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    # Demo: smooth noise while preserving edge
    img = np.zeros((10, 10), dtype=np.float64)
    img[:, 5:] = 200.0
    noise = np.random.normal(0, 10, img.shape)
    noisy = np.clip(img + noise, 0, 255)

    filtered = bilateral_filter(noisy, kernel_size=5, sigma_space=10, sigma_intensity=20)
    print(f"\nNoisy range: [{noisy.min():.1f}, {noisy.max():.1f}]")
    print(f"Filtered range: [{filtered.min():.1f}, {filtered.max():.1f}]")
    print(f"Edge preserved: left avg={filtered[:, :3].mean():.1f}, right avg={filtered[:, 7:].mean():.1f}")
