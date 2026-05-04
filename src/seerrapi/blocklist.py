from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Any, Protocol

from .base import Base, Endpoints, MediaType
from .context import client_context
from .http import APIPath
from .users import User

if TYPE_CHECKING:
    from .base import Requestable

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
    async def list(
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

        resp = await self.http.request(
            "GET",
            APIPath(
                "/blocklist",
            ),
            params=params,
        )

        return BlocklistItem.from_data_list(resp["results"])

    async def add(self, media: MediaInfo) -> None:
        client = client_context.get()
        user = await client.me()
        payload = {
            "tmdb_id": media.tmdb_id,
            "title": media.title,
            "media_type": media.media_type,
            "user": user.id,
        }

        await self.http.request("POST", APIPath("/blocklist"), payload=payload)

    async def details(self, media: Requestable) -> BlocklistItem:
        if media.media_type not in (MediaType.MOVIE, MediaType.TV):
            msg = f"Unsupported media type: {media.media_type}"
            raise ValueError(msg)
        return BlocklistItem.from_data(
            await self.http.request(
                "GET",
                APIPath("/blocklist/{tmdb_id}", tmdb_id=media.id),
                params={"media_type": media.media_type},
            ),
        )

    async def remove(self, media: Requestable) -> None:
        if media.media_type not in (MediaType.MOVIE, MediaType.TV):
            msg = f"Unsupported media type: {media.media_type}"
            raise ValueError(msg)
        await self.http.request(
            "DELETE",
            APIPath("/blocklist/{tmdb_id}", tmdb_id=media.id),
            params={"media_type": media.media_type},
        )
