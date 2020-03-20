from django.http import JsonResponse
import networkx as nx
import json

from .models import Node
from workflow.models import Workflow, WorkflowException

workflow = Workflow()


def node(request):
    """ Add new Node to graph

    """

    # Load workflow from session
    workflow.retrieve_from_session(request)

    # Check if a graph is present
    if workflow.graph is None:
        return JsonResponse({
            'message': 'A workflow has not been created yet.'
        }, status=404)

    # Create a new Node with POST info
    # TODO: id is num + 1; rest of info is hard-coded
    num_nodes = workflow.graph.number_of_nodes()
    node_id = num_nodes + 1
    new_node = Node(node_id=node_id, node_type="blank", num_ports_in=1, num_ports_out=1)

    # Add Node to graph and re-save workflow to session
    workflow.add_node(new_node)
    workflow.store_in_session(request)

    return JsonResponse({
        'message': 'Added new node to graph with ID #' + str(num_nodes + 1)
    })
