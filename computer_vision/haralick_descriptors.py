"""
Haralick Descriptors — texture features from the GLCM (Gray-Level Co-occurrence Matrix).

The GLCM captures how often pairs of pixel intensities occur at a given
spatial offset (distance, angle). From the GLCM, Haralick defined 14+
texture descriptors including:

- Contrast: measures local intensity variation
- Correlation: measures linear dependency of gray levels
- Energy (ASM): measures texture uniformity / orderliness
- Homogeneity (IDM): measures closeness of GLCM elements to the diagonal
- Entropy: measures randomness / disorder of the texture

Reference: TheAlgorithms/Python — computer_vision/haralick_descriptors.py
Paper: Haralick et al., "Textural Features for Image Classification" (1973)

>>> import numpy as np
>>> img = np.array([[0, 1, 2, 3], [1, 2, 3, 0], [2, 3, 0, 1], [3, 0, 1, 2]], dtype=np.uint8)
>>> glcm = compute_glcm(img, distance=1, angle=0, levels=4)
>>> glcm.shape
(4, 4)
>>> float(glcm.sum())
1.0
"""

from __future__ import annotations

import numpy as np


def compute_glcm(
    image: np.ndarray,
    distance: int = 1,
    angle: float = 0,
    levels: int = 256,
) -> np.ndarray:
    """
    Compute the Gray-Level Co-occurrence Matrix (GLCM).

    For each pixel (i, j), counts the pair (image[i,j], image[i+dy, j+dx])
    where (dx, dy) is determined by distance and angle.

    Args:
        image: 2D grayscale image (integer values 0..levels-1).
        distance: pixel pair distance.
        angle: direction in radians (0=right, pi/2=down, pi=left, etc.).
        levels: number of gray levels.

    Returns:
        Normalized GLCM (levels x levels), sums to 1.

    >>> import numpy as np
    >>> img = np.array([[0, 1], [1, 0]], dtype=np.uint8)
    >>> glcm = compute_glcm(img, distance=1, angle=0, levels=2)
    >>> glcm.shape
    (2, 2)
    """
    dx = int(round(distance * np.cos(angle)))
    dy = int(round(distance * np.sin(angle)))

    rows, cols = image.shape
    glcm = np.zeros((levels, levels), dtype=np.float64)

    for i in range(rows):
        for j in range(cols):
            ni = i + dy
            nj = j + dx
            if 0 <= ni < rows and 0 <= nj < cols:
                glcm[image[i, j], image[ni, nj]] += 1

    # Normalize
    total = glcm.sum()
    if total > 0:
        glcm /= total

    return glcm


def haralick_contrast(glcm: np.ndarray) -> float:
    """
    Contrast: sum of (i-j)^2 * P(i,j). High for rough textures.

    >>> import numpy as np
    >>> glcm = np.eye(4) / 4.0
    >>> haralick_contrast(glcm)
    0.0
    """
    levels = glcm.shape[0]
    i, j = np.meshgrid(range(levels), range(levels), indexing="ij")
    return float(np.sum((i - j) ** 2 * glcm))


def haralick_correlation(glcm: np.ndarray) -> float:
    """
    Correlation: measures linear dependency between gray levels.

    correlation = sum_ij [ (i - mu_i)(j - mu_j) * P(i,j) ] / (sigma_i * sigma_j)

    >>> import numpy as np
    >>> glcm = np.eye(4) / 4.0
    >>> abs(haralick_correlation(glcm) - 1.0) < 0.01
    True
    """
    levels = glcm.shape[0]
    i_idx, j_idx = np.meshgrid(range(levels), range(levels), indexing="ij")

    mu_i = np.sum(i_idx * glcm)
    mu_j = np.sum(j_idx * glcm)
    sigma_i = np.sqrt(np.sum((i_idx - mu_i) ** 2 * glcm))
    sigma_j = np.sqrt(np.sum((j_idx - mu_j) ** 2 * glcm))

    if sigma_i < 1e-10 or sigma_j < 1e-10:
        return 0.0

    correlation = np.sum((i_idx - mu_i) * (j_idx - mu_j) * glcm) / (sigma_i * sigma_j)
    return float(correlation)


def haralick_energy(glcm: np.ndarray) -> float:
    """
    Energy (ASM — Angular Second Moment): sum of P(i,j)^2.
    High for uniform textures, low for random.

    >>> import numpy as np
    >>> glcm = np.eye(4) / 4.0
    >>> haralick_energy(glcm)
    0.25
    """
    return float(np.sum(glcm**2))


def haralick_homogeneity(glcm: np.ndarray) -> float:
    """
    Homogeneity (IDM — Inverse Difference Moment):
    sum of P(i,j) / (1 + |i-j|). High when GLCM is concentrated on diagonal.

    >>> import numpy as np
    >>> glcm = np.eye(4) / 4.0
    >>> haralick_homogeneity(glcm)
    1.0
    """
    levels = glcm.shape[0]
    i, j = np.meshgrid(range(levels), range(levels), indexing="ij")
    return float(np.sum(glcm / (1 + np.abs(i - j))))


def haralick_entropy(glcm: np.ndarray) -> float:
    """
    Entropy: -sum of P(i,j) * log(P(i,j)). High for random textures.

    >>> import numpy as np
    >>> glcm = np.eye(4) / 4.0
    >>> abs(haralick_entropy(glcm) - np.log2(4)) < 0.01
    True
    """
    mask = glcm > 0
    return float(-np.sum(glcm[mask] * np.log2(glcm[mask])))


def compute_all_descriptors(
    image: np.ndarray, distance: int = 1, levels: int = 256
) -> dict[str, float]:
    """
    Compute all Haralick descriptors averaged over 4 angles (0, 45, 90, 135 degrees).

    >>> import numpy as np
    >>> img = np.array([[0, 1, 2], [1, 2, 3], [2, 3, 0]], dtype=np.uint8)
    >>> desc = compute_all_descriptors(img, levels=4)
    >>> sorted(desc.keys())
    ['contrast', 'correlation', 'energy', 'entropy', 'homogeneity']
    """
    angles = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]
    descriptors_list = []

    for angle in angles:
        glcm = compute_glcm(image, distance=distance, angle=angle, levels=levels)
        descriptors_list.append({
            "contrast": haralick_contrast(glcm),
            "correlation": haralick_correlation(glcm),
            "energy": haralick_energy(glcm),
            "homogeneity": haralick_homogeneity(glcm),
            "entropy": haralick_entropy(glcm),
        })

    # Average over angles
    result = {}
    for key in descriptors_list[0]:
        result[key] = sum(d[key] for d in descriptors_list) / len(descriptors_list)

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
