import json
from datetime import datetime
from enum import Enum
from typing import List, Optional, Tuple, Dict, Union

from pydantic import Field

from rf_api_client.models.base_model import ApiBaseModel
from rf_api_client.models.node_types_api_models import NodePropertyType


class NodeAccessType(str, Enum):
    user_all = 'user_all'
    user_rwh = 'user_rwh'
    user_rw = 'user_rw'
    user_rc = 'user_rc'
    user_r = 'user_r'
    user_none = 'user_none'


class PositionType(str, Enum):
    R = 'R'
    L = 'L'
    P = 'P'


NodePosition = Tuple[PositionType, str]


class NodeCommonMetaDto(ApiBaseModel):
    creation_timestamp: Optional[datetime]
    author: Optional[str]
    last_modified_timestamp: Optional[datetime]
    last_modified_user: Optional[str]

    can_move: bool
    editable: bool
    commentable: bool
    can_set_access: bool


class NodeBodyMetaDto(NodeCommonMetaDto):
    subscribed: bool = False


class NodeMetaDto(NodeCommonMetaDto):
    leaf: bool


class GlobalGroupDto(ApiBaseModel):
    title: str


class StyleGroupDto(ApiBaseModel):
    color: Optional[str]


class UserPropertyDto(ApiBaseModel):
    key: str
    value: Optional[str]
    type_id: NodePropertyType
    visible: bool


class FileInfoDto(ApiBaseModel):
    name: str  # file name for user
    filepath: str  # same as UploadFileResponse.file_id
    last_modified_timestamp: datetime = Field(alias='lastModifiedTimestamp')  # ISO 8601
    last_modified_user: str = Field(alias='lastModifiedUser')


class FilePropertyValue:
    """
    File property value is List[FileInfoDto] serialized to string, this is helper to work with it
    """

    class __Serializer(ApiBaseModel):
        __root__: List[FileInfoDto]

    @staticmethod
    def from_string(value: str) -> List[FileInfoDto]:
        return FilePropertyValue.__Serializer(__root__=json.loads(value)).__root__

    @staticmethod
    def to_string(files: List[FileInfoDto]) -> str:
        return FilePropertyValue.__Serializer(__root__=files).json(by_alias=True)


DictLikeGroup = Dict[str, Optional[str]]


class NodePropertiesDto(ApiBaseModel):
    global_: GlobalGroupDto = Field(alias='global')
    by_type: DictLikeGroup = Field(alias='byType')
    by_user: List[UserPropertyDto] = Field(alias='byUser')
    style: StyleGroupDto
    by_extension: DictLikeGroup = Field(alias='byExtension')


class NodeBodyDto(ApiBaseModel):
    id: str
    map_id: str
    type_id: Optional[str]
    parent: Optional[str]
    children: List[str]
    access: NodeAccessType = NodeAccessType.user_none
    unread_comments_count: int
    comments_count: int
    readers: List[str] = []
    meta: NodeBodyMetaDto
    properties: Optional[NodePropertiesDto]


class NodeDto(ApiBaseModel):
    id: str
    map_id: str
    parent: Optional[str]
    original_parent: Optional[str] = Field(alias='originalParent')
    position: NodePosition
    access: NodeAccessType
    hidden: bool
    readers: List[str] = []
    node_level: int = Field(0, alias='nodelevel')
    meta: NodeMetaDto
    body: NodeBodyDto


class NodeTreeBodyDto(NodeBodyDto):
    children: List['NodeTreeDto']


class NodeTreeDto(NodeDto):
    body: NodeTreeBodyDto


NodeTreeBodyDto.update_forward_refs()


class CreateNodePropertiesDto(NodePropertiesDto):
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


class CreateNodeDto(ApiBaseModel):
    map_id: str
    parent: str
    position: NodePosition
    properties: CreateNodePropertiesDto
    type_id: Optional[str]


class CreateNodeLinkDto(ApiBaseModel):
    map_id: str
    parent: str
    position: NodePosition
    link: str


class UserPropertyCreateDto(ApiBaseModel):
    group: str = 'byUser'
    key: str
    value: str
    type_id: NodePropertyType
    visible: bool


class GlobalPropertyUpdateDto(ApiBaseModel):
    group: str = 'global'
    key: str = 'title'
    value: str


class TypePropertyUpdateDto(ApiBaseModel):
    group: str = 'byType'
    key: str
    value: str


class UserPropertyUpdateDto(ApiBaseModel):
    group: str = 'byUser'
    key: str
    value: Optional[str]
    type_id: Optional[NodePropertyType]
    visible: Optional[bool]


class ObjectPropertyCreateOrUpdateDto(ApiBaseModel):
    group: str = 'style'
    key: str
    value: Union[str, int]


UpdatePropertiesType = Union[
    GlobalPropertyUpdateDto, TypePropertyUpdateDto, UserPropertyUpdateDto, ObjectPropertyCreateOrUpdateDto
]


class UserPropertyDeleteDto(ApiBaseModel):
    group: str = 'byUser'
    key: str


class PropertiesUpdateDto(ApiBaseModel):
    add: Optional[List[UserPropertyCreateDto]]
    update: Optional[List[UpdatePropertiesType]]
    delete: Optional[List[UserPropertyDeleteDto]]
    rename: Optional[List[str]]


class NodeUpdateDto(ApiBaseModel):
    properties: Optional[PropertiesUpdateDto]
    type_id: Optional[str]
    position: Optional[NodePosition]


class InsertOptions(ApiBaseModel):
    comments: bool = True
    styleProperties: bool = True
    userProperties: bool = True
    quiet: bool = False


class NodeInsertOptions(ApiBaseModel):
    # Move (cut) or copy operation
    move: bool

    # Apply operation for a single node or branch
    for_branch: bool

    # These options are for copy operation,
    #  InsertOptions(comments=False, styleProperties=False, userProperties=False, quiet=False) if not specified
    insert_options: Optional[InsertOptions] = None

    # Count of tree levels in response, all if not specified
    level_count: Optional[int] = None


class NodeInsertResult(ApiBaseModel):
    root: NodeTreeDto
