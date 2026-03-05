class SeerrError(Exception):
    """Base error class for SeerrAPI.

    This can be used to catch all the errors raised from this library.
    """


class SeerrConnectionError(SeerrError):
    """Error raised from a connection error to Seerr."""


class SeerrAuthenticationError(SeerrError):
    """Error raised from a unauthenticated call to Seerr."""
