from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Protocol, TypedDict, Unpack

from .auth import AuthEndpoints
from .base import MediaType
from .blocklist import BlocklistEndpoints
from .collection import CollectionEndpoints
from .http import HTTP, APIPath
from .movies import MovieEndpoints
from .person import PersonEndpoints
from .public import StatusEndpoints
from .request import (
    Request,
    RequestCount,
)
from .search import DiscoverEndpoints, SearchEndpoints
from .service import ServiceEndpoints
from .settings import MainSettings, NetworkSettings
from .tv import TVEndpoints

if TYPE_CHECKING:
    from .request import (
        RequestFilter,
        RequestMediaType,
        RequestSort,
        RequestSortDirection,
    )
    from .users import User

    class RequestParams(TypedDict, total=False):
        take: int
        skip: int
        filter_: RequestFilter | None
        sort: RequestSort | None
        sort_direction: RequestSortDirection | None
        requested_by: int | None
        media_type: RequestMediaType | None

    class Media(Protocol):
        tvdb_id: int
        media_type: MediaType
        seasons: list[int] | Literal["all"]


class SeerrClient:
    def __init__(self, *, host: str, api_key: str | None = None) -> None:
        self.host = host.removesuffix("/")
        self.api_key = api_key
        self.http = HTTP(host=host, _api_key=api_key)
        self._cookie_auth: str | None = None

        self.status = StatusEndpoints(self)
        self.auth = AuthEndpoints(self)
        self.blocklist = BlocklistEndpoints(self)
        self.search = SearchEndpoints(self)
        self.discover = DiscoverEndpoints(self)
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

    # Requests endpoints

    async def request(self, media: Media) -> Request:
        request_data = {
            "media_type": media.media_type,
            "media_id": media.tvdb_id,
            "tvdb_id": media.tvdb_id,
        }
        if media.media_type == MediaType.TV:
            request_data["seasons"] = media.seasons
        return Request.from_data(
            await self.http.request("POST", APIPath("/request"), payload=request_data),
            http=self.http,
        )

    async def get_requests(self, **params: Unpack[RequestParams]) -> list[Request]:
        resp = await self.http.request("GET", APIPath("/request"), params=params)  # pyright: ignore[reportArgumentType]

        return Request.from_data_list(resp["results"], http=self.http)

    async def get_requests_count(self) -> RequestCount:
        return RequestCount.from_data(
            await self.http.request("GET", APIPath("/request/count")),
        )

    async def get_request(self, request_id: int) -> Request:
        return Request.from_data(
            await self.http.request(
                "GET",
                APIPath(f"/request/{request_id}", request_id=request_id),
            ),
            http=self.http,
        )
