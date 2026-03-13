import pytest
import pytest_asyncio

from seerrapi import Genre, Keyword, MediaType, ProductionCompany
from seerrapi.client import SeerrClient
from seerrapi.languages import Language
from seerrapi.movies import Movie
from seerrapi.person import Person
from seerrapi.request import Request
from seerrapi.service import Radarr, Sonarr
from seerrapi.settings import MainSettings
from seerrapi.tv import TV

from . import MediaInfo
from .config import SEERR_API_KEY, SEERR_HOST


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
    return await seerr_client.movie(105)


@pytest_asyncio.fixture
async def seerr_tv(seerr_client: SeerrClient) -> TV:
    return await seerr_client.get_tv(96580)


@pytest.fixture
def seerr_genre() -> Genre:
    return Genre(id=16, name="Animation")


@pytest.fixture
def seerr_language() -> Language:
    return Language.FRENCH


@pytest.fixture
def seerr_studio() -> ProductionCompany:
    return ProductionCompany(
        id=2,
        name="Walt Disney Pictures",
        origin_country="US",
        description="",
        headquarters="Burbank, California",
        homepage="https://movies.disney.com",
        logo_path="/wdrCwmRnLFJhEoH8GSfymY85KHT.png",
    )


@pytest.fixture
def seerr_network() -> ProductionCompany:
    return ProductionCompany(
        id=2,
        name="ABC",
        origin_country="US",
        headquarters="New York City, New York",
        homepage="https://abc.com",
        logo_path="/2uy2ZWcplrSObIyt4x0Y9rkG6qO.png",
    )


@pytest.fixture
def seerr_keyword() -> Keyword:
    return Keyword(id=242214, name="origin story")


@pytest_asyncio.fixture
async def seerr_person(seerr_client: SeerrClient) -> Person:
    return await seerr_client.get_person(1)


@pytest_asyncio.fixture
async def seerr_radarr(seerr_client: SeerrClient) -> Radarr:
    return (await seerr_client.service.radarr())[0]


@pytest_asyncio.fixture
async def seerr_sonarr(seerr_client: SeerrClient) -> Sonarr:
    return (await seerr_client.service.sonarr())[0]


@pytest.fixture
def seerr_media() -> MediaInfo:
    return MediaInfo(
        tmdb_id=1413097,
        title="Melania",
        media_type=MediaType.MOVIE,
        user=1,
    )
