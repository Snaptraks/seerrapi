import builtins
from typing import Any

from rich import print as rprint

type JsonData = dict[str, Any]

builtins.print = rprint
