"""
Download the 'og:image' from an Instagram post URL.

Saves image as a timestamped .jpg file in the current directory.
"""

from datetime import UTC, datetime

import requests
from bs4 import BeautifulSoup


def download_image(url: str) -> str:
    """
    Scrape the og:image meta tag from the URL and download the image.

    Returns a message indicating success or the type of failure.

    >>> download_image("https://www.instagram.com")  # doctest: +SKIP
    'Image downloaded and saved in the file 2024-01-01_12-00-00.jpg'
    >>> download_image("https://httpstat.us/404")  # doctest: +SKIP
    'An error occurred during the HTTP request ...'
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"An error occurred during the HTTP request to {url}: {e!r}"

    soup = BeautifulSoup(response.text, "html.parser")
    image_meta_tag = soup.find("meta", {"property": "og:image"})
    if not image_meta_tag:
        return "No meta tag with property 'og:image' was found."

    image_url = image_meta_tag.get("content")
    if not image_url:
        return f"Image URL not found in meta tag {image_meta_tag}."

    try:
        image_data = requests.get(image_url, timeout=10).content
    except requests.RequestException as e:
        return f"An error occurred during the HTTP request to {image_url}: {e!r}"

    if not image_data:
        return f"Failed to download the image from {image_url}."

    file_name = f"{datetime.now(tz=UTC).astimezone():%Y-%m-%d_%H-%M-%S}.jpg"
    with open(file_name, "wb") as out_file:
        out_file.write(image_data)
    return f"Image downloaded and saved in the file {file_name}"


if __name__ == "__main__":
    url = input("Enter image URL: ").strip() or "https://www.instagram.com"
    print(f"download_image({url}): {download_image(url)}")
