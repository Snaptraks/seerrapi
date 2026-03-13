import pytest

from seerrapi import IMDBRatings, RottenTomatoesRatings
from seerrapi.client import SeerrClient
from seerrapi.movies import Movie, MovieRecommendation


@pytest.mark.asyncio
async def test_movie(seerr_client: SeerrClient) -> None:
    movie = await seerr_client.movie(105)
    assert isinstance(movie, Movie)


@pytest.mark.asyncio
async def test_movie_get_recommendations(seerr_movie: Movie) -> None:
    recommendations = await seerr_movie.get_recommendations()

    assert isinstance(recommendations, list)
    assert len(recommendations) > 0
    for recommendation in recommendations:
        assert isinstance(recommendation, MovieRecommendation)


@pytest.mark.asyncio
async def test_movie_get_similar(seerr_movie: Movie) -> None:
    recommendations = await seerr_movie.get_similar()

    assert isinstance(recommendations, list)
    assert len(recommendations) > 0
    for recommendation in recommendations:
        assert isinstance(recommendation, MovieRecommendation)


@pytest.mark.asyncio
async def test_movie_get_ratings(seerr_movie: Movie) -> None:
    ratings = await seerr_movie.get_ratings()
    assert isinstance(ratings, RottenTomatoesRatings)


@pytest.mark.asyncio
async def test_movie_get_ratings_combined(seerr_movie: Movie) -> None:
    rt_ratings, imdb_ratings = await seerr_movie.get_ratings_combined()
    assert isinstance(rt_ratings, RottenTomatoesRatings)
    assert isinstance(imdb_ratings, IMDBRatings)
