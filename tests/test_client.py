import pytest

from seerrapi.client import SeerrClient
from seerrapi.settings import MainSettings, NetworkSettings

# Settings methods


@pytest.mark.asyncio
async def test_client_get_main_settings(seerr_client: SeerrClient) -> None:
    main_settings = await seerr_client.get_main_settings()
    assert isinstance(main_settings, MainSettings)


@pytest.mark.asyncio
async def test_client_get_network_settings(seerr_client: SeerrClient) -> None:
    network_settings = await seerr_client.get_network_settings()
    assert isinstance(network_settings, NetworkSettings)
