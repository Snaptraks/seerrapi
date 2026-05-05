import pytest

from seerrapi.base import Keyword, WatchProviderDetails
from seerrapi.client import SeerrClient
from seerrapi.errors import TMDBKeywordNotFoundError
from seerrapi.other import Certification, WatchProviderRegions
from seerrapi.regions import Region

from . import assert_list_of_instances


@pytest.mark.asyncio
async def test_other_keyword_id(seerr_client: SeerrClient) -> None:
    keyword = await seerr_client.other.keyword(207317)

    assert isinstance(keyword, Keyword)
    assert keyword.name == "christmas"


@pytest.mark.asyncio
async def test_other_keyword_not_found(seerr_client: SeerrClient) -> None:
    with pytest.raises(TMDBKeywordNotFoundError):
        await seerr_client.other.keyword(1)


@pytest.mark.asyncio
async def test_other_watch_providers_regions(seerr_client: SeerrClient) -> None:
    regions = await seerr_client.other.watch_providers.regions()

    assert_list_of_instances(regions, WatchProviderRegions)


@pytest.mark.asyncio
async def test_other_watch_providers_movies(seerr_client: SeerrClient) -> None:
    providers = await seerr_client.other.watch_providers.movies(Region.CANADA)

    assert_list_of_instances(providers, WatchProviderDetails)


@pytest.mark.asyncio
async def test_other_watch_providers_tv(seerr_client: SeerrClient) -> None:
    providers = await seerr_client.other.watch_providers.tv(Region.CANADA)

    assert_list_of_instances(providers, WatchProviderDetails)


@pytest.mark.asyncio
async def test_other_watch_certification_movie(seerr_client: SeerrClient) -> None:
    certifications = await seerr_client.other.certifications.movie()

    assert isinstance(certifications, dict)
    for certs in certifications.values():
        assert_list_of_instances(certs, Certification)


@pytest.mark.asyncio
async def test_other_watch_certification_tv(seerr_client: SeerrClient) -> None:
    certifications = await seerr_client.other.certifications.tv()

    assert isinstance(certifications, dict)
    for certs in certifications.values():
        assert_list_of_instances(certs, Certification)
