"""
Download an Instagram video or IGTV using downloadgram.net.

Saves the video as a timestamped .mp4 file in the current directory.
"""

from datetime import UTC, datetime

import requests

DOWNLOADGRAM_URL = "https://downloadgram.net/wp-json/wppress/video-downloader/video?url="


def download_video(url: str) -> bytes:
    """
    Resolve and download Instagram video bytes via downloadgram.net.

    >>> isinstance(download_video("https://www.instagram.com/p/example/"), bytes)  # doctest: +SKIP
    True
    """
    video_url = requests.get(DOWNLOADGRAM_URL + url, timeout=10).text.strip()
    return requests.get(video_url, timeout=30).content


if __name__ == "__main__":
    url = input("Enter Video/IGTV url: ").strip()
    file_name = f"{datetime.now(tz=UTC).astimezone():%Y-%m-%d_%H-%M-%S}.mp4"
    with open(file_name, "wb") as fp:
        fp.write(download_video(url))
    print(f"Done. Video saved to disk as {file_name}.")
