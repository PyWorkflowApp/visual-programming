from django.http import JsonResponse
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from pyworkflow import Node
from modulefinder import ModuleFinder

import os
import inspect
import sys


@swagger_auto_schema(method='get', responses={200:'JSON response with data'})
@api_view(['GET'])
def info(request):
    """Retrieve app info.

       Args:
           request: Django request Object

       Returns:
           200 - JSON response with data.
       """
    data = {
        "application": "visual_programming",
        "version": "negative something",
        "about": "super-duper workflows!"
    }
    return JsonResponse(data)


@swagger_auto_schema(method='get',
                     operation_summary='Retrieve a list of installed Nodes',
                     operation_description='Retrieves a list of installed Nodes, in JSON.',
                     responses={
                         200: 'List of installed Nodes, in JSON',
                     })
@api_view(['GET'])
def retrieve_nodes_for_user(request):
    """Assembles list of Nodes accessible to workflows.

    Retrieve a list of classes from the Node module in `pyworkflow`.
    List is split into 'types' (e.g., 'IO' and 'Manipulation') and
    'keys', or individual command Nodes (e.g., 'ReadCsv', 'Pivot').
    """
    data = dict()

    # Iterate through installed Nodes
    for parent in Node.__subclasses__():
        key = getattr(parent, "display_name", parent.__name__)
        data[key] = list()

        # Iterate through node 'keys'
        for child in parent.__subclasses__():
            node = extract_node_info(parent, child)
            data[key].append(node)

    # Check for any installed Custom Nodes
    # TODO: Workflow loading excluded in middleware for this route
    #       Should probably have a way to access the 'custom_node` dir dynamically
    custom_node_path = os.path.join(os.getcwd(), '../pyworkflow/custom_nodes')
    data['CustomNode'] = import_custom_node(custom_node_path)

    return JsonResponse(data)


def check_missing_packages(node_path):
    finder = ModuleFinder(node_path)
    finder.run_script(node_path)

    uninstalled = list()
    for missing_package in finder.badmodules.keys():
        if missing_package not in sys.modules:
            uninstalled.append(missing_package)

    return uninstalled


def extract_node_info(parent, child):
    # TODO: check attribute(s) accessing is handled correctly
    return {
        'name': child.name,
        'node_key': child.__name__,
        'node_type': str(parent),
        'num_in': child.num_in,
        'num_out': child.num_out,
        'color': child.color or parent.color or 'black',
        'doc': child.__doc__,
        'options': {k: v.get_value() for k, v in child.options.items()},
        'option_types': child.option_types,
        'download_result': getattr(child, "download_result", False)
    }


def import_custom_node(root_path):
    # Get list of files in path
    try:
        files = os.listdir(root_path)
    except OSError as e:
        return None

    data = list()
    for file in files:
        # Check file is not a dir
        node_path = os.path.join(root_path, file)
        if not os.path.isfile(node_path):
            continue

        node, ext = os.path.splitext(file)

        try:
            package = __import__('custom_nodes.' + node)
            module = getattr(package, node)
        except ModuleNotFoundError:
            data.append({
                "name": node,
                "missing_packages": check_missing_packages(node_path)
            })
            continue

        for name, klass in inspect.getmembers(module):
            if inspect.isclass(klass) and klass.__module__.startswith('custom_nodes.'):
                custom_node = extract_node_info(node, klass)
                data.append(custom_node)

    return data


