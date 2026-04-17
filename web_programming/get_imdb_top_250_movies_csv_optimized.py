"""
IMDB Top 250 CSV – three CSV-writing approaches + benchmark.

Approach 1: csv.writer (original)
Approach 2: pandas DataFrame.to_csv
Approach 3: manual string join
"""

import io
import time

SAMPLE_MOVIES = {
    "The Shawshank Redemption": 9.3,
    "The Godfather": 9.2,
    "The Dark Knight": 9.0,
    "Schindler's List": 8.9,
    "The Lord of the Rings: The Return of the King": 8.9,
}


# ---------------------------------------------------------------------------
# Approach 1 – csv.writer (original)
# ---------------------------------------------------------------------------
def write_movies_csv_writer(movies: dict[str, float]) -> str:
    """
    Write movies to CSV using csv.writer, return content as string.

    >>> out = write_movies_csv_writer({"Film A": 9.1})
    >>> "Film A" in out
    True
    >>> "9.1" in out
    True
    """
    import csv

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["Movie title", "IMDb rating"])
    for title, rating in movies.items():
        writer.writerow([title, rating])
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Approach 2 – pandas to_csv
# ---------------------------------------------------------------------------
def write_movies_pandas(movies: dict[str, float]) -> str:
    """
    Write movies to CSV using pandas DataFrame.to_csv(), return as string.

    >>> out = write_movies_pandas({"Film A": 9.1})
    >>> "Film A" in out
    True
    """
    import pandas as pd

    df = pd.DataFrame(movies.items(), columns=["Movie title", "IMDb rating"])
    return df.to_csv(index=False)


# ---------------------------------------------------------------------------
# Approach 3 – manual string join
# ---------------------------------------------------------------------------
def write_movies_manual(movies: dict[str, float]) -> str:
    """
    Write movies to CSV manually using string join.

    >>> out = write_movies_manual({"Film A": 9.1})
    >>> out.startswith("Movie title")
    True
    >>> "Film A,9.1" in out
    True
    """
    lines = ["Movie title,IMDb rating"]
    for title, rating in movies.items():
        lines.append(f"{title},{rating}")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Benchmark
# ---------------------------------------------------------------------------
def benchmark(runs: int = 10_000) -> None:
    approaches = [
        ("csv.writer", write_movies_csv_writer),
        ("pandas", write_movies_pandas),
        ("manual join", write_movies_manual),
    ]
    for name, fn in approaches:
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(SAMPLE_MOVIES)
        elapsed = time.perf_counter() - t0
        print(f"{name:12s}: {runs} runs in {elapsed:.4f}s ({elapsed/runs*1e6:.2f} µs/run)")


if __name__ == "__main__":
    from doctest import testmod
    testmod()
    benchmark()
