import asyncio

import pytest

from rf_api_client import RfApiClient
from rf_api_client.models.maps_api_models import MapDto
from rf_api_client.models.nodes_api_models import CreateNodePropertiesDto, CreateNodeDto, PositionType
from tests.conftest import Secret
from tests.prepare_map import prepare_map


@pytest.mark.asyncio
async def test_search_nodes(secret: Secret, api: RfApiClient):
    m = await prepare_search_map(api, secret)
    await search_simple_test(api, m)
    await search_advanced_test(api, m)
    await search_aggregation_test(api, m)


async def prepare_search_map(api, secret) -> MapDto:
    m = await prepare_map(api, secret.developer_prefix, 'test_search_nodes')

    p = CreateNodePropertiesDto.empty()
    p.global_.title = 'first node'
    await api.nodes.create(CreateNodeDto(
        map_id=m.id,
        parent=m.root_node_id,
        type_id=None,
        position=(PositionType.R, '1'),
        properties=p
    ))

    p = CreateNodePropertiesDto.empty()
    p.global_.title = 'second node'
    await api.nodes.create(CreateNodeDto(
        map_id=m.id,
        parent=m.root_node_id,
        type_id=None,
        position=(PositionType.R, '1'),
        properties=p
    ))

    # rf must have time to index new nodes
    await asyncio.sleep(5)
    return m


async def search_simple_test(api: RfApiClient, m: MapDto):
    result = await api.maps.search_nodes('node', [m.id])
    assert len(result) > 0

    result = await api.maps.search_nodes('first', [m.id])
    assert len(result) > 0


async def search_advanced_test(api: RfApiClient, m: MapDto):
    result = await api.maps.search_nodes_advanced(
        {
            "query_string": {
                "query": "type: \"some_type\"",
            }
        },
        map_ids=[m.id],
    )
    assert len(result) == 0

    result = await api.maps.search_nodes_advanced(
        {
            "query_string": {
                "query": "title: \"first\"",
            }
        },
        map_ids=[m.id],
    )
    assert len(result) > 0


async def search_aggregation_test(api: RfApiClient, m: MapDto):
    result = await api.maps.search_nodes_aggregation(
        query={
            "match_all": {},
        },
        aggs={
            "top_hits_agg": {
                "top_hits": {},
            },
        },
        map_ids=[m.id],
    )
    assert len(result["top_hits_agg"]["hits"]) > 0
