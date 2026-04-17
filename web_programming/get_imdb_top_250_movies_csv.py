"""
Scrape the IMDB Top 250 movies list and write results to a CSV file.

Parses title and rating from the IMDB chart page.
"""

from __future__ import annotations

import csv

import requests
from bs4 import BeautifulSoup

IMDB_TOP_250_URL = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"


def get_imdb_top_250_movies(url: str = "") -> dict[str, float]:
    """
    Scrape IMDB Top 250 and return {movie_title: imdb_rating} dict.

    >>> isinstance(get_imdb_top_250_movies(), dict)  # doctest: +SKIP
    True
    """
    url = url or IMDB_TOP_250_URL
    soup = BeautifulSoup(requests.get(url, timeout=10).text, "html.parser")
    titles = soup.find_all("h3", class_="ipc-title__text")
    ratings = soup.find_all("span", class_="ipc-rating-star--rating")
    return {
        title.a.text: float(rating.strong.text)
        for title, rating in zip(titles, ratings)
    }


def write_movies(filename: str = "IMDb_Top_250_Movies.csv") -> None:
    """
    Write the IMDB Top 250 to a CSV file with columns 'Movie title' and 'IMDb rating'.

    >>> write_movies("test_imdb.csv")  # doctest: +SKIP
    """
    movies = get_imdb_top_250_movies()
    with open(filename, "w", newline="") as out_file:
        writer = csv.writer(out_file)
        writer.writerow(["Movie title", "IMDb rating"])
        for title, rating in movies.items():
            writer.writerow([title, rating])


if __name__ == "__main__":
    write_movies()
    print("IMDb_Top_250_Movies.csv written.")
