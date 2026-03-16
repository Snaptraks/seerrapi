from __future__ import annotations

from .base import _Endpoints
from .http import APIPath
from .movies import Collection


class CollectionEndpoints(_Endpoints):
    async def __call__(self, collection_id: int, *, language: str = "en") -> Collection:
        return Collection.from_data(
            await self.client.http.request(
                "GET",
                APIPath("/collection/{collection_id}", collection_id=collection_id),
                params={"language": language},
            ),
        )
