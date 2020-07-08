import asyncio
import os

from rf_api_client import RfApiClient
from rf_api_client.models.maps_api_models import MapLayout, NewMapDto
from rf_api_client.rf_api_client import UserAuth

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

MAP_ID = os.getenv('MAP_ID')


async def load_map():
    async with RfApiClient(
        auth=UserAuth(USERNAME, PASSWORD),
    ) as api_client:
        m = await api_client.maps.get_map_by_id(MAP_ID)
        print('Map name:', m.name)
        print('Nodes total:', m.node_count)

        root = await api_client.maps.get_map_nodes(MAP_ID)
        print('Root node title:', root.body.properties.global_.title)


async def create_map():
    async with RfApiClient(
        auth=UserAuth(USERNAME, PASSWORD),
    ) as api_client:
        m = await api_client.maps.create_map(NewMapDto(
            name='Example Map',
            layout=MapLayout.LR
        ))
        print('New map name:', m.name)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(load_map())
    loop.run_until_complete(create_map())

    loop.run_until_complete(asyncio.sleep(0))
    loop.close()
