import pytest

from seerrapi.client import SeerrClient
from seerrapi.errors import SeerrAuthenticationError
from seerrapi.users import User

from .config import PLEX_AUTH_TOKEN


@pytest.mark.asyncio
async def test_client_auth_plex(temp_seerr_client: SeerrClient) -> None:
    await temp_seerr_client.auth.plex(PLEX_AUTH_TOKEN)

    assert temp_seerr_client.http._cookie_auth is not None

    me = await temp_seerr_client.auth.me()
    assert isinstance(me, User)


@pytest.mark.skip
@pytest.mark.asyncio
async def test_client_auth_jellyseerr(temp_seerr_client: SeerrClient) -> None:
    await temp_seerr_client.auth.jellyfin(
        username="notausername",
        password="notreallythepassword",  # noqa: S106
        hostname="http://jellyfin:8096",
        email="me@example.com",
    )

    assert temp_seerr_client.http._cookie_auth is not None
    me = await temp_seerr_client.auth.me()
    assert isinstance(me, User)


@pytest.mark.skip
@pytest.mark.asyncio
async def test_client_auth_local(temp_seerr_client: SeerrClient) -> None:
    await temp_seerr_client.auth.local(
        email="me@example.com",
        password="notreallythepassword",  # noqa: S106
    )

    assert temp_seerr_client.http._cookie_auth is not None
    me = await temp_seerr_client.auth.me()
    assert isinstance(me, User)


@pytest.mark.asyncio
async def test_client_logout(temp_seerr_client: SeerrClient) -> None:
    await temp_seerr_client.auth.plex(PLEX_AUTH_TOKEN)
    await temp_seerr_client.auth.logout()

    with pytest.raises(SeerrAuthenticationError):
        await temp_seerr_client.auth.me()
