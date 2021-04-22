from typing import List, Optional, Dict, Any

from rf_api_client.api.base_api import BaseApi
from rf_api_client.models.maps_api_models import MapDto, NewMapDto
from rf_api_client.models.node_types_api_models import NodeTypeDto
from rf_api_client.models.nodes_api_models import NodeTreeDto
from rf_api_client.models.search_hit import SearchHitDto, SearchResponse
from rf_api_client.models.users_api_models import UserDto


class MapsApi(BaseApi):
    async def get_map_by_id(self, map_id: str) -> MapDto:
        url = self.context.base_url / f'api/maps/{map_id}'

        async with self.session.get(url) as resp:
            body = await resp.json()

            return MapDto(**body)

    async def create_map(self, new_map: NewMapDto) -> MapDto:
        url = self.context.base_url / 'api/maps'

        async with self.session.post(url, json=new_map.dict(by_alias=True)) as resp:
            body = await resp.json()

            return MapDto(**body)

    async def delete_map_by_id(self, map_id: str):
        url = self.context.base_url / f'api/maps/{map_id}'

        await self.session.delete(url)

    async def get_map_types(self, map_id: str) -> List[NodeTypeDto]:
        url = self.context.base_url / f'api/maps/{map_id}/node_types'

        async with self.session.get(url) as resp:
            body = await resp.json()

            return [NodeTypeDto(**t) for t in body]

    async def get_map_users(self, map_id: str) -> List[UserDto]:
        url = self.context.base_url / f'api/maps/{map_id}/users'

        async with self.session.get(url) as resp:
            body = await resp.json()

            return [UserDto(**u) for u in body]

    async def get_all_maps(self) -> List[MapDto]:
        url = self.context.base_url / 'api/maps'

        async with self.session.get(url) as resp:
            body = await resp.json()

            return [MapDto(**m) for m in body]

    async def get_map_nodes(
            self,
            map_id: str,
            root_id: Optional[str] = None,
            level_count: Optional[int] = None,
    ) -> NodeTreeDto:
        url = self.context.base_url / f'api/maps/{map_id}/nodes'
        if root_id is not None:
            url = url / root_id
        if level_count is not None:
            url = url / f'level_count/{level_count}'

        async with self.session.get(url) as resp:
            body = await resp.json()

            return NodeTreeDto(**body)

    async def get_map_nodes_on_path(
            self,
            map_id: str,
            from_id: str,
            to_id: str,
    ) -> NodeTreeDto:
        url = self.context.base_url / f'api/maps/{map_id}/nodes/path/{from_id}/to/{to_id}'

        async with self.session.get(url) as resp:
            body = await resp.json()

            return NodeTreeDto(**body)

    async def search_nodes(
            self,
            query: str,
            map_ids: List[str],
            full_docs: bool = True,
            hits_limit: int = 50,
            root_id: str = None,
            with_node_links: bool = False,
    ) -> List[SearchHitDto]:
        url = self.context.base_url / 'api/search'

        params = dict(
            full_docs=full_docs,
            hits_limit=hits_limit,
            map_ids=map_ids,
            query=query,
            root_id=root_id,
            with_node_links=with_node_links,
        )

        async with self.session.post(url, json=params) as resp:
            body = await resp.json()

        return SearchResponse(**body).hits

    async def search_nodes_advanced(
            self,
            query: Dict[str, Any],
            map_ids: List[str],
            full_docs: bool = True,
            hits_limit: int = 50,
            root_id: str = None,
            with_node_links: bool = False,
    ) -> List[SearchHitDto]:
        url = self.context.base_url / 'api/search/advanced'

        params = dict(
            full_docs=full_docs,
            hits_limit=hits_limit,
            map_ids=map_ids,
            query=query,
            root_id=root_id,
            with_node_links=with_node_links,
        )

        async with self.session.post(url, json=params) as resp:
            body = await resp.json()

        return SearchResponse(**body).hits

    async def search_nodes_aggregation(
            self,
            query: Dict[str, Any],
            aggs: Dict[str, Any],
            map_ids: List[str],
            root_id: str = None,
            with_node_links: bool = False,
    ) -> Dict[str, Any]:
        url = self.context.base_url / 'api/search/aggregation'

        params = dict(
            query=query,
            aggs=aggs,
            map_ids=map_ids,
            root_id=root_id,
            with_node_links=with_node_links,
        )

        async with self.session.post(url, json=params) as resp:
            body = await resp.json()

        return body
