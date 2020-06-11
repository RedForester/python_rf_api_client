from typing import Union

from rf_api_client.api.base_api import BaseApi
from rf_api_client.models.nodes_api_models import NodeDto, CreateNodeDto, CreateNodeLinkDto


class NodesApi(BaseApi):
    async def get_by_id(self, node_id: str) -> NodeDto:
        url = self.context.base_url / f'api/nodes/{node_id}'

        async with self.session.get(url) as resp:
            body = await resp.json()

            return NodeDto(**body)

    async def create(self, node: Union[CreateNodeDto, CreateNodeLinkDto]):
        url = self.context.base_url / 'api/nodes'

        async with self.session.post(url, json=node.dict(by_alias=True)) as resp:
            body = await resp.json()

            return NodeDto(**body)
