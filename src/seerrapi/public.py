from .base import Base, Endpoints
from .http import APIPath


class Status(Base):
    version: str
    commit_tag: str
    update_available: bool
    commits_behind: int
    restart_required: bool


class AppData(Base):
    app_data: bool
    app_data_path: str
    app_data_permissions: bool


class StatusEndpoints(Endpoints):
    async def __call__(self) -> Status:
        return Status.from_data(
            await self.client.http.request("GET", APIPath("/status")),
        )

    async def app_data(self) -> AppData:
        return AppData.from_data(
            await self.client.http.request("GET", APIPath("/status/appdata")),
        )
