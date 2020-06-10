from enum import Enum
from typing import Optional

from pydantic import BaseModel


class DialogSize(BaseModel):
    width: int
    height: int


class DialogRequest(BaseModel):
    user_id: str
    session_id: Optional[str]
    dialog_src: str
    dialog_size: Optional[DialogSize]


class NotificationType(str, Enum):
    info = 'info'
    warning = 'warning'
    error = 'error'
    success = 'success'
    alert = 'alert'


class NotifyRequest(BaseModel):
    user_id: str
    session_id: Optional[str]
    notification_text: str
    notification_type: Optional[NotificationType]


class UrlRequest(BaseModel):
    user_id: str
    session_id: Optional[str]
    url: str
