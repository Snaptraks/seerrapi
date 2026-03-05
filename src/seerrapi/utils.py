from typing import Any

from apischema.utils import to_camel_case


def to_camel_case_dict(data: dict[str, Any]) -> dict[str, Any]:
    return {to_camel_case(k): v for k, v in data.items()}
