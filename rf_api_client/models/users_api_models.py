from datetime import datetime
from typing import Optional

from rf_api_client.models.base_model import ApiBaseModel


class UserDto(ApiBaseModel):
    user_id: str
    username: str
    name: Optional[str]
    surname: Optional[str]
    avatar: Optional[str]
    birthday: Optional[datetime]
    is_extension_user: Optional[bool]
    language: Optional[str]  # en-US
    timezone: Optional[str]  # Europe/Moscow


class CurrentUserDto(UserDto):
    registration_date: datetime
    kv_session: str
