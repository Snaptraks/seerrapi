from __future__ import annotations

from typing import TYPE_CHECKING, Self, TypedDict, Unpack

from pydantic import Field

from . import Base, Stateful
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


class Quota(Base):
    limit: int | None = Field(default=None, alias="quotaLimit")
    days: int | None = Field(default=None, alias="quotaDays")


class DefaultQuotas(Base):
    movie: Quota = Field(default_factory=Quota)
    tv: Quota = Field(default_factory=Quota)


class MainSettings(Stateful):
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

    async def update(self, **payload: Unpack[MainSettingsDict]) -> MainSettings:
        return MainSettings.from_data(
            await self.http.request("POST", APIPath("/settings/main"), payload=payload),  # pyright: ignore[reportArgumentType]
            http=self.http,
        )

    async def regenerate(self) -> MainSettings:
        path = APIPath("/settings/main/regenerate")
        resp = await self.http.request("POST", path)

        return MainSettings.from_data(resp, http=self.http)


class Proxy(Base):
    enabled: bool
    hostname: str
    port: int
    use_ssl: bool
    user: str
    password: str
    bypass_filter: str
    bypass_local_addresses: bool


class DNSCache(Base):
    enabled: bool
    force_min_ttl: int
    force_max_ttl: int


class NetworkSettings(Stateful):
    csrf_protection: bool
    force_ipv4_first: bool
    trust_proxy: bool
    proxy: Proxy
    dns_cache: DNSCache
    api_request_timeout: int

    async def update(self, **payload: Unpack[NetworkSettingsDict]) -> NetworkSettings:
        return NetworkSettings.from_data(
            await self.http.request("POST", APIPath("/settings/main"), payload=payload),  # pyright: ignore[reportArgumentType]
            http=self.http,
        )
