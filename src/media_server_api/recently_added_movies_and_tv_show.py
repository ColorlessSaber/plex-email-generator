import os
import re
from datetime import datetime
from enum import Enum, auto, unique

from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from plex_server_instance import PlexServerInstance


@unique
class RangeOptions(Enum):
    PLEX_API = auto()
    DAY = auto()
    WEEK = auto()
    MONTH = auto()

def specified_range_movies_and_tv_show_generator(plex_instance: PlexServerInstance):
    """
    Returns the media in the movie(s) and TV show(s) sections on the Plex server.

    :return:
    """
    load_dotenv()

    for movie_section in [os.environ.get("MOVIE_SECTION_ONE"), os.environ.get("MOVIE_SECTION_TWO")]:
        for i in plex_instance.server_port.library.section(movie_section).all():
            yield i

    for tv_show_section in [os.environ.get("TV_SHOW_SECTION_ONE"), os.environ.get("TV_SHOW_SECTION_TWO")]:
        for i in plex_instance.server_port.library.section(tv_show_section).all():
            yield i

def recently_added_movies_and_tv_show(range: RangeOptions = RangeOptions.PLEX_API) -> tuple[tuple[str, str], ...]:
    """
    Pulls the recently added movie and TV shows from the plex server. Default is using Plex's recentlyAdded API.

    range: Specify a different range to be considered recently added than Plex's recentlyAdded API.
    :return:
    """
    plex_server_instance = PlexServerInstance()

    # Pull in the recently added contented from the movie and TV show sections; get the media title of each new content
    # along with their poster, if they have one. The end returned structure is a tuple with a sub-tuple containing: (media tile, poster url).
    #
    # Given the structure of the return object need to detect entries that are TV versus movies
    # because the TV show entry stores the name in parentTitle while Title is the season folder name.
    recently_added_media = []
    if range == RangeOptions.PLEX_API:
        for media_entry in plex_server_instance.server_port.library.recentlyAdded():

            # Use .librarySectionTitle to determine if the entry is a movie or TV show
            if 'Movies' in media_entry.librarySectionTitle:
                print(f"library section title: {media_entry.librarySectionTitle}, title: {media_entry.title}; date added: {media_entry.addedAt}")
            elif 'TV Shows' in media_entry.librarySectionTitle:
                if 'Specials' in media_entry.title:
                    season_text = media_entry.title
                else:
                    season_text = re.split(r'\s', media_entry.title)[1]
                print(f"library section title: {media_entry.librarySectionTitle}, title: {media_entry.parentTitle}, season: {season_text}; date added: {media_entry.addedAt}")
    else:
        # subtract the specified value in the given range from the current date to create a cutoff date when filtering
        # through the media
        timezone = datetime.now().astimezone().tzinfo
        match range:
            case RangeOptions.DAY:
                cutoff_date = datetime.now(tz=timezone) - relativedelta(days=1)
            case RangeOptions.WEEK:
                cutoff_date = datetime.now(tz=timezone) - relativedelta(weeks=1)
            case RangeOptions.MONTH:
                cutoff_date = datetime.now(tz=timezone) - relativedelta(months=1)

        for media_entry in specified_range_movies_and_tv_show_generator(plex_server_instance):
            # Use .librarySectionTitle to determine if the entry is a movie or TV show
            if media_entry.addedAt > cutoff_date:
                if 'Movies' in media_entry.librarySectionTitle:
                    print(f"library section title: {media_entry.librarySectionTitle}, title: {media_entry.title}; date added: {media_entry.addedAt}")
                elif 'TV Shows' in media_entry.librarySectionTitle:
                    if 'Specials' in media_entry.title:
                        season_text = media_entry.title
                    else:
                        season_text = re.split(r'\s', media_entry.title)[1]
                    print(f"library section title: {media_entry.librarySectionTitle}, title: {media_entry.title}, season: {season_text}; date added: {media_entry.addedAt}")

if __name__ == "__main__":
    recently_added_movies_and_tv_show(range=RangeOptions.MONTH)