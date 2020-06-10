from enum import Enum
from typing import Optional

from pydantic import BaseModel


class MapLayout(str, Enum):
    L = 'L'
    R = 'R'
    LR = 'LR'


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
