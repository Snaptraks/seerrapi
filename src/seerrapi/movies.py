from __future__ import annotations

from pydantic import AliasPath, Field

from .base import (
    Base,
    Credits,
    Endpoints,
    ExternalIds,
    Genre,
    IMDBRatings,
    Keyword,
    MediaType,
    ProductionCompany,
    ProductionCountry,
    RelatedVideo,
    Release,
    RottenTomatoesRatings,
    SpokenLanguage,
    Stateful,
    WatchProvider,
)
from .http import APIPath
from .request import MediaInfo
from .utils import DateOrEmptyStr


class PartialCollection(Base):
    id: int
    name: str
    poster_path: str
    backdrop_path: str


class Collection(PartialCollection):
    overview: str
    parts: list[CollectionMovie]


class _MovieBase(Stateful):
    id: int
    adult: bool
    backdrop_path: str | None
    media_info: MediaInfo | None = None
    original_language: str
    original_title: str
    overview: str
    popularity: float
    poster_path: str | None
    release_date: DateOrEmptyStr
    title: str
    video: bool
    vote_average: float
    vote_count: int


class CollectionMovie(_MovieBase):
    genre_ids: list[int]
    media_type: MediaType


class MovieRecommendation(_MovieBase):
    genre_ids: list[int]
    media_type: MediaType


class Movie(_MovieBase):
    budget: int
    collection: PartialCollection
    credits: Credits
    external_ids: ExternalIds
    genres: list[Genre]
    homepage: str
    imdb_id: str
    keywords: list[Keyword]
    on_user_watchlist: bool
    production_companies: list[ProductionCompany]
    production_countries: list[ProductionCountry]
    related_videos: list[RelatedVideo]
    releases: list[Release] = Field(validation_alias=AliasPath("releases", "results"))
    revenue: int | None = None
    runtime: int
    spoken_languages: list[SpokenLanguage]
    status: str
    tagline: str
    watch_providers: list[WatchProvider]

    async def get_recommendations(
        self,
        *,
        page: int = 1,
        language: str = "en",
    ) -> list[MovieRecommendation]:
        resp = await self.http.request(
            "GET",
            APIPath("/movie/{movie_id}/recommendations", movie_id=self.id),
            params={"page": page, "language": language},
        )
        return MovieRecommendation.from_data_list(resp["results"], http=self.http)

    async def get_similar(
        self,
        *,
        page: int = 1,
        language: str = "en",
    ) -> list[MovieRecommendation]:
        resp = await self.http.request(
            "GET",
            APIPath("/movie/{movie_id}/similar", movie_id=self.id),
            params={"page": page, "language": language},
        )
        return MovieRecommendation.from_data_list(resp["results"], http=self.http)

    async def get_ratings(self) -> RottenTomatoesRatings:
        # Only Rotten Tomatoes
        return RottenTomatoesRatings.from_data(
            await self.http.request(
                "GET",
                APIPath("/movie/{movie_id}/ratings", movie_id=self.id),
            ),
        )

    async def get_ratings_combined(self) -> tuple[RottenTomatoesRatings, IMDBRatings]:
        resp = await self.http.request(
            "GET",
            APIPath("/movie/{movie_id}/ratingscombined", movie_id=self.id),
        )

        return (
            RottenTomatoesRatings.from_data(resp["rt"]),
            IMDBRatings.from_data(resp["imdb"]),
        )


class MovieEndpoints(Endpoints):
    async def get(self, movie_id: int, *, language: str = "en") -> Movie:
        return Movie.from_data(
            await self.client.http.request(
                "GET",
                APIPath("/movie/{movie_id}", movie_id=movie_id),
                params={"language": language},
            ),
            http=self.client.http,
        )
