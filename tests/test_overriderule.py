import pytest

from seerrapi.base import Keyword
from seerrapi.client import SeerrClient
from seerrapi.genres import MovieGenre
from seerrapi.languages import Language
from seerrapi.overriderule import OverrideRule
from seerrapi.service import Radarr

from . import assert_list_of_instances


@pytest.mark.asyncio
async def test_override_rule_get(seerr_client: SeerrClient) -> None:
    override_rules = await seerr_client.overriderule.get()
    assert_list_of_instances(override_rules, OverrideRule)


@pytest.mark.asyncio
async def test_override_rule_create(
    seerr_client: SeerrClient, seerr_radarr: Radarr, seerr_keyword: Keyword
) -> None:
    root_folders = await seerr_radarr.get_root_folders()
    quality_profiles = await seerr_radarr.get_profiles()
    override_rule = await seerr_client.overriderule.create(
        service=seerr_radarr,
        users=[await seerr_client.me()],
        genres=[MovieGenre.ACTION, MovieGenre.HISTORY],
        languages=[Language.ENGLISH, Language.FRENCH],
        keywords=[seerr_keyword],
        root_folder=root_folders[0],
        quality_profile=quality_profiles[0],
    )

    assert isinstance(override_rule, OverrideRule)


@pytest.mark.asyncio
async def test_override_rule_update(seerr_client: SeerrClient) -> None:
    override_rule = (await seerr_client.overriderule.get())[-1]

    await override_rule.update(genres=[MovieGenre.ROMANCE])

    updated_override_rule = next(
        r for r in await seerr_client.overriderule.get() if r.id == override_rule.id
    )

    assert override_rule.genre != updated_override_rule.genre


@pytest.mark.asyncio
async def test_override_rule_delete(seerr_client: SeerrClient) -> None:
    override_rules = await seerr_client.overriderule.get()

    override_rule = override_rules[-1]

    await override_rule.delete()

    new_override_rules = await seerr_client.overriderule.get()

    assert len(override_rules) == len(new_override_rules) + 1
