import pytest

from seerrapi.client import SeerrClient
from seerrapi.public import AppData, Status


@pytest.mark.asyncio
async def test_client_get_status(seerr_client: SeerrClient) -> None:
    status = await seerr_client.status.get()
    assert isinstance(status, Status)


@pytest.mark.asyncio
async def test_client_get_app_data(seerr_client: SeerrClient) -> None:
    app_data = await seerr_client.status.app_data()
    assert isinstance(app_data, AppData)
