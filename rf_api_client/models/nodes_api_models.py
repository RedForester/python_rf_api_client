from datetime import datetime
from enum import Enum
from typing import List, Optional, Tuple, Dict

from pydantic import BaseModel, Field

from rf_api_client.models.node_types_api_models import NodePropertyType


class NodeAccessType(str, Enum):
    user_all = 'user_all'
    # todo find out all values


class PositionType(str, Enum):
    R = 'R'
    L = 'L'
    P = 'P'


class NodeCommonMetaDto(BaseModel):
    creation_timestamp: datetime
    author: str
    last_modified_timestamp: datetime
    last_modified_user: str

    can_move: bool
    editable: bool
    commentable: bool
    can_set_access: bool


class NodeBodyMetaDto(NodeCommonMetaDto):
    subscribed: bool


class NodeMetaDto(NodeCommonMetaDto):
    leaf: bool


class GlobalGroupDto(BaseModel):
    title: str


class StyleGroupDto(BaseModel):
    color: Optional[str]


class UserPropertyDto(BaseModel):
    key: str
    value: str
    type_id: NodePropertyType
    visible: bool


DictLikeGroup = Dict[str, Optional[str]]


class NodePropertiesDto(BaseModel):
    global_: GlobalGroupDto = Field(alias='global')
    by_type: DictLikeGroup = Field(alias='byType')
    by_user: List[UserPropertyDto] = Field(alias='byUser')
    style: StyleGroupDto
    by_extension: DictLikeGroup = Field(alias='byExtension')


class NodeBodyDto(BaseModel):
    id: str
    map_id: str
    type_id: Optional[str]
    parent: Optional[str]
    children: List[str]
    access: NodeAccessType
    unread_comments_count: int
    comments_count: int
    readers: List[str]
    meta: NodeBodyMetaDto
    properties: Optional[NodePropertiesDto]


class NodeDto(BaseModel):
    id: str
    map_id: str
    parent: Optional[str]
    original_parent: Optional[str] = Field(alias='originalParent')
    position: Tuple[PositionType, str]
    access: NodeAccessType
    hidden: bool
    readers: List[str]
    node_level: int = Field(alias='nodelevel')
    meta: NodeMetaDto
    body: NodeBodyDto


class NodeTreeBodyDto(NodeBodyDto):
    children: List['NodeTreeDto']


class NodeTreeDto(NodeDto):
    body: NodeTreeBodyDto


NodeTreeBodyDto.update_forward_refs()
