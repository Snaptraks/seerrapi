import pytest

from seerrapi.service import Radarr, ServiceProfile, ServiceRootFolder


@pytest.mark.asyncio
async def test_radarr_get_profiles(seerr_radarr: Radarr) -> None:
    profiles = await seerr_radarr.get_profiles()
    assert isinstance(profiles, list)
    for profile in profiles:
        assert isinstance(profile, ServiceProfile)


@pytest.mark.asyncio
async def test_radarr_get_root_folders(seerr_radarr: Radarr) -> None:
    root_folders = await seerr_radarr.get_root_folders()
    assert isinstance(root_folders, list)
    for profile in root_folders:
        assert isinstance(profile, ServiceRootFolder)


@pytest.mark.asyncio
async def test_sonarr_get_profiles(seerr_sonarr: Radarr) -> None:
    profiles = await seerr_sonarr.get_profiles()
    assert isinstance(profiles, list)
    for profile in profiles:
        assert isinstance(profile, ServiceProfile)


@pytest.mark.asyncio
async def test_sonarr_get_root_folders(seerr_sonarr: Radarr) -> None:
    root_folders = await seerr_sonarr.get_root_folders()
    assert isinstance(root_folders, list)
    for profile in root_folders:
        assert isinstance(profile, ServiceRootFolder)
