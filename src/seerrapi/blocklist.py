from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Any, Protocol

from .base import Base, Endpoints, MediaType
from .http import APIPath
from .users import User

if TYPE_CHECKING:

    class MediaInfo(Protocol):
        title: str
        tmdb_id: int
        media_type: MediaType


class BlocklistItem(Base):
    id: int
    blocklisted_tags: str | None = None
    created_at: datetime
    media_type: MediaType
    title: str
    tmdb_id: int
    user: User | None


class BlocklistFilter(StrEnum):
    ALL = "all"
    MANUAL = "manual"
    BLOCKLISTED_TAGS = "blocklistedTags"


class BlocklistEndpoints(Endpoints):
    async def __call__(
        self,
        take: int = 25,
        skip: int = 0,
        search: str | None = None,
        blocklist_filter: BlocklistFilter | None = None,
    ) -> list[BlocklistItem]:
        params: dict[str, Any] = {
            "take": take,
            "skip": skip,
        }

        if search is not None:
            params["search"] = search
        if blocklist_filter is not None:
            params["filter"] = blocklist_filter

        resp = await self.client.http.request(
            "GET",
            APIPath(
                "/blocklist",
            ),
            params=params,
        )

        return BlocklistItem.from_data_list(resp["results"])

    async def add(self, media: MediaInfo) -> None:
        user = await self.client.me()
        payload = {
            "tmdb_id": media.tmdb_id,
            "title": media.title,
            "media_type": media.media_type,
            "user": user.id,
        }

        await self.client.http.request("POST", APIPath("/blocklist"), payload=payload)

    async def details(self, tmdb_id: int) -> BlocklistItem:
        return BlocklistItem.from_data(
            await self.client.http.request(
                "GET",
                APIPath("/blocklist/{tmdb_id}", tmdb_id=tmdb_id),
            ),
        )

    async def remove(self, tmdb_id: int) -> None:
        await self.client.http.request(
            "DELETE",
            APIPath("/blocklist/{tmdb_id}", tmdb_id=tmdb_id),
        )
