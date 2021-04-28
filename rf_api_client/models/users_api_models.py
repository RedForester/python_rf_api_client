from datetime import datetime
from typing import Optional, List

from rf_api_client.models.base_model import ApiBaseModel


class UserDto(ApiBaseModel):
    user_id: str
    username: str
    name: Optional[str]
    surname: Optional[str]
    avatar: Optional[str]
    birthday: Optional[datetime]
    is_extension_user: bool
    language: str  # en-US
    timezone: str  # Europe/Moscow


class TagDto(ApiBaseModel):
    id: str
    name: str
    removable: bool


class CurrentUserDto(UserDto):
    registration_date: datetime
    kv_session: str
    last_accessed: Optional[datetime]
    tags: List[TagDto]
