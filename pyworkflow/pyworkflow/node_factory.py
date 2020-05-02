from .nodes import *
import importlib


def node_factory(node_info):
    # Create a new Node with info
    # TODO: should perform error-checking or add default values if missing
    node_type = node_info.get('node_type')
    node_key = node_info.get('node_key')

    if node_type == 'io':
        new_node = io_node(node_key, node_info)
    elif node_type == 'manipulation':
        new_node = manipulation_node(node_key, node_info)
    elif node_type == 'flow_control':
        new_node = flow_node(node_key, node_info)
    elif node_type == 'visualization':
        new_node = visualization_node(node_key, node_info)
    else:
        new_node = custom_node(node_key, node_info)

    return new_node


def flow_node(node_key, node_info):
    if node_key == 'StringNode':
        return StringNode(node_info)
    elif node_key == 'IntegerNode':
        return IntegerNode(node_info)
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
    elif node_key == 'FilterNode':
        return FilterNode(node_info)
    else:
        return None


def visualization_node(node_key, node_info):
    if node_key == 'GraphNode':
        return GraphNode(node_info)
    else:
        return None


def custom_node(node_key, node_info):
    try:
        filename = node_info.get('filename')
        module = importlib.import_module(f'pyworkflow.nodes.custom_nodes.{filename}')
        my_class = getattr(module, node_key)
        instance = my_class(node_info)

        return instance
    except Exception as e:
        print(str(e))
        return None
