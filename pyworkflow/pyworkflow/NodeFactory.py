from .node import *


def node_factory(node_info):
    # Create a new Node with info
    # TODO: should perform error-checking or add default values if missing
    if node_info['node_type'] == 'IO':
        new_node = io_node(node_info)
    elif node_info['node_type'] == 'Manipulation':
        new_node = manipulation_node(node_info)
    else:
        new_node = None

    return new_node


def io_node(node_info):
    if node_info['node_key'] == 'read-csv':
        return ReadCsvNode(node_info)
    elif node_info['node_key'] == 'write-csv':
        return WriteCsvNode(node_info)
    else:
        return None


def manipulation_node(node_info):
    if node_info['node_key'] == 'filter':
        return ManipulationNode(node_info)
    elif node_info['node_key'] == 'pivot':
        return ManipulationNode(node_info)
    elif node_info['node_key'] == 'multi-in':
        return ManipulationNode(node_info)
    else:
        return None
