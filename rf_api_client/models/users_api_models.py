from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserDto(BaseModel):
    user_id: str
    username: str
    name: Optional[str]
    surname: Optional[str]
    avatar: Optional[str]
    birthday: Optional[datetime]  # todo check
    is_extension_user: Optional[bool]


class CurrentUserDto(UserDto):
    registration_date: datetime
    kv_session: str
