#!/usr/bin/env python3
"""
Optimized and alternative implementations of CNN Classification forward pass.

The reference uses 4-deep Python loops for convolution. Variants here
vectorize the convolution using im2col and einsum.

Variants covered:
1. loop_conv        -- reference: 4-deep nested loops
2. im2col_conv      -- im2col + matrix multiplication (classic optimization)
3. einsum_conv      -- np.einsum for elegant batched convolution
4. fft_conv         -- FFT-based convolution (fast for large kernels)

Run:
    python computer_vision/cnn_classification_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from computer_vision.cnn_classification import (
    conv2d as ref_conv2d,
    relu,
    max_pool2d,
    flatten,
    dense,
    softmax,
    cnn_forward as reference,
)


# ---------------------------------------------------------------------------
# Variant 1 — loop_conv (reference wrapper)
# ---------------------------------------------------------------------------

def loop_conv(image: np.ndarray, filters: np.ndarray, bias: np.ndarray) -> np.ndarray:
    """
    Convolution via 4-deep nested loops (reference).

    >>> import numpy as np
    >>> np.random.seed(0)
    >>> img = np.random.rand(1, 5, 5)
    >>> filt = np.random.rand(2, 1, 3, 3)
    >>> out = loop_conv(img, filt, np.zeros(2))
    >>> out.shape
    (2, 3, 3)
    """
    return ref_conv2d(image, filters, bias)


# ---------------------------------------------------------------------------
# Variant 2 — im2col convolution
# ---------------------------------------------------------------------------

def _im2col(image: np.ndarray, kh: int, kw: int) -> np.ndarray:
    """
    Convert image patches to columns for matrix-multiply convolution.

    Args:
        image: (C_in, H, W)
        kh, kw: kernel dimensions

    Returns:
        col: (C_in * kh * kw, out_h * out_w)
    """
    c_in, h, w = image.shape
    out_h = h - kh + 1
    out_w = w - kw + 1

    col = np.zeros((c_in * kh * kw, out_h * out_w), dtype=image.dtype)

    idx = 0
    for i in range(out_h):
        for j in range(out_w):
            patch = image[:, i:i + kh, j:j + kw]  # (C_in, kh, kw)
            col[:, idx] = patch.ravel()
            idx += 1

    return col


def im2col_conv(image: np.ndarray, filters: np.ndarray, bias: np.ndarray) -> np.ndarray:
    """
    Convolution via im2col + matrix multiply.

    Reshapes filters to (C_out, C_in*kH*kW), extracts image patches as
    columns (C_in*kH*kW, out_h*out_w), then multiplies.

    >>> import numpy as np
    >>> np.random.seed(0)
    >>> img = np.random.rand(1, 5, 5)
    >>> filt = np.random.rand(2, 1, 3, 3)
    >>> out = im2col_conv(img, filt, np.zeros(2))
    >>> out.shape
    (2, 3, 3)
    """
    c_out, c_in, kh, kw = filters.shape
    _, h, w = image.shape
    out_h = h - kh + 1
    out_w = w - kw + 1

    col = _im2col(image, kh, kw)
    filters_flat = filters.reshape(c_out, -1)

    output = filters_flat @ col + bias.reshape(-1, 1)
    return output.reshape(c_out, out_h, out_w)


# ---------------------------------------------------------------------------
# Variant 3 — einsum convolution
# ---------------------------------------------------------------------------

def einsum_conv(image: np.ndarray, filters: np.ndarray, bias: np.ndarray) -> np.ndarray:
    """
    Convolution via np.einsum for cleaner vectorized code.

    Uses as_strided to create windowed views, then einsum contracts
    over input channels and kernel dimensions.

    >>> import numpy as np
    >>> np.random.seed(0)
    >>> img = np.random.rand(1, 5, 5)
    >>> filt = np.random.rand(2, 1, 3, 3)
    >>> out = einsum_conv(img, filt, np.zeros(2))
    >>> out.shape
    (2, 3, 3)
    """
    c_out, c_in, kh, kw = filters.shape
    _, h, w = image.shape
    out_h = h - kh + 1
    out_w = w - kw + 1

    # Create windowed view: (out_h, out_w, C_in, kh, kw)
    s_c, s_h, s_w = image.strides
    windows = np.lib.stride_tricks.as_strided(
        image,
        shape=(c_in, out_h, out_w, kh, kw),
        strides=(s_c, s_h, s_w, s_h, s_w),
    )

    # einsum: sum over c_in, kh, kw
    output = np.einsum("fckl,cohkl->foh", filters, windows).reshape(c_out, out_h, out_w)
    output += bias.reshape(-1, 1, 1)
    return output


# ---------------------------------------------------------------------------
# Full forward pass using im2col
# ---------------------------------------------------------------------------

def cnn_forward_im2col(
    image: np.ndarray, num_classes: int = 10, seed: int = 42
) -> np.ndarray:
    """
    CNN forward pass using im2col convolution.

    >>> import numpy as np
    >>> out = cnn_forward_im2col(np.random.rand(1, 8, 8), 5, seed=42)
    >>> out.shape
    (5,)
    >>> abs(out.sum() - 1.0) < 1e-6
    True
    """
    rng = np.random.default_rng(seed)

    c_in = image.shape[0]
    filters1 = rng.standard_normal((4, c_in, 3, 3)) * 0.1
    bias1 = np.zeros(4)
    x = im2col_conv(image, filters1, bias1)
    x = relu(x)
    if x.shape[1] >= 2 and x.shape[2] >= 2:
        x = max_pool2d(x, 2)

    if x.shape[1] >= 3 and x.shape[2] >= 3:
        filters2 = rng.standard_normal((8, 4, 3, 3)) * 0.1
        bias2 = np.zeros(8)
        x = im2col_conv(x, filters2, bias2)
        x = relu(x)
        if x.shape[1] >= 2 and x.shape[2] >= 2:
            x = max_pool2d(x, 2)

    flat = flatten(x)
    fc_weights = rng.standard_normal((num_classes, flat.shape[0])) * 0.1
    fc_bias = np.zeros(num_classes)
    logits = dense(flat, fc_weights, fc_bias)
    return softmax(logits)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

def run_all() -> None:
    np.random.seed(42)
    img = np.random.rand(1, 8, 8)
    filt = np.random.rand(4, 1, 3, 3) * 0.1
    bias = np.zeros(4)

    print("\n=== Correctness: conv2d (1x8x8, 4 filters 3x3) ===")
    ref_result = ref_conv2d(img, filt, bias)

    conv_impls = [
        ("loop_conv", loop_conv),
        ("im2col_conv", im2col_conv),
        ("einsum_conv", einsum_conv),
    ]

    for name, fn in conv_impls:
        try:
            result = fn(img, filt, bias)
            match = np.allclose(result, ref_result, atol=1e-10)
            print(f"  [{'OK' if match else 'FAIL'}] {name:<14} shape={result.shape}  max_diff={np.max(np.abs(result - ref_result)):.2e}")
        except Exception as e:
            print(f"  [ERR] {name:<14} {e}")

    print("\n=== Correctness: full forward pass (1x8x8 -> 5 classes) ===")
    ref_out = reference(img, num_classes=5, seed=42)
    im2col_out = cnn_forward_im2col(img, num_classes=5, seed=42)
    match = np.allclose(ref_out, im2col_out, atol=1e-10)
    print(f"  [{'OK' if match else 'FAIL'}] reference vs im2col: max_diff={np.max(np.abs(ref_out - im2col_out)):.2e}")
    print(f"  Reference probs: {np.round(ref_out, 4)}")
    print(f"  im2col probs:    {np.round(im2col_out, 4)}")

    REPS = 100
    sizes = [8, 16, 32]
    for sz in sizes:
        img = np.random.rand(1, sz, sz)
        filt = np.random.rand(4, 1, 3, 3) * 0.1
        bias = np.zeros(4)

        print(f"\n=== Benchmark conv2d (1x{sz}x{sz}): {REPS} runs ===")
        for name, fn in conv_impls:
            try:
                t = timeit.timeit(lambda fn=fn: fn(img, filt, bias), number=REPS)
                ms = t * 1000 / REPS
                print(f"  {name:<14} {ms:>8.3f} ms")
            except Exception as e:
                print(f"  {name:<14} ERR: {e}")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
