from __future__ import annotations

from datetime import datetime
from enum import IntEnum, StrEnum
from typing import TYPE_CHECKING, Literal, TypedDict, Unpack

from pydantic import Field

from . import Base, Stateful
from .http import APIPath
from .users import User

if TYPE_CHECKING:
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

    class RequestUpdateDict(TypedDict, total=False):
        media_type: MediaType
        seasons: list[int]
        is4k: bool
        server_id: int | None
        profile_id: int | None
        root_folder: str | None
        language_profile_id: int
        user_id: int
        tags: list[str] | None


# Media objects


class MediaType(StrEnum):
    MOVIE = "movie"
    TV = "tv"


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
    seasons: list[Season]
    modified_by: User
    requested_by: User
    season_count: int | None = None
    profile_name: str | None = None
    can_remove: bool | None = None

    async def update(self, **payload: Unpack[RequestUpdateDict]) -> Request:
        self_payload: RequestUpdateDict = {
            "media_type": self.type,
            "language_profile_id": self.language_profile_id or 0,
            "profile_id": self.profile_id or 0,
            "root_folder": self.root_folder,
            "server_id": self.server_id or 0,
            "tags": self.tags,
        }

        return Request.from_data(
            await self.http.request(
                "PUT",
                APIPath("/request/{request_id}", request_id=self.id),
                payload=self_payload | payload,  # pyright: ignore[reportArgumentType]
            ),
            http=self.http,
        )

    async def delete(self) -> None:
        await self.http.request(
            "DELETE", APIPath("/request/{request_id}", request_id=self.id)
        )

    async def retry(self) -> Request:
        return Request.from_data(
            await self.http.request(
                "POST", APIPath("/request/{request_id}/retry", request_id=self.id)
            ),
            http=self.http,
        )

    async def update_status(self, status: Literal["approve", "decline"]) -> Request:
        return Request.from_data(
            await self.http.request(
                "POST",
                APIPath(
                    "/request/{request_id}/{status}", request_id=self.id, status=status
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
