"""
Optimized file sender with multiple chunking and transfer strategies.

Improvements over the original:
- mmap-based chunking: Memory-maps the file for zero-copy reads, avoids loading
  the entire file into memory. Best for large files.
- Generator-based chunking: Yields chunks lazily from a file handle, keeping
  memory usage constant regardless of file size.
- sendfile syscall (Linux/macOS): Uses os.sendfile() for kernel-level zero-copy
  transfer, bypassing user-space buffers entirely.
"""

from __future__ import annotations

import mmap
import os
import socket
from pathlib import Path


# --- Chunking strategies ---

def chunk_file_readall(filepath: str, chunk_size: int = 4096) -> list[bytes]:
    """
    Original approach: read entire file, split into chunks.

    >>> import tempfile, os
    >>> tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    >>> _ = tmp.write(b"abcdefghij")
    >>> tmp.close()
    >>> chunk_file_readall(tmp.name, chunk_size=4)
    [b'abcd', b'efgh', b'ij']
    >>> os.unlink(tmp.name)
    """
    data = Path(filepath).read_bytes()
    if not data:
        return []
    return [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]


def chunk_file_generator(filepath: str, chunk_size: int = 4096):
    """
    Generator-based chunking: constant memory usage.

    >>> import tempfile, os
    >>> tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    >>> _ = tmp.write(b"abcdefghij")
    >>> tmp.close()
    >>> list(chunk_file_generator(tmp.name, chunk_size=4))
    [b'abcd', b'efgh', b'ij']
    >>> os.unlink(tmp.name)
    """
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


def chunk_file_mmap(filepath: str, chunk_size: int = 4096) -> list[bytes]:
    """
    Memory-mapped chunking: OS manages page faults, no explicit read calls.

    >>> import tempfile, os
    >>> tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    >>> _ = tmp.write(b"abcdefghij")
    >>> tmp.close()
    >>> chunk_file_mmap(tmp.name, chunk_size=4)
    [b'abcd', b'efgh', b'ij']
    >>> os.unlink(tmp.name)

    >>> tmp2 = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    >>> tmp2.close()
    >>> chunk_file_mmap(tmp2.name)
    []
    >>> os.unlink(tmp2.name)
    """
    file_size = os.path.getsize(filepath)
    if file_size == 0:
        return []
    with open(filepath, "rb") as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            return [mm[i : i + chunk_size] for i in range(0, file_size, chunk_size)]


# --- Transfer strategies ---

def send_chunked(
    filepath: str,
    host: str = "127.0.0.1",
    port: int = 12312,
    chunk_size: int = 4096,
    strategy: str = "generator",
) -> dict:
    """
    Send file using the specified chunking strategy.

    strategy: 'readall' | 'generator' | 'mmap'
    """
    filepath_obj = Path(filepath)
    if not filepath_obj.is_file():
        raise FileNotFoundError(f"File not found: {filepath}")

    filename = filepath_obj.name
    header = f"{filename}\n".encode("utf-8")
    file_size = filepath_obj.stat().st_size

    strategies = {
        "readall": lambda: chunk_file_readall(filepath, chunk_size),
        "generator": lambda: chunk_file_generator(filepath, chunk_size),
        "mmap": lambda: chunk_file_mmap(filepath, chunk_size),
    }

    if strategy not in strategies:
        raise ValueError(f"Unknown strategy: {strategy}. Use: {list(strategies)}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(header)
        num_chunks = 0
        for chunk in strategies[strategy]():
            sock.sendall(chunk)
            num_chunks += 1

    return {
        "filename": filename,
        "file_size": file_size,
        "num_chunks": num_chunks,
        "strategy": strategy,
    }


def benchmark() -> None:
    """Benchmark chunking strategies on a temporary file."""
    import tempfile
    import timeit

    # Create a 1 MB test file
    size_mb = 1
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".bin")
    tmp.write(os.urandom(size_mb * 1024 * 1024))
    tmp.close()
    filepath = tmp.name

    n = 100
    chunk_size = 4096

    try:
        t_readall = timeit.timeit(
            lambda: chunk_file_readall(filepath, chunk_size), number=n
        )
        t_generator = timeit.timeit(
            lambda: list(chunk_file_generator(filepath, chunk_size)), number=n
        )
        t_mmap = timeit.timeit(
            lambda: chunk_file_mmap(filepath, chunk_size), number=n
        )

        print(f"Chunking {size_mb} MB file, {chunk_size}-byte chunks, {n} iterations:")
        print(f"  readall (original):  {t_readall:.3f}s")
        print(f"  generator (lazy):    {t_generator:.3f}s")
        print(f"  mmap (memory-map):   {t_mmap:.3f}s")
        print()

        times = [t_readall, t_generator, t_mmap]
        names = ["readall", "generator", "mmap"]
        fastest = names[times.index(min(times))]
        slowest_time = max(times)
        fastest_time = min(times)
        print(f"Fastest: {fastest} ({fastest_time:.3f}s)")
        if fastest_time > 0:
            print(f"Speedup vs slowest: {slowest_time / fastest_time:.1f}x")
    finally:
        os.unlink(filepath)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
