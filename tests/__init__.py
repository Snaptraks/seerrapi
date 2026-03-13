import builtins
from dataclasses import dataclass
from typing import Any
from warnings import warn

from rich import print as rprint

from seerrapi import MediaType

type JsonData = dict[str, Any]

builtins.print = rprint


@dataclass
class MediaInfo:
    tmdb_id: int
    title: str
    media_type: MediaType
    user: int


def _test_list_of_instances(
    sequence: list[Any], check_type: type[Any] | tuple[type[Any], ...]
) -> bool:
    assert isinstance(sequence, list)
    if len(sequence) == 0:
        warn("Sequence to test the items for is empty.", stacklevel=2)

    for item in sequence:
        assert isinstance(item, check_type)

    return True
