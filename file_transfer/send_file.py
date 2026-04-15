"""
Socket-based file sender.

Protocol:
1. Connect to receiver on (host, port) via TCP.
2. Send filename as UTF-8 string, terminated by newline.
3. Send file contents in fixed-size chunks until EOF.
4. Close socket to signal completion.

Source: https://github.com/TheAlgorithms/Python/blob/master/file_transfer/send_file.py
"""

from __future__ import annotations

import socket
from pathlib import Path


def make_header(filename: str) -> bytes:
    """
    Create a newline-terminated header containing the filename.

    >>> make_header("notes.txt")
    b'notes.txt\\n'
    >>> make_header("my file.pdf")
    b'my file.pdf\\n'
    >>> make_header("")
    b'\\n'
    """
    return f"{filename}\n".encode("utf-8")


def chunk_file(filepath: str, chunk_size: int = 4096) -> list[bytes]:
    """
    Read a file and return its contents as a list of byte chunks.

    >>> import tempfile, os
    >>> tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    >>> _ = tmp.write(b"hello world")
    >>> tmp.close()
    >>> chunks = chunk_file(tmp.name, chunk_size=5)
    >>> chunks
    [b'hello', b' worl', b'd']
    >>> b"".join(chunks)
    b'hello world'
    >>> os.unlink(tmp.name)

    >>> tmp2 = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    >>> tmp2.close()
    >>> chunk_file(tmp2.name)
    []
    >>> os.unlink(tmp2.name)
    """
    data = Path(filepath).read_bytes()
    if not data:
        return []
    return [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]


def compute_transfer_stats(filepath: str, chunk_size: int = 4096) -> dict:
    """
    Compute transfer statistics without actually sending.

    >>> import tempfile, os
    >>> tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
    >>> _ = tmp.write(b"x" * 10000)
    >>> tmp.close()
    >>> stats = compute_transfer_stats(tmp.name, chunk_size=4096)
    >>> stats["file_size"]
    10000
    >>> stats["num_chunks"]
    3
    >>> stats["chunk_size"]
    4096
    >>> stats["last_chunk_size"]
    1808
    >>> os.unlink(tmp.name)

    >>> tmp2 = tempfile.NamedTemporaryFile(delete=False, suffix=".bin")
    >>> _ = tmp2.write(b"a" * 4096)
    >>> tmp2.close()
    >>> stats2 = compute_transfer_stats(tmp2.name, chunk_size=4096)
    >>> stats2["num_chunks"]
    1
    >>> stats2["last_chunk_size"]
    4096
    >>> os.unlink(tmp2.name)
    """
    file_size = Path(filepath).stat().st_size
    if file_size == 0:
        return {
            "file_size": 0,
            "num_chunks": 0,
            "chunk_size": chunk_size,
            "last_chunk_size": 0,
        }
    num_chunks = (file_size + chunk_size - 1) // chunk_size
    last_chunk_size = file_size % chunk_size or chunk_size
    return {
        "file_size": file_size,
        "num_chunks": num_chunks,
        "chunk_size": chunk_size,
        "last_chunk_size": last_chunk_size,
    }


def send_file(
    filepath: str,
    host: str = "127.0.0.1",
    port: int = 12312,
    chunk_size: int = 4096,
) -> dict:
    """
    Send a file to a receiver listening on (host, port).

    Returns transfer stats dict with keys: file_size, num_chunks, filename.
    """
    filepath_obj = Path(filepath)
    if not filepath_obj.is_file():
        raise FileNotFoundError(f"File not found: {filepath}")

    filename = filepath_obj.name
    header = make_header(filename)
    chunks = chunk_file(filepath, chunk_size)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(header)
        for chunk in chunks:
            sock.sendall(chunk)

    return {
        "filename": filename,
        "file_size": filepath_obj.stat().st_size,
        "num_chunks": len(chunks),
    }


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    # Live demo requires receive_file.py running on localhost:12312
    # Usage: python -m file_transfer.send_file
    print("\n--- send_file demo ---")
    print("To test: start receive_file.py first, then run this script with a file arg.")
    print("Example: python -c \"from file_transfer.send_file import send_file; "
          "send_file('README.md')\"")
