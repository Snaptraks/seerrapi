from dataclasses import dataclass

from . import Base


@dataclass
class Status(Base):
    version: str
    commit_tag: str
    update_available: bool
    commits_behind: int
    restart_required: bool


@dataclass
class AppData(Base):
    app_data: bool
    app_data_path: str
    app_data_permissions: bool
