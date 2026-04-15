"""
Socket-based file receiver.

Protocol:
1. Bind to (host, port) and listen for one TCP connection.
2. Read until newline to extract the filename.
3. Read remaining data in chunks until sender closes connection.
4. Write received bytes to output directory with the original filename.

Source: https://github.com/TheAlgorithms/Python/blob/master/file_transfer/receive_file.py
"""

from __future__ import annotations

import socket
from pathlib import Path


def parse_header(raw: bytes) -> tuple[str, bytes]:
    """
    Extract filename from header bytes and return (filename, remaining_data).

    The header is the first newline-terminated line.

    >>> parse_header(b"notes.txt\\nHello World")
    ('notes.txt', b'Hello World')
    >>> parse_header(b"file.bin\\n")
    ('file.bin', b'')
    >>> parse_header(b"my doc.pdf\\n\\x00\\x01\\x02")
    ('my doc.pdf', b'\\x00\\x01\\x02')
    >>> parse_header(b"\\n")
    ('', b'')
    """
    newline_pos = raw.index(b"\n")
    filename = raw[:newline_pos].decode("utf-8")
    remaining = raw[newline_pos + 1 :]
    return filename, remaining


def reassemble_chunks(chunks: list[bytes]) -> bytes:
    """
    Reassemble received byte chunks into complete file data.

    >>> reassemble_chunks([b"hello", b" ", b"world"])
    b'hello world'
    >>> reassemble_chunks([])
    b''
    >>> reassemble_chunks([b"single"])
    b'single'
    >>> reassemble_chunks([b"\\x00\\x01", b"\\x02\\x03"])
    b'\\x00\\x01\\x02\\x03'
    """
    return b"".join(chunks)


def validate_filename(filename: str) -> bool:
    """
    Check whether a received filename is safe (no path traversal).

    >>> validate_filename("notes.txt")
    True
    >>> validate_filename("my_file.pdf")
    True
    >>> validate_filename("../../../etc/passwd")
    False
    >>> validate_filename("/absolute/path.txt")
    False
    >>> validate_filename("sub/dir/file.txt")
    False
    >>> validate_filename("")
    False
    >>> validate_filename(".")
    False
    >>> validate_filename("..")
    False
    """
    if not filename or "/" in filename or "\\" in filename:
        return False
    if filename in (".", "..") or filename.startswith(".."):
        return False
    return True


def receive_file(
    host: str = "127.0.0.1",
    port: int = 12312,
    output_dir: str = ".",
    chunk_size: int = 4096,
) -> dict:
    """
    Listen for a single file transfer on (host, port).

    Returns dict with keys: filename, file_size, output_path.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen(1)
        print(f"Listening on {host}:{port}...")

        conn, addr = server.accept()
        print(f"Connection from {addr}")

        with conn:
            # Receive all data
            chunks: list[bytes] = []
            while True:
                data = conn.recv(chunk_size)
                if not data:
                    break
                chunks.append(data)

    raw_data = reassemble_chunks(chunks)
    filename, file_data = parse_header(raw_data)

    if not validate_filename(filename):
        raise ValueError(f"Unsafe filename received: {filename!r}")

    output_path = Path(output_dir) / filename
    output_path.write_bytes(file_data)

    return {
        "filename": filename,
        "file_size": len(file_data),
        "output_path": str(output_path),
    }


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)

    print("\n--- receive_file demo ---")
    print("Starting receiver on localhost:12312...")
    print("Run send_file.py in another terminal to transfer a file.")
    # Uncomment to actually listen:
    # result = receive_file()
    # print(f"Received: {result}")
