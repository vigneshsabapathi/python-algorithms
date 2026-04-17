"""
Search Google Images and download results to a local folder.

Creates a directory named 'query_<term>' and saves up to max_images JPEGs.
"""

import json
import os
import re
import urllib.request

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        " (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    )
}
GOOGLE_IMAGES_URL = "https://www.google.com/search"


def build_image_search_params(query: str) -> dict:
    """
    Build query parameters for a Google Images search.

    >>> p = build_image_search_params("cats")
    >>> p["q"]
    'cats'
    >>> p["tbm"]
    'isch'
    """
    return {"q": query, "tbm": "isch", "hl": "en", "ijn": "0"}


def download_images_from_google_query(query: str = "dhaka", max_images: int = 5) -> int:
    """
    Search Google Images for 'query' and download up to max_images images.

    Returns the number of images downloaded.

    >>> download_images_from_google_query("dhaka", 5)  # doctest: +SKIP
    5
    """
    max_images = min(max_images, 50)
    params = build_image_search_params(query)
    html = requests.get(GOOGLE_IMAGES_URL, params=params, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(html.text, "html.parser")
    matched_images_data = "".join(
        re.findall(r"AF_initDataCallback\(([^<]+)\);", str(soup.select("script")))
    )
    matched_images_data_fix = json.dumps(matched_images_data)
    matched_images_data_json = json.loads(matched_images_data_fix)
    matched_google_image_data = re.findall(
        r'\["GRID_STATE0",null,\[\[1,\[0,".*?",(.*?),"All",',
        matched_images_data_json,
    )
    if not matched_google_image_data:
        return 0

    removed_thumbnails = re.sub(
        r'\["(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)",\d+,\d+\]',
        "",
        str(matched_google_image_data),
    )
    matched_full_res_images = re.findall(
        r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]",
        removed_thumbnails,
    )
    path_name = f"query_{query.replace(' ', '_')}"
    if not os.path.exists(path_name):
        os.makedirs(path_name)

    opener = urllib.request.build_opener()
    opener.addheaders = [("User-Agent", HEADERS["User-Agent"])]
    urllib.request.install_opener(opener)

    for index, fixed_full_res_image in enumerate(matched_full_res_images):
        if index >= max_images:
            return index
        original_size_img = bytes(
            bytes(fixed_full_res_image, "ascii").decode("unicode-escape"), "ascii"
        ).decode("unicode-escape")
        urllib.request.urlretrieve(  # noqa: S310
            original_size_img, f"{path_name}/original_size_img_{index}.jpg"
        )
    return len(matched_full_res_images)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python download_images_from_google_query.py <search term>")
    else:
        count = download_images_from_google_query(sys.argv[1])
        print(f"{count} images were downloaded to disk.")
