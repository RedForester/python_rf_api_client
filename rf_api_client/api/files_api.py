from rf_api_client.api.base_api import BaseApi
from rf_api_client.models.files_api_models import UploadFileResponseDto


class FilesApi(BaseApi):
    async def get_file_bytes(self, file_id) -> bytes:
        url = self.context.base_url / f'api/files/{file_id}'

        async with self.session.get(url) as resp:
            data = await resp.read()
            return data

    async def upload_file_bytes(self, data: bytes) -> UploadFileResponseDto:
        url = self.context.base_url / 'api/files'

        async with self.session.put(url, data=data) as resp:
            body = await resp.json()

            return UploadFileResponseDto(**body)
