from django.http import JsonResponse
from .models import Workflow, WorkflowException
import networkx as nx
import json
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Initialize a Workflow object
workflow = Workflow()

def open_workflow(request):
    """Opens a workflow.

    If file is specified in GET request, that file is opened.
    Otherwise, a temporary example with 3 nodes is created.

    Args:
        request: Django request Object

    Returns:
        JSON response with data.
    """
    # Extract file name from GET request
    file_path = request.GET.get('file')

    # If no file parameter given, create new graph
    if file_path is None:
        DG = nx.DiGraph()
        DG.add_nodes_from([1, 2, 3])
        DG.add_edges_from([(1, 2), (2, 3)])

        workflow.graph = DG
    # Otherwise, open the file
    else:
        try:
            workflow.file_path = file_path
            workflow.read_json()
        except WorkflowException as e:
            return JsonResponse({
                e.action: e.reason
            })

    # Construct response
    data = {
        'graph': nx.readwrite.json_graph.node_link_data(workflow.graph),
        'nodes': workflow.graph.number_of_nodes(),
    }

    workflow.store_in_session(request)

    return JsonResponse(data)


def save_workflow(request):
    """Saves a workflow to disk.

    Args:
        request: Django request Object

    Returns:
        JSON response with data.
    """

    if workflow.graph is None:
        return JsonResponse({'message': 'No graph exists.'}, status=404)

    workflow.write_json()

    return JsonResponse({
        'message': 'Saved the graph to ' + workflow.file_path + '!'
    })
