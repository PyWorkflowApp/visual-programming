from django.http import JsonResponse
import networkx as nx
import json

from .models import Node
from workflow.models import Workflow, WorkflowException


def node(request):
    """ Add new Node to graph

    """

    # Load workflow from session
    workflow = Workflow()
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


def handle_node(request, node_id):
    """ Retrieve a Node from the graph

    Returns:
        200 - Node was found; data in JSON format
        404 - Graph or Node does not exist
        405 - Method not allowed
        500 - Error processing Node change
    """

    # Load workflow from session
    workflow = Workflow()
    workflow.retrieve_from_session(request)

    # Check if a graph is present
    if workflow.graph is None:
        return JsonResponse({
            'message': 'A workflow has not been created yet.'
        }, status=404)

    # Check if the graph contains the requested Node
    if workflow.graph.has_node(node_id) is not True:
        return JsonResponse({
            'message': 'The workflow does not contain node id ' + str(node_id)
        }, status=404)

    # Process request
    try:
        # Retrieve node - reads in as Dict
        # TODO: translate to Node class for more complex methods
        node = workflow.graph.nodes[node_id]

        if request.method == 'GET':
            return JsonResponse(node)
        elif request.method == 'DELETE':
            workflow.remove_node(node)
            return JsonResponse({
                'message': 'Removed node ID #' + str(node['node_id'])
            })
        else:
            return JsonResponse({
                'message': request.method + ' not yet handled.'
            }, status=405)
    except WorkflowException as e:
        return JsonResponse(e, status=500)
