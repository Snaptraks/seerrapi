import pytest

from seerrapi.base import Credits
from seerrapi.client import SeerrClient
from seerrapi.person import Person

# Person methods


@pytest.mark.asyncio
async def test_person(seerr_client: SeerrClient) -> None:
    person = await seerr_client.person.get(1)
    assert isinstance(person, Person)


@pytest.mark.asyncio
async def test_person_get_combined_credits(seerr_person: Person) -> None:
    credits_ = await seerr_person.get_combined_credits()
    assert isinstance(credits_, Credits)
