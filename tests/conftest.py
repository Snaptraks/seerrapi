from dataclasses import dataclass

import pytest
import pytest_asyncio

from seerrapi.client import SeerrClient
from seerrapi.movies import Movie
from seerrapi.person import Person
from seerrapi.request import MediaType, Request
from seerrapi.service import Radarr, Sonarr
from seerrapi.settings import MainSettings
from seerrapi.tv import TV

from .config import SEERR_API_KEY, SEERR_HOST


@dataclass
class MediaInfo:
    tmdb_id: int
    title: str
    media_type: MediaType
    user: int


@pytest.fixture(scope="session")
def seerr_client() -> SeerrClient:
    return SeerrClient(host=SEERR_HOST, api_key=SEERR_API_KEY)


@pytest_asyncio.fixture(scope="function")
async def temp_seerr_client() -> SeerrClient:
    return SeerrClient(host=SEERR_HOST)


@pytest_asyncio.fixture
async def seerr_settings(seerr_client: SeerrClient) -> MainSettings:
    return await seerr_client.get_main_settings()


@pytest_asyncio.fixture
async def seerr_request(seerr_client: SeerrClient) -> Request:
    return await seerr_client.get_request(1)


@pytest_asyncio.fixture
async def seerr_movie(seerr_client: SeerrClient) -> Movie:
    return await seerr_client.get_movie(105)


@pytest_asyncio.fixture
async def seerr_tv(seerr_client: SeerrClient) -> TV:
    return await seerr_client.get_tv(96580)


@pytest_asyncio.fixture
async def seerr_person(seerr_client: SeerrClient) -> Person:
    return await seerr_client.get_person(1)


@pytest_asyncio.fixture
async def seerr_radarr(seerr_client: SeerrClient) -> Radarr:
    return (await seerr_client.get_radarr())[0]


@pytest_asyncio.fixture
async def seerr_sonarr(seerr_client: SeerrClient) -> Sonarr:
    return (await seerr_client.get_sonarr())[0]


@pytest.fixture
def seerr_media() -> MediaInfo:
    return MediaInfo(
        tmdb_id=1413097,
        title="Melania",
        media_type=MediaType.MOVIE,
        user=1,
    )
