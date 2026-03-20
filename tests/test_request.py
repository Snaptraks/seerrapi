from dataclasses import dataclass
from typing import Literal

import pytest

from seerrapi.base import MediaType
from seerrapi.client import SeerrClient
from seerrapi.request import Request, RequestCount, RequestStatus


@pytest.mark.asyncio
async def test_client_get_requests(seerr_client: SeerrClient) -> None:
    requests = await seerr_client.request.list()
    assert isinstance(requests, list)
    for request in requests:
        assert isinstance(request, Request)


@pytest.mark.skip
@pytest.mark.asyncio
async def test_client_post_request(seerr_client: SeerrClient) -> None:
    @dataclass
    class Media:
        media_type: MediaType
        id: int
        seasons: list[int] | Literal["all"]

    media = Media(
        media_type=MediaType.TV,
        id=456,
        seasons=[1, 2, 3],
    )

    request = await seerr_client.request.create(media, seasons=media.seasons)

    assert isinstance(request, Request)


@pytest.mark.asyncio
async def test_client_get_requests_count(seerr_client: SeerrClient) -> None:
    requests_count = await seerr_client.request.count()
    assert isinstance(requests_count, RequestCount)


@pytest.mark.asyncio
async def test_client_get_request_by_id(seerr_client: SeerrClient) -> None:
    request = await seerr_client.request.get(1)
    assert isinstance(request, Request)


@pytest.mark.asyncio
async def test_request_update(seerr_request: Request) -> None:
    seasons = [1, 2]
    r = await seerr_request.update(seasons=seasons)

    assert isinstance(r, Request)
    assert r is not seerr_request
    assert len(r.seasons) == len(seasons)

    await r.update(seasons=[1])


@pytest.mark.asyncio
async def test_request_update_status(seerr_request: Request) -> None:
    r = await seerr_request.update_status("decline")
    assert isinstance(r, Request)
    assert r is not seerr_request
    assert r.status == RequestStatus.DECLINED

    await r.update_status("approve")
