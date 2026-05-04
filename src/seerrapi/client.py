from __future__ import annotations

from typing import TYPE_CHECKING

from .auth import AuthEndpoints
from .blocklist import BlocklistEndpoints
from .collection import CollectionEndpoints
from .context import client_context, http_context
from .http import HTTP, APIPath
from .issue import IssueEndpoints
from .media import MediaEndpoints
from .movies import MovieEndpoints
from .overriderule import OverrideRuleEndpoints
from .person import PersonEndpoints
from .public import StatusEndpoints
from .request import (
    RequestEndpoints,
)
from .search import DiscoverEndpoints, SearchEndpoints
from .service import ServiceEndpoints
from .settings import MainSettings, NetworkSettings
from .tmdb import TMDBEndpoints
from .tv import TVEndpoints
from .watchlist import WatchlistEndpoints

if TYPE_CHECKING:
    from .users import User


class SeerrClient:
    def __init__(self, *, host: str, api_key: str | None = None) -> None:
        self.host = host.removesuffix("/")
        self.api_key = api_key
        self.http = HTTP(host=host, api_key=api_key)

        self.status = StatusEndpoints()
        self.auth = AuthEndpoints()
        self.blocklist = BlocklistEndpoints()
        self.search = SearchEndpoints()
        self.discover = DiscoverEndpoints()
        self.request = RequestEndpoints()
        self.movie = MovieEndpoints()
        self.tv = TVEndpoints()
        self.person = PersonEndpoints()
        self.collection = CollectionEndpoints()
        self.service = ServiceEndpoints()
        self.watchlist = WatchlistEndpoints()
        self.tmdb = TMDBEndpoints()
        self.media = MediaEndpoints()
        self.overriderule = OverrideRuleEndpoints()
        self.issue = IssueEndpoints()

        client_context.set(self)
        http_context.set(self.http)

    # shortcut methods
    async def me(self) -> User:
        return await self.auth.me()

    async def logout(self) -> None:
        await self.auth.logout()

    # Settings endpoints

    async def get_main_settings(self) -> MainSettings:
        return MainSettings.from_data(
            await self.http.request("GET", APIPath("/settings/main"))
        )

    async def get_network_settings(self) -> NetworkSettings:
        return NetworkSettings.from_data(
            await self.http.request("GET", APIPath("/settings/network"))
        )
