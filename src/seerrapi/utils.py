import re
from datetime import date
from typing import Annotated, Any

from pydantic import BeforeValidator

SNAKE_CASE_REGEX = re.compile(r"_([a-z\d])")
CAMEL_CASE_REGEX = re.compile(r"([a-z\d])([A-Z])")


def to_camel_case(s: str) -> str:
    return SNAKE_CASE_REGEX.sub(lambda m: m.group(1).upper(), s)


def to_snake_case(s: str) -> str:
    return CAMEL_CASE_REGEX.sub(lambda m: m.group(1) + "_" + m.group(2).lower(), s)


def to_pascal_case(s: str) -> str:
    camel = to_camel_case(s)
    return camel[0].upper() + camel[1:] if camel else camel


def to_camel_case_dict(data: dict[str, Any]) -> dict[str, Any]:
    return {to_camel_case(k): v for k, v in data.items()}


def empty_str_to_none(v: str | None) -> str | None:
    if isinstance(v, str) and v.strip() == "":
        return None
    return v


# Create a reusable custom type alias
# Annotated allows adding extra validation/coercion logic to a type
DateOrEmptyStr = Annotated[date | None, BeforeValidator(empty_str_to_none)]
