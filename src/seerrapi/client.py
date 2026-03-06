from __future__ import annotations

from typing import TYPE_CHECKING, Literal, Protocol, TypedDict, Unpack

from .http import HTTP, APIPath
from .movies import Movie
from .public import AppData, Status
from .request import (
    MediaType,
    Request,
    RequestCount,
)
from .settings import MainSettings, NetworkSettings
from .tv import TV

if TYPE_CHECKING:
    from .request import (
        RequestFilter,
        RequestMediaType,
        RequestSort,
        RequestSortDirection,
    )

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
    def __init__(self, *, host: str, api_key: str) -> None:
        self.host = host.removesuffix("/")
        self.api_key = api_key
        self.http = HTTP(host=host, api_key=api_key)

    # Public endpoints

    async def get_status(self) -> Status:
        return Status.from_data(await self.http.request("GET", APIPath("/status")))

    async def get_app_data(self) -> AppData:
        return AppData.from_data(
            await self.http.request("GET", APIPath("/status/appdata"))
        )

    # Settings endpoints

    async def get_main_settings(self) -> MainSettings:
        return MainSettings.from_data(
            await self.http.request("GET", APIPath("/settings/main")), http=self.http
        )

    async def get_network_settings(self) -> NetworkSettings:
        return NetworkSettings.from_data(
            await self.http.request("GET", APIPath("/settings/network")), http=self.http
        )

    # Requests endpoints

    async def request(self, media: Media) -> Request:
        request_data = {
            "mediaType": media.media_type,
            "mediaId": media.tvdb_id,
            "tvdbId": media.tvdb_id,
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
            await self.http.request("GET", APIPath("/request/count"))
        )

    async def get_request(self, request_id: int) -> Request:
        return Request.from_data(
            await self.http.request(
                "GET", APIPath(f"/request/{request_id}", request_id=request_id)
            ),
            http=self.http,
        )

    # Movies endpoints

    async def get_movie(self, movie_id: int, *, language: str = "en") -> Movie:
        return Movie.from_data(
            await self.http.request(
                "GET",
                APIPath("/movie/{movie_id}", movie_id=movie_id),
                params={"language": language},
            ),
            http=self.http,
        )

    # TV endpoints

    async def get_tv(self, tv_id: int, *, language: str = "en") -> TV:
        return TV.from_data(
            await self.http.request(
                "GET",
                APIPath("/tv/{tv_id}", tv_id=tv_id),
                params={"language": language},
            ),
            http=self.http,
        )
