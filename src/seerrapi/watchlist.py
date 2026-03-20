from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from .base import Endpoints, MediaType, Stateful
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
            "DELETE", APIPath("/watchlist/{tmdb_id}", tmdb_id=self.tmdb_id)
        )


class WatchlistEndpoints(Endpoints):
    async def add(self, media: Requestable) -> WatchlistItem:
        payload = {"tmdb_id": media.id, "media_type": media.media_type}
        resp = await self.client.http.request(
            "POST", APIPath("/watchlist"), payload=payload
        )

        return WatchlistItem.from_data(resp, http=self.client.http)

    async def list(self) -> list[WatchlistItem]:
        user = await self.client.me()
        resp = await self.client.http.request(
            "GET", APIPath("/user/{user_id}/watchlist", user_id=user.id)
        )

        return WatchlistItem.from_data_list(resp["results"], http=self.client.http)
