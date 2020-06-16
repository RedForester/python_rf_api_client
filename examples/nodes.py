import asyncio
import os
from asyncio import sleep

from rf_api_client import RfApiClient
from rf_api_client.models.node_types_api_models import NodePropertyType
from rf_api_client.models.nodes_api_models import NodeUpdateDto, PropertiesUpdateDto, GlobalPropertyUpdateDto, \
    UserPropertyCreateDto, CreateNodePropertiesDto, CreateNodeDto, PositionType

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

MAP_ID = os.getenv('MAP_ID')


async def create_and_update_node():
    async with RfApiClient(
            username=USERNAME,
            password=PASSWORD
    ) as api_client:
        sleep_time = 5.0

        m = await api_client.maps.get_map_by_id(MAP_ID)

        props = CreateNodePropertiesDto.empty()
        props.global_.title = f'New node title  \nWait {sleep_time} seconds to update'
        node = await api_client.nodes.create(CreateNodeDto(
            map_id=m.id,
            parent=m.root_node_id,
            position=(PositionType.P, '-1'),
            properties=props
        ))

        print('New node properties:', node.body.properties.dict(by_alias=True))

        await sleep(sleep_time)

        updated_node = await api_client.nodes.update_by_id(
            node.id,
            NodeUpdateDto(
                properties=PropertiesUpdateDto(
                    update=[
                        GlobalPropertyUpdateDto(
                            value='Title updated'
                        )
                    ],
                    add=[
                        UserPropertyCreateDto(
                            key='user property',
                            type_id=NodePropertyType.TEXT,
                            value='Value of user property',
                            visible=True,
                        )
                    ]
                )
            )
        )

        print('Updated node properties:', updated_node.body.properties.dict(by_alias=True))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_and_update_node())

    loop.run_until_complete(asyncio.sleep(0))
    loop.close()
