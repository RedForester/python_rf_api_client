from typing import List

from rf_api_client.api.base_api import BaseApi
from rf_api_client.models.tags_api_models import TaggedNodeDto, NewTaggedNodeDto


class TagsApi(BaseApi):
    async def get_nodes(self, tag_id: str) -> List[TaggedNodeDto]:
        url = self.context.base_url / f'api/tags/{tag_id}'

        async with self.session.get(url) as resp:
            body = await resp.json()

            return [TaggedNodeDto(**t) for t in body]

    async def add_tag(self, tag_id: str, node_id: str) -> NewTaggedNodeDto:
        url = self.context.base_url / f'api/tags/{tag_id}/node/{node_id}'

        async with self.session.post(url) as resp:
            body = await resp.json()

            return NewTaggedNodeDto(**body)

    async def remove_tag(self, tag_id: str, node_id: str) -> None:
        url = self.context.base_url / f'api/tags/{tag_id}/node/{node_id}'

        await self.session.delete(url)
