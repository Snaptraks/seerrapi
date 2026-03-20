import pytest

from seerrapi.base import MediaType
from seerrapi.client import SeerrClient
from seerrapi.watchlist import WatchlistItem

from . import MediaInfo, assert_list_of_instances

MEDIA = MediaInfo(tmdb_id=105, media_type=MediaType.MOVIE, title="Test Movie", user=1)


@pytest.mark.asyncio
async def test_watchlist_add(seerr_client: SeerrClient) -> None:
    wl_item = await seerr_client.watchlist.add(MEDIA)

    assert isinstance(wl_item, WatchlistItem)


@pytest.mark.asyncio
async def test_watchlist_list(seerr_client: SeerrClient) -> None:
    watchlist = await seerr_client.watchlist.list()

    assert assert_list_of_instances(watchlist, WatchlistItem)


@pytest.mark.asyncio
async def test_watchlist_delete(seerr_client: SeerrClient) -> None:
    watchlist = await seerr_client.watchlist.list()

    item = next(w for w in watchlist if w.tmdb_id == MEDIA.tmdb_id)

    await item.delete()
