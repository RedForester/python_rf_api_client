from enum import Enum, unique
from typing import List, Optional

from rf_api_client.models.base_model import ApiBaseModel


@unique
class NodePropertyType(int, Enum):
    INTEGER = 1,
    REAL = 2,
    BOOLEAN = 3,
    TEXT = 5,
    HTML = 6,
    DATE = 7,
    TIME = 8,
    DATETIME = 9,
    FILE = 10,
    USER = 11,
    ENUM = 12,


class NodeTypePropertyOwner(str, Enum):
    node_type = 'node_type'
    # todo find out all values


class NodeTypePropertyIcon(ApiBaseModel):
    img: str
    text: str


class NodeTypePropertyDto(ApiBaseModel):
    name: str
    owner_id: str
    owner_type: NodeTypePropertyOwner
    position: int
    type_id: NodePropertyType
    default_value: str
    icons: List[NodeTypePropertyIcon]
    multivalued: bool
    displayable: bool
    as_icon: bool


class NodeTypeDto(ApiBaseModel):
    id: str
    map_id: str
    name: str
    icon: Optional[str]
    displayable: bool
    default_child_node_type_id: Optional[str]
    properties: List[NodeTypePropertyDto]
