from rf_api_client.api.base_api import BaseApi
from rf_api_client.models.node_types_api_models import NodeTypeDto


class NodeTypesApi(BaseApi):
    async def get_by_id(self, type_id: str) -> NodeTypeDto:
        url = self.context.base_url / f'api/node_types/{type_id}'

        async with self.session.get(url) as resp:
            body = await resp.json()

            return NodeTypeDto(**body)
