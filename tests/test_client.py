import pytest

from seerrapi.base import MediaType
from seerrapi.client import SeerrClient
from seerrapi.settings import MainSettings, NetworkSettings

# Settings methods


@pytest.mark.asyncio
async def test_client_get_main_settings(seerr_client: SeerrClient) -> None:
    main_settings = await seerr_client.get_main_settings()
    assert isinstance(main_settings, MainSettings)


@pytest.mark.asyncio
async def test_client_get_network_settings(seerr_client: SeerrClient) -> None:
    network_settings = await seerr_client.get_network_settings()
    assert isinstance(network_settings, NetworkSettings)


# Search and Request flow


@pytest.mark.asyncio
async def test_client_search_movie_and_request(seerr_client: SeerrClient) -> None:
    results = await seerr_client.search("Back to the Future")

    bttf_movie = next(r for r in results if r.media_type == MediaType.MOVIE)

    request = await seerr_client.request.create(bttf_movie)

    requests = await seerr_client.request.list()

    assert any(r.id == request.id for r in requests)
    assert any(r.media.tmdb_id == bttf_movie.id for r in requests)

    await request.delete()


@pytest.mark.asyncio
async def test_client_search_movie_and_request_with_seasons_warns(
    seerr_client: SeerrClient,
) -> None:
    results = await seerr_client.search("Back to the Future")

    bttf_movie = next(r for r in results if r.media_type == MediaType.MOVIE)

    with pytest.warns():
        request = await seerr_client.request.create(bttf_movie, seasons=[1, 2])

    requests = await seerr_client.request.list()

    assert any(r.id == request.id for r in requests)
    assert any(r.media.tmdb_id == bttf_movie.id for r in requests)

    await request.delete()


@pytest.mark.asyncio
async def test_client_search_tv_and_request(seerr_client: SeerrClient) -> None:
    results = await seerr_client.search("Back to the Future")

    bttf_tv = next(r for r in results if r.media_type == MediaType.TV)

    request = await seerr_client.request.create(bttf_tv, seasons=[1, 2])

    requests = await seerr_client.request.list()

    assert any(r.id == request.id for r in requests)
    assert any(r.media.tmdb_id == bttf_tv.id for r in requests)

    await request.delete()
