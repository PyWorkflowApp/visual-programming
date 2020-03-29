import json
import csv
import inspect

from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view
from pyworkflow import Workflow, WorkflowException, Node
from drf_yasg.utils import swagger_auto_schema

fs = FileSystemStorage(location=settings.MEDIA_ROOT)


@swagger_auto_schema(method='get',
                     operation_summary='Create a new workflow.',
                     operation_description='Creates a new workflow with empty DiGraph.',
                     responses={
                         200: 'Created new DiGraph'
                     })
@api_view(['GET'])
def new_workflow(request):
    """Create a new workflow.

    Initialize a new, empty, NetworkX DiGraph object and store it in the session.

    Return:
        200 - Created new DiGraph
    """
    # Create new Workflow
    workflow = Workflow()
    # Save to session
    request.session.update(workflow.to_session_dict())
    data = workflow.to_graph_json()
    return JsonResponse(data)


@swagger_auto_schema(method='get',
                     operation_summary='Open workflow from file.',
                     operation_description='Loads a JSON file from disk and translates into Workflow object',
                     responses={
                         200: 'Workflow representation in JSON',
                         400: 'No file specified',
                         404: 'File specified not found or not JSON graph'
                     })
@api_view(['GET'])
def open_workflow(request):
    """Open a workflow.

    If file is specified in GET request, that file is opened.

    Args:
        request: Django request Object

    Returns:
        200 - JSON response with data.
        400 - No file specified
        404 - File specified not found, or not JSON graph
    """
    # If file included in request, extract it
    file_path = request.GET.get('file')
    if file_path is None:
        return JsonResponse({'message': 'File must be specified.'}, status=400)

    # Read info into Workflow object
    try:
        with fs.open(file_path) as file_like:
            workflow = Workflow.from_file(file_like)
    except OSError as e:
        return JsonResponse({'message': e.strerror}, status=404)
    except nx.NetworkXError as e:
        return JsonResponse({'message': str(e)}, status=404)
    except WorkflowException as e:
        return JsonResponse({e.action: e.reason}, status=404)

    # Construct response
    data = {
        'graph': workflow.to_graph_json(),
        'nodes': workflow.graph.number_of_nodes(),
    }

    # Save Workflow info to session
    request.session.update(workflow.to_session_dict())
    return JsonResponse(data)


@swagger_auto_schema(method='post',
                     operation_summary='Save workflow to JSON file',
                     operation_description='Saves workflow to JSON file for download.',
                     responses={
                         200: 'Workflow representation in JSON',
                         400: 'No file specified',
                         404: 'File specified not found or not JSON graph'
                     })
@api_view(['POST'])
def save_workflow(request):
    """Save workflow.

    Saves a workflow to disk.

    Args:
        request: Django request Object

    Returns:
        Downloads JSON file representing graph.
    """
    # Check session for existing graph
    if request.session.get('graph') is None:
        return JsonResponse({'message': 'No graph exists.'}, status=404)

    # Load session data into Workflow object. If successful, return
    # serialized graph
    try:
        workflow = Workflow.from_session(request.session)
        json_str = json.dumps(workflow.to_graph_json())
        response = HttpResponse(json_str, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=%s' % workflow.file_path
        return response
    except WorkflowException as e:
        return JsonResponse({e.action: e.reason}, status=404)


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
        data[parent.__name__] = list()

        # Iterate through node 'keys'
        for child in parent.__subclasses__():
            # TODO: check attribute-scope is handled correctly
            child_node = {
                'name': child.name,
                'key': child.__name__,
                'type': parent.__name__,
                'num_in': child.num_in,
                'num_out': child.num_out,
                'color': child.color,
                'doc': child.__doc__,
            }

            data[parent.__name__].append(child_node)

    return JsonResponse(data)


def retrieve_csv(request, node_id):
    if request.method == 'GET':
        """
        Retrieves a CSV after the associated node execution and returns it as a json.
        Currently just using a demo CSV in workspace. 
        """
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        writer = csv.writer(response)
        writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
        writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

        return response
