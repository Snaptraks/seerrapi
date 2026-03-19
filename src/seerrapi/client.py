from __future__ import annotations

from typing import TYPE_CHECKING

from .auth import AuthEndpoints
from .blocklist import BlocklistEndpoints
from .collection import CollectionEndpoints
from .http import HTTP, APIPath
from .movies import MovieEndpoints
from .person import PersonEndpoints
from .public import StatusEndpoints
from .request import (
    RequestEndpoints,
)
from .search import DiscoverEndpoints, SearchEndpoints
from .service import ServiceEndpoints
from .settings import MainSettings, NetworkSettings
from .tv import TVEndpoints

if TYPE_CHECKING:
    from .users import User


class SeerrClient:
    def __init__(self, *, host: str, api_key: str | None = None) -> None:
        self.host = host.removesuffix("/")
        self.api_key = api_key
        self.http = HTTP(host=host, _api_key=api_key)

        self.status = StatusEndpoints(self)
        self.auth = AuthEndpoints(self)
        self.blocklist = BlocklistEndpoints(self)
        self.search = SearchEndpoints(self)
        self.discover = DiscoverEndpoints(self)
        self.request = RequestEndpoints(self)
        self.movie = MovieEndpoints(self)
        self.tv = TVEndpoints(self)
        self.person = PersonEndpoints(self)
        self.collection = CollectionEndpoints(self)
        self.service = ServiceEndpoints(self)

    # shortcut methods
    async def me(self) -> User:
        return await self.auth.me()

    async def logout(self) -> None:
        await self.auth.logout()

    # Settings endpoints

    async def get_main_settings(self) -> MainSettings:
        return MainSettings.from_data(
            await self.http.request("GET", APIPath("/settings/main")),
            http=self.http,
        )

    async def get_network_settings(self) -> NetworkSettings:
        return NetworkSettings.from_data(
            await self.http.request("GET", APIPath("/settings/network")),
            http=self.http,
        )
