from pydantic import Field

from rf_api_client.models.base_model import ApiBaseModel


class UploadFileResponseDto(ApiBaseModel):
    file_id: str = Field(alias='fileId')  # Same as FilePropertyValue.filepath
    user_id: str = Field(alias='userId')  # Current user id
