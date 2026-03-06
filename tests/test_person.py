import pytest

from seerrapi import Credits
from seerrapi.person import Person


@pytest.mark.asyncio
async def test_person_get_combined_credits(seerr_person: Person) -> None:
    credits_ = await seerr_person.get_combined_credits()
    assert isinstance(credits_, Credits)
