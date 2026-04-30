from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING, Any, Literal

from .base import Endpoints, Stateful
from .http import APIPath
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


class IssueComment(Stateful):
    id: int
    user: User | None = None
    message: str


class Issue(Stateful):
    id: int
    issue_type: IssueType
    media: MediaInfo
    created_by: User
    modified_by: User | None = None
    comments: list[IssueComment]


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

        resp = await self.http.request("GET", APIPath("/issue"))

        return Issue.from_data_list(resp["results"])
