import pytest

from seerrapi.blocklist import BlocklistFilter, BlocklistItem
from seerrapi.client import SeerrClient

from . import MediaInfo


@pytest.mark.asyncio
async def test_blocklist(seerr_client: SeerrClient) -> None:
    blocklist = await seerr_client.blocklist()

    assert isinstance(blocklist, list)
    for item in blocklist:
        assert isinstance(item, BlocklistItem)


@pytest.mark.asyncio
async def test_blocklist_filter_manual(seerr_client: SeerrClient) -> None:
    blocklist = await seerr_client.blocklist(blocklist_filter=BlocklistFilter.MANUAL)

    for item in blocklist:
        assert item.user is not None


@pytest.mark.asyncio
async def test_blocklist_filter_tags(seerr_client: SeerrClient) -> None:
    blocklist = await seerr_client.blocklist(
        blocklist_filter=BlocklistFilter.BLOCKLISTED_TAGS,
    )

    for item in blocklist:
        assert item.user is None


@pytest.mark.asyncio
async def test_blocklist_add(seerr_client: SeerrClient, seerr_media: MediaInfo) -> None:
    await seerr_client.blocklist.add(seerr_media)


@pytest.mark.asyncio
async def test_blocklist_details(
    seerr_client: SeerrClient, seerr_media: MediaInfo,
) -> None:
    # not great, but this test checks the media added
    # in test_blocklist_add, which is run before
    blocklist_item = await seerr_client.blocklist.details(seerr_media.tmdb_id)
    assert isinstance(blocklist_item, BlocklistItem)


@pytest.mark.asyncio
async def test_blocklist_remove(
    seerr_client: SeerrClient, seerr_media: MediaInfo,
) -> None:
    # not great, but this test removes the media added
    # in test_blocklist_add, which is run before
    await seerr_client.blocklist.remove(seerr_media.tmdb_id)
