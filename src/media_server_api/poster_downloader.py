from pathlib import Path

import requests

from ..config import POSTERS_DIR
from .recently_added_movies_and_tv_show import MediaItem


def poster_downloader(posters_to_download: tuple[MediaItem, ...]) -> None:
    """
    Downloads poster images from Plex server from the given list of poster urls.

    :param posters_to_download: the list of poster urls to be downloaded.
    :return:
    """
    Path(POSTERS_DIR).mkdir(parents=True, exist_ok=True) # create the data/posters folder if it does not exist

    # While looping through the list of posters that need to be downloaded check to see if the poster
    # has already been downloaded. If so skip it and move onto the next poster to download
    for media_item in posters_to_download:
        if not (POSTERS_DIR / f"{media_item.title}.jpg").is_file():
            response = requests.get(media_item.poster_url, stream=True)
            if response.status_code == 200:
                with open(POSTERS_DIR / f"{media_item.title}.jpg", 'wb') as file:
                    file.write(response.content)
            else:
                print(f"failed to download {media_item.title}. Status code: {response.status_code}") # TODO have this error be logged
        else:
            print(f"{media_item.title} poster is already downloaded.")