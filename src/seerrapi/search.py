from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING, Annotated, Literal, Protocol

from pydantic import Field

from . import (
    Base,
    Genre,
    Keyword,
    MediaType,
    ProductionCompany,
    WatchlistItem,
    WatchProviderDetails,
    _Endpoints,
)
from .errors import SeerrSearchError
from .http import APIPath
from .request import MediaInfo
from .utils import DateOrEmptyStr

if TYPE_CHECKING:
    from collections.abc import Sequence
    from datetime import datetime

    from seerrapi.client import SeerrClient

    from .languages import Language
    from .regions import Region

    class HasID(Protocol):
        id: int


def _validate_media_type(media_data: dict) -> MovieResult | TVResult | PersonResult:
    media_conv: dict[str, type[MovieResult | TVResult | PersonResult]] = {
        "movie": MovieResult,
        "tv": TVResult,
        "person": PersonResult,
    }
    return media_conv[media_data["mediaType"]].from_data(media_data)


def _join_ids(objs: Sequence[HasID], sep: Literal[",", "|"] = ",") -> str:
    return sep.join(f"{obj.id}" for obj in objs)


class CertificationMode(StrEnum):
    EXACT = "exact"
    RANGE = "range"


class MovieResult(Base):
    id: int
    media_type: Literal[MediaType.MOVIE]
    popularity: float
    poster_path: str | None
    backdrop_path: str | None
    vote_count: int
    vote_average: float
    genre_ids: list[int]
    original_language: str
    title: str
    original_title: str | None = None
    release_date: DateOrEmptyStr
    adult: bool
    video: bool
    media_info: MediaInfo | None = None


class TVResult(Base):
    id: int
    media_type: Literal[MediaType.TV]
    popularity: float
    poster_path: str | None
    backdrop_path: str | None
    vote_count: int
    vote_average: float
    genre_ids: list[int]
    overview: str
    original_language: str
    name: str
    original_name: str | None = None
    origin_country: list[str]
    first_air_date: DateOrEmptyStr
    media_info: MediaInfo | None = None


class PersonResult(Base):
    id: int
    profile_path: str | None
    adult: bool
    media_type: Literal[MediaType.PERSON]
    known_for: list[
        Annotated[MovieResult | TVResult, Field(discriminator="media_type")]
    ]


class GenreSlider(Genre):
    backdrops: list[str]


class SearchEndpoints(_Endpoints):
    async def __call__(
        self, query: str, *, page: int = 1, language: str = "en"
    ) -> list[MovieResult | TVResult | PersonResult]:
        params = {"query": query, "page": page, "language": language}
        resp = await self.client.http.request("GET", APIPath("/search"), params=params)

        return [_validate_media_type(media) for media in resp["results"]]

    async def keyword(self, query: str, *, page: int = 1) -> list[Keyword]:
        params = {"query": query, "page": page}
        resp = await self.client.http.request(
            "GET", APIPath("/search/keyword"), params=params
        )

        return Keyword.from_data_list(resp["results"])

    async def company(self, query: str, *, page: int = 1) -> list[ProductionCompany]:
        params = {"query": query, "page": page}
        resp = await self.client.http.request(
            "GET", APIPath("/search/company"), params=params
        )

        return ProductionCompany.from_data_list(resp["results"])


class DiscoverMovies(_Endpoints):
    async def __call__(  # noqa: C901, PLR0912, PLR0913
        self,
        *,
        page: int = 1,
        language: str = "en",
        genre: Genre | None = None,
        studio: ProductionCompany | None = None,
        keywords: Sequence[Keyword] | None = None,
        exclude_keywords: Sequence[Keyword] | None = None,
        sort_by: str | None = None,
        primary_release_date_gte: datetime | None = None,
        primary_release_date_lte: datetime | None = None,
        with_runtime_gte: datetime | None = None,
        with_runtime_lte: datetime | None = None,
        vote_average_gte: float | None = None,
        vote_average_lte: float | None = None,
        vote_count_gte: int | None = None,
        vote_count_lte: int | None = None,
        watch_region: Region | None = None,
        watch_providers: WatchProviderDetails | None = None,
        certification: str | None = None,
        certification_gte: str | None = None,
        certification_lte: str | None = None,
        certification_country: str | None = None,
        certification_mode: CertificationMode | None = None,
    ) -> list[MovieResult]:
        if certification_mode is CertificationMode.EXACT and (
            certification_gte is not None or certification_lte is not None
        ):
            msg = "Cannot use certification range in EXACT mode."
            raise SeerrSearchError(msg)

        if certification_mode is CertificationMode.RANGE and certification is not None:
            msg = "Cannot specify certification in RANGE mode."
            raise SeerrSearchError(msg)

        params = {
            "page": page,
            "language": language,
        }
        if genre:
            params["genre"] = genre.id
        if studio:
            params["studio"] = studio.id
        if keywords:
            params["keywords"] = _join_ids(keywords)
        if exclude_keywords:
            params["exclude_keywords"] = _join_ids(exclude_keywords)
        if sort_by:
            params["sort_by"] = sort_by
        if primary_release_date_gte:
            params["primary_release_date_gte"] = primary_release_date_gte
        if primary_release_date_lte:
            params["primary_release_date_lte"] = primary_release_date_lte
        if with_runtime_gte:
            params["with_runtime_gte"] = with_runtime_gte
        if with_runtime_lte:
            params["with_runtime_lte"] = with_runtime_lte
        if vote_average_gte:
            params["vote_average_gte"] = vote_average_gte
        if vote_average_lte:
            params["vote_average_lte"] = vote_average_lte
        if vote_count_gte:
            params["vote_count_gte"] = vote_count_gte
        if vote_count_lte:
            params["vote_count_lte"] = vote_count_lte
        if watch_region:
            params["watch_region"] = watch_region
        if watch_providers:
            params["watch_providers"] = watch_providers.id
        if certification_country:
            params["certification_country"] = certification_country

        match certification:
            case CertificationMode.RANGE:
                if certification_gte:
                    params["certification_gte"] = certification_gte
                if certification_lte:
                    params["certification_lte"] = certification_lte
            case CertificationMode.EXACT:
                if certification:
                    params["certification"] = certification

        resp = await self.client.http.request(
            "GET", APIPath("/discover/movies"), params=params
        )

        return MovieResult.from_data_list(resp["results"])

    async def genre(
        self, genre: Genre, *, page: int = 1, language: str = "en"
    ) -> list[MovieResult]:
        params = {"page": page, "language": language}
        resp = await self.client.http.request(
            "GET",
            APIPath("/discover/movies/genre/{genre_id}", genre_id=genre.id),
            params=params,
        )

        return MovieResult.from_data_list(resp["results"])

    async def language(
        self, original_language: Language, *, page: int = 1, language: str = "en"
    ) -> list[MovieResult]:
        params = {"page": page, "language": language}
        resp = await self.client.http.request(
            "GET",
            APIPath(
                "/discover/movies/language/{original_language}",
                original_language=original_language,
            ),
            params=params,
        )

        return MovieResult.from_data_list(resp["results"])

    async def studio(
        self, studio: ProductionCompany, *, page: int = 1, language: str = "en"
    ) -> list[MovieResult]:
        params = {"page": page, "language": language}
        resp = await self.client.http.request(
            "GET",
            APIPath(
                "/discover/movies/studio/{studio_id}",
                studio_id=studio.id,
            ),
            params=params,
        )

        return MovieResult.from_data_list(resp["results"])

    async def upcoming(
        self, *, page: int = 1, language: str = "en"
    ) -> list[MovieResult]:
        params = {"page": page, "language": language}
        resp = await self.client.http.request(
            "GET",
            APIPath(
                "/discover/movies/upcoming",
            ),
            params=params,
        )

        return MovieResult.from_data_list(resp["results"])


class DiscoverTV(_Endpoints):
    async def __call__(  # noqa: C901, PLR0912, PLR0913, PLR0915
        self,
        *,
        page: int = 1,
        language: str = "en",
        genre: Genre | None = None,
        network: ProductionCompany | None = None,
        keywords: Sequence[Keyword] | None = None,
        exclude_keywords: Sequence[Keyword] | None = None,
        sort_by: str | None = None,
        first_air_date_gte: datetime | None = None,
        first_air_date_lte: datetime | None = None,
        with_runtime_gte: datetime | None = None,
        with_runtime_lte: datetime | None = None,
        vote_average_gte: float | None = None,
        vote_average_lte: float | None = None,
        vote_count_gte: int | None = None,
        vote_count_lte: int | None = None,
        watch_region: Region | None = None,
        watch_providers: WatchProviderDetails | None = None,
        status: str | None = None,
        certification: str | None = None,
        certification_gte: str | None = None,
        certification_lte: str | None = None,
        certification_country: str | None = None,
        certification_mode: CertificationMode | None = None,
    ) -> list[TVResult]:
        if certification_mode is CertificationMode.EXACT and (
            certification_gte is not None or certification_lte is not None
        ):
            msg = "Cannot use certification range in EXACT mode."
            raise SeerrSearchError(msg)

        if certification_mode is CertificationMode.RANGE and certification is not None:
            msg = "Cannot specify certification in RANGE mode."
            raise SeerrSearchError(msg)

        params = {
            "page": page,
            "language": language,
        }
        if genre:
            params["genre"] = genre.id
        if network:
            params["network"] = network.id
        if keywords:
            params["keywords"] = _join_ids(keywords)
        if exclude_keywords:
            params["exclude_keywords"] = _join_ids(exclude_keywords)
        if sort_by:
            params["sort_by"] = sort_by
        if first_air_date_gte:
            params["first_air_date_gte"] = first_air_date_gte
        if first_air_date_lte:
            params["first_air_date_lte"] = first_air_date_lte
        if with_runtime_gte:
            params["with_runtime_gte"] = with_runtime_gte
        if with_runtime_lte:
            params["with_runtime_lte"] = with_runtime_lte
        if vote_average_gte:
            params["vote_average_gte"] = vote_average_gte
        if vote_average_lte:
            params["vote_average_lte"] = vote_average_lte
        if vote_count_gte:
            params["vote_count_gte"] = vote_count_gte
        if vote_count_lte:
            params["vote_count_lte"] = vote_count_lte
        if watch_region:
            params["watch_region"] = watch_region
        if watch_providers:
            params["watch_providers"] = watch_providers.id
        if status:
            params["status"] = status
        if certification_country:
            params["certification_country"] = certification_country

        match certification:
            case CertificationMode.RANGE:
                if certification_gte:
                    params["certification_gte"] = certification_gte
                if certification_lte:
                    params["certification_lte"] = certification_lte
            case CertificationMode.EXACT:
                if certification:
                    params["certification"] = certification

        resp = await self.client.http.request(
            "GET", APIPath("/discover/tv"), params=params
        )

        return TVResult.from_data_list(resp["results"])

    async def genre(
        self, genre: Genre, *, page: int = 1, language: str = "en"
    ) -> list[TVResult]:
        params = {"page": page, "language": language}
        resp = await self.client.http.request(
            "GET",
            APIPath("/discover/tv/genre/{genre_id}", genre_id=genre.id),
            params=params,
        )

        return TVResult.from_data_list(resp["results"])

    async def language(
        self, original_language: Language, *, page: int = 1, language: str = "en"
    ) -> list[TVResult]:
        params = {"page": page, "language": language}
        resp = await self.client.http.request(
            "GET",
            APIPath(
                "/discover/tv/language/{original_language}",
                original_language=original_language,
            ),
            params=params,
        )

        return TVResult.from_data_list(resp["results"])

    async def network(
        self, network: ProductionCompany, *, page: int = 1, language: str = "en"
    ) -> list[TVResult]:
        params = {"page": page, "language": language}
        resp = await self.client.http.request(
            "GET",
            APIPath(
                "/discover/tv/network/{network_id}",
                network_id=network.id,
            ),
            params=params,
        )

        return TVResult.from_data_list(resp["results"])

    async def upcoming(self, page: int = 1, language: str = "en") -> list[TVResult]:
        params = {"page": page, "language": language}
        resp = await self.client.http.request(
            "GET",
            APIPath(
                "/discover/tv/upcoming",
            ),
            params=params,
        )

        return TVResult.from_data_list(resp["results"])


class DiscoverEndpoints(_Endpoints):
    def __init__(self, client: SeerrClient) -> None:
        super().__init__(client)
        self.movies = DiscoverMovies(client)
        self.tv = DiscoverTV(client)

    async def trending(
        self, *, page: int = 1, language: str = "en"
    ) -> list[MovieResult | TVResult]:
        params = {"page": page, "language": language}
        resp = await self.client.http.request(
            "GET", APIPath("/discover/trending"), params=params
        )

        return [_validate_media_type(media) for media in resp["results"]]  # pyright: ignore[reportReturnType]

    # /discover/keyword/{keywordId}/movies -> use /discover/movies?keywords=... instead

    async def genre_slider(
        self,
        media_type: Literal[MediaType.MOVIE, MediaType.TV],
        *,
        language: str = "en",
    ) -> list[GenreSlider]:
        params = {"language": language}
        resp = await self.client.http.request(
            "GET",
            APIPath(f"/discover/genreslider/{media_type}"),
            params=params,
        )

        return GenreSlider.from_data_list(resp)

    async def watchlist(self, *, page: int = 1) -> list[WatchlistItem]:
        params = {"page": page}
        resp = await self.client.http.request(
            "GET", APIPath("/discover/watchlist"), params=params
        )

        return WatchlistItem.from_data_list(resp["results"])
