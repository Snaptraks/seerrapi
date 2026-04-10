import pytest

from seerrapi.base import (
    Genre,
    MediaType,
    ProductionCompany,
    ProductionCountry,
    SpokenLanguage,
)
from seerrapi.client import SeerrClient

from . import assert_list_of_instances


@pytest.mark.asyncio
async def test_tmdb_regions(seerr_client: SeerrClient) -> None:
    backdrops = await seerr_client.tmdb.regions()

    assert assert_list_of_instances(backdrops, ProductionCountry)


@pytest.mark.asyncio
async def test_tmdb_languages(seerr_client: SeerrClient) -> None:
    languages = await seerr_client.tmdb.languages()

    assert assert_list_of_instances(languages, SpokenLanguage)


@pytest.mark.asyncio
async def test_tmdb_studio(seerr_client: SeerrClient) -> None:
    studio = await seerr_client.tmdb.studio(1)

    assert isinstance(studio, ProductionCompany)


@pytest.mark.asyncio
async def test_tmdb_network(seerr_client: SeerrClient) -> None:
    network = await seerr_client.tmdb.network(1)

    assert isinstance(network, ProductionCompany)


@pytest.mark.asyncio
async def test_tmdb_genres_movie(seerr_client: SeerrClient) -> None:
    genres = await seerr_client.tmdb.genres(MediaType.MOVIE)

    assert assert_list_of_instances(genres, Genre)


@pytest.mark.asyncio
async def test_tmdb_genres_tv(seerr_client: SeerrClient) -> None:
    genres = await seerr_client.tmdb.genres(MediaType.TV)

    assert assert_list_of_instances(genres, Genre)


@pytest.mark.asyncio
async def test_tmdb_backdrops(seerr_client: SeerrClient) -> None:
    backdrops = await seerr_client.tmdb.backdrops()

    assert assert_list_of_instances(backdrops, str)
