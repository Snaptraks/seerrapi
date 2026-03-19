from datetime import date

from pydantic import Field

from .base import Credits, Endpoints, Gender, Stateful
from .http import APIPath
from .movies import Movie
from .tv import TV


class Person(Stateful):
    id: int
    name: str
    birthday: date | None
    deathdat: date | None = None
    known_for: list[Movie | TV] = Field(default_factory=list)
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


class PersonEndpoints(Endpoints):
    async def __call__(self, person_id: int, *, language: str = "en") -> Person:
        return Person.from_data(
            await self.client.http.request(
                "GET",
                APIPath("/person/{person_id}", person_id=person_id),
                params={"language": language},
            ),
            http=self.client.http,
        )
