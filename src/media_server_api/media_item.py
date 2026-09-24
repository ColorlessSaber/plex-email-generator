from dataclasses import dataclass


@dataclass
class MediaItem:
    """
    Object that represents a media item.

    Attributes:
        _type: The type of the media item--show or movie.
        _title: The title of the media item.
        _poster_url: The URL for the poster of the media item.
    """
    _type: str
    _title: str
    _poster_url: str

    @property
    def type(self) -> str:
        return self._type

    @property
    def title(self) -> str:
        return self._title

    @property
    def poster_url(self) -> str:
        return self._poster_url

    def __repr__(self):
        return f"MediaItem(type={self.type}, title={self.title}, posterUrl={self.poster_url})"

    def __str__(self):
        return f"{self.title}"
