from pathlib import Path

from pyfakefs.fake_filesystem_unittest import TestCase

from src.config import POSTERS_DIR
from src.media_server_api.poster_downloader import poster_downloader
from src.media_server_api.recently_added_movies_and_tv_show import MediaItem


class TestPosterDownloader(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

        self.fs.create_dir(POSTERS_DIR)

    def test_successful_poster_downloads(self):
        """
        Validate that the posters are downloaded successfully

        :return:
        """
        posters_list = (
            MediaItem(
                "show",
                "Crusher Joe OVA",
                "http://127.0.0.1:32400/library/metadata/12437/thumb/1788297678?X-Plex-Token=eDi5g5yhmzVPEsGoySeK",
            ),
            MediaItem(
                "show",
                "Lost Universe",
                "http://127.0.0.1:32400/library/metadata/12367/thumb/1784913386?X-Plex-Token=eDi5g5yhmzVPEsGoySeK",
            ),
            MediaItem(
                "show",
                "Spice & Wolf",
                "http://127.0.0.1:32400/library/metadata/12409/thumb/1787599839?X-Plex-Token=eDi5g5yhmzVPEsGoySeK",
            ),
        )

        poster_downloader(posters_list)

        assert Path(POSTERS_DIR / "Crusher Joe OVA.jpg").exists(), (
            "failed to download Crusher Joe OVA poster"
        )
        assert Path(POSTERS_DIR / "Lost Universe.jpg").exists(), (
            "failed to download Lost Universe poster"
        )
        assert Path(POSTERS_DIR / "Spice & Wolf.jpg").exists(), (
            "failed to download Spice & Wolf poster"
        )

    def test_bad_url_path(self):
        """
        Validate that function handles a case of a bad URL path.

        :return:
        """
        posters_list = (
            MediaItem(
                "show",
                "Crusher Joe OVA",
                "http://127.0.0.1:32400/library/metadata/12437/thumb/1788297678?X-Plex-Token=eDi5g5yhmzVPEsGoySeK",
            ),
            MediaItem(
                "show",
                "Lost Universe",
                "http://127.0.0.1:32400/library/metadata/12367/thumb/1784913386",
            ),
            MediaItem(
                "show",
                "Spice & Wolf",
                "http://127.0.0.1:32400/library/metadata/12409/thumb/1787599839?X-Plex-Token=eDi5g5yhmzVPEsGoySeK",
            ),
        )

        poster_downloader(posters_list)

        assert Path(POSTERS_DIR / "Lost Universe.jpg").exists() == False, (
            "failed to handle bad URL path"
        )

    def test_existing_poster_downloads(self):
        """
        Validate that the function will skip over existing poster(s) that are already downloaded

        :return:
        """
        posters_list = (
            MediaItem(
                "show",
                "Crusher Joe OVA",
                "http://127.0.0.1:32400/library/metadata/12437/thumb/1788297678?X-Plex-Token=eDi5g5yhmzVPEsGoySeK",
            ),
            MediaItem(
                "show",
                "Crusher Joe OVA",
                "http://127.0.0.1:32400/library/metadata/12437/thumb/1788297678?X-Plex-Token=eDi5g5yhmzVPEsGoySeK",
            ),
        )

        poster_downloader(posters_list)

        result = sum(1 for file in POSTERS_DIR.iterdir() if file.is_file())

        assert result == 1, "failed to handle existing posters"
