from __future__ import annotations

from datetime import datetime
from enum import IntEnum
from typing import (
    TYPE_CHECKING,
    Literal,
)
from warnings import warn

from pydantic import Field

from .base import Base, Endpoints, MediaType, Stateful
from .http import APIPath
from .users import User

if TYPE_CHECKING:
    from typing import Any

    from .base import Requestable

    type RequestFilter = Literal[
        "all",
        "approved",
        "available",
        "pending",
        "processing",
        "unavailable",
        "failed",
        "deleted",
        "completed",
    ]
    type RequestSort = Literal["added", "modified"]
    type RequestSortDirection = Literal["asc", "desc"]
    type RequestMediaType = MediaType | Literal["all"]

# Media objects


class MediaStatus(IntEnum):
    UNKNOWN = 1
    PENDING = 2
    PROCESSING = 3
    PARTIALLY_AVAILABLE = 4
    AVAILABLE = 5
    DELETED = 6


class _MediaInfoBase(Base):
    download_status: list[str]
    download_status_4k: list[str]
    id: int
    media_type: MediaType
    tmdb_id: int | None
    tvdb_id: int | None
    imdb_id: int | None
    status: MediaStatus
    status_4k: MediaStatus
    created_at: datetime
    updated_at: datetime
    last_season_change: datetime
    media_added_at: datetime
    service_id: int | None
    service_id_4k: int | None
    external_service_id: int | None
    external_service_id_4k: int | None
    external_service_slug: str | None
    external_service_slug_4k: str | None
    rating_key: str | None
    rating_key_4k: str | None
    jellyfin_media_id: int | None
    jellyfin_media_id_4k: int | None
    requests: list[Request] = Field(default_factory=list)
    service_url: str | None = None


class MediaInfo(_MediaInfoBase):
    seasons: list[int] | Literal["all"] = Field(default_factory=list)


# Request objects


class RequestStatus(IntEnum):
    PENDING_APPROVAL = 1
    APPROVED = 2
    DECLINED = 3
    FAILED = 4


class PageInfo(Base):
    pages: int
    page_size: int
    results: int
    page: int


class Season(Base):
    id: int
    season_number: int
    status: RequestStatus
    created_at: datetime
    updated_at: datetime


class Request(Stateful):
    id: int
    status: RequestStatus
    created_at: datetime
    updated_at: datetime
    type: MediaType
    is4k: bool
    server_id: int | None
    profile_id: int | None
    root_folder: str | None
    language_profile_id: int | None
    tags: list[str] | None
    is_auto_request: bool
    media: MediaInfo
    seasons: list[Season] = Field(default_factory=list)
    modified_by: User
    requested_by: User
    season_count: int | None = None
    profile_name: str | None = None
    can_remove: bool | None = None

    async def update(  # noqa: PLR0913
        self,
        *,
        media_type: MediaType | None = None,
        seasons: list[int] | None = None,
        is_4k: bool | None = None,
        server_id: int | None = None,
        profile_id: int | None = None,
        root_folder: str | None = None,
        language_profile_id: int | None = None,
        user_id: int | None = None,
        tags: list[str] | None = None,
    ) -> Request:
        self_payload: dict[str, Any] = {
            "media_type": self.type,
            "language_profile_id": self.language_profile_id or 0,
            "profile_id": self.profile_id or 0,
            "root_folder": self.root_folder,
            "server_id": self.server_id or 0,
            "tags": self.tags,
        }
        payload: dict[str, Any] = {}
        if media_type is not None:
            payload["media_type"] = media_type
        if seasons is not None:
            payload["seasons"] = seasons
        if is_4k is not None:
            payload["is_4k"] = is_4k
        if server_id is not None:
            payload["server_id"] = server_id
        if profile_id is not None:
            payload["profile_id"] = profile_id
        if root_folder is not None:
            payload["root_folder"] = root_folder
        if language_profile_id is not None:
            payload["language_profile_id"] = language_profile_id
        if user_id is not None:
            payload["user_id"] = user_id
        if tags is not None:
            payload["tags"] = tags

        return Request.from_data(
            await self.http.request(
                "PUT",
                APIPath("/request/{request_id}", request_id=self.id),
                payload=self_payload | payload,
            ),
            http=self.http,
        )

    async def delete(self) -> None:
        await self.http.request(
            "DELETE",
            APIPath("/request/{request_id}", request_id=self.id),
        )

    async def retry(self) -> Request:
        return Request.from_data(
            await self.http.request(
                "POST",
                APIPath("/request/{request_id}/retry", request_id=self.id),
            ),
            http=self.http,
        )

    async def update_status(self, status: Literal["approve", "decline"]) -> Request:
        return Request.from_data(
            await self.http.request(
                "POST",
                APIPath(
                    "/request/{request_id}/{status}",
                    request_id=self.id,
                    status=status,
                ),
            ),
            http=self.http,
        )


class RequestCount(Base):
    total: int
    movie: int
    tv: int
    pending: int
    approved: int
    declined: int
    processing: int
    available: int
    completed: int


class RequestEndpoints(Endpoints):
    async def create(
        self, media: Requestable, *, seasons: list[int] | Literal["all"] | None = None
    ) -> Request:
        request_data = {
            "media_type": media.media_type,
            "media_id": media.id,
        }
        if media.media_type == MediaType.TV:
            request_data["seasons"] = seasons
        if media.media_type == MediaType.MOVIE and seasons is not None:
            warn("Requested a Movie with Seasons data, ignoring seasons.", stacklevel=2)
        return Request.from_data(
            await self.client.http.request(
                "POST", APIPath("/request"), payload=request_data
            ),
            http=self.client.http,
        )

    async def list(  # noqa: PLR0913
        self,
        *,
        take: int = 20,
        skip: int = 0,
        filter_: RequestFilter | None = None,
        sort: RequestSort | None = None,
        sort_direction: RequestSortDirection | None = None,
        requested_by: int | None = None,
        media_type: RequestMediaType | None = None,
    ) -> list[Request]:
        params: dict[str, Any] = {"take": take, "skip": skip}
        if filter_:
            params["filter"] = filter_
        if sort:
            params["sort"] = sort
        if sort_direction:
            params["sort_direction"] = sort_direction
        if requested_by:
            params["requested_by"] = requested_by
        if media_type:
            params["media_type"] = media_type

        resp = await self.client.http.request("GET", APIPath("/request"), params=params)  # pyright: ignore[reportArgumentType]

        return Request.from_data_list(resp["results"], http=self.client.http)

    async def count(self) -> RequestCount:
        return RequestCount.from_data(
            await self.client.http.request("GET", APIPath("/request/count")),
        )

    async def get(self, request_id: int) -> Request:
        return Request.from_data(
            await self.client.http.request(
                "GET",
                APIPath(f"/request/{request_id}", request_id=request_id),
            ),
            http=self.client.http,
        )
