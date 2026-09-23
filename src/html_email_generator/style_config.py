"""
Holds the style config settings for the HTML emails.
"""


class RequiredStyleConfigAttrsMixin:
    """
    Holds the required attributes each StyleConfig needs to have.

    Attributes:
        tag: the target HTML tag; will throw an error if not provided.
        selector_class: The selector class that will be used if provided.
    """

    __slots__ = ("selector_class", "tag")

    def __init__(self, tag: str | None = None, selector_class: str | None = None):
        if tag is None:
            raise ValueError("No tag kwarg was provided")
        self.tag = tag
        self.selector_class = selector_class


class StyleConfigBuilder(RequiredStyleConfigAttrsMixin):
    """
    Holds the style config settings for an HTML tag.
    """

    def __init__(self, **kwargs):
        super().__init__(
            tag=kwargs.get("tag", None), selector_class=kwargs.get("selector_class")
        )
        for key, value in kwargs.items():
            if key not in self.__slots__:
                setattr(
                    self, key, str(value)
                )  # want each entry to be a string. Makes it easier to handle

    def __str__(self) -> str:
        selector_class = f".{self.selector_class}" if self.selector_class else ""
        style_config = f"{self.tag}{selector_class}" + " {\n"

        for key, value in vars(self).items():
            if key not in self.__slots__:
                key = key.replace("_", "-")
                if self.tag == ":root":  # turn key into a variable
                    key = "--" + key

                attr_value = (
                    f"var({value})" if value.startswith("--") else value
                )  # handle CSS variables
                attr_value = attr_value.replace("_", "-")
                style_config += f"{key}: {attr_value}\n"

        style_config += "}"

        return style_config


# The style configs that have double-underscores defines the start of the selector class.
# Example: P__MEDIA_TITLES, p is the tag and media-titles is the selector class.
ROOT = StyleConfigBuilder(
    tag=":root",
    email_background_color="#FFF8EC",
    header_background_color="#FEC601",
    poster_background_color="#DFE0DF",
    text_section_background_color="#DFE0DF",
)
BODY = StyleConfigBuilder(
    tag="body",
    margin="0",
    padding="0",
    background_color="--email-background-color",
)

H_ONE: StyleConfigBuilder = StyleConfigBuilder(
    tag="h1",
    text_align="center",
)

P__MEDIA_TITLES = StyleConfigBuilder(
    tag="p",
    selector_class="media-titles",
    text_align="center",
    font_size="30px",
    font_weight="bold",
    margin_top="-5%",
)

P__CD_TITLE = StyleConfigBuilder(
    tag="p",
    selector_class="cd-title",
    text_align="center",
    font_size="30px",
    font_weight="bold",
    margin_top="-5%",
)

P__OVERFLOW = StyleConfigBuilder(
    tag="p",
    selector_class="overflow",
    text_align="center",
    font_size="24px",
    line_height="1.6",
)

# ~~ table tag and related style configs ~~

TABLE__CONTAINER = StyleConfigBuilder(
    tag="table",
    selector_class="container",
    width="100%",
)
TD__HEADER = StyleConfigBuilder(
    tag="td",
    selector_class="header",
    border="solid 1px black",
    border_radius="15px",
    background_color="--header-background-color",
)
TD__COLUMN = StyleConfigBuilder(
    tag="td",
    selector_class="column",
    border="solid 1px black",
    border_radius="15px",
    background_color="--poster-background-color",
)
TD__TEXT_SECTION = StyleConfigBuilder(
    tag="td",
    selector_class="column",
    border="solid 1px black",
    border_radius="15px",
    background_color="--text-section-background-color",
)

# ~~ img tag style configs ~~

IMG__PLEX_LOGO = StyleConfigBuilder(
    tag="table",
    selector_class="container",
    width="100%",
    height="auto",
    border_radius="30px",
    scale="50%",
    margin_top="-10%",
    margin_bottom="-10%",
)
IMG__POSTER = StyleConfigBuilder(
    tag="img",
    selector_class="poster",
    width="100%",
    height="auto",
    border_radius="30px",
    scale="50%",
    margin_top="-30%",
    margin_bottom="-30%",
)
IMG__ALBUM_COVER = StyleConfigBuilder(
    tag="img",
    selector_class="album-cover",
    width="100%",
    height="auto",
    border_radius="30px",
    scale="45%",
    margin_top="-20%",
    margin_bottom="-20%",
)
