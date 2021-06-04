from typing import Optional, List

from rf_api_client.models.base_model import ApiBaseModel


class CommentDto(ApiBaseModel):
    id: str
    node: str
    content: str
    reply_comment: Optional[str]
    author: str
    timestamp: str
    last_time_edited: Optional[str]


class UnreadDto(ApiBaseModel):
    count_comments_since: int
    last_read_timestamp: str


class CommentsDto(ApiBaseModel):
    comments: List[CommentDto]
    unread: Optional[UnreadDto]
