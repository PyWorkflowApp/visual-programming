from django.http import JsonResponse
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from pyworkflow import Node

import os
import inspect


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

    # Iterate through node 'types'
    for parent in Node.__subclasses__():
        key = getattr(parent, "display_name", parent.__name__)
        data[key] = list()

        # Iterate through node 'keys'
        for child in parent.__subclasses__():
            # TODO: check attribute-scope is handled correctly
            child_node = {
                'name': child.name,
                'node_key': child.__name__,
                'node_type': parent.__name__,
                'num_in': child.num_in,
                'num_out': child.num_out,
                'color': child.color or parent.color,
                'doc': child.__doc__,
                'options': {k: v.get_value() for k, v in child.options.items()},
                'option_types': child.option_types,
                'download_result':  getattr(child, "download_result", False)
            }

            data[key].append(child_node)

    return JsonResponse(data)


@swagger_auto_schema(method='get',
                     operation_summary='Retrieve a list of custom Nodes',
                     operation_description='Retrieves a list of custom Nodes, in JSON.',
                     responses={
                         200: 'List of installed Nodes, in JSON',
                     })
@api_view(['GET'])
def retrieve_custom_nodes_for_user(request):
    data = dict()

    # TODO: Workflow loading excluded in middleware for this route
    #       Should probably have a way to access the 'custom_node` dir dynamically
    custom_node_path = os.path.join(os.getcwd(), '../pyworkflow/custom_nodes')

    try:
        nodes = os.listdir(custom_node_path)
    except OSError as e:
        return JsonResponse({"message": str(e)}, status=500)

    for node in nodes:
        # Parse file type
        node_name, ext = os.path.splitext(node)

        try:
            package = __import__('custom_nodes.' + node_name)
            module = getattr(package, node_name)
        except ModuleNotFoundError as e:
            # TODO: This will only catch the first missing package. Can we get more?
            data[node_name] = f"Please install missing packages and restart the server. Missing '{e.name}'"
            continue

        for name, klass in inspect.getmembers(module):
            if inspect.isclass(klass) and klass.__module__.startswith('custom_nodes.'):
                custom_node = {
                    'name': klass.name,
                    'node_key': name,
                    'node_type': node_name,
                    'num_in': klass.num_in,
                    'num_out': klass.num_out,
                    'color': klass.color or 'black',
                    'doc': klass.__doc__,
                    'options': {k: v.get_value() for k, v in klass.options.items()},
                    'option_types': klass.option_types,
                    'download_result': getattr(klass, "download_result", False)
                }

                data[node_name] = custom_node

    return JsonResponse(data, safe=False)
