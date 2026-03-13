from __future__ import annotations

from dataclasses import dataclass
from importlib import metadata
from json import JSONDecodeError
from typing import TYPE_CHECKING, Any, Literal
from urllib.parse import quote as _uriquote

import httpx

from .errors import SeerrAuthenticationError, SeerrConnectionError
from .utils import to_camel_case_dict

if TYPE_CHECKING:
    type Method = Literal["GET", "POST", "PUT", "DELETE"]


VERSION = metadata.version(__package__)  # pyright: ignore[reportArgumentType]


class APIPath:
    def __init__(self, path: str, **parameters: Any) -> None:
        parsed_path = path.format_map(
            {
                k: _uriquote(v) if isinstance(v, str) else v
                for k, v in parameters.items()
            }
        )
        self._path = f"/api/v1{parsed_path}"

    def __str__(self) -> str:
        return self._path


@dataclass
class HTTP:
    host: str
    _api_key: str | None = None
    _cookie_auth: str | None = None

    async def request(
        self,
        method: Method,
        path: APIPath,
        *,
        payload: dict | None = None,
        params: dict | None = None,
    ) -> Any:

        resp = await self._raw_request(method, path, payload=payload, params=params)

        try:
            return resp.json()
        except JSONDecodeError:
            return None

    async def _raw_request(
        self,
        method: Method,
        path: APIPath,
        *,
        payload: dict | None = None,
        params: dict | None = None,
    ) -> httpx.Response:
        headers = {
            "User-Agent": f"SeerrAPI/{VERSION}",
            "Accept": "application/json",
        }
        cookies: dict[str, str] = {}
        if self._api_key is not None:
            headers["X-Api-Key"] = self._api_key

        if self._cookie_auth is not None:
            cookies["connect.sid"] = self._cookie_auth

        url = f"{self.host}{path}"
        if payload is not None:
            payload = to_camel_case_dict(payload)

        if params is not None:
            params = to_camel_case_dict(params)
            params = {
                k: _uriquote(v) if isinstance(v, str) else v for k, v in params.items()
            }

        try:
            async with httpx.AsyncClient(headers=headers, cookies=cookies) as session:
                resp = await session.request(method, url, json=payload, params=params)
        except (httpx.ConnectError, httpx.RequestError) as e:
            msg = "Error occured while connecting to Seerr"
            raise SeerrConnectionError(msg) from e

        if resp.status_code == 403:  # noqa: PLR2004
            msg = "Client is not authenticated"
            raise SeerrAuthenticationError(msg)

        if resp.status_code >= 400:  # noqa: PLR2004
            content_type = resp.headers.get("Content-Type", "")
            text = resp.text
            msg = "Unexpected response from Seerr"
            raise SeerrConnectionError(
                msg,
                {
                    "Content-Type": content_type,
                    "response": text,
                    "status_code": resp.status_code,
                },
            )

        return resp
