from typing import List

from rf_api_client.api.base_api import BaseApi
from rf_api_client.models.maps_api_models import MapDto
from rf_api_client.models.node_types_api_models import NodeTypeDto
from rf_api_client.models.nodes_api_models import NodeTreeDto
from rf_api_client.models.users_api_models import UserDto


class MapsApi(BaseApi):
    async def get_map_by_id(self, map_id: str) -> MapDto:
        url = f"{self._context.base_url}/api/maps/{map_id}"

        async with self.get_session() as session:
            async with session.get(url) as resp:
                body = await resp.json()

                return MapDto(**body)

    async def get_map_types(self, map_id: str) -> List[NodeTypeDto]:
        url = f"{self._context.base_url}/api/maps/{map_id}/node_types"

        async with self.get_session() as session:
            async with session.get(url) as resp:
                body = await resp.json()

                return [NodeTypeDto(**t) for t in body]

    async def get_map_users(self, map_id: str) -> List[UserDto]:
        url = f"{self._context.base_url}/api/maps/{map_id}/users"
        async with self.get_session() as session:
            async with session.get(url) as resp:
                body = await resp.json()

                return [UserDto(**u) for u in body]

    async def get_all_maps(self) -> List[MapDto]:
        url = f"{self._context.base_url}/api/maps"

        async with self.get_session() as session:
            async with session.get(url) as resp:
                body = await resp.json()

                return [MapDto(**m) for m in body]

    async def get_map_nodes(self, map_id: str) -> NodeTreeDto:
        url = f"{self._context.base_url}/api/maps/{map_id}/nodes"

        async with self.get_session() as session:
            async with session.get(url) as resp:
                body = await resp.json()

                return NodeTreeDto(**body)
