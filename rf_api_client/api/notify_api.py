from rf_api_client.api.base_api import BaseApi
from rf_api_client.models.notify_models import NotifyRequest, DialogRequest, UrlRequest


class NotifyApi(BaseApi):
    async def show_dialog(self, map_id: str, request: DialogRequest):
        url = self.context.base_url / f'api/notify/dialog/map/{map_id}'

        async with self.session.post(url, json=request.dict()):
            pass

    async def show_notification(self, map_id: str, request: NotifyRequest):
        url = self.context.base_url / f'api/notify/notification/map/{map_id}'

        async with self.session.post(url, json=request.dict()):
            pass

    async def show_url(self, map_id: str, request: UrlRequest):
        url = self.context.base_url / f'api/notify/url/map/{map_id}'

        async with self.session.post(url, json=request.dict()):
            pass
