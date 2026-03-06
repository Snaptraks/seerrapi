import pytest
import pytest_asyncio

from seerrapi.client import SeerrClient
from seerrapi.movies import Movie
from seerrapi.request import Request
from seerrapi.settings import MainSettings
from seerrapi.tv import TV

from .config import SEERR_API_KEY


@pytest.fixture(scope="session")
def seerr_client() -> SeerrClient:
    return SeerrClient(host="http://localhost:5055", api_key=SEERR_API_KEY)


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
