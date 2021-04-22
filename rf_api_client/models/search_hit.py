from datetime import datetime
from typing import List, Optional, Any

from rf_api_client.models.base_model import ApiBaseModel


class HitPropDto(ApiBaseModel):
    key: str
    value: Optional[str]
    group: str


class SearchHitDto(ApiBaseModel):
    id: str
    src_id: Optional[str]
    map_id: str
    parent: Optional[str]
    title: str
    type: str
    type_id: str
    access: List[str]
    color: Optional[str]
    props: List[HitPropDto]

    timestamp: datetime
    last_modified_timestamp: datetime
    score: float


class SearchResponse(ApiBaseModel):
    hits: List[SearchHitDto]
    original_query: Any
