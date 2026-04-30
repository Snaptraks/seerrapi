import pytest

from seerrapi.client import SeerrClient
from seerrapi.issue import Issue

from . import assert_list_of_instances


@pytest.mark.asyncio
async def test_issue_get(seerr_client: SeerrClient) -> None:
    issues = await seerr_client.issue.get()

    assert_list_of_instances(issues, Issue)
