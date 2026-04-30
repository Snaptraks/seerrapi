from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from .base import Endpoints, Keyword, Stateful
from .http import APIPath
from .service import Radarr, Sonarr

if TYPE_CHECKING:
    from collections.abc import Sequence

    from .genres import MovieGenre, TVGenre
    from .languages import Language
    from .service import Service, ServiceProfile, ServiceRootFolder
    from .users import User


class OverrideRule(Stateful):
    id: int
    radarr_service_id: int | None
    sonarr_service_id: int | None
    users: str
    genre: str | None
    language: str | None
    keywords: str | None
    profile_id: int
    root_folder: str | None
    tags: str | None
    created_at: datetime
    updated_at: datetime

    async def update(  # noqa: C901, PLR0913
        self,
        *,
        service: Service | None = None,
        users: Sequence[User] | None = None,
        genres: Sequence[MovieGenre | TVGenre] | None = None,
        languages: Sequence[Language] | None = None,
        keywords: Sequence[Keyword] | None = None,
        root_folder: ServiceRootFolder | None = None,
        quality_profile: ServiceProfile | None = None,
        tags: Sequence[str] | None = None,
    ) -> None:
        payload: dict[str, Any] = {}
        if service is not None:
            if isinstance(service, Radarr):
                payload["radarr_service_id"] = service.id
            elif isinstance(service, Sonarr):
                payload["sonarr_service_id"] = service.id
        if users is not None:
            payload["users"] = ",".join(f"{user.id}" for user in users)
        if genres is not None:
            payload["genre"] = ",".join(f"{genre}" for genre in genres)
        if languages is not None:
            payload["language"] = "|".join(language for language in languages)
        if keywords is not None:
            payload["keywords"] = ",".join(f"{keyword.id}" for keyword in keywords)
        if root_folder is not None:
            payload["root_folder"] = root_folder.path
        if quality_profile is not None:
            payload["profile_id"] = quality_profile.id
        if tags is not None:
            payload["tags"] = ",".join(tags)

        await self.http.request(
            "PUT",
            APIPath("/overrideRule/{rule_id}", rule_id=self.id),
            payload=payload,
        )

    async def delete(self) -> None:
        await self.http.request(
            "DELETE", APIPath("/overrideRule/{rule_id}", rule_id=self.id)
        )


class OverrideRuleEndpoints(Endpoints):
    async def get(self) -> list[OverrideRule]:
        return OverrideRule.from_data_list(
            await self.http.request("GET", APIPath("/overrideRule"))
        )

    async def create(  # noqa: C901, PLR0913
        self,
        *,
        service: Service | None = None,
        users: Sequence[User] | None = None,
        genres: Sequence[MovieGenre | TVGenre] | None = None,
        languages: Sequence[Language] | None = None,
        keywords: Sequence[Keyword] | None = None,
        root_folder: ServiceRootFolder | None = None,
        quality_profile: ServiceProfile | None = None,
        tags: Sequence[str] | None = None,
    ) -> OverrideRule:
        payload: dict[str, Any] = {}
        if service is not None:
            if isinstance(service, Radarr):
                payload["radarr_service_id"] = service.id
            elif isinstance(service, Sonarr):
                payload["sonarr_service_id"] = service.id
        if users is not None:
            payload["users"] = ",".join(f"{user.id}" for user in users)
        if genres is not None:
            payload["genre"] = ",".join(f"{genre}" for genre in genres)
        if languages is not None:
            payload["language"] = "|".join(language for language in languages)
        if keywords is not None:
            payload["keywords"] = ",".join(f"{keyword.id}" for keyword in keywords)
        if root_folder is not None:
            payload["root_folder"] = root_folder.path
        if quality_profile is not None:
            payload["profile_id"] = quality_profile.id
        if tags is not None:
            payload["tags"] = ",".join(tags)

        return OverrideRule.from_data(
            await self.http.request("POST", APIPath("/overrideRule"), payload=payload)
        )
