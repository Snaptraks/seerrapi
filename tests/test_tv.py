import pytest

from seerrapi.base import RottenTomatoesRatings
from seerrapi.client import SeerrClient
from seerrapi.tv import TV, Season, TVRecommendation

# TV methods


@pytest.mark.asyncio
async def test_tv(seerr_client: SeerrClient) -> None:
    tv = await seerr_client.tv(96580)
    assert isinstance(tv, TV)


@pytest.mark.asyncio
async def test_tv_get_season(seerr_tv: TV) -> None:
    season = await seerr_tv.get_season(1)
    assert isinstance(season, Season)


@pytest.mark.asyncio
async def test_tv_get_recommendations(seerr_tv: TV) -> None:
    recommendations = await seerr_tv.get_recommendations()

    assert isinstance(recommendations, list)
    assert len(recommendations) > 0
    for recommendation in recommendations:
        assert isinstance(recommendation, TVRecommendation)


@pytest.mark.asyncio
async def test_tv_get_similar(seerr_tv: TV) -> None:
    recommendations = await seerr_tv.get_similar()

    assert isinstance(recommendations, list)
    assert len(recommendations) > 0
    for recommendation in recommendations:
        assert isinstance(recommendation, TVRecommendation)


@pytest.mark.asyncio
async def test_tv_get_ratings(seerr_tv: TV) -> None:
    ratings = await seerr_tv.get_ratings()
    assert isinstance(ratings, RottenTomatoesRatings)
