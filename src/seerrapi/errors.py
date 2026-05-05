from typing import Any


class SeerrError(Exception):
    """Base error class for SeerrAPI.

    This can be used to catch all the errors raised from this library.
    """

    def __init__(self, msg: str, extras: dict[str, Any] | None = None) -> None:
        self.msg = msg
        self.extras = extras or {}
        super().__init__(msg)


class SeerrConnectionError(SeerrError):
    """Error raised from a connection error to Seerr."""


class SeerrAuthenticationError(SeerrError):
    """Error raised from a unauthenticated call to Seerr."""


class SeerrSearchError(SeerrError):
    """Error raised when invalid parameters are passed to discover search."""


class SeerrNotFoundError(SeerrError):
    """Error raised when the API returns a 404 HTTP code."""


class SeerrIssueNotFoundError(SeerrNotFoundError):
    """Error raised when the requested issue does not exist."""


class TMDBKeywordNotFoundError(SeerrNotFoundError):
    """Error raised when searching for a keyword that does not exist in TMDB."""

    def __init__(self, keyword_id: int) -> None:
        super().__init__(f"Keyword with ID {keyword_id} not found.")
