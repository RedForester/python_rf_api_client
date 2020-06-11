from datetime import datetime
from enum import Enum
from typing import List, Optional, Tuple, Dict, Union

from pydantic import BaseModel, Field

from rf_api_client.models.node_types_api_models import NodePropertyType


class NodeAccessType(str, Enum):
    user_all = 'user_all'
    # todo find out all values


class PositionType(str, Enum):
    R = 'R'
    L = 'L'
    P = 'P'


NodePosition = Tuple[PositionType, str]


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
    position: NodePosition
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


class CreateNodePropertiesDto(NodePropertiesDto):
    class Config:
        allow_population_by_field_name = True

    @classmethod
    def empty(cls) -> 'CreateNodePropertiesDto':
        return cls(
            global_=GlobalGroupDto(title=''),
            by_type={},
            by_user=[],
            by_extension={},
            style=StyleGroupDto()
        )

    # todo build ?


class CreateNodeDto(BaseModel):
    map_id: str
    parent: str
    position: NodePosition
    properties: CreateNodePropertiesDto
    type_id: Optional[str]


class CreateNodeLinkDto(BaseModel):
    map_id: str
    parent: str
    position: NodePosition
    link: str


class UserPropertyCreateDto(BaseModel):
    group: str = 'byUser'
    key: str
    value: str
    type_id: NodePropertyType
    visible: bool


class GlobalPropertyUpdateDto(BaseModel):
    group: str = 'global'
    key: str = 'title'
    value: str


class TypePropertyUpdateDto(BaseModel):
    group: str = 'byType'
    key: str
    value: str


class UserPropertyUpdateDto(BaseModel):
    group: str = 'byUser'
    key: str
    value: Optional[str]
    type_id: Optional[NodePropertyType]
    visible: Optional[bool]


class ObjectPropertyCreateOrUpdateDto(BaseModel):
    group: str = 'style'
    key: str
    value: Union[str, int]


UpdatePropertiesType = Union[
    GlobalPropertyUpdateDto, TypePropertyUpdateDto, UserPropertyUpdateDto, ObjectPropertyCreateOrUpdateDto
]


class UserPropertyDeleteDto(BaseModel):
    group: str = 'byUser'
    key: str


class PropertiesUpdateDto(BaseModel):
    add: Optional[List[UserPropertyCreateDto]]
    update: Optional[List[UpdatePropertiesType]]
    delete: Optional[List[UserPropertyDeleteDto]]
    rename: Optional[List[str]]


class NodeUpdateDto(BaseModel):
    properties: Optional[PropertiesUpdateDto]
    type_id: Optional[str]
    position: Optional[NodePosition]
