from io import TextIOWrapper
from pathlib import Path

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum, unique, auto

from src.config import HTML_DIR
from src.media_server_api.recently_added_movies_and_tv_show import MediaItem
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

class HtmlLanguage(StrEnum):
    ENGLISH = 'en'
    GERMAN = 'de'
    JAPANESE = 'ja'

class HtmlCharSet(StrEnum):
    UTF8 = 'utf-8'

@dataclass
class HtmlConfig:
    """
    Holds the HTML configuration for the HTML generator.

    Default is: english for language, UTF-8 for charset, 2 white spaces,
    and blank for server name.

    Parameters:
        language: What language to generate HTML for.
        charset: What charset to generate HTML for.
        white_space_indent: How many white spaces to indent HTML chars with.
        server_name: The name of the Plex server.
    """
    language: HtmlLanguage = HtmlLanguage.ENGLISH
    charset: HtmlCharSet = HtmlCharSet.UTF8
    white_space_indent: int = 2
    server_name: str | None = None

def write_to_html_file(html_file: TextIOWrapper, space_indent_count: int, content: str) -> None:
    """
    Writes the HTML content to a file. It handles adding the space indents and writing a newline.

    Parameters:
        html_file: HTML file to be written.
        space_indent_count: How many spaces to indent HTML content with.
        content: The content to be written.
    """
    indent = ""
    for _ in range(space_indent_count):
        indent += " "

    html_file.write(indent + content)
    html_file.write('\n')

def generator_html(
        html_config: HtmlConfig,
        html_type: HtmlType,
        body_message: str | None = None,
        media_added_to_server: tuple[MediaItem, ...] | None = None,
) -> None:
    """
    Generates the HTML to be sent out via an email. The HTML will be saved in data/html.

    Parameters:
        html_config: HTML configuration for the HTML generator.
        html_type: What kind of HTML to generate.
        body_message: The message to insert for maintenance HTML email. Defaults to None.
        media_added_to_server: The media that has been added recently to the Plex server. Defaults to None.
    """
    Path(HTML_DIR).mkdir(
        parents=True, exist_ok=True
    ) # create the data/html folder if it does not exist

    # Check to see what type of HTML was selected and from there continue the process of generating
    # the HTML to be sent out via email. The name of the HTML will be what type it is with a date
    # added to the end.
    #
    # During the process of generating the email the white space count has to be tracked; IE, is it time
    # to indent up or done. The starting value is what is specified in the html_config.
    html_file_name = html_type.value + datetime.today().strftime('__%Y_%m_%d') + ".html"
    white_space_indent_count = html_config.white_space_indent

    with open(HTML_DIR / html_file_name, "w", encoding=html_config.charset) as file:
        write_to_html_file(
            file,
            0,
            '<!DOCTYPE html>'
        )
        write_to_html_file(
            file,
            0,
            '<html lang="' + html_config.language.value + '">'
        )
        write_to_html_file(
            file,
            0,
            '<head>'
        )
        write_to_html_file(
            file,
            white_space_indent_count,
            '<meta charset="' + html_config.charset + '">'
        )

        # generate the <title> tag
        server_name = f" {html_config.server_name} " if html_config.server_name else ''
        match html_type:
            case HtmlType.MAINTENANCE:
                write_to_html_file(
                    file,
                    white_space_indent_count,
                    '<title>Plex Media' + server_name + 'server maintenance notice</title>'
                )

            case _:
                write_to_html_file(
                    file,
                    white_space_indent_count,
                    '<title>Weekly Plex Media' + server_name + 'server update</title>'
                )

        # generate <style> section
        write_to_html_file(
            file,
            white_space_indent_count,
            '<style>'
        )

        # Loop through the styles to be added to the HTML file based on the html_type.
        styles_to_print = html_type.styles_for_type()

        write_to_html_file(
            file,
            white_space_indent_count,
            '</style>'
        )

if __name__ == '__main__':
    generator_html(
        HtmlConfig(server_name='Admin'),
        HtmlType.MAINTENANCE,
    )
