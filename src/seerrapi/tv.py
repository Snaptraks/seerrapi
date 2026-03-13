from __future__ import annotations

from datetime import date
from typing import Any

from pydantic import AliasPath, Field, model_validator

from . import (
    Base,
    Creator,
    Credits,
    ExternalIds,
    Genre,
    Keyword,
    MediaType,
    ProductionCompany,
    ProductionCountry,
    RottenTomatoesRatings,
    SpokenLanguage,
    Stateful,
    WatchProvider,
    _Endpoints,
)
from .http import APIPath
from .request import _MediaInfoBase


class ContentRatings(Base):
    descriptors: list[str]
    iso_3166_1: str = Field(alias="iso_3166_1")
    rating: str


class Episode(Base):
    id: int
    name: str
    air_date: date | None = None
    episode_number: int
    overview: str
    production_code: str
    season_number: int
    show_id: int
    still_path: str | None = None
    vote_average: float
    vote_count: int


class Season(Base):
    id: int
    air_date: date | None = None
    episode_count: int
    episodes: list[Episode] = Field(default_factory=list)
    name: str
    overview: str
    poster_path: str
    season_number: int

    @model_validator(mode="before")
    @classmethod
    def count_episodes(cls, data: Any) -> Any:
        if data.get("episodeCount", None) is None:
            data["episodeCount"] = len(data["episodes"])

        return data


class TVMediaInfo(_MediaInfoBase):
    seasons: list[Season]


class _TVBase(Stateful):
    id: int
    backdrop_path: str | None
    first_air_date: date
    name: str
    origin_country: list[str]
    original_language: str
    original_name: str
    overview: str
    popularity: float
    poster_path: str
    vote_average: float
    vote_count: int


class TVRecommendation(_TVBase):
    genre_ids: list[int]
    media_type: MediaType


class TV(_TVBase):
    content_ratings: list[ContentRatings] = Field(
        validation_alias=AliasPath("contentRatings", "results"),
    )
    created_by: list[Creator]
    credits: Credits
    episode_run_time: list[float]
    external_ids: ExternalIds
    genres: list[Genre]
    homepage: str
    in_production: bool
    keywords: list[Keyword]
    languages: list[str]
    last_air_date: date
    last_episode_to_air: Episode | None = None
    media_info: _MediaInfoBase | None = None
    networks: list[ProductionCompany]
    next_episode_to_air: Episode | None = None
    number_of_episodes: int
    number_of_seasons: int
    production_companies: list[ProductionCompany]
    production_countries: list[ProductionCountry]
    seasons: list[Season]
    spoken_languages: list[SpokenLanguage]
    status: str
    tagline: str
    type: str
    watch_providers: list[WatchProvider]

    async def get_season(self, season_number: int, *, language: str = "en") -> Season:
        return Season.from_data(
            await self.http.request(
                "GET",
                APIPath(
                    "/tv/{tv_id}/season/{season_number}",
                    tv_id=self.id,
                    season_number=season_number,
                ),
                params={"language": language},
            ),
        )

    async def get_recommendations(
        self, *, page: int = 1, language: str = "en",
    ) -> list[TVRecommendation]:
        resp = await self.http.request(
            "GET",
            APIPath("/tv/{tv_id}/recommendations", tv_id=self.id),
            params={"page": page, "language": language},
        )
        return TVRecommendation.from_data_list(resp["results"], http=self.http)

    async def get_similar(
        self, *, page: int = 1, language: str = "en",
    ) -> list[TVRecommendation]:
        resp = await self.http.request(
            "GET",
            APIPath("/tv/{tv_id}/similar", tv_id=self.id),
            params={"page": page, "language": language},
        )
        return TVRecommendation.from_data_list(resp["results"], http=self.http)

    async def get_ratings(self) -> RottenTomatoesRatings:
        # Only Rotten Tomatoes
        return RottenTomatoesRatings.from_data(
            await self.http.request(
                "GET", APIPath("/tv/{tv_id}/ratings", tv_id=self.id),
            ),
        )


class TVEndpoints(_Endpoints):
    async def __call__(self, tv_id: int, *, language: str = "en") -> TV:
        return TV.from_data(
            await self.client.http.request(
                "GET",
                APIPath("/tv/{tv_id}", tv_id=tv_id),
                params={"language": language},
            ),
            http=self.client.http,
        )
