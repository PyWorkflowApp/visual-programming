from .node import *


def node_factory(node_info):
    # Create a new Node with info
    # TODO: should perform error-checking or add default values if missing
    node_type = node_info.get('node_type')
    node_key = node_info.get('node_key')

    if node_type == 'IO':
        new_node = io_node(node_key, node_info)
    elif node_type == 'Manipulation':
        new_node = manipulation_node(node_key, node_info)
    else:
        new_node = None

    return new_node


def io_node(node_key, node_info):
    if node_key == 'read-csv':
        return ReadCsvNode(node_info)
    elif node_key == 'write-csv':
        return WriteCsvNode(node_info)
    else:
        return None


def manipulation_node(node_key, node_info):
    if node_key == 'join':
        return JoinNode(node_info)
    elif node_key == 'pivot':
        return PivotNode(node_info)
    elif node_key == 'multi-in':
        return ManipulationNode(node_info)
    else:
        return None
