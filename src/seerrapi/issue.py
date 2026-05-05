from __future__ import annotations

from datetime import datetime
from enum import IntEnum
from typing import TYPE_CHECKING, Any, Literal

from .base import Base, Endpoints, Stateful
from .errors import SeerrConnectionError, SeerrIssueNotFoundError, SeerrNotFoundError
from .http import APIPath
from .request import MediaInfo
from .users import User

if TYPE_CHECKING:
    from .base import Requestable

    type IssueSort = Literal["added", "modified"]
    type IssueFilter = Literal["all", "open", "resolved"]


class IssueType(IntEnum):
    VIDEO = 1
    AUDIO = 2
    SUBTITLES = 3
    OTHER = 4


class IssueComment(Base, Stateful):
    id: int
    user: User | None = None
    message: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    async def details(self) -> IssueComment:
        return IssueComment.from_data(
            await self.http.request(
                "GET", APIPath("/issueComment/{comment_id}", comment_id=self.id)
            )
        )

    async def update(self, message: str) -> IssueComment:
        resp = await self.http.request(
            "PUT",
            APIPath("/issueComment/{comment_id}", comment_id=self.id),
            payload={"message": message},
        )

        return IssueComment.from_data(resp)

    async def delete(self) -> None:
        await self.http.request(
            "DELETE", APIPath("/issueComment/{comment_id}", comment_id=self.id)
        )


class Issue(Base, Stateful):
    id: int
    issue_type: IssueType
    problem_season: int
    problem_episode: int
    created_at: datetime
    updated_at: datetime
    created_by: User
    media: MediaInfo
    modified_by: User | None = None
    comments: list[IssueComment]

    async def delete(self) -> None:
        try:
            await self.http.request(
                "DELETE", APIPath("/issue/{issue_id}", issue_id=self.id)
            )
        except (SeerrNotFoundError, SeerrConnectionError) as e:
            raise SeerrIssueNotFoundError(e.msg) from e

    async def comment(self, message: str) -> Issue:
        return Issue.from_data(
            await self.http.request(
                "POST",
                APIPath("/issue/{issue_id}/comment", issue_id=self.id),
                payload={"message": message},
            )
        )

    async def update(self, status: Literal["open", "resolved"]) -> Issue:
        return Issue.from_data(
            await self.http.request(
                "POST",
                APIPath("/issue/{issue_id}/{status}", issue_id=self.id, status=status),
            )
        )


class IssueCount(Base):
    total: int
    video: int
    audio: int
    subtitles: int
    others: int
    open: int
    closed: int


class IssueEndpoints(Endpoints):
    async def get(self, issue_id: int) -> Issue:
        try:
            resp = await self.http.request(
                "GET", APIPath("/issue/{issue_id}", issue_id=issue_id)
            )
        except (SeerrNotFoundError, SeerrConnectionError) as e:
            raise SeerrIssueNotFoundError(e.msg) from e

        return Issue.from_data(resp)

    async def list(
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

        resp = await self.http.request("GET", APIPath("/issue"), params=params)

        return Issue.from_data_list(resp["results"])

    async def create(
        self,
        *,
        issue_type: IssueType,
        message: str,
        media: Requestable,
        problem_season: int = 0,
        problem_episode: int = 0,
    ) -> Issue:
        payload = {
            "issue_type": issue_type,
            "message": message,
            "media_id": media.id,
            "problem_season": problem_season,
            "problem_episode": problem_episode,
        }

        return Issue.from_data(
            await self.http.request("POST", APIPath("/issue"), payload=payload)
        )

    async def count(self) -> IssueCount:
        return IssueCount.from_data(
            await self.http.request("GET", APIPath("/issue/count"))
        )
