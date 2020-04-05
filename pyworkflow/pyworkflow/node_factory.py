from .node import *
import json


def create_node(payload):
    json_data = json.loads(payload)

    try:
        return node_factory(json_data)
    except OSError as e:
        raise NodeException('create_node', 'Problem parsing JSON')

def node_factory(node_info):
    # Create a new Node with info
    # TODO: should perform error-checking or add default values if missing
    node_type = node_info.get('node_type')
    node_key = node_info.get('node_key')

    if node_type == 'IONode':
        new_node = io_node(node_key, node_info)
    elif node_type == 'ManipulationNode':
        new_node = manipulation_node(node_key, node_info)
    else:
        new_node = None

    return new_node


def io_node(node_key, node_info):
    if node_key == 'ReadCsvNode':
        return ReadCsvNode(node_info)
    elif node_key == 'WriteCsvNode':
        return WriteCsvNode(node_info)
    else:
        return None


def manipulation_node(node_key, node_info):
    if node_key == 'JoinNode':
        return JoinNode(node_info)
    elif node_key == 'PivotNode':
        return PivotNode(node_info)
    elif node_key == 'multi-in':
        return ManipulationNode(node_info)
    else:
        return None
