from enum import StrEnum, unique, auto

from src.html_generator.style_config import (
    BODY,
    H_ONE,
    IMG__ALBUM_COVER,
    IMG__PLEX_LOGO,
    IMG__POSTER,
    P__CD_TITLE,
    P__MEDIA_TITLES,
    P__OVERFLOW,
    ROOT,
    TABLE__CONTAINER,
    TD__COLUMN,
    TD__HEADER,
    TD__TEXT_SECTION,
    StyleConfigBuilder,
)

# group the style into groups
BASE_STYLE = [ROOT, BODY]
COMMON_STYLES = [
    TABLE__CONTAINER,
    IMG__PLEX_LOGO,
    TD__HEADER,
    TD__TEXT_SECTION,
    H_ONE,
    P__OVERFLOW,
]

@unique
class HtmlType(StrEnum):
    MAINTENANCE = auto()
    MEDIA_LEAVING = auto()
    NEW_MOVIE_TV_SHOW = auto()
    NEW_MUSIC = auto()

    def styles_for_type(self) -> list[StyleConfigBuilder]:
        """
        Returns a list of styles that needed for the HTML type.

        Returns:
            List of StyleConfigBuilder objects.
        """
        match self.value:
            case self.MAINTENANCE | self.MEDIA_LEAVING:
                return BASE_STYLE + COMMON_STYLES
            case self.NEW_MOVIE_TV_SHOW:
                return BASE_STYLE + COMMON_STYLES + [IMG__POSTER, P__MEDIA_TITLES, TD__COLUMN]
            case self.NEW_MUSIC:
                return BASE_STYLE + COMMON_STYLES + [IMG__ALBUM_COVER, P__CD_TITLE, TD__COLUMN]
            case _: # not needed but necessary to stop it from throwing a warning
                return BASE_STYLE + COMMON_STYLES
