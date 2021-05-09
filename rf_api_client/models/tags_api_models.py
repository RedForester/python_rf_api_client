from typing import Optional

from rf_api_client.models.base_model import ApiBaseModel


class TaggedNodeMapDto(ApiBaseModel):
    id: str
    name: str


class TaggedNodeTypeDto(ApiBaseModel):
    id: str
    name: str
    icon: Optional[str]


class TaggedNodeDto(ApiBaseModel):
    id: str
    link: Optional[str]
    color: Optional[str]
    parent_title: Optional[str]
    title: Optional[str]
    map: TaggedNodeMapDto
    node_type: Optional[TaggedNodeTypeDto]


class NewTaggedNodeDto(ApiBaseModel):
    tag_id: str
    node: TaggedNodeDto
    order: int
