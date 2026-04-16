from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from .base import Base, Endpoints, Stateful
from .http import APIPath
from .request import Season, _MediaInfoBase
from .users import User

if TYPE_CHECKING:
    type MediaFilter = Literal[
        "all",
        "available",
        "partial",
        "allavailable",
        "processing",
        "pending",
        "deleted",
    ]
    type MediaSort = Literal[
        "added",
        "modified",
        "mediaAdded",
    ]
    type MediaStatus = Literal[
        "available",
        "partial",
        "processing",
        "pending",
        "unknown",
        "deleted",
    ]


class WatchData(Base):
    users: list[User]
    play_count: int
    play_count_7_days: int
    play_count_30_days: int


class Media(Stateful, _MediaInfoBase):  # pyright: ignore[reportIncompatibleMethodOverride]
    seasons: list[Season]

    async def delete(self, *, file: bool = False) -> None:
        path = f"/media/{{media_id}}{'/file' if file else ''}"

        await self.http.request("DELETE", APIPath(path, media_id=self.id))

    async def update_status(self, status: MediaStatus) -> Media:
        resp = await self.http.request(
            "POST",
            APIPath("/media/{media_id}/{status}", media_id=self.id, status=status),
            payload={},  # needs an empty payload?
        )

        return Media.from_data(resp, http=self.http)

    async def watch_data(self) -> ...:
        resp = await self.http.request(
            "GET", APIPath("/media/{media_id}/watch_data", media_id=self.id)
        )

        return WatchData.from_data(resp["data"])


class MediaEndpoints(Endpoints):
    async def get(
        self,
        *,
        take: int = 20,
        skip: int = 0,
        filter_: MediaFilter | None = None,
        sort: MediaSort | None = None,
    ) -> list[Media]:
        params: dict[str, Any] = {"take": take, "skip": skip}
        if filter_:
            params["filter"] = filter_
        if sort:
            params["sort"] = sort

        resp = await self.client.http.request("GET", APIPath("/media"), params=params)

        return Media.from_data_list(resp["results"], http=self.client.http)
