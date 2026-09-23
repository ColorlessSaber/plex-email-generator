# ruff: noqa: DTZ005
## Cannot specify a timezone for Plex doesn't specify a timezone
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
    ONE_DAY = relativedelta(days=1)
    THREE_DAYS = relativedelta(days=3)
    ONE_WEEK = relativedelta(weeks=1)
    TWO_WEEKS = relativedelta(weeks=2)
    THREE_WEEKS = relativedelta(weeks=3)
    ONE_MONTH = relativedelta(months=1)
    TWO_MONTHS = relativedelta(months=2)
    THREE_MONTHS = relativedelta(months=3)

    def __sub__(self, other):
        if isinstance(other, relativedelta | datetime):
            return self.value - other
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, relativedelta | datetime):
            return other - self.value
        return NotImplemented

@dataclass
class MediaItem:
    """
    Object that represents a media item.

    Attributes:
        __type: The type of the media item--show or movie.
        __title: The title of the media item.
        __poster_url: The URL for the poster of the media item.
    """
    __type: str
    __title: str
    __poster_url: str

    @property
    def type(self) -> str:
        return self.__type

    @property
    def title(self) -> str:
        return self.__title

    @property
    def poster_url(self) -> str:
        return self.__poster_url

    def __repr__(self):
        return f"MediaItem(type={self.type}, title={self.title}, posterUrl={self.poster_url})"

    def __str__(self):
        return f"{self.title}"

T = TypeVar("T") # using a generic type for the generator and return plex_api Movie or Show object

def specified_range_movies_and_tv_show_generator() -> Generator[T]:
    """
    Returns the media in the movie(s) and TV show(s) sections on the Plex server.

    Returns:
        A generator of either movie(s) or TV show(s)
    """
    plex_server_instance = PlexServerInstance()
    load_dotenv()

    for movie_section in [
        os.environ.get("MOVIE_SECTION_ONE"),
        os.environ.get("MOVIE_SECTION_TWO"),
    ]:
        for i in plex_server_instance.server_port.library.section(movie_section).all():
            yield i

    for tv_show_section in [
        os.environ.get("TV_SHOW_SECTION_ONE"),
        os.environ.get("TV_SHOW_SECTION_TWO"),
    ]:
        for i in plex_server_instance.server_port.library.section(tv_show_section).all():
            yield i


def recently_added_movies_and_tv_show(
    recently_added_range: RecentlyAddedRangeOptions,
) -> tuple[MediaItem, ...]:
    """
    Pulls the recently added movie and TV shows from the plex server.

    Parameters:
        recently_added_range: the range to be considered "recently added" movie(s) and TV show(s).

    Returns:
        A tuple of movie(s) and TV show(s)
    """
    recently_added_media = []

    # Calculate the cutoff_date to filter media that have been added afterward.
    #
    # Cannot specify a timezone for Plex doesn't specify a timezone
    cutoff_date = datetime.now() - recently_added_range

    # filter out the media on the server that don't meet the cutoff date requirements. From each media that pass
    # pull the title, posterUrl, and TYPE (i.e., movie or TV show) and save it to the MediaItem dataclass.
    for media_entry in specified_range_movies_and_tv_show_generator():
        if media_entry.addedAt > cutoff_date.replace(microsecond=0):  # removed microseconds given Plex datetime only goes down to the second
            recently_added_media.append(
                MediaItem(media_entry.TYPE, media_entry.title, media_entry.posterUrl)
            )

    return tuple(recently_added_media)


# use for testing given cannot write unit test code
if __name__ == "__main__":
    bar = recently_added_movies_and_tv_show(RecentlyAddedRangeOptions.THREE_MONTHS)
    print(bar)
