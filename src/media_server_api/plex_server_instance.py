from plexapi.server import PlexServer
from dotenv import load_dotenv
import os

class PlexServerInstance:

    def __init__(self):
        load_dotenv()
        self.plex = PlexServer(
            os.environ.get("BASE_URL"),
            os.environ.get("AUTH_TOKEN"),
        )
