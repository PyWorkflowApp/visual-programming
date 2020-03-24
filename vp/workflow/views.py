from django.http import JsonResponse
from .models import Workflow, WorkflowException
import networkx as nx
import json
import os

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

def retrieve_nodes_for_user(request):
    if request.method =='GET':
        """
        Retrieve all nodes that a user can have access to in the IDE.
        Currently returning default set of nodes. 
        //TODO pick these node files from a file in the system.
        """
        data = {
            "I/O": [
                {"key": "read-csv", "name": "Read CSV", "numPortsIn": 0, "color": "black"}
            ],
            "Manipulation": [
                {"key": "filter", "name": "Filter Rows", "color": "red"},
                {"key": "pivot", "name": "Pivot Table", "color": "blue"},
                {"key": "multi-in", "name": "Multi-Input Example", "numPortsIn": 3, "color": "green"}
            ]
        }
        return JsonResponse(data, safe=False)