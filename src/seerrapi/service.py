from . import Base, Stateful, _Endpoints
from .http import APIPath


class ServiceProfile(Base):
    id: int
    name: str


class ServiceRootFolder(Base):
    id: int
    free_space: int
    path: str


class Service(Stateful):
    id: int
    name: str
    is_4k: bool
    is_default: bool
    active_directory: str
    active_profile_id: int
    active_tags: list[str]


class Radarr(Service):
    async def get_profiles(self) -> list[ServiceProfile]:
        resp = await self.http.request(
            "GET", APIPath("/service/radarr/{radarr_id}", radarr_id=self.id)
        )
        return ServiceProfile.from_data_list(resp["profiles"])

    async def get_root_folders(self) -> list[ServiceRootFolder]:
        resp = await self.http.request(
            "GET", APIPath("/service/radarr/{radarr_id}", radarr_id=self.id)
        )
        return ServiceRootFolder.from_data_list(resp["rootFolders"])


class Sonarr(Service):
    async def get_profiles(self) -> list[ServiceProfile]:
        resp = await self.http.request(
            "GET", APIPath("/service/sonarr/{radarr_id}", radarr_id=self.id)
        )
        return ServiceProfile.from_data_list(resp["profiles"])

    async def get_root_folders(self) -> list[ServiceRootFolder]:
        resp = await self.http.request(
            "GET", APIPath("/service/sonarr/{radarr_id}", radarr_id=self.id)
        )
        return ServiceRootFolder.from_data_list(resp["rootFolders"])


class ServiceEndpoints(_Endpoints):
    async def radarr(self) -> list[Radarr]:
        return Radarr.from_data_list(
            await self.client.http.request("GET", APIPath("/service/radarr")),
            http=self.client.http,
        )

    async def sonarr(self) -> list[Sonarr]:
        return Sonarr.from_data_list(
            await self.client.http.request("GET", APIPath("/service/sonarr")),
            http=self.client.http,
        )
