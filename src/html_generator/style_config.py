"""
Holds the style config settings for the HTML emails.
"""
from src.html_generator.css_rule_object.css_rule import CSSRule

# style configs that have double-underscores defines the start of the selector class.
# Example: P__MEDIA_TITLES, p is the tag and media-titles is the selector class.
ROOT = CSSRule(
    selector=":root",
    properties={
        "email-background-color": "#FFF8EC",
        "header-background-color": "#FEC601",
        "poster-background-color": "#DFE0DF",
        "text-section-background-color": "#DFE0DF",
    }
)

BODY = CSSRule(
    selector="body",
    properties={
        "margin": 0,
        "padding": 0,
        "background-color": "var(--email-background-color)",
    }
)

H_ONE = CSSRule(
    selector="h1",
    properties={
        "text-align": "center",
    }
)

P__MEDIA_TITLES = CSSRule(
    selector="p.media-title",
    properties={
        "text-align": "center",
        "font-size": "30px",
        "font-weight": "bold",
        "margin-top": "-5%",
    }
)

P__CD_TITLES = CSSRule(
    selector="p.cd-title",
    properties={
        "text-align": "center",
        "font-size": "30px",
        "font-weight": "bold",
        "margin-top": "-5%",
    }
)

P__OVERFLOW = CSSRule(
    selector="p.overflow",
    properties={
        "text-align": "center",
        "font-size": "24px",
        "line-height": "1.6",
    }
)

# ~~ table tag and related style configs ~~
TABLE__CONTAINER = CSSRule(
    selector="table.container",
    properties={
        "width": "100%",
    }
)

TD__HEADER = CSSRule(
    selector="td.header",
    properties={
        "border": "solid 1px black",
        "border-radius": "15px",
        "background-color": "var(--header-background-color)",
    }
)

TD__COLUMN = CSSRule(
    selector="td.column",
    properties={
        "border": "solid 1px black",
        "border-radius": "15px",
        "background-color": "var(--poster-background-color)",
    }
)

TD__TEXT_SECTION = CSSRule(
    selector="td.text",
    properties={
        "border": "solid 1px black",
        "border-radius": "15px",
        "background-color": "var(--text-section-background-color)",
    }
)

# ~~ img tag style configs ~~
IMG__PLEX_LOGO = CSSRule(
    selector="img.plex-logo",
    properties={
        "width": "100%",
        "height": "auto",
        "scale": "50%",
        "margin-top": "-10%",
        "margin-bottom": "-10%",
    }
)

IMG__POSTER = CSSRule(
    selector="img.poster",
    properties={
        "width": "100%",
        "height": "auto",
        "border-radius": "30px",
        "scale": "50%",
        "margin-top": "-30%",
        "margin-bottom": "-30%",
    }
)

IMG__ALBUM_COVER = CSSRule(
    selector="img.album",
    properties={
        "width": "100%",
        "height": "auto",
        "border-radius": "30px",
        "scale": "45%",
        "margin-top": "-20%",
        "margin-bottom": "-20%",
    }
)
