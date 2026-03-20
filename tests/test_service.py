import pytest

from seerrapi.client import SeerrClient
from seerrapi.service import Radarr, ServiceProfile, ServiceRootFolder, Sonarr

from . import assert_list_of_instances


@pytest.mark.asyncio
async def test_service_radarr(seerr_client: SeerrClient) -> None:
    services = await seerr_client.service.radarr()

    assert assert_list_of_instances(services, Radarr)


@pytest.mark.asyncio
async def test_service_sonarr(seerr_client: SeerrClient) -> None:
    services = await seerr_client.service.sonarr()

    assert assert_list_of_instances(services, Sonarr)


@pytest.mark.asyncio
async def test_radarr_get_profiles(seerr_radarr: Radarr) -> None:
    profiles = await seerr_radarr.get_profiles()

    assert assert_list_of_instances(profiles, ServiceProfile)


@pytest.mark.asyncio
async def test_radarr_get_root_folders(seerr_radarr: Radarr) -> None:
    root_folders = await seerr_radarr.get_root_folders()

    assert assert_list_of_instances(root_folders, ServiceRootFolder)


@pytest.mark.asyncio
async def test_sonarr_get_profiles(seerr_sonarr: Sonarr) -> None:
    profiles = await seerr_sonarr.get_profiles()

    assert assert_list_of_instances(profiles, ServiceProfile)


@pytest.mark.asyncio
async def test_sonarr_get_root_folders(seerr_sonarr: Sonarr) -> None:
    root_folders = await seerr_sonarr.get_root_folders()

    assert assert_list_of_instances(root_folders, ServiceRootFolder)
