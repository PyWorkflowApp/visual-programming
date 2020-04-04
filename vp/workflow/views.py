import json
import csv
import inspect

from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.decorators import api_view
from pyworkflow import Workflow, WorkflowException
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
    request.pyworkflow = Workflow()
    request.session.update(request.pyworkflow.to_session_dict())

    return JsonResponse(request.pyworkflow.to_graph_json())


@swagger_auto_schema(method='post',
                     operation_summary='Open workflow from file.',
                     operation_description='Loads a JSON file from disk and translates into Workflow object and JSON object of front-end',
                     responses={
                         200: 'Workflow representation in JSON',
                         400: 'No file specified',
                         404: 'File specified not found or not JSON graph'
                     })
@api_view(['POST'])
def open_workflow(request):
    """Open a workflow.

    User uploads a JSON file to the front-end that passes JSON data to be
    parsed and validated on the back-end.

    Args:
        request: Django request Object, should follow the pattern:
            {
                react: {react-diagrams JSON},
                networkx: {networkx graph as JSON},
            }

    Raises:
        JSONDecodeError: invalid JSON data
        KeyError: request missing either 'react' or 'networkx' data
        WorkflowException: error loading JSON into NetworkX DiGraph

    Returns:
        200 - JSON response with data.
        400 - No file specified
        404 - File specified not found, or not JSON graph
        500 - Missing JSON data or
    """
    try:
        # If multi-part form-data, use this
        # TODO: file is parsed into JSON in memory;
        #       may want to save to 'fs' for large files
        uploaded_file = request.FILES['file']
        combined_json = json.load(uploaded_file)

        # If file is passed in as raw JSON, use this
        # combined_json = json.loads(request.body)

        request.pyworkflow = Workflow.from_request(combined_json['networkx'])
        request.session.update(request.pyworkflow.to_session_dict())
        react = combined_json['react']
    except KeyError as e:
        return JsonResponse({'open_workflow': 'Missing data for ' + str(e)}, status=500)
    except json.JSONDecodeError as e:
        return JsonResponse({'No React JSON provided': str(e)}, status=500)
    except WorkflowException as e:
        return JsonResponse({e.action: e.reason}, status=404)

    # Construct response
    return JsonResponse({
        'react': react,
        'networkx': request.pyworkflow.to_graph_json(),
    })


@swagger_auto_schema(method='post',
                     operation_summary='Save workflow to JSON file',
                     operation_description='Saves workflow to JSON file for download.',
                     responses={
                         200: 'Workflow representation in JSON',
                         400: 'No file specified',
                         404: 'File specified not found or not JSON graph',
                         500: 'No valid JSON in request body'
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
    # Load session data into Workflow object. If successful, return
    # serialized graph
    try:
        combined_json = json.dumps({
            'react': json.loads(request.body),
            'networkx': request.pyworkflow.to_graph_json(),
            'filename': request.pyworkflow.file_path
        })

        return HttpResponse(combined_json, content_type='application/json')
    except json.JSONDecodeError as e:
        return JsonResponse({'No React JSON provided': str(e)}, status=500)
    except WorkflowException as e:
        return JsonResponse({e.action: e.reason}, status=404)


@swagger_auto_schema(method='get',
                     operation_summary='Retrieve sorted list of node execution.',
                     operation_description='Retrieves a list of nodes, sorted in execution order.',
                     responses={
                         200: 'List of nodes, sorted in execution order.',
                         404: 'No graph exists.',
                         500: 'Error generating the topological sort for the graph.'
                     })
@api_view(['GET'])
def execute_workflow(request):
    """Execute workflow.

    Generates a list of all nodes in the NetworkX DiGraph topologically sorted.

    Returns:
        List of nodes, sorted in execution order.
    """
    try:
        order = request.pyworkflow.execution_order()
    except WorkflowException as e:
        return JsonResponse({e.action: e.reason}, status=500)

    return JsonResponse(order, safe=False)

@swagger_auto_schema(method='get',
                     operation_summary='Retrieve sorted list of successors from a node.',
                     operation_description='Retrieves a list of successor nodes, sorted in execution order.',
                     responses={
                         200: 'List of successor nodes, sorted in execution order.',
                         404: 'No graph exists.',
                         500: 'Error retrieving list of successors for the graph.'
                     })
@api_view(['GET'])
def get_successors(request, node_id):
    """Get sorted list of Node successors.

    Generates a list of all nodes in the NetworkX DiGraph topologically sorted.

    Returns:
        List of nodes, sorted in execution order.
    """
    try:
        order = request.pyworkflow.get_node_successors(node_id)
    except WorkflowException as e:
        return JsonResponse({e.action: e.reason}, status=500)

    return JsonResponse(order, safe=False)


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

@swagger_auto_schema(method='post',
                     operation_summary='Uploads a file to server.',
                     operation_description='Uploads a new file to server location.',
                     responses={
                         200: 'File uploaded',
                         404: 'No specified file'
                     })
@api_view(['POST'])
def upload_file(request):
    if 'file' not in request.data:
        return JsonResponse("Empty content", status=404)

    f = request.data['file']

    fs.save(f.name, f)

    return JsonResponse("File Uploaded", status=201, safe=False)