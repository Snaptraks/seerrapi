import pytest

from seerrapi import Genre, Keyword, MediaType, ProductionCompany, WatchlistItem
from seerrapi.client import SeerrClient
from seerrapi.errors import SeerrSearchError
from seerrapi.languages import Language
from seerrapi.search import (
    CertificationMode,
    GenreSlider,
    MovieResult,
    PersonResult,
    TVResult,
)

from . import _test_list_of_instances


@pytest.mark.asyncio
async def test_search(seerr_client: SeerrClient) -> None:
    results = await seerr_client.search("Bob Ross")

    assert _test_list_of_instances(results, (MovieResult, TVResult, PersonResult))


@pytest.mark.asyncio
async def test_search_keyword(seerr_client: SeerrClient) -> None:
    keywords = await seerr_client.search.keyword("painting")

    assert _test_list_of_instances(keywords, Keyword)


@pytest.mark.asyncio
async def test_search_company(seerr_client: SeerrClient) -> None:
    companies = await seerr_client.search.company("disney")

    assert _test_list_of_instances(companies, ProductionCompany)


@pytest.mark.asyncio
async def test_discover_movies(seerr_client: SeerrClient) -> None:
    movies = await seerr_client.discover.movies()

    assert _test_list_of_instances(movies, MovieResult)


@pytest.mark.asyncio
async def test_discover_movies_error_certification_exact_gte(
    seerr_client: SeerrClient,
) -> None:
    with pytest.raises(SeerrSearchError):
        await seerr_client.discover.movies(
            certification_mode=CertificationMode.EXACT,
            certification_gte="PG-13",
        )


@pytest.mark.asyncio
async def test_discover_movies_error_certification_exact_lte(
    seerr_client: SeerrClient,
) -> None:
    with pytest.raises(SeerrSearchError):
        await seerr_client.discover.movies(
            certification_mode=CertificationMode.EXACT,
            certification_lte="PG-13",
        )


@pytest.mark.asyncio
async def test_discover_movies_error_certification_range(
    seerr_client: SeerrClient,
) -> None:
    with pytest.raises(SeerrSearchError):
        await seerr_client.discover.movies(
            certification_mode=CertificationMode.RANGE,
            certification="PG-13",
        )


@pytest.mark.asyncio
async def test_discover_movies_genre(
    seerr_client: SeerrClient, seerr_genre: Genre,
) -> None:
    movies = await seerr_client.discover.movies.genre(seerr_genre)

    assert _test_list_of_instances(movies, MovieResult)


@pytest.mark.asyncio
async def test_discover_movies_language(
    seerr_client: SeerrClient, seerr_language: Language,
) -> None:
    movies = await seerr_client.discover.movies.language(seerr_language)

    assert _test_list_of_instances(movies, MovieResult)


@pytest.mark.asyncio
async def test_discover_movies_studio(
    seerr_client: SeerrClient, seerr_studio: ProductionCompany,
) -> None:
    movies = await seerr_client.discover.movies.studio(seerr_studio)

    assert _test_list_of_instances(movies, MovieResult)


@pytest.mark.asyncio
async def test_discover_movies_upcoming(seerr_client: SeerrClient) -> None:
    movies = await seerr_client.discover.movies.upcoming()

    assert _test_list_of_instances(movies, MovieResult)


@pytest.mark.asyncio
async def test_discover_tv(seerr_client: SeerrClient) -> None:
    tvs = await seerr_client.discover.tv()

    assert _test_list_of_instances(tvs, TVResult)


@pytest.mark.asyncio
async def test_discover_tv_error_certification_exact_gte(
    seerr_client: SeerrClient,
) -> None:
    with pytest.raises(SeerrSearchError):
        await seerr_client.discover.tv(
            certification_mode=CertificationMode.EXACT,
            certification_gte="PG-13",
        )


@pytest.mark.asyncio
async def test_discover_tv_error_certification_exact_lte(
    seerr_client: SeerrClient,
) -> None:
    with pytest.raises(SeerrSearchError):
        await seerr_client.discover.tv(
            certification_mode=CertificationMode.EXACT,
            certification_lte="PG-13",
        )


@pytest.mark.asyncio
async def test_discover_tv_error_certification_range(
    seerr_client: SeerrClient,
) -> None:
    with pytest.raises(SeerrSearchError):
        await seerr_client.discover.tv(
            certification_mode=CertificationMode.RANGE,
            certification="PG-13",
        )


@pytest.mark.asyncio
async def test_discover_tv_genre(seerr_client: SeerrClient, seerr_genre: Genre) -> None:
    tvs = await seerr_client.discover.tv.genre(seerr_genre)

    assert _test_list_of_instances(tvs, TVResult)


@pytest.mark.asyncio
async def test_discover_tv_language(
    seerr_client: SeerrClient, seerr_language: Language,
) -> None:
    tvs = await seerr_client.discover.tv.language(seerr_language)

    assert _test_list_of_instances(tvs, TVResult)


@pytest.mark.asyncio
async def test_discover_tv_network(
    seerr_client: SeerrClient, seerr_network: ProductionCompany,
) -> None:
    tvs = await seerr_client.discover.tv.network(seerr_network)

    assert _test_list_of_instances(tvs, TVResult)


@pytest.mark.asyncio
async def test_discover_tv_upcoming(seerr_client: SeerrClient) -> None:
    tvs = await seerr_client.discover.tv.upcoming()

    assert _test_list_of_instances(tvs, TVResult)


@pytest.mark.asyncio
async def test_discover_trending(seerr_client: SeerrClient) -> None:
    media = await seerr_client.discover.trending()

    assert _test_list_of_instances(media, (MovieResult, TVResult))


@pytest.mark.asyncio
async def test_discover_genre_slider_movie(seerr_client: SeerrClient) -> None:
    movies = await seerr_client.discover.genre_slider(MediaType.MOVIE)

    assert _test_list_of_instances(movies, GenreSlider)


@pytest.mark.asyncio
async def test_discover_genre_slider_tv(seerr_client: SeerrClient) -> None:
    tvs = await seerr_client.discover.genre_slider(MediaType.TV)

    assert _test_list_of_instances(tvs, GenreSlider)


@pytest.mark.asyncio
async def test_discover_watchlist(seerr_client: SeerrClient) -> None:
    watchlist = await seerr_client.discover.watchlist()

    assert _test_list_of_instances(watchlist, WatchlistItem)
