from enum import Enum
from typing import Optional

from pydantic import BaseModel


class MapLayout(str, Enum):
    L = 'L'
    R = 'R'
    LR = 'LR'


class MapDefaultUsersAccess(str, Enum):
    user_invited = 'user_invited'
    user_not_invited = 'user_not_invited'


class MapPrivacyType(str, Enum):
    public = 'public'
    private = 'private'


class MapDto(BaseModel):
    id: str
    name: str
    description: Optional[str]
    root_node_id: str
    owner: str
    owner_username: str
    owner_name: Optional[str]
    owner_surname: Optional[str]
    owner_avatar: Optional[str]
    layout: MapLayout
    public: bool
    node_count: int
    user_count: int
    is_admin: bool


class NewMapDto(BaseModel):
    name: str
    layout: MapLayout
    default_others: Optional[MapDefaultUsersAccess]
    privacy_type: Optional[MapPrivacyType]
