# ruff: noqa: DTZ005
## Cannot specify a timezone for Plex uses an offset-native date times.
import os
from collections.abc import Generator
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto, unique
from typing import TypeVar

from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

from .plex_server_instance import PlexServerInstance


@unique
class RecentlyAddedRangeOptions(Enum):
    DAY = auto()
    THREE_DAYS = auto()
    WEEK = auto()
    TWO_WEEKS = auto()
    THREE_WEEKS = auto()
    MONTH = auto()
    TWO_MONTHS = auto()
    THREE_MONTHS = auto()

@dataclass
class MediaItem:
    type : str
    title : str
    posterUrl : str

    def __repr__(self):
        return f"MediaItem(type={self.type}, title={self.title}, posterUrl={self.posterUrl})"

    def __str__(self):
        return f"{self.title}"

T = TypeVar("T") # using a generic type for the generator and return plex_api Movie or Show object
def specified_range_movies_and_tv_show_generator() -> Generator[T]:
    """
    Returns the media in the movie(s) and TV show(s) sections on the Plex server.

    :return:
    """
    plex_server_instance = PlexServerInstance()
    load_dotenv()

    for movie_section in [os.environ.get("MOVIE_SECTION_ONE"), os.environ.get("MOVIE_SECTION_TWO")]:
        for i in plex_server_instance.server_port.library.section(movie_section).all():
            yield i

    for tv_show_section in [os.environ.get("TV_SHOW_SECTION_ONE"), os.environ.get("TV_SHOW_SECTION_TWO")]:
        for i in plex_server_instance.server_port.library.section(tv_show_section).all():
            yield i

def recently_added_movies_and_tv_show(recently_added_range: RecentlyAddedRangeOptions) -> tuple[MediaItem, ...]:
    """
    Pulls the recently added movie and TV shows from the plex server.

    :param recently_added_range: the range to be considered "recently added" movie(s) and TV show(s).
    :return: A tuple of movie(s) and TV show(s)
    """
    recently_added_media = []

    # Calculate the cutoff_date to filter media that have been added afterward.
    #
    # Cannot specify a timezone for Plex uses an offset-native date times.
    match recently_added_range:
        case RecentlyAddedRangeOptions.DAY:
            cutoff_date = datetime.now() - relativedelta(days=1)
        case RecentlyAddedRangeOptions.THREE_DAYS:
            cutoff_date = datetime.now() - relativedelta(days=3)
        case RecentlyAddedRangeOptions.WEEK:
            cutoff_date = datetime.now() - relativedelta(weeks=1)
        case RecentlyAddedRangeOptions.TWO_WEEKS:
            cutoff_date = datetime.now() - relativedelta(weeks=2)
        case RecentlyAddedRangeOptions.THREE_WEEKS:
            cutoff_date = datetime.now() - relativedelta(weeks=3)
        case RecentlyAddedRangeOptions.MONTH:
            cutoff_date = datetime.now() - relativedelta(months=1)
        case RecentlyAddedRangeOptions.TWO_MONTHS:
            cutoff_date = datetime.now() - relativedelta(months=2)
        case RecentlyAddedRangeOptions.THREE_MONTHS:
            cutoff_date = datetime.now() - relativedelta(months=3)

    # filter out the media on the server that don't meet the cutoff date requirements. From each media that pass
    # pull the title, posterUrl, and TYPE (i.e., movie or TV show) and save it to the MediaItem dataclass.
    for media_entry in specified_range_movies_and_tv_show_generator():
        if media_entry.addedAt > cutoff_date.replace(microsecond=0): # removed microseconds given Plex datetime only goes down to the second
            recently_added_media.append(MediaItem(media_entry.TYPE, media_entry.title, media_entry.posterUrl))

    return tuple(recently_added_media)

# use for testing given cannot write unit test code
if __name__ == "__main__":
    bar = recently_added_movies_and_tv_show(RecentlyAddedRangeOptions.THREE_MONTHS)
    print(bar)
