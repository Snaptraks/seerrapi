import contextlib
from collections.abc import AsyncGenerator
from dataclasses import dataclass

import pytest
import pytest_asyncio

from seerrapi.base import MediaType
from seerrapi.client import SeerrClient
from seerrapi.errors import SeerrIssueNotFoundError
from seerrapi.issue import Issue, IssueComment, IssueCount, IssueType

from . import assert_list_of_instances

TEST_ISSUE: Issue


@dataclass
class Media:
    id: int
    media_type: MediaType


@pytest.fixture
def media() -> Media:
    return Media(id=524, media_type=MediaType.TV)


@pytest_asyncio.fixture
async def issue(seerr_client: SeerrClient, media: Media) -> AsyncGenerator[Issue]:
    issue = await seerr_client.issue.create(
        issue_type=IssueType.OTHER,
        message="pytest message",
        media=media,
        problem_season=1,
        problem_episode=2,
    )
    issue = await issue.comment("pytest comment")

    yield issue

    with contextlib.suppress(SeerrIssueNotFoundError):
        await issue.delete()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def clean_issues(seerr_client: SeerrClient) -> AsyncGenerator[None]:
    issues = await seerr_client.issue.list(filter_="resolved")

    yield

    for issue in issues:
        await issue.delete()


@pytest.mark.asyncio
async def test_issue_list(seerr_client: SeerrClient) -> None:
    issues = await seerr_client.issue.list()

    assert_list_of_instances(issues, Issue)


@pytest.mark.asyncio
async def test_issue_get(seerr_client: SeerrClient, issue: Issue) -> None:
    issue_ = await seerr_client.issue.get(issue.id)

    assert isinstance(issue_, Issue)
    assert issue_.id == issue.id
    assert issue_.issue_type == issue.issue_type


@pytest.mark.asyncio
@pytest.mark.skip
async def test_issue_list_resolved(seerr_client: SeerrClient) -> None:
    issues = await seerr_client.issue.list(filter_="resolved")

    assert_list_of_instances(issues, Issue)


@pytest.mark.asyncio
async def test_issue_count(seerr_client: SeerrClient) -> None:
    issue_count = await seerr_client.issue.count()

    assert isinstance(issue_count, IssueCount)


@pytest.mark.asyncio
async def test_issue_create(
    seerr_client: SeerrClient,
    media: Media,
) -> None:
    issue = await seerr_client.issue.create(
        issue_type=IssueType.OTHER,
        message="pytest message",
        media=media,
        problem_season=1,
        problem_episode=2,
    )

    assert isinstance(issue, Issue)

    await issue.delete()


@pytest.mark.asyncio
async def test_issue_comment(issue: Issue) -> None:
    comment_message = "I am commenting"
    commented_issue = await issue.comment(comment_message)

    assert isinstance(commented_issue, Issue)
    assert any(
        comment.message == comment_message for comment in commented_issue.comments
    )


@pytest.mark.asyncio
async def test_issue_comment_details(issue: Issue) -> None:
    issue_comment = await issue.comments[0].details()

    assert isinstance(issue_comment, IssueComment)


@pytest.mark.asyncio
async def test_issue_comment_update(issue: Issue) -> None:
    comment = issue.comments[0]

    message = "updated_comment"
    updated_comment = await comment.update(message)

    assert isinstance(updated_comment, IssueComment)
    assert updated_comment.message == message


@pytest.mark.asyncio
async def test_issue_comment_delete(seerr_client: SeerrClient, issue: Issue) -> None:
    comment = issue.comments[0]
    await comment.delete()

    updated_issue = await seerr_client.issue.get(issue.id)

    assert len(updated_issue.comments) == len(issue.comments) - 1


@pytest.mark.asyncio
async def test_issue_update(seerr_client: SeerrClient, issue: Issue) -> None:
    updated_issue = await issue.update("resolved")

    assert isinstance(updated_issue, Issue)

    open_issues = await seerr_client.issue.list(filter_="open")
    assert all(open_issue.id != updated_issue.id for open_issue in open_issues)


@pytest.mark.asyncio
async def test_issue_delete(seerr_client: SeerrClient, issue: Issue) -> None:
    await issue.delete()

    with pytest.raises(SeerrIssueNotFoundError):
        await seerr_client.issue.get(issue.id)
