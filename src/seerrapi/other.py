from pydantic import AliasChoices, Field

from .base import Base, Endpoints, Keyword, WatchProviderDetails
from .errors import TMDBKeywordNotFoundError
from .http import APIPath
from .regions import Region


class WatchProviderRegions(Base):
    iso_3166_1: str = Field(alias="iso_3166_1")
    english_name: str = Field(
        validation_alias=AliasChoices("english_name", "englishName"),
    )
    native_name: str = Field(
        validation_alias=AliasChoices("native_name", "nativeName"),
    )


class Certification(Base):
    certification: str
    meaning: str
    order: int


class WatchProvidersEndpoints(Endpoints):
    async def regions(self) -> list[WatchProviderRegions]:
        return WatchProviderRegions.from_data_list(
            await self.http.request("GET", APIPath("/watchproviders/regions"))
        )

    async def movies(self, region: Region) -> list[WatchProviderDetails]:
        return WatchProviderDetails.from_data_list(
            await self.http.request(
                "GET",
                APIPath("/watchproviders/movies"),
                params={"watch_region": region},
            )
        )

    async def tv(self, region: Region) -> list[WatchProviderDetails]:
        return WatchProviderDetails.from_data_list(
            await self.http.request(
                "GET",
                APIPath("/watchproviders/tv"),
                params={"watch_region": region},
            )
        )


class CertificationsEndpoints(Endpoints):
    async def movie(self) -> dict[Region | str, list[Certification]]:
        resp = await self.http.request("GET", APIPath("/certifications/movie"))

        certifications: dict[Region | str, list[Certification]] = {}
        for region, certs in resp["certifications"].items():
            certifications[region] = Certification.from_data_list(certs)

        return certifications

    async def tv(self) -> dict[Region | str, list[Certification]]:
        resp = await self.http.request("GET", APIPath("/certifications/tv"))

        certifications: dict[Region | str, list[Certification]] = {}
        for region, certs in resp["certifications"].items():
            certifications[region] = Certification.from_data_list(certs)

        return certifications


class OtherEndpoints(Endpoints):
    def __init__(self) -> None:
        self.watch_providers = WatchProvidersEndpoints()
        self.certifications = CertificationsEndpoints()

    async def keyword(self, keyword_id: int) -> Keyword:
        resp = await self.http.request(
            "GET", APIPath("/keyword/{keyword_id}", keyword_id=keyword_id)
        )

        if resp is None:
            raise TMDBKeywordNotFoundError(keyword_id)

        return Keyword.from_data(resp)
