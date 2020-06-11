from typing import Union

from rf_api_client.api.base_api import BaseApi, ClientInternalError
from rf_api_client.models.nodes_api_models import NodeDto, CreateNodeDto, CreateNodeLinkDto, NodeUpdateDto


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

    async def update_by_id(self, node_id: str, update: NodeUpdateDto):
        url = self.context.base_url / f'api/nodes/{node_id}'

        j = update.dict(by_alias=True, exclude_none=True)
        async with self.session.patch(url, json=j) as resp:
            body = await resp.json()

            nodes = (NodeDto(**n) for n in body)
            updated = next(filter(lambda n: n.id == node_id, nodes), None)
            if not updated:
                raise ClientInternalError('Could not find updated node in update response')

            return updated

    async def delete_by_id(self, node_id: str):
        url = self.context.base_url / f'api/nodes/{node_id}'

        await self.session.delete(url)
