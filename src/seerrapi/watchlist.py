from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from .base import Endpoints, MediaType, Stateful
from .context import client_context
from .http import APIPath
from .request import MediaInfo
from .users import User

if TYPE_CHECKING:
    from .base import Requestable


class WatchlistItem(Stateful):
    id: int
    title: str
    media_type: MediaType
    tmdb_id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    requested_by: User | None = None
    media: MediaInfo | None = None

    async def delete(self) -> None:
        await self.http.request(
            "DELETE",
            APIPath("/watchlist/{tmdb_id}", tmdb_id=self.tmdb_id),
            params={"media_type": self.media_type},
        )


class WatchlistEndpoints(Endpoints):
    async def add(self, media: Requestable) -> WatchlistItem:
        payload = {"tmdb_id": media.id, "media_type": media.media_type}
        resp = await self.http.request("POST", APIPath("/watchlist"), payload=payload)

        return WatchlistItem.from_data(resp)

    async def list(self) -> list[WatchlistItem]:
        client = client_context.get()
        user = await client.me()
        resp = await self.http.request(
            "GET", APIPath("/user/{user_id}/watchlist", user_id=user.id)
        )

        return WatchlistItem.from_data_list(resp["results"])
