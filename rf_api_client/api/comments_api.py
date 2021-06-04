from rf_api_client.api.base_api import BaseApi
from rf_api_client.models.comments_api_models import CommentsDto


class CommentsApi(BaseApi):
    async def get_by_node(self, node_id: str) -> CommentsDto:
        url = self.context.base_url / f'api/nodes/{node_id}/comments'

        async with self.session.get(url) as resp:
            body = await resp.json()

            return CommentsDto(**body)
