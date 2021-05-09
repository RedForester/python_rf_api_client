import asyncio
import os

from rf_api_client import RfApiClient
from rf_api_client.rf_api_client import UserAuth

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')


MAP_ID = os.getenv('MAP_ID')


async def get_current_user():
    async with RfApiClient(
            auth=UserAuth(USERNAME, PASSWORD),
    ) as api_client:
        me = await api_client.users.get_current()
        print(me)


async def get_favorite_nodes():
    async with RfApiClient(
            auth=UserAuth(USERNAME, PASSWORD),
    ) as api_client:
        m = await api_client.maps.get_map_by_id(MAP_ID)
        print(m)

        me = await api_client.users.get_current()
        print(me)

        favorite_tag = me.tags[0]
        favorite_nodes = await api_client.tags.get_nodes(favorite_tag.id)
        print(favorite_nodes)

        tagged = await api_client.tags.add_tag(favorite_tag.id, m.root_node_id)
        print("tagged: ", tagged)

        await api_client.tags.remove_tag(favorite_tag.id, m.root_node_id)
        print("and removed")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_current_user())
    loop.run_until_complete(get_favorite_nodes())

    loop.run_until_complete(asyncio.sleep(0))
    loop.close()
