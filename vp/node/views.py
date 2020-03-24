from django.http import JsonResponse
import networkx as nx
import json

from .models import Node
from workflow.models import Workflow, WorkflowException


def node(request):
    """ Add new Node to graph

    Returns:
        200 - New Node was added to the graph
        400 - Node with 'id' already exists in the graph
        404 - Graph or Node does not exist
    """

    # Load workflow from session
    workflow = Workflow()
    workflow.retrieve_from_session(request)

    # Check if a graph is present
    if workflow.graph is None:
        return JsonResponse({
            'message': 'A workflow has not been created yet.'
        }, status=404)

    # Extract request info for node creation
    # TODO: info is passed via GET, not POST, for easier testing
    node_id = request.GET.get('id')
    node_type = request.GET.get('type')
    num_in = request.GET.get('numPortsIn')
    num_out = request.GET.get('numPortsOut')

    if workflow.get_node(node_id) is not None:
        return JsonResponse({
            'message': 'A node with id %s already exists in the graph.' % node_id
        }, status=400)

    # Create a new Node with info
    # TODO: should perform error-checking or add default values if missing
    new_node = Node(node_id=node_id,
                    node_type=node_type,
                    num_ports_in=num_in,
                    num_ports_out=num_out)

    # Add Node to graph and re-save workflow to session
    workflow.add_node(new_node)
    workflow.store_in_session(request)

    return JsonResponse({
        'message': 'Added new node to graph with id: %s' % (node_id)
    })


def edge(request, node_from_id, node_to_id):
    """ Add new edge to the graph

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
    node_from = workflow.get_node(node_from_id)
    node_to = workflow.get_node(node_to_id)

    if node_from is None or node_to is None:
        return JsonResponse({
            'message': 'The workflow does not contain the node(s) requested.'
        }, status=404)

    # Add Edge between the Nodes to the graph and re-save workflow to session
    workflow.add_edge(node_from, node_to)
    workflow.store_in_session(request)

    return JsonResponse({
        'message': 'Added new edge to graph from node %s to node %s' %
                   (node_from.node_id, node_to.node_id)
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
    node = workflow.get_node(node_id)

    if node is None:
        return JsonResponse({
            'message': 'The workflow does not contain node id ' + str(node_id)
        }, status=404)

    # Process request
    try:
        if request.method == 'GET':
            # Node class is not JSON serializable, so pass in __dict__
            return JsonResponse(node.__dict__, safe=False)
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
