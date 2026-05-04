import pytest
import pytest_asyncio

from seerrapi.client import SeerrClient
from seerrapi.issue import Issue, IssueComment

from . import assert_list_of_instances


@pytest_asyncio.fixture
async def seerr_issue(seerr_client: SeerrClient) -> Issue:
    issues = await seerr_client.issue.get()

    return issues[0]


@pytest.mark.asyncio
async def test_issue_get(seerr_client: SeerrClient) -> None:
    issues = await seerr_client.issue.get()

    assert_list_of_instances(issues, Issue)


@pytest.mark.asyncio
async def test_issue_get_resolved(seerr_client: SeerrClient) -> None:
    issues = await seerr_client.issue.get(filter_="resolved")

    assert_list_of_instances(issues, Issue)


@pytest.mark.asyncio
async def test_issue_comment_details(seerr_issue: Issue) -> None:
    issue_comment = await seerr_issue.comments[0].details()

    assert isinstance(issue_comment, IssueComment)
