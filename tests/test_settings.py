import pytest
from apischema import deserialize

from seerrapi.settings import DefaultQuotas, MainSettings, Quota


def test_quota() -> None:
    limit, days = 0, 7
    quota = deserialize(Quota, {"quotaLimit": limit, "quotaDays": days})
    assert quota.limit == limit
    assert quota.days == days


def test_default_quotas() -> None:
    data = {
        "movie": {"quotaLimit": 1, "quotaDays": 2},
        "tv": {"quotaLimit": 3},
    }

    quotas = deserialize(DefaultQuotas, data)

    assert quotas.movie.limit == data["movie"]["quotaLimit"]
    assert quotas.movie.days == data["movie"]["quotaDays"]
    assert quotas.tv.limit == data["tv"]["quotaLimit"]
    assert quotas.tv.days is None


@pytest.mark.asyncio
async def test_settings_update(seerr_settings: MainSettings) -> None:
    yt_url = "https://yt.example.com"
    new_settings = await seerr_settings.update(youtube_url=yt_url)

    assert seerr_settings.youtube_url == yt_url
    assert new_settings.youtube_url == yt_url


@pytest.mark.skip
@pytest.mark.asyncio
async def test_settings_regenerate(seerr_settings: MainSettings) -> None:
    new_settings = await seerr_settings.regenerate()

    assert seerr_settings.api_key != new_settings.api_key
