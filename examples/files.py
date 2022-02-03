import asyncio
import os
from datetime import datetime

from rf_api_client import RfApiClient
from rf_api_client.models.node_types_api_models import NodePropertyType
from rf_api_client.models.nodes_api_models import CreateNodeDto, CreateNodePropertiesDto, PositionType, NodeUpdateDto, \
    PropertiesUpdateDto, UserPropertyCreateDto, FilePropertyValue, FileInfoDto
from rf_api_client.rf_api_client import UserAuth


USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
MAP_ID = os.getenv('MAP_ID')

FILE_NAME = 'file.txt'
FILE_PATH = f'./{FILE_NAME}'
OUTPUT_FILE_NAME = 'file_output.txt'
OUTPUT_FILE_PATH = f'./{OUTPUT_FILE_NAME}'


async def file_property():
    async with RfApiClient(
            auth=UserAuth(USERNAME, PASSWORD),
    ) as api_client:
        me = await api_client.users.get_current()

        m = await api_client.maps.get_map_by_id(MAP_ID)

        props = CreateNodePropertiesDto.empty()
        props.global_.title = 'Node with file property'
        node = await api_client.nodes.create(CreateNodeDto(
            map_id=m.id,
            parent=m.root_node_id,
            position=(PositionType.P, '-1'),
            properties=props
        ))

        # Upload file
        with open(FILE_PATH, 'rb') as f:
            data = f.read()
            file = await api_client.files.upload_file_bytes(data)
            print('Uploaded:', file)

        # Prepare file property data
        serialized_value = FilePropertyValue.to_string([
            FileInfoDto(
                name=FILE_NAME,
                filepath=file.file_id,
                last_modified_timestamp=datetime.now().astimezone(),
                last_modified_user=me.user_id
            )
        ])
        print(serialized_value)

        # Attach file to node
        updated_node = await api_client.nodes.update_by_id(node.id, NodeUpdateDto(
            properties=PropertiesUpdateDto(
                add=[
                    UserPropertyCreateDto(
                        key='files',
                        type_id=NodePropertyType.FILE,
                        value=serialized_value,
                        visible=True,
                    )
                ]
            )
        ))

        # Read file property from node
        deserialized_value = FilePropertyValue.from_string(updated_node.body.properties.by_user[0].value)
        print(deserialized_value)

        file_info = deserialized_value[0]

        # Download file
        file = await api_client.files.get_file_bytes(file_info.filepath)
        with open(OUTPUT_FILE_PATH, 'wb') as f:
            f.write(file)
            print('Downloaded')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(file_property())

    loop.run_until_complete(asyncio.sleep(0))
    loop.close()
