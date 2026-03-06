from datetime import date

from . import Credits, Gender, Stateful
from .http import APIPath


class Person(Stateful):
    id: int
    name: str
    birthday: date
    deathdat: date | None = None
    known_for_department: str
    also_known_as: list[str]
    gender: Gender
    biography: str
    popularity: float
    place_of_birth: str
    profile_path: str
    adult: bool
    imdb_id: str
    homepage: str | None

    async def get_combined_credits(self, *, language: str = "en") -> Credits:
        return Credits.from_data(
            await self.http.request(
                "GET",
                APIPath("/person/{person_id}/combined_credits", person_id=self.id),
                params={"language": language},
            ),
        )
