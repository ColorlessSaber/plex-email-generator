# ruff: noqa: DTZ005
## Cannot specify a timezone for Plex doesn't specify a timezone
from datetime import datetime
from enum import Enum, unique
from itertools import chain

from dateutil.relativedelta import relativedelta

from src.media_server_api.media_item import MediaItem
from src.media_server_api.plex_server_instance import PlexServerInstance


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
    plex_server_instance = PlexServerInstance()
    recently_added_media = []

    # Calculate the cutoff_date to filter media that have been added afterward.
    #
    # Cannot specify a timezone for Plex doesn't specify a timezone
    cutoff_date = datetime.now() - recently_added_range

    # filter out the media on the server that don't meet the cutoff date requirements. From each media that pass
    # pull the title, posterUrl, and TYPE (i.e., movie or TV show) and save it to the MediaItem dataclass.
    for media_entry in chain(
        plex_server_instance.all_movies(),
        plex_server_instance.all_tv_shows(),
    ):
        if media_entry.addedAt > cutoff_date.replace(microsecond=0):  # removed microseconds given Plex datetime only goes down to the second
            recently_added_media.append(
                MediaItem(media_entry.TYPE, media_entry.title, media_entry.posterUrl)
            )

    return tuple(recently_added_media)


# use for testing given cannot write unit test code
if __name__ == "__main__":
    bar = recently_added_movies_and_tv_show(RecentlyAddedRangeOptions.THREE_MONTHS)
    print(bar)
