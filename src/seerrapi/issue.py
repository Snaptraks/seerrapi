from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING, Any, Literal, Self

from pydantic import model_validator

from .base import Base, Endpoints, Stateful
from .http import HTTP, APIPath, client_http_context
from .request import MediaInfo
from .users import User

if TYPE_CHECKING:
    type IssueSort = Literal["added", "modified"]
    type IssueFilter = Literal["all", "open", "resolved"]


class IssueType(IntEnum):
    VIDEO = 1
    AUDIO = 2
    SUBTITLES = 3
    OTHER = 4


class IssueComment(Base):
    id: int
    user: User | None = None
    message: str

    @property
    def http(self) -> HTTP:
        return client_http_context.get()


class Issue(Base):
    id: int
    issue_type: IssueType
    media: MediaInfo
    created_by: User
    modified_by: User | None = None
    comments: list[IssueComment]

    @property
    def http(self) -> HTTP:
        return client_http_context.get()


class IssueEndpoints(Endpoints):
    async def get(
        self,
        *,
        take: int = 20,
        skip: int = 0,
        sort: IssueSort | None = None,
        filter_: IssueFilter | None = None,
        requested_by: int | None = None,
    ) -> list[Issue]:
        params: dict[str, Any] = {"take": take, "skip": skip}
        if filter_:
            params["filter"] = filter_
        if sort:
            params["sort"] = sort
        if requested_by:
            params["requested_by"] = requested_by

        resp = await self.client.http.request("GET", APIPath("/issue"))

        return Issue.from_data_list(resp["results"])
