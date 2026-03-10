from datetime import datetime

from . import Base


class User(Base):
    permissions: int
    warnings: list
    id: int
    email: str
    plex_username: str | None
    jellyfin_username: str | None
    username: str | None
    recovery_link_expiration_date: datetime | None
    user_type: int
    plex_id: int | None
    jellyfin_user_id: int | None
    avatar: str | None
    avatar_e_tag: str | None
    avatar_version: int | None
    movie_quota_limit: int | None
    movie_quota_days: int | None
    tv_quota_limit: int | None
    tv_quota_days: int | None
    created_at: datetime
    updated_at: datetime
    request_count: int
    display_name: str
    settings: None = None
