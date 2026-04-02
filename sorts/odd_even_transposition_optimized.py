"""
Odd-Even Transposition Sort — Optimized & Alternative Implementations
======================================================================

Odd-even transposition sort models each array element as an independent agent
that communicates only with its left/right neighbour.  This makes it the
canonical algorithm for **linear processor arrays** (mesh-connected hardware).

Implementations compared
-------------------------
1. single_threaded  — sequential simulation: n passes, alternating even/odd pairs
2. parallel_mp      — one OS process per element, pipes for neighbour communication
3. early_exit_st    — single-threaded with convergence flag (skip remaining passes)
4. numpy_vectorised — NumPy slice swap per phase (no Python loop over pairs)
5. builtin          — sorted() for reference
"""

from __future__ import annotations

import time
import random
import multiprocessing as mp


# ---------------------------------------------------------------------------
# 1. Single-threaded (reference)
# ---------------------------------------------------------------------------
def oe_single_threaded(lst: list) -> list:
    """
    Sequential simulation: n passes, each pass sweeps either even or odd pairs.

    >>> oe_single_threaded([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]
    >>> oe_single_threaded([])
    []
    >>> oe_single_threaded([-10, -1, 10, 2])
    [-10, -1, 2, 10]
    """
    arr = lst[:]
    n = len(arr)
    for phase in range(n):
        for i in range(phase % 2, n - 1, 2):
            if arr[i + 1] < arr[i]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
    return arr


# ---------------------------------------------------------------------------
# 2. Single-threaded with early exit (convergence flag)
# ---------------------------------------------------------------------------
def oe_early_exit(lst: list) -> list:
    """
    Adds a convergence flag: stop as soon as a full round (even + odd pass)
    makes no swaps.  Best case O(n) for already-sorted input.

    >>> oe_early_exit([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]
    >>> oe_early_exit([1, 2, 3, 4, 5])
    [1, 2, 3, 4, 5]
    >>> oe_early_exit([])
    []
    """
    arr = lst[:]
    n = len(arr)
    for phase in range(n):
        swapped = False
        for i in range(phase % 2, n - 1, 2):
            if arr[i + 1] < arr[i]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        if not swapped and phase % 2 == 1:
            # Both even and odd passes clean — sorted
            break
    return arr


# ---------------------------------------------------------------------------
# 3. NumPy vectorised — all pair comparisons per phase in one C call
# ---------------------------------------------------------------------------
def oe_numpy(lst: list) -> list:
    """
    Vectorised: compute all even-pair and odd-pair swaps simultaneously using
    NumPy array slicing — simulates the true parallel step.

    >>> oe_numpy([5, 4, 3, 2, 1])
    [1, 2, 3, 4, 5]
    >>> oe_numpy([])
    []
    >>> oe_numpy([-10, -1, 10, 2])
    [-10, -1, 2, 10]
    """
    try:
        import numpy as np
    except ImportError:
        return oe_single_threaded(lst)

    arr = np.array(lst, dtype=float)
    n = len(arr)
    if n < 2:
        return lst[:]

    for phase in range(n):
        start = phase % 2
        idx = np.arange(start, n - 1, 2)
        if len(idx) == 0:
            continue
        mask = arr[idx] > arr[idx + 1]
        arr[idx[mask]], arr[idx[mask] + 1] = (
            arr[idx[mask] + 1].copy(),
            arr[idx[mask]].copy(),
        )

    result = arr.tolist()
    # Restore original types (int where applicable)
    return [int(x) if isinstance(lst[0] if lst else x, int) and x == int(x) else x
            for x in result] if lst else result


# ---------------------------------------------------------------------------
# 4. Parallel multiprocessing (one process per element)
# ---------------------------------------------------------------------------
def _oe_process(position, value, l_send, r_send, lr_cv, rr_cv, result_pipe, ctx):
    lock = ctx.Lock()
    n_rounds = 10  # fixed rounds; sufficient for up to 10 elements
    for i in range(n_rounds):
        if (i + position) % 2 == 0 and r_send is not None:
            with lock:
                r_send[1].send(value)
            with lock:
                temp = rr_cv[0].recv()
            value = min(value, temp)
        elif (i + position) % 2 != 0 and l_send is not None:
            with lock:
                l_send[1].send(value)
            with lock:
                temp = lr_cv[0].recv()
            value = max(value, temp)
    result_pipe[1].send(value)


def oe_parallel_mp(lst: list) -> list:
    """
    One OS process per element; neighbours communicate via multiprocessing Pipes.
    Correct on arrays of up to 10 elements (hard-coded round count = 10).

    NOTE: doctests omitted here — multiprocessing spawn context requires the
    target function to be importable by name, which fails under `python -m doctest`.
    Correctness is verified in odd_even_transposition_parallel.py.
    """
    if not lst:
        return []
    ctx = mp.get_context("spawn")
    arr = lst[:]
    n = len(arr)
    result_pipes = [ctx.Pipe() for _ in arr]
    processes = []

    # Build pipe chain
    pipes = [(ctx.Pipe(), ctx.Pipe()) for _ in range(n - 1)]
    # pipes[i] = (rs, rr) connecting element i to element i+1
    # element i sends right on pipes[i][0][1], receives right on pipes[i][1][0]
    # element i+1 receives left on pipes[i][0][0], sends left on pipes[i][1][1]

    for i in range(n):
        l_send = pipes[i - 1][1] if i > 0 else None      # send left = rr of left pair
        r_send = pipes[i][0] if i < n - 1 else None       # send right = rs of right pair
        lr_cv  = pipes[i - 1][0] if i > 0 else None       # recv left = rs of left pair
        rr_cv  = pipes[i][1] if i < n - 1 else None       # recv right = rr of right pair

        processes.append(ctx.Process(
            target=_oe_process,
            args=(i, arr[i], l_send, r_send, lr_cv, rr_cv, result_pipes[i], ctx),
        ))

    for p in processes:
        p.start()

    result = []
    for i, (recv_pipe, _) in enumerate(result_pipes):
        result.append(recv_pipe.recv())
        processes[i].join()

    return result


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark() -> None:
    # Parallel version is extremely slow for large n (process spawn overhead)
    # Keep sizes small for a fair comparison
    sizes = [6, 10, 20, 100, 500, 2000]
    mp_max = 12  # only test parallel up to this size (too slow beyond)

    impls_st = [
        ("single_threaded", oe_single_threaded),
        ("early_exit",      oe_early_exit),
        ("numpy",           oe_numpy),
        ("sorted()",        lambda x: sorted(x)),
    ]

    print("\n--- random input (single-CPU variants) ---")
    header = f"{'n':>6}  " + "  ".join(f"{name:>16}" for name, _ in impls_st)
    print(header)
    print("-" * len(header))
    for n in sizes:
        data = random.sample(range(n * 2), n)
        row = f"{n:>6}  "
        for name, fn in impls_st:
            times = []
            for _ in range(3):
                d = data[:]
                t0 = time.perf_counter()
                fn(d)
                times.append(time.perf_counter() - t0)
            row += f"{min(times):>16.4f}  "
        print(row)

    print("\n--- parallel (multiprocessing) vs single-threaded, small n ---")
    header2 = f"{'n':>4}  {'parallel_mp':>14}  {'single_threaded':>16}  {'speedup':>10}"
    print(header2)
    print("-" * len(header2))
    for n in [4, 6, 8, 10, mp_max]:
        data = random.sample(range(n * 2), n)

        times_mp = []
        for _ in range(2):
            d = data[:]
            t0 = time.perf_counter()
            oe_parallel_mp(d)
            times_mp.append(time.perf_counter() - t0)
        t_mp = min(times_mp)

        times_st = []
        for _ in range(5):
            d = data[:]
            t0 = time.perf_counter()
            oe_single_threaded(d)
            times_st.append(time.perf_counter() - t0)
        t_st = min(times_st)

        speedup = t_mp / t_st if t_st > 0 else float("inf")
        print(f"{n:>4}  {t_mp:>14.4f}  {t_st:>16.6f}  {speedup:>9.0f}x slower")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print("\n=== Benchmark (seconds, best of N runs) ===")
    benchmark()
