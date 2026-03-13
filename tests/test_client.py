from dataclasses import dataclass
from typing import Literal

import pytest

from seerrapi import MediaType
from seerrapi.client import SeerrClient
from seerrapi.errors import SeerrAuthenticationError
from seerrapi.movies import Collection, Movie
from seerrapi.person import Person
from seerrapi.request import Request, RequestCount
from seerrapi.service import Radarr, Sonarr
from seerrapi.settings import MainSettings, NetworkSettings
from seerrapi.tv import TV
from seerrapi.users import User

from .config import PLEX_AUTH_TOKEN

# Settings methods


@pytest.mark.asyncio
async def test_client_get_main_settings(seerr_client: SeerrClient) -> None:
    main_settings = await seerr_client.get_main_settings()
    assert isinstance(main_settings, MainSettings)


@pytest.mark.asyncio
async def test_client_get_network_settings(seerr_client: SeerrClient) -> None:
    network_settings = await seerr_client.get_network_settings()
    assert isinstance(network_settings, NetworkSettings)


# Auth methods


@pytest.mark.asyncio
async def test_client_auth_plex(temp_seerr_client: SeerrClient) -> None:
    await temp_seerr_client.auth_plex(PLEX_AUTH_TOKEN)

    assert temp_seerr_client.http._cookie_auth is not None

    me = await temp_seerr_client.me()
    assert isinstance(me, User)


@pytest.mark.skip
@pytest.mark.asyncio
async def test_client_auth_jellyseerr(temp_seerr_client: SeerrClient) -> None:
    await temp_seerr_client.auth_jellyfin(
        username="notausername",
        password="notreallythepassword",  # noqa: S106
        hostname="http://jellyfin:8096",
        email="me@example.com",
    )

    assert temp_seerr_client.http._cookie_auth is not None
    me = await temp_seerr_client.me()
    assert isinstance(me, User)


@pytest.mark.skip
@pytest.mark.asyncio
async def test_client_auth_local(temp_seerr_client: SeerrClient) -> None:
    await temp_seerr_client.auth_local(
        email="me@example.com",
        password="notreallythepassword",  # noqa: S106
    )

    assert temp_seerr_client.http._cookie_auth is not None
    me = await temp_seerr_client.me()
    assert isinstance(me, User)


@pytest.mark.asyncio
async def test_client_logout(temp_seerr_client: SeerrClient) -> None:
    await temp_seerr_client.auth_plex(PLEX_AUTH_TOKEN)
    await temp_seerr_client.logout()

    with pytest.raises(SeerrAuthenticationError):
        await temp_seerr_client.me()


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


# TV methods


@pytest.mark.asyncio
async def test_client_get_tv(seerr_client: SeerrClient) -> None:
    tv = await seerr_client.get_tv(96580)
    assert isinstance(tv, TV)


# Person methods


@pytest.mark.asyncio
async def test_client_get_person(seerr_client: SeerrClient) -> None:
    person = await seerr_client.get_person(1)
    assert isinstance(person, Person)


# Collection methods


@pytest.mark.asyncio
async def test_client_get_collection(seerr_client: SeerrClient) -> None:
    collection = await seerr_client.get_collection(119)
    assert isinstance(collection, Collection)


# Service methods


@pytest.mark.asyncio
async def test_client_get_radarr(seerr_client: SeerrClient) -> None:
    services = await seerr_client.get_radarr()

    assert isinstance(services, list)
    for service in services:
        assert isinstance(service, Radarr)


@pytest.mark.asyncio
async def test_client_get_sonarr(seerr_client: SeerrClient) -> None:
    services = await seerr_client.get_sonarr()

    assert isinstance(services, list)
    for service in services:
        assert isinstance(service, Sonarr)
