import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pyworkflow import Workflow, WorkflowException, Node, NodeException, node_factory
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(method='post',
                     operation_summary='Add a node to the graph',
                     operation_description='Adds a node to the graph.',
                     responses={
                         200: 'Node added to graph',
                         400: 'Node with id already exists in graph, or missing info',
                         404: 'Node/graph not found'
                     })
@api_view(['POST'])
@csrf_exempt
def node(request):
    """ Add new Node to graph

    Adds a new node with specified data to the graph.

    Returns:
        200 - New Node was added to the graph
        400 - Missing info; Node with 'id' already exists in the graph
        404 - Graph or Node does not exist
        405 - Method not allowed
    """
    # Load workflow from session
    workflow = Workflow.from_session(request.session)

    # Check if a graph is present
    if workflow.graph is None:
        return JsonResponse({
            'message': 'A workflow has not been created yet.'
        }, status=404)

    # Extract request info for node creation
    new_node = create_node(request.body)

    # If None, create_node failed
    if new_node is None:
        return JsonResponse({
            'message': 'Missing required Node information'
        }, status=400)

    # Check node_id is unique in graph
    if workflow.get_node(new_node.node_id) is not None:
        return JsonResponse({
            'message': 'A node with id %s already exists in the graph.' % new_node.node_id
        }, status=400)

    # Add Node to graph and re-save workflow to session
    workflow.update_or_add_node(new_node)
    request.session.update(workflow.to_session_dict())

    return JsonResponse({
        'message': 'Added new node to graph with id: %s' % new_node.node_id
    })


@swagger_auto_schema(method='post',
                     operation_summary='Add an edge to the graph',
                     operation_description='Adds an edge to the graph.',
                     responses={
                         200: 'Added edge to graph',
                         404: 'Workflow not created yet/Workflow does not contain specified node',
                         500: 'Error processing Edge request in NetworkX'
                     })
@swagger_auto_schema(method='delete',
                     operation_summary='Remove an edge from the graph',
                     operation_description='Removes an edge from the graph.',
                     responses={
                         200: 'Removed edge from graph',
                         404: 'Workflow not created yet/Workflow does not contain specified node',
                         500: 'Error processing Edge request in NetworkX'
                     })
@api_view(['POST', 'DELETE'])
def handle_edge(request, node_from_id, node_to_id):
    """ Add new edge to the graph

        Creates a new edge from node_from_id to node_to_id.
    """
    # Load workflow from session
    workflow = Workflow.from_session(request.session)

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

    try:
        if request.method == 'POST':
            response = JsonResponse({
                'edge_added': workflow.add_edge(node_from, node_to)
            })
        elif request.method == 'DELETE':
            response = JsonResponse({
                'removed_edge': workflow.remove_edge(node_from, node_to)
            })
        else:
            return JsonResponse({
                'message': request.method + ' not yet handled.'
            }, status=405)
    except WorkflowException as e:
        return JsonResponse({e.action: e.reason}, status=500)

    # Re-save workflow to session
    request.session.update(workflow.to_session_dict())

    return response


@swagger_auto_schema(method='get',
                     operation_summary='Retrieve a node from the graph',
                     operation_description='Retrieves a node from the graph.',
                     responses={
                         200: 'JSON response with data',
                         400: 'No file specified',
                         404: 'Node/graph not found'
                     })
@swagger_auto_schema(method='post',
                     operation_summary='Update a node from the graph',
                     operation_description='Updates a node from the graph.',
                     responses={
                         200: 'JSON response with data',
                         400: 'No file specified',
                         404: 'Node/graph not found'
                     })
@swagger_auto_schema(method='delete',
                     operation_summary='Delete a node from the graph',
                     operation_description='Deletes a node from the graph.',
                     responses={
                         200: 'JSON response with data',
                         400: 'No file specified',
                         404: 'Node/graph not found',
                         405: 'Method not allowed',
                         500: 'Error processing Node change'
                     })
@api_view(['GET', 'POST', 'DELETE'])
@csrf_exempt
def handle_node(request, node_id):
    """ Retrieve, update, or delete a Node from the graph

    Returns:
        200 - Node was found; data in JSON format
        404 - Graph or Node does not exist
        405 - Method not allowed
        500 - Error processing Node change
    """
    # Load workflow from session
    workflow = Workflow.from_session(request.session)

    # Check if a graph is present
    if workflow.graph is None:
        return JsonResponse({
            'message': 'A workflow has not been created yet.'
        }, status=404)

    # Check if the graph contains the requested Node
    retrieved_node = workflow.get_node(node_id)

    if retrieved_node is None:
        return JsonResponse({
            'message': 'The workflow does not contain node id ' + str(node_id)
        }, status=404)

    # Process request
    # Node class not JSON serializable; pass __dict__ to response for display
    try:
        if request.method == 'GET':
            response = JsonResponse(retrieved_node.__dict__, safe=False)
        elif request.method == 'POST':
            updated_node = create_node(request.body)

            # Nodes need to be the same type to update
            if type(retrieved_node) != type(updated_node):
                return JsonResponse({
                    'message': 'Node types do not match. Need correct info.',
                    'retrieve_node': str(type(retrieved_node)),
                    'updated_node': str(type(updated_node)),
                }, status=500)

            workflow.update_or_add_node(updated_node)
            response = JsonResponse(updated_node.__dict__, safe=False)
        elif request.method == 'DELETE':
            workflow.remove_node(retrieved_node)
            response = JsonResponse({
                'message': 'Removed node ID #' + str(retrieved_node.node_id)
            })
        else:
            return JsonResponse({
                'message': request.method + ' not yet handled.'
            }, status=405)
    except WorkflowException as e:
        return JsonResponse({e.action: e.reason}, status=500)
    except NodeException as e:
        return JsonResponse({e.action: e.reason}, status=500)

    # Save any changes back to session
    request.session.update(workflow.to_session_dict())
    return response


@swagger_auto_schema(method='get',
                     operation_summary='Execute a node in the graph.',
                     operation_description='Executes a node in the graph.',
                     responses={
                         200: 'Node successfully executed',
                         404: 'Workflow not created yet/Workflow does not contain specified node'
                     })
@api_view(['GET'])
def execute_node(request, node_id):
    """Execute the specified node

    """
    # Load workflow from session
    workflow = Workflow.from_session(request.session)

    # Check if the graph contains the requested Node
    node_to_execute = workflow.get_node(node_id)

    if node_to_execute is None:
        return JsonResponse({
            'message': 'The workflow does not contain node id ' + str(node_id)
        }, status=404)

    # Execute node
    try:
        node_to_execute.execute()
        return JsonResponse({
            'message': 'Node Execution successful!',
            'node_type': node_to_execute.node_type,
            'data': node_to_execute.data,
        }, safe=False)
    except NodeException as e:
        return JsonResponse({e.action: e.reason}, status=500)


def create_node(node_info):
    """Pass all request info to Node Factory.

    """
    json_data = json.loads(node_info)

    try:
        return node_factory(json_data)
    except OSError as e:
        return JsonResponse({'message': e.strerror}, status=404)
    except NodeException as e:
        return JsonResponse({e.action: e.reason}, status=400)
