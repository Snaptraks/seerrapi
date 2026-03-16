from __future__ import annotations

from datetime import datetime
from enum import IntEnum, StrEnum
from typing import TYPE_CHECKING, Any, Self

from pydantic import AliasChoices, AliasGenerator, BaseModel, ConfigDict, Field

from .utils import to_camel_case

if TYPE_CHECKING:
    from .client import SeerrClient
    from .http import HTTP


_model_config = ConfigDict(
    alias_generator=AliasGenerator(
        validation_alias=to_camel_case,
        serialization_alias=to_camel_case,
    ),
)


class _Endpoints:
    def __init__(self, client: SeerrClient) -> None:
        self.client = client


class Base(BaseModel):
    model_config = _model_config

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> Self:
        return cls.model_validate(data, by_alias=True)

    @classmethod
    def from_data_list(cls, data: list[dict[str, Any]]) -> list[Self]:
        return [cls.model_validate(d, by_alias=True) for d in data]


class Stateful(BaseModel):
    model_config = _model_config

    @property
    def http(self) -> HTTP:
        return self._http

    @http.setter
    def http(self, value: HTTP) -> None:
        self._http = value

    @classmethod
    def from_data(cls, data: dict[str, Any], *, http: HTTP) -> Self:
        obj = cls.model_validate(data, by_alias=True)
        obj.http = http

        return obj

    @classmethod
    def from_data_list(cls, data: list[dict[str, Any]], *, http: HTTP) -> list[Self]:
        objs = [cls.model_validate(d, by_alias=True) for d in data]
        for obj in objs:
            obj.http = http

        return objs


class MediaServerType(IntEnum):
    PLEX = 1
    JELLYFIN = 2
    EMBY = 3
    NOT_CONFIGURED = 4


class MediaType(StrEnum):
    MOVIE = "movie"
    TV = "tv"
    PERSON = "person"


class Genre(Base):
    id: int
    name: str


class Keyword(Base):
    id: int
    name: str


class VideoType(StrEnum):
    CLIP = "Clip"
    TEASER = "Teaser"
    TRAILER = "Trailer"
    FEATURETTE = "Featurette"
    OPENING_CREDITS = "Opening Credits"
    BEHIND_THE_SCENES = "Behind the Scenes"
    BLOOPERS = "Bloopers"


class RelatedVideo(Base):
    site: str
    key: str
    name: str
    size: int
    type: VideoType
    url: str


class ProductionCompany(Base):
    id: int
    description: str | None = None
    headquarters: str | None = None
    homepage: str | None = None
    logo_path: str | None = None
    name: str
    origin_country: str | None = None


class ProductionCountry(Base):
    name: str
    iso_3166_1: str = Field(alias="iso_3166_1")


class ReleaseDate(Base):
    certification: str
    note: str
    type: int
    descriptors: list[str]
    iso_639_1: str = Field(alias="iso_639_1")
    release_date: datetime = Field(alias="release_date")


class Release(Base):
    iso_3166_1: str = Field(alias="iso_3166_1")
    release_dates: list[ReleaseDate] = Field(alias="release_dates")
    rating: str | None = None


class SpokenLanguage(Base):
    name: str
    english_name: str = Field(
        validation_alias=AliasChoices("english_name", "englishName"),
    )
    iso_639_1: str = Field(alias="iso_639_1")


class Gender(IntEnum):
    NOT_SPECIFIED = 0
    FEMALE = 1
    MALE = 2
    NON_BINARY = 3


class Cast(Base):
    id: int
    cast_id: int | None = None
    character: str
    credit_id: str
    gender: Gender | None = None
    name: str | None = None
    order: int | None = None
    profile_path: str | None = None


class Crew(Base):
    id: int
    credit_id: str
    gender: Gender | None = None
    name: str | None = None
    job: str
    department: str
    profile_path: str | None = None


class Credits(Base):
    cast: list[Cast]
    crew: list[Crew]


class ExternalIds(Base):
    facebook: str | None = Field(default=None)
    freebase: str | None = Field(default=None)
    freebase_m: str | None = Field(default=None)
    imdb: str | None = Field(default=None)
    instagram: str | None = Field(default=None)
    tvdb: str | None = Field(default=None)
    tvrage: str | None = Field(default=None)
    twitter: str | None = Field(default=None)


class WatchProviderDetails(Base):
    display_priority: int
    logo_path: str
    id: int
    name: str


class WatchProvider(Base):
    link: str
    buy: list[WatchProviderDetails]
    flatrate: list[WatchProviderDetails]
    iso_3166_1: str = Field(alias="iso_3166_1")


class AudienceRating(StrEnum):
    SPILLED = "Spilled"
    UPRIGHT = "Upright"


class CriticsRating(StrEnum):
    ROTTEN = "Rotten"
    FRESH = "Fresh"
    CERTIFIED_FRESH = "Certified Fresh"


class Ratings(Base):
    title: str
    url: str
    critics_score: float


class RottenTomatoesRatings(Ratings):
    year: int
    audience_score: int
    audience_rating: AudienceRating
    critics_rating: CriticsRating


class IMDBRatings(Ratings):
    critics_score_count: int


class Creator(Base):
    id: int
    credit_id: str = Field(alias="credit_id")
    name: str
    original_name: str = Field(alias="original_name")
    gender: int
    profile_path: str | None = Field(default=None, alias="profile_path")


class WatchlistItem(Base):
    id: int
    media_type: MediaType
    rating_key: str
    title: str
    tmdb_id: int
