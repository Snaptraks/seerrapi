from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Self, TypedDict, Unpack

from apischema import alias, deserialize

from . import Base
from .http import APIPath

if TYPE_CHECKING:

    class MainSettingsDict(TypedDict, total=False):
        application_title: str
        application_url: str
        cache_images: bool
        default_permissions: int
        default_quotas: DefaultQuotas
        hide_available: bool
        hide_blocklisted: bool
        local_login: bool
        media_server_login: bool
        new_plex_login: bool
        discover_region: str
        streaming_region: str
        original_language: str
        blocklisted_tags: str
        blocklisted_tags_limit: int
        media_server_type: int
        partial_requests_enabled: bool
        enable_special_episodes: bool
        locale: str
        youtube_url: str

    class NetworkSettingsDict(TypedDict, total=False):
        csrf_protection: bool
        force_ipv4_first: bool
        truust_proxy: bool
        proxy: Proxy
        dns_cache: DNSCache
        api_request_timeout: int


@alias(lambda s: f"quota{s.title()}")
@dataclass
class Quota:
    limit: int | None = None
    days: int | None = None


@dataclass
class DefaultQuotas:
    movie: Quota = field(default_factory=Quota)
    tv: Quota = field(default_factory=Quota)


@dataclass
class MainSettings(Base):
    api_key: str
    application_title: str
    application_url: str
    cache_images: bool
    default_permissions: int
    default_quotas: DefaultQuotas
    hide_available: bool
    hide_blocklisted: bool
    local_login: bool
    media_server_login: bool
    new_plex_login: bool
    discover_region: str
    streaming_region: str
    original_language: str
    blocklisted_tags: str
    blocklisted_tags_limit: int
    media_server_type: int
    partial_requests_enabled: bool
    enable_special_episodes: bool
    locale: str
    youtube_url: str

    async def update(self, **payload: Unpack[MainSettingsDict]) -> Self:
        for k, v in payload.items():
            self.__setattr__(k, v)
        path = APIPath("/settings/main")
        await self.http.request("POST", path, payload=payload)  # pyright: ignore[reportArgumentType]

        return self

    async def regenerate(self) -> MainSettings:
        path = APIPath("/settings/main/regenerate")
        resp = await self.http.request("POST", path)

        return deserialize(MainSettings, await resp.json())


@dataclass
class Proxy:
    enabled: bool
    hostname: str
    port: int
    use_ssl: bool
    user: str
    password: str
    bypass_filter: str
    bypass_local_addresses: bool


@dataclass
class DNSCache:
    enabled: bool
    force_min_ttl: int
    force_max_ttl: int


@dataclass
class NetworkSettings(Base):
    csrf_protection: bool
    force_ipv4_first: bool
    trust_proxy: bool
    proxy: Proxy
    dns_cache: DNSCache
    api_request_timeout: int

    async def update(self, **parameters: Unpack[NetworkSettingsDict]) -> Self:
        for k, v in parameters.items():
            self.__setattr__(k, v)
        path = APIPath("/settings/network")
        await self.http.request("POST", path, payload=parameters)  # pyright: ignore[reportArgumentType]

        return self
