from dataclasses import dataclass, field
from typing import Any, Self

from apischema import deserialize, metadata, settings

from .http import HTTP

# Set aliases to convert the camelCase from API
# responses to snake_case in Python style
settings.camel_case = True


@dataclass
class Base:
    http: HTTP = field(init=False, metadata=metadata.skip(serialization=True))

    @classmethod
    def from_data(cls, data: dict[str, Any], *, http: HTTP) -> Self:
        obj = deserialize(cls, data)
        obj.http = http

        return obj

    @classmethod
    def from_data_list(cls, data: list[dict[str, Any]], *, http: HTTP) -> list[Self]:
        objs = deserialize(list[cls], data)
        for obj in objs:
            obj.http = http

        return objs
