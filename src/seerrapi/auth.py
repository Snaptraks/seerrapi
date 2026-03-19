from .base import Endpoints, MediaServerType
from .http import APIPath
from .users import User


class AuthEndpoints(Endpoints):
    async def me(self) -> User:
        return User.from_data(
            await self.client.http.request("GET", APIPath("/auth/me"))
        )

    async def plex(self, auth_token: str) -> None:
        resp = await self.client.http._raw_request(
            "POST",
            APIPath("/auth/plex"),
            payload={"auth_token": auth_token},
        )
        self.client.http._cookie_auth = resp.cookies["connect.sid"]

    async def jellyfin(
        self,
        *,
        username: str,
        password: str,
        hostname: str,
        email: str,
    ) -> None:
        payload = {
            "username": username,
            "password": password,
            "hostname": hostname,
            "email": email,
            "server_type": MediaServerType.JELLYFIN,
        }
        resp = await self.client.http._raw_request(
            "POST",
            APIPath("/auth/jellyfin"),
            payload=payload,
        )
        self.client.http._cookie_auth = resp.cookies["connect.sid"]

    async def local(self, *, email: str, password: str) -> None:
        payload = {"email": email, "password": password}
        resp = await self.client.http._raw_request(
            "POST",
            APIPath("/auth/local"),
            payload=payload,
        )
        self.client.http._cookie_auth = resp.cookies["connect.sid"]

    async def logout(self) -> None:
        await self.client.http._raw_request("POST", APIPath("/auth/logout"))
