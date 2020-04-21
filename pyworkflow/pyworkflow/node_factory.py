from .node import *


def node_factory(node_info):
    # Create a new Node with info
    # TODO: should perform error-checking or add default values if missing
    node_type = node_info.get('node_type')
    node_key = node_info.get('node_key')

    if node_type == 'IONode':
        new_node = io_node(node_key, node_info)
    elif node_type == 'ManipulationNode':
        new_node = manipulation_node(node_key, node_info)
    elif node_type == 'FlowNode':
        new_node = flow_node(node_key, node_info)
    else:
        new_node = custom_node(node_type, node_key, node_info)

    return new_node


def flow_node(node_key, node_info):
    if node_key == 'StringNode':
        return StringNode(node_info)
    else:
        return None


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
    elif node_key == 'FilterNode':
        return FilterNode(node_info)
    else:
        return None


def custom_node(filename, node_key, node_info):
    try:
        package = __import__('custom_nodes.' + filename)
        module = getattr(package, filename)
        my_class = getattr(module, node_key)
        instance = my_class(node_info)

        return instance
    except Exception as e:
        print(str(e))
        return None
