from . import Base, Stateful
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
