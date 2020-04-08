from django.http import JsonResponse
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from pyworkflow import Node


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
                'options': {**parent.DEFAULT_OPTIONS, **child.DEFAULT_OPTIONS},
                'option_types': getattr(child, "OPTION_TYPES", dict()),
                'download_result':  getattr(child, "download_result", False)
            }

            data[key].append(child_node)

    return JsonResponse(data)