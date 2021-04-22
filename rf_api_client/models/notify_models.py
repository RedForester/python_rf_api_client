from enum import Enum
from typing import Optional

from rf_api_client.models.base_model import ApiBaseModel


class DialogSize(ApiBaseModel):
    width: int
    height: int


class DialogRequest(ApiBaseModel):
    user_id: str
    session_id: Optional[str]
    dialog_src: str
    dialog_title: Optional[str]
    dialog_size: Optional[DialogSize]


class NotificationType(str, Enum):
    info = 'info'
    warning = 'warning'
    error = 'error'
    success = 'success'
    alert = 'alert'


class NotifyRequest(ApiBaseModel):
    user_id: str
    session_id: Optional[str]
    notification_text: str
    notification_type: Optional[NotificationType]


class UrlRequest(ApiBaseModel):
    user_id: str
    session_id: Optional[str]
    url: str
