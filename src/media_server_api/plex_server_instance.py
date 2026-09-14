import os

from dotenv import load_dotenv
from plexapi.server import PlexServer


class PlexServerInstance:

    def __init__(self):
        load_dotenv()
        self.server_port = PlexServer(
            os.environ.get("BASE_URL"),
            os.environ.get("AUTH_TOKEN"),
        )
