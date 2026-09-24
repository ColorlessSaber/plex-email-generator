from dataclasses import dataclass
from enum import StrEnum

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
