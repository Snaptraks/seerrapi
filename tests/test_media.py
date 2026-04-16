from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio

from seerrapi.base import MediaType
from seerrapi.client import SeerrClient
from seerrapi.media import Media, WatchData

from . import assert_list_of_instances


@pytest_asyncio.fixture
async def media(seerr_client: SeerrClient) -> AsyncGenerator[Media]:
    medias = await seerr_client.media.get(take=20)
    media = next(m for m in medias if m.media_type == MediaType.TV)

    yield media

    await media.update_status("available")


@pytest.mark.asyncio
async def test_media_get(seerr_client: SeerrClient) -> None:
    media = await seerr_client.media.get()

    assert assert_list_of_instances(media, Media)


@pytest.mark.skip
@pytest.mark.asyncio
async def test_media_delete(media: Media) -> None:
    await media.delete()


@pytest.mark.skip
@pytest.mark.asyncio
async def test_media_delete_file(media: Media) -> None:
    await media.delete(file=True)


@pytest.mark.asyncio
async def test_media_update_status(media: Media) -> None:
    await media.update_status("processing")


@pytest.mark.asyncio
async def test_media_watch_data(media: Media) -> None:
    watch_data = await media.watch_data()

    assert isinstance(watch_data, WatchData)
