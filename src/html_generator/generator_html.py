from io import TextIOWrapper
from pathlib import Path

from datetime import datetime

from src.config import HTML_DIR
from src.html_generator.html_type_enum import HtmlType
from src.html_generator.html_config import HtmlConfig
from src.media_server_api.recently_added_movies_and_tv_show import MediaItem

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
        white_space_indent_count += html_config.white_space_indent
        for style_entry in html_type.styles_for_type():
            for line_item in style_entry:
                if any(i in line_item for i in ['{', '}']): # The start and end of a style entry
                    write_to_html_file(
                        file,
                        white_space_indent_count,
                        line_item
                    )
                else:
                    write_to_html_file(
                        file,
                        white_space_indent_count + html_config.white_space_indent,
                        line_item
                    )

        white_space_indent_count -= html_config.white_space_indent
        write_to_html_file(
            file,
            white_space_indent_count,
            '</style>'
        )

if __name__ == '__main__':
    generator_html(
        HtmlConfig(server_name='Admin'),
        HtmlType.NEW_MOVIE_TV_SHOW,
    )
