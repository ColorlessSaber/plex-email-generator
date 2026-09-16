"""
Holds the style config settings for the HTML emails.
"""
from typing import Optional
from dataclasses import dataclass


class RequiredStyleConfigAttrsMixin:
    """
    Holds the required attributes each StyleConfig needs to have.

    Attributes:
        tag: the target HTML tag; will throw an error if not provided.
        selector_class: The selector class that will be used if provided.
    """
    __slots__ = ('tag', 'selector_class')

    def __init__(self, tag: Optional[str] = None, selector_class: Optional[str] = None):
        if tag is None:
            raise ValueError("No tag kwarg was provided")
        self.tag = tag
        self.selector_class = selector_class

class StyleConfigBuilder(RequiredStyleConfigAttrsMixin):
    """
    Holds the style config settings for an HTML tag.
    """

    def __init__(self, **kwargs):
        super().__init__(tag=kwargs.get("tag", None), selector_class=kwargs.get("selector_class"))
        for key, value in kwargs.items():
            if key not in self.__slots__:
                setattr(self, key, str(value)) # want each entry to be a string. Makes it easier to handle

    
    def __str__(self) -> str:
        selector_class = f".{self.selector_class}" if self.selector_class else ""
        style_config = f"{self.tag}{selector_class}" + " {\n"

        for key, value in vars(self).items():
            if key not in self.__slots__:
                attr_value = f"var({value})" if value.startswith("--") else value # handle CSS variables
                style_config += f"{key}: {attr_value}\n"

        style_config += "}"

        return style_config


@dataclass
class StyleConfigs:
    """
    Holds all the style config settings for each HTML tag.

    Attributes that have double-underscores defines the start of the selector class.
    Example: P__MEDIA_TITLES, p is the tag and media-titles is the selector class.
    """
    ROOT: StyleConfigBuilder = StyleConfigBuilder(**{
        'tag': ':root',
        '--email-background-color': '#FFF8EC',
        '--header-background-color': '#FEC601',
        '--poster-background-color': '#DFE0DF',
        '--text-section-background-color': '#DFE0DF',
    })
    BODY: StyleConfigBuilder = StyleConfigBuilder(**{
        'tag': 'body',
        'margin': '0',
        'padding': '0',
        'background-color': '--email-background-color',
    })
    H_ONE: StyleConfigBuilder = StyleConfigBuilder(**{
        'tag': 'h1',
        'text-align': 'center',
    })
    P__MEDIA_TITLES = StyleConfigBuilder(**{
        'tag': 'p',
        'selector_class': 'media-titles',
        'text-align': 'center',
        'font-size': '30px',
        'font-weight': 'bold',
        'margin-top': '-5%',
    })
    P__OVERFLOW = StyleConfigBuilder(**{
        'tag': 'p',
        'selector_class': 'overflow',
        'text-align': 'center',
        'font-size': '24px',
        'line-height': '1.6',
    })

    # ~~ table tag and related style configs ~~

    TABLE__CONTAINER = StyleConfigBuilder(**{
        'tag': 'table',
        'selector_class': 'container',
        'width': '100%',
    })
    TD__HEADER = StyleConfigBuilder(**{
        'tag': 'td',
        'selector_class': 'header',
        'border': 'solid 1px black',
        'border-radius': '15px',
        'background-color': '--header-background-color',
    })
    TD__COLUMN = StyleConfigBuilder(**{
        'tag': 'td',
        'selector_class': 'column',
        'border': 'solid 1px black',
        'border-radius': '15px',
        'background-color': '--poster-background-color',
    })
    TD__TEXT_SECTION = StyleConfigBuilder(**{
        'tag': 'td',
        'selector_class': 'column',
        'border': 'solid 1px black',
        'border-radius': '15px',
        'background-color': '--text-section-background-color',
    })

    # ~~ img tag style configs ~~

    IMG__PLEX_LOGO = StyleConfigBuilder(**{
        'tag': 'table',
        'selector_class': 'container',
        'width': '100%',
        'height': 'auto',
        'border-radius': '30px',
        'scale': '50%',
        'margin-top': '-10%',
        'margin-bottom': '-10%',
    })
    IMG__POSTER = StyleConfigBuilder(**{
        'tag': 'img',
        'selector_class': 'poster',
        'width': '100%',
        'height': 'auto',
        'border-radius': '30px',
        'scale': '50%',
        'margin-top': '-30%',
        'margin-bottom': '-30%',
    })
