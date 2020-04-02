from .node import *


def node_factory(payload):
    # Create a new Node with info
    # TODO: should perform error-checking or add default values if missing
    node_info = payload["node_info"]
    node_config = payload["config"]
    node_type = node_info.get('node_type')
    node_key = node_info.get('node_key')

    if node_type == 'IONode':
        new_node = io_node(node_key, node_info, node_config)
    elif node_type == 'ManipulationNode':
        new_node = manipulation_node(node_key, node_info, node_config)
    else:
        new_node = None

    return new_node


def io_node(node_key, node_info, node_config):
    if node_key == 'ReadCsvNode':
        return ReadCsvNode(node_info, node_config)
    elif node_key == 'WriteCsvNode':
        return WriteCsvNode(node_info, node_config)
    else:
        return None


def manipulation_node(node_key, node_info, node_config):
    if node_key == 'JoinNode':
        return JoinNode(node_info, node_config)
    elif node_key == 'PivotNode':
        return PivotNode(node_info, node_config)
    elif node_key == 'multi-in':
        return ManipulationNode(node_info, node_config)
    else:
        return None
