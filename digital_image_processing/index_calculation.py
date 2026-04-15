"""
Index Calculation for Remote Sensing

Computes vegetation and soil indices from multispectral image bands.
Common indices: NDVI, SAVI, BNDVI, GLI.

Reference: https://github.com/TheAlgorithms/Python/blob/master/digital_image_processing/index_calculation.py
"""

import numpy as np


def ndvi(nir: np.ndarray, red: np.ndarray) -> np.ndarray:
    """
    Normalized Difference Vegetation Index.
    NDVI = (NIR - Red) / (NIR + Red)
    Range: [-1, 1]. Higher values indicate healthier vegetation.

    >>> nir = np.array([[0.8, 0.6]], dtype=np.float64)
    >>> red = np.array([[0.2, 0.4]], dtype=np.float64)
    >>> np.round(ndvi(nir, red), 4)
    array([[0.6, 0.2]])

    >>> ndvi(np.array([[0.0]]), np.array([[0.0]]))
    array([[0.]])
    """
    denominator = nir.astype(np.float64) + red.astype(np.float64)
    return np.where(denominator == 0, 0.0, (nir - red) / denominator)


def savi(nir: np.ndarray, red: np.ndarray, soil_factor: float = 0.5) -> np.ndarray:
    """
    Soil-Adjusted Vegetation Index.
    SAVI = ((NIR - Red) / (NIR + Red + L)) * (1 + L)
    L is the soil brightness correction factor (default 0.5).

    >>> nir = np.array([[0.8, 0.6]], dtype=np.float64)
    >>> red = np.array([[0.2, 0.4]], dtype=np.float64)
    >>> np.round(savi(nir, red), 4)
    array([[0.6, 0.2]])

    >>> np.round(savi(nir, red, soil_factor=0.0), 4)
    array([[0.6, 0.2]])
    """
    l = soil_factor
    denominator = nir.astype(np.float64) + red.astype(np.float64) + l
    return np.where(
        denominator == 0, 0.0, ((nir - red) / denominator) * (1 + l)
    )


def bndvi(nir: np.ndarray, blue: np.ndarray) -> np.ndarray:
    """
    Blue Normalized Difference Vegetation Index.
    BNDVI = (NIR - Blue) / (NIR + Blue)

    >>> nir = np.array([[0.8]], dtype=np.float64)
    >>> blue = np.array([[0.1]], dtype=np.float64)
    >>> np.round(bndvi(nir, blue), 4)
    array([[0.7778]])
    """
    denominator = nir.astype(np.float64) + blue.astype(np.float64)
    return np.where(denominator == 0, 0.0, (nir - blue) / denominator)


def gli(green: np.ndarray, red: np.ndarray, blue: np.ndarray) -> np.ndarray:
    """
    Green Leaf Index.
    GLI = (2 * Green - Red - Blue) / (2 * Green + Red + Blue)

    >>> g = np.array([[0.5]], dtype=np.float64)
    >>> r = np.array([[0.3]], dtype=np.float64)
    >>> b = np.array([[0.2]], dtype=np.float64)
    >>> np.round(gli(g, r, b), 4)
    array([[0.3333]])
    """
    numerator = 2 * green.astype(np.float64) - red.astype(np.float64) - blue.astype(np.float64)
    denominator = 2 * green.astype(np.float64) + red.astype(np.float64) + blue.astype(np.float64)
    return np.where(denominator == 0, 0.0, numerator / denominator)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    # Demo with synthetic bands
    np.random.seed(42)
    nir_band = np.random.uniform(0.3, 0.9, (4, 4))
    red_band = np.random.uniform(0.1, 0.5, (4, 4))
    blue_band = np.random.uniform(0.05, 0.3, (4, 4))
    green_band = np.random.uniform(0.1, 0.6, (4, 4))

    print(f"\nNDVI range: [{ndvi(nir_band, red_band).min():.4f}, {ndvi(nir_band, red_band).max():.4f}]")
    print(f"SAVI range: [{savi(nir_band, red_band).min():.4f}, {savi(nir_band, red_band).max():.4f}]")
    print(f"BNDVI range: [{bndvi(nir_band, blue_band).min():.4f}, {bndvi(nir_band, blue_band).max():.4f}]")
    print(f"GLI range: [{gli(green_band, red_band, blue_band).min():.4f}, {gli(green_band, red_band, blue_band).max():.4f}]")
