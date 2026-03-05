import pytest

from seerrapi.request import Request, RequestStatus


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
