from plexapi.exceptions import Unauthorized

from src.media_server_api.plex_server_instance import PlexServerInstance


class TestPlexServerInstance:
    def test_plex_server_instance(self):
        """
        Validate the Plex Server Instance is generated and working
        :return:
        """

        try:
            _ = PlexServerInstance()
            assert True
        except Unauthorized:
            assert False
