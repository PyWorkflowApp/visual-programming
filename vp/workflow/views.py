from json import JSONDecodeError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Workflow, WorkflowException
import networkx as nx
import json, csv
import os
from django.http import HttpResponse


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def new_workflow(request):
    """ Create a new workflow.

    Initialize a new, empty, NetworkX DiGraph object and store it in
    the session

    Return:
        200 - Created new DiGraph
    """
    # Create new NetworkX graph
    DG = nx.DiGraph()
    json_graph = nx.readwrite.json_graph.node_link_data(DG)

    # Construct response
    data = {
        'graph': json_graph,
        'nodes': DG.number_of_nodes(),
    }

    # Save to session
    request.session['graph'] = json_graph
    return JsonResponse(data)


def open_workflow(request):
    """Opens a workflow.

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

    # Create Workflow to store info
    workflow = Workflow()

    # Read info into Workflow object
    try:
        workflow.file_path = file_path
        workflow.graph = workflow.read_json()
    except OSError as e:
        return JsonResponse({'message': e.strerror}, status=404)
    except nx.NetworkXError as e:
        return JsonResponse({'message': str(e)}, status=404)
    except WorkflowException as e:
        return JsonResponse({e.action: e.reason}, status=404)

    # Construct response
    data = {
        'graph': nx.readwrite.json_graph.node_link_data(workflow.graph),
        'nodes': workflow.graph.number_of_nodes(),
    }

    # Save Workflow info to session
    workflow.store_in_session(request)
    return JsonResponse(data)


def save_workflow(request):
    """Saves a workflow to disk.

    Args:
        request: Django request Object

    Returns:
        JSON response with data.
    """
    # Check session for existing graph
    if request.session['graph'] is None:
        return JsonResponse({'message': 'No graph exists.'}, status=404)

    # Load session data into Workflow object
    workflow = Workflow()
    try:
        workflow.retrieve_from_session(request)
        # Write to disk
        workflow.write_json()
    except WorkflowException as e:
        return JsonResponse({e.action: e.reason}, status=404)

    return JsonResponse({
        'message': 'Saved the graph to ' + workflow.file_path + '!'
    })

def retrieve_nodes_for_ide(request):
    if request.method == 'GET':
        """Retrieve all nodes that a user can have access to in the IDE from a specified file in request body.
        
        Args:
            request: Django request Object
       
         Returns:
            200 - JSON response with data.
            400 - No file specified/issues reading json file.
            404 - File specified not found, or not JSON graph.
        """
        try:
            request_body = json.loads(request.body)
            file_to_load = request_body['file']
            if file_to_load is None:
                return JsonResponse({'message': 'Please specify nodes file.'}, status=400)
            elif not os.path.exists(file_to_load):
                return JsonResponse({'message': 'Unable to locate nodes file.'}, status=404)
            with open(file_to_load) as f:
                data = json.load(f)
        except OSError as e:
            return JsonResponse({e.action: e.reason}, status=404)
        except JSONDecodeError as e:
            return JsonResponse({'message': 'Issues decoding json.'}, status=400)
        
        return JsonResponse(data, safe=False, status=200)

@csrf_exempt
def save_nodes_for_ide(request):
    if request.method == 'POST':
        """Saves all nodes that a user can have access to in the IDE to a specified file in request body.

        Args:
            request: Django request Object

         Returns:
            200 - JSON response with data.
            400 - No file specified, no nodes specified or issues reading json file.
            404 - I/O issues
        """
        try:
            request_body = json.loads(request.body)
            file_to_save = request_body['file']
            data_to_save = request_body['nodes']
            if file_to_save is None:
                return JsonResponse({'message': 'Please specify nodes file.'}, status=400)
            if data_to_save is None:
                return JsonResponse({'message': 'Please specify nodes to be saved.'}, status=400)

            with open(file_to_save, 'w') as outfile:
               json.dump(data_to_save, outfile)

        except OSError as e:
            return JsonResponse({e.action: e.reason}, status=404)
        except JSONDecodeError as e:
            return JsonResponse({'message': 'Issues decoding json.'}, status=400)

    return JsonResponse({'message': 'Nodes saved.'}, status=200)

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