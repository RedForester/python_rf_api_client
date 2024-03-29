from typing import List

import pytest

from rf_api_client import RfApiClient
from rf_api_client.models.nodes_api_models import CreateNodeDto, CreateNodePropertiesDto, PositionType, \
    CreateNodeLinkDto, NodeUpdateDto, PropertiesUpdateDto, GlobalPropertyUpdateDto, NodeDto, NodeTreeDto, \
    NodeInsertOptions
from tests.conftest import Secret
from tests.prepare_map import prepare_map


def flatten(tree: NodeTreeDto) -> List[str]:
    ids = [tree.id]
    for child in tree.body.children:
        ids.extend(flatten(child))
    return ids


@pytest.mark.asyncio
async def test_login(secret: Secret, api: RfApiClient):
    user = await api.users.get_current()

    assert user.username == secret.username


@pytest.mark.asyncio
async def test_read_maps(api: RfApiClient):
    maps = await api.maps.get_all_maps()

    assert len(maps) >= 0


@pytest.mark.asyncio
async def test_nodes(secret: Secret, api: RfApiClient):
    m = await prepare_map(api, secret.developer_prefix, 'test_create_nodes')

    p = CreateNodePropertiesDto.empty()
    p.global_.title = 'first_node'
    child_1 = await api.nodes.create(CreateNodeDto(
        map_id=m.id,
        parent=m.root_node_id,
        type_id=None,
        position=(PositionType.R, '1'),
        properties=p
    ))

    # link to first_node, also child of first_node
    _ = await api.nodes.create(CreateNodeLinkDto(
        map_id=m.id,
        parent=child_1.id,
        position=(PositionType.R, '1'),
        link=child_1.id
    ))

    # read all nodes
    nodes = await api.maps.get_map_nodes(m.id)

    c1 = nodes.body.children[0]
    c2 = c1.body.children[0]

    # check if c2 is the link to c1
    assert c1.id == c1.body.id
    assert c2.id != c2.body.id
    assert c2.body.id == c1.body.id

    c1_updated = await api.nodes.update_by_id(child_1.id, NodeUpdateDto(
        properties=PropertiesUpdateDto(
            update=[
                GlobalPropertyUpdateDto(
                    key='title',
                    value='first_node_updated'
                )
            ]
        )
    ))

    assert c1_updated.body.properties.global_.title == 'first_node_updated'

    # delete the first node (also delete the second node, which is a link to the first)
    await api.nodes.delete_by_id(child_1.id)

    # read all nodes again and check if both c1 and c2 are deleted
    repeated_nodes = await api.maps.get_map_nodes(m.id)

    assert len(repeated_nodes.body.children) == 0


@pytest.mark.asyncio
async def test_partial_load(secret: Secret, api: RfApiClient):
    m = await prepare_map(api, secret.developer_prefix, 'test_partial_load')

    async def create_node(parent: str, title: str) -> NodeDto:
        p = CreateNodePropertiesDto.empty()
        p.global_.title = title
        return await api.nodes.create(CreateNodeDto(
            map_id=m.id,
            parent=parent,
            type_id=None,
            position=(PositionType.R, '1'),
            properties=p
        ))

    n1 = await create_node(m.root_node_id, 'first')
    n2 = await create_node(n1.id, 'second')
    n3 = await create_node(n2.id, 'third')

    result = flatten(await api.maps.get_map_nodes(m.id, level_count=0))
    assert result == [m.root_node_id]

    result = flatten(await api.maps.get_map_nodes(m.id, level_count=2))
    assert result == [m.root_node_id, n1.id, n2.id]

    result = flatten(await api.maps.get_map_nodes(m.id, root_id=n2.id, level_count=0))
    assert result == [n2.id]

    result = flatten(await api.maps.get_map_nodes(m.id, root_id=n2.id))
    assert result == [n2.id, n3.id]


@pytest.mark.asyncio
async def test_nodes_on_path(secret: Secret, api: RfApiClient):
    m = await prepare_map(api, secret.developer_prefix, 'test_nodes_on_path')

    p = CreateNodePropertiesDto.empty()
    p.global_.title = '1.1 node'
    await api.nodes.create(CreateNodeDto(
        map_id=m.id,
        parent=m.root_node_id,
        type_id=None,
        position=(PositionType.R, '1'),
        properties=p
    ))

    p = CreateNodePropertiesDto.empty()
    p.global_.title = '1.2 node'
    parent = await api.nodes.create(CreateNodeDto(
        map_id=m.id,
        parent=m.root_node_id,
        type_id=None,
        position=(PositionType.R, '1'),
        properties=p
    ))

    p = CreateNodePropertiesDto.empty()
    p.global_.title = '1.2.1 node'
    await api.nodes.create(CreateNodeDto(
        map_id=m.id,
        parent=parent.id,
        type_id=None,
        position=(PositionType.R, '1'),
        properties=p
    ))

    p = CreateNodePropertiesDto.empty()
    p.global_.title = '1.2.2 node'
    node = await api.nodes.create(CreateNodeDto(
        map_id=m.id,
        parent=parent.id,
        type_id=None,
        position=(PositionType.R, '1'),
        properties=p
    ))

    result = flatten(await api.maps.get_map_nodes_on_path(
        m.id,
        m.root_node_id,
        m.root_node_id,
    ))
    assert len(result) == 1

    result = flatten(await api.maps.get_map_nodes_on_path(
        m.id,
        m.root_node_id,
        node.id
    ))
    assert len(result) == 3

    result = flatten(await api.maps.get_map_nodes(m.id, m.root_node_id))
    assert len(result) == 5


@pytest.mark.asyncio
async def test_copy_cut_nodes(secret: Secret, api: RfApiClient):
    m = await prepare_map(api, secret.developer_prefix, 'test_copy_cut_nodes')

    p = CreateNodePropertiesDto.empty()
    p.global_.title = 'source'
    source_node = await api.nodes.create(CreateNodeDto(
        map_id=m.id,
        parent=m.root_node_id,
        type_id=None,
        position=(PositionType.R, '1'),
        properties=p
    ))

    p = CreateNodePropertiesDto.empty()
    p.global_.title = 'test_node'
    test_node = await api.nodes.create(CreateNodeDto(
        map_id=m.id,
        parent=source_node.id,
        type_id=None,
        position=(PositionType.P, '1'),
        properties=p
    ))

    p = CreateNodePropertiesDto.empty()
    p.global_.title = 'first_child'
    first_child = await api.nodes.create(CreateNodeDto(
        map_id=m.id,
        parent=test_node.id,
        type_id=None,
        position=(PositionType.P, '1'),
        properties=p
    ))

    p = CreateNodePropertiesDto.empty()
    p.global_.title = 'target'
    target_node = await api.nodes.create(CreateNodeDto(
        map_id=m.id,
        parent=m.root_node_id,
        type_id=None,
        position=(PositionType.L, '1'),
        properties=p
    ))

    all_nodes_before = {m.root_node_id, source_node.id, test_node.id, first_child.id, target_node.id}
    all_nodes = set(flatten(await api.maps.get_map_nodes(m.id)))
    assert all_nodes == all_nodes_before

    # Copy test
    resp = await api.nodes.insert_to(test_node.id, target_node.id, NodeInsertOptions(move=False, for_branch=True))
    copied_nodes = flatten(resp.root)
    assert len(copied_nodes) == 2

    target_branch_after = {target_node.id, *copied_nodes}
    target_branch = set(flatten(await api.maps.get_map_nodes(m.id, root_id=target_node.id)))
    assert target_branch == target_branch_after

    # Cut test
    await api.nodes.insert_to(test_node.id, target_node.id, NodeInsertOptions(move=True, for_branch=True))

    source_branch_after = {source_node.id}
    source_branch = set(flatten(await api.maps.get_map_nodes(m.id, root_id=source_node.id)))
    assert source_branch == source_branch_after

    # fixme After cut, the backend only returns one node
    # target_branch_after = {*target_branch_after, *cut_nodes}
    # target_branch = set(flatten(await api.maps.get_map_nodes(m.id, root_id=target_node.id)))
    # assert target_branch == target_branch_after

    target_branch = set(flatten(await api.maps.get_map_nodes(m.id, root_id=target_node.id)))
    assert len(target_branch) == 5

    # todo Test more variants (for_branch, level_count, insert_options for copy)
