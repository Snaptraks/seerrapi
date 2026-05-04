from __future__ import annotations

from contextvars import ContextVar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import SeerrClient
    from .http import HTTP

client_context: ContextVar[SeerrClient] = ContextVar("client_context_client")
http_context: ContextVar[HTTP] = ContextVar("client_http_session")
