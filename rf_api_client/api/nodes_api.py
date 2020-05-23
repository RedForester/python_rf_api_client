from rf_api_client.api.base_api import BaseApi
from rf_api_client.models.nodes_api_models import NodeDto


class NodesApi(BaseApi):
    async def get_by_id(self, node_id: str) -> NodeDto:
        url = f"{self._context.base_url}/api/nodes/{node_id}"

        async with self.get_session() as session:
            async with session.get(url) as resp:
                body = await resp.json()

                return NodeDto(**body)
