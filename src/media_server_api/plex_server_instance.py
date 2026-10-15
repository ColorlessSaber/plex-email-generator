import os
from collections.abc import Generator
from typing import TypeVar

from dotenv import load_dotenv
from plexapi.server import PlexServer

_T = TypeVar("_T") # needed to allow chaining of iterables returned from class
class PlexServerInstance:
    def __init__(self):
        load_dotenv()
        self.server_port = PlexServer(
            os.environ.get("BASE_URL"),
            os.environ.get("AUTH_TOKEN"),
        )

    def all_movies(self) -> Generator[_T]:
        """
        Returns all the movies in the server.

        Returns:
            Generator[Movie] - A generator of Movie objects
        """
        load_dotenv()

        for movie_section in [
            os.environ.get("MOVIE_SECTION_ONE"),
            os.environ.get("MOVIE_SECTION_TWO"),
        ]:
            for i in self.server_port.library.section(movie_section).all():
                yield from i

    def all_tv_shows(self) -> Generator[_T]:
        """
        Returns all the TV shows in the server.

        Returns:
            Generator[_T] - A generator of TV show objects
        """
        load_dotenv()

        for tv_show_section in [
            os.environ.get("TV_SHOW_SECTION_ONE"),
            os.environ.get("TV_SHOW_SECTION_TWO"),
        ]:
            for i in self.server_port.library.section(tv_show_section).all():
                yield from i