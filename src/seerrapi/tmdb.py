from typing import Literal

from .base import (
    Endpoints,
    Genre,
    MediaType,
    ProductionCompany,
    ProductionCountry,
    SpokenLanguage,
)
from .http import APIPath


class TMDBEndpoints(Endpoints):
    async def regions(self) -> list[ProductionCountry]:
        resp = await self.client.http.request("GET", APIPath("/regions"))

        return ProductionCountry.from_data_list(resp)

    async def languages(self) -> list[SpokenLanguage]:
        resp = await self.client.http.request("GET", APIPath("/languages"))

        return SpokenLanguage.from_data_list(resp)

    async def studio(self, studio_id: int) -> ProductionCompany:
        resp = await self.client.http.request(
            "GET", APIPath("/studio/{studio_id}", studio_id=studio_id)
        )

        return ProductionCompany.from_data(resp)

    async def network(self, network_id: int) -> ProductionCompany:
        resp = await self.client.http.request(
            "GET", APIPath("/studio/{network_id}", network_id=network_id)
        )

        return ProductionCompany.from_data(resp)

    async def genres(
        self, media_type: Literal[MediaType.MOVIE, MediaType.TV]
    ) -> list[Genre]:
        resp = await self.client.http.request(
            "GET", APIPath("/genres/{media_type}", media_type=media_type)
        )

        return Genre.from_data_list(resp)

    async def backdrops(self) -> list[str]:
        return await self.client.http.request("GET", APIPath("/backdrops"))
