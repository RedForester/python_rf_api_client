from typing import Optional

from rf_api_client import RfApiClient
from rf_api_client.models.maps_api_models import MapDto, NewMapDto, MapLayout


async def prepare_map(api: RfApiClient, developer_prefix: str, name: str):
    maps = await api.maps.get_all_maps()

    real_name = f'{developer_prefix}_{name}'

    old_map: Optional[MapDto] = next(filter(lambda m: m.name == real_name, maps), None)
    if old_map:
        await api.maps.delete_map_by_id(old_map.id)

    return await api.maps.create_map(NewMapDto(name=real_name, layout=MapLayout.LR))
