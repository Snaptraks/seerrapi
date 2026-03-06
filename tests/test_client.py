from dataclasses import dataclass
from typing import Literal

import pytest

from seerrapi.client import SeerrClient
from seerrapi.movies import Movie
from seerrapi.public import AppData, Status
from seerrapi.request import MediaType, Request, RequestCount
from seerrapi.settings import MainSettings, NetworkSettings

# Public methods


@pytest.mark.asyncio
async def test_client_get_status(seerr_client: SeerrClient) -> None:
    status = await seerr_client.get_status()
    assert isinstance(status, Status)


@pytest.mark.asyncio
async def test_client_get_app_data(seerr_client: SeerrClient) -> None:
    app_data = await seerr_client.get_app_data()
    assert isinstance(app_data, AppData)


# Settings methods


@pytest.mark.asyncio
async def test_client_get_main_settings(seerr_client: SeerrClient) -> None:
    main_settings = await seerr_client.get_main_settings()
    assert isinstance(main_settings, MainSettings)


@pytest.mark.asyncio
async def test_client_get_network_settings(seerr_client: SeerrClient) -> None:
    network_settings = await seerr_client.get_network_settings()
    assert isinstance(network_settings, NetworkSettings)


# Request methods


@pytest.mark.asyncio
async def test_client_get_requests(seerr_client: SeerrClient) -> None:
    requests = await seerr_client.get_requests()
    assert isinstance(requests, list)
    for request in requests:
        assert isinstance(request, Request)


@pytest.mark.skip
@pytest.mark.asyncio
async def test_client_post_request(seerr_client: SeerrClient) -> None:
    @dataclass
    class Media:
        media_type: MediaType
        tvdb_id: int
        seasons: list[int] | Literal["all"]

    media = Media(
        media_type=MediaType.TV,
        tvdb_id=456,
        seasons=[1, 2, 3],
    )

    request = await seerr_client.request(media)

    assert isinstance(request, Request)


@pytest.mark.asyncio
async def test_client_get_requests_count(seerr_client: SeerrClient) -> None:
    requests_count = await seerr_client.get_requests_count()
    assert isinstance(requests_count, RequestCount)


@pytest.mark.asyncio
async def test_client_get_request_by_id(seerr_client: SeerrClient) -> None:
    request = await seerr_client.get_request(1)
    assert isinstance(request, Request)


# Movies methods


@pytest.mark.asyncio
async def test_client_get_movie(seerr_client: SeerrClient) -> None:
    movie = await seerr_client.get_movie(105)
    assert isinstance(movie, Movie)
