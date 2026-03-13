import pytest

from seerrapi.client import SeerrClient
from seerrapi.movies import Collection


@pytest.mark.asyncio
async def test_collection(seerr_client: SeerrClient) -> None:
    collection = await seerr_client.collection(119)
    assert isinstance(collection, Collection)
