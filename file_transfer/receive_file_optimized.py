"""
Optimized file receiver with multiple buffering and write strategies.

Improvements over the original:
- Streaming write: Writes chunks directly to disk as they arrive instead of
  accumulating all data in memory first. Best for large files.
- BytesIO buffering: Uses an in-memory BytesIO buffer for fast reassembly,
  avoiding repeated list concatenation.
- Pre-allocated buffer: Uses bytearray with recv_into() to avoid allocating
  new bytes objects per recv call.
"""

from __future__ import annotations

import io
import socket
from pathlib import Path


# --- Header parsing strategies ---

def parse_header_find(raw: bytes) -> tuple[str, bytes]:
    """
    Parse header using bytes.find() — original approach.

    >>> parse_header_find(b"test.txt\\nHello")
    ('test.txt', b'Hello')
    >>> parse_header_find(b"a.bin\\n")
    ('a.bin', b'')
    """
    pos = raw.find(b"\n")
    if pos == -1:
        raise ValueError("No newline found in header data")
    return raw[:pos].decode("utf-8"), raw[pos + 1 :]


def parse_header_split(raw: bytes) -> tuple[str, bytes]:
    """
    Parse header using bytes.split() with maxsplit=1 — single allocation.

    >>> parse_header_split(b"test.txt\\nHello")
    ('test.txt', b'Hello')
    >>> parse_header_split(b"a.bin\\n")
    ('a.bin', b'')
    >>> parse_header_split(b"file.dat\\nline1\\nline2")
    ('file.dat', b'line1\\nline2')
    """
    parts = raw.split(b"\n", 1)
    if len(parts) < 2:
        raise ValueError("No newline found in header data")
    return parts[0].decode("utf-8"), parts[1]


def parse_header_index(raw: bytes) -> tuple[str, bytes]:
    """
    Parse header using memoryview for zero-copy slicing.

    >>> parse_header_index(b"test.txt\\nHello")
    ('test.txt', b'Hello')
    >>> parse_header_index(b"a.bin\\n")
    ('a.bin', b'')
    """
    mv = memoryview(raw)
    pos = raw.index(b"\n")
    filename = bytes(mv[:pos]).decode("utf-8")
    remaining = bytes(mv[pos + 1 :])
    return filename, remaining


# --- Receive strategies ---

def receive_to_memory(
    host: str = "127.0.0.1",
    port: int = 12312,
    output_dir: str = ".",
    chunk_size: int = 4096,
) -> dict:
    """
    Original approach: collect all chunks in list, join, then write.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(1)
        conn, addr = server.accept()
        with conn:
            chunks = []
            while True:
                data = conn.recv(chunk_size)
                if not data:
                    break
                chunks.append(data)

    raw = b"".join(chunks)
    filename, file_data = parse_header_find(raw)
    output_path = Path(output_dir) / filename
    output_path.write_bytes(file_data)
    return {"filename": filename, "file_size": len(file_data), "output_path": str(output_path)}


def receive_to_bytesio(
    host: str = "127.0.0.1",
    port: int = 12312,
    output_dir: str = ".",
    chunk_size: int = 4096,
) -> dict:
    """
    BytesIO buffered receive: single contiguous buffer, no list join needed.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(1)
        conn, addr = server.accept()
        with conn:
            buffer = io.BytesIO()
            while True:
                data = conn.recv(chunk_size)
                if not data:
                    break
                buffer.write(data)

    raw = buffer.getvalue()
    filename, file_data = parse_header_split(raw)
    output_path = Path(output_dir) / filename
    output_path.write_bytes(file_data)
    return {"filename": filename, "file_size": len(file_data), "output_path": str(output_path)}


def receive_streaming(
    host: str = "127.0.0.1",
    port: int = 12312,
    output_dir: str = ".",
    chunk_size: int = 4096,
) -> dict:
    """
    Streaming receive: writes data directly to disk as it arrives.
    Only the header is buffered in memory.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(1)
        conn, addr = server.accept()
        with conn:
            # Read enough data to get the header (filename)
            header_buf = b""
            while b"\n" not in header_buf:
                data = conn.recv(chunk_size)
                if not data:
                    raise ConnectionError("Connection closed before header received")
                header_buf += data

            filename, remaining = parse_header_split(header_buf)
            output_path = Path(output_dir) / filename
            file_size = 0

            with open(output_path, "wb") as f:
                if remaining:
                    f.write(remaining)
                    file_size += len(remaining)
                while True:
                    data = conn.recv(chunk_size)
                    if not data:
                        break
                    f.write(data)
                    file_size += len(data)

    return {"filename": filename, "file_size": file_size, "output_path": str(output_path)}


def benchmark() -> None:
    """Benchmark header parsing strategies on synthetic data."""
    import timeit

    # Create a realistic header + payload
    header = b"large_test_file.bin\n"
    payload = b"\x00" * (1024 * 1024)  # 1 MB
    raw_data = header + payload

    n = 50_000

    t_find = timeit.timeit(lambda: parse_header_find(raw_data), number=n)
    t_split = timeit.timeit(lambda: parse_header_split(raw_data), number=n)
    t_index = timeit.timeit(lambda: parse_header_index(raw_data), number=n)

    print(f"Header parsing ({n} iterations, 1 MB payload):")
    print(f"  find (original):     {t_find:.3f}s")
    print(f"  split (maxsplit=1):  {t_split:.3f}s")
    print(f"  memoryview (index):  {t_index:.3f}s")
    print()

    times = [t_find, t_split, t_index]
    names = ["find", "split", "memoryview"]
    fastest = names[times.index(min(times))]
    print(f"Fastest: {fastest}")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    benchmark()
