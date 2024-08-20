import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pyworkflow import WorkflowException, NodeException, ParameterValidationError, node_factory
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
    # Extract request info for node creation
    try:
        new_node = create_node(request)
    except NodeException as e:
        return JsonResponse({e.action: e.reason}, status=400)

    # If None, create_node failed
    if new_node is None:
        return JsonResponse({
            'message': 'Missing required Node information'
        }, status=400)

    # Check Node is unique in the graph
    if new_node.is_global:
        node_exists = request.pyworkflow.get_flow_var(new_node.node_id)
    else:
        node_exists = request.pyworkflow.get_node(new_node.node_id)

    if node_exists:
        return JsonResponse({
            'message': 'A %s with id %s already exists in the graph.' % (
                'flow variable' if new_node.is_global else 'node',
                new_node.node_id
            )
        }, status=400)

    # Add to the graph
    try:
        request.pyworkflow.update_or_add_node(new_node)
    except WorkflowException as e:
        return JsonResponse({e.action: e.reason}, status=400)

    return JsonResponse({
        'message': 'Added new %s to graph with id: %s' % (
            'flow variable' if new_node.is_global else 'node',
            new_node.node_id
        )
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
    """Add new edge to the graph

    Creates a new edge from node_from_id to node_to_id.
    """
    # Check if the graph contains the requested Node
    node_from = request.pyworkflow.get_node(node_from_id)
    node_to = request.pyworkflow.get_node(node_to_id)

    if node_from is None or node_to is None:
        return JsonResponse({
            'message': 'The workflow does not contain the node(s) requested.'
        }, status=404)

    try:
        if request.method == 'POST':
            response = JsonResponse({
                'edge_added': request.pyworkflow.add_edge(node_from, node_to)
            })
        elif request.method == 'DELETE':
            response = JsonResponse({
                'removed_edge': request.pyworkflow.remove_edge(node_from, node_to)
            })
        else:
            return JsonResponse({
                'message': request.method + ' not yet handled.'
            }, status=405)
    except WorkflowException as e:
        return JsonResponse({e.action: e.reason}, status=500)

    return response


@swagger_auto_schema(method='get',
                     operation_summary='Retrieve a node from the graph',
                     operation_description='Retrieves a node from the graph.',
                     responses={
                         200: 'JSON response with data',
                         400: 'No file specified',
                         404: 'Node/graph not found'
                     })
@swagger_auto_schema(method='patch',
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
@api_view(['GET', 'PATCH', 'DELETE'])
@csrf_exempt
def handle_node(request, node_id):
    """Retrieve, update, or delete a Node from the graph

    Returns:
        200 - Node was found; data in JSON format
        404 - Graph or Node does not exist
        405 - Method not allowed
        500 - Error processing Node change
    """
    # Retrieve the global or local Node
    if request.path_info.startswith('/node/global/'):
        retrieved_node = request.pyworkflow.get_flow_var(node_id)
    else:
        retrieved_node = request.pyworkflow.get_node(node_id)

    if retrieved_node is None:
        return JsonResponse({
            'message': 'The workflow does not contain node id ' + str(node_id)
        }, status=404)

    # Process request
    try:
        if request.method == 'GET':
            response = JsonResponse({
                "retrieved_node": retrieved_node.to_json(),
                "flow_variables": request.pyworkflow.get_all_flow_var_options(node_id),
            }, safe=False)
        elif request.method == 'PATCH':
            updated_node = create_node(request)

            # Nodes need to be the same type to update
            if type(retrieved_node) != type(updated_node):
                return JsonResponse({
                    'message': 'Node types do not match. Need correct info.',
                    'retrieved_node': str(type(retrieved_node)),
                    'updated_node': str(type(updated_node)),
                }, status=500)

            # Nodes need to be the same type to update
            if retrieved_node.is_global != updated_node.is_global:
                return JsonResponse({
                    'message': 'Node scopes do not match. Need correct info.',
                    'retrieved_node': str(retrieved_node.is_global),
                    'updated_node': str(updated_node.is_global),
                }, status=500)

            # Validation raises exception if failed
            updated_node.validate()

            request.pyworkflow.update_or_add_node(updated_node)
            response = JsonResponse(updated_node.to_json(), safe=False)
        elif request.method == 'DELETE':
            request.pyworkflow.remove_node(retrieved_node)
            response = JsonResponse({
                'message': 'Removed node ID #' + str(retrieved_node.node_id)
            })
        else:
            return JsonResponse({
                'message': request.method + ' not yet handled.'
            }, status=405)
    except (NodeException, WorkflowException) as e:
        return JsonResponse({e.action: e.reason}, status=500)
    except ParameterValidationError as e:
        return JsonResponse({'message': str(e)}, status=500)

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

    Uses Workflow to handle preceding Nodes and reading/writing data. Returns
    an updated Node, with the filename for any new data written to disk stored
    in the 'data' attribute, for later access.
    """
    try:
        # Use Workflow to load preceding Node data and execute
        executed_node = request.pyworkflow.execute(node_id)

        # Save executed Node, with new data, back to Workflow
        request.pyworkflow.update_or_add_node(executed_node)

        return JsonResponse({
            'message': 'Node Execution successful!',
            'data_file': executed_node.data,
        }, safe=False)
    except (NodeException, WorkflowException) as e:
        return JsonResponse({e.action: e.reason}, status=500)


@swagger_auto_schema(method='get',
                     operation_summary='Gets the data frame at the executed node.',
                     operation_description='Retrieves the state of data at that point in the graph.',
                     responses={
                         200: 'Data successfully retrieved'
                     })
@api_view(['GET'])
def retrieve_data(request, node_id):
    try:
        node_to_retrieve = request.pyworkflow.get_node(node_id)
        data = request.pyworkflow.retrieve_node_data(node_to_retrieve)
        return JsonResponse(data, safe=False, status=200)
    except WorkflowException as e:
        return JsonResponse({e.action: e.reason}, status=500)


def create_node(request):
    """Pass all request info to Node Factory.

    """
    # Any filenames/paths passed through as-is
    # A Workflow-specific path is constructed at execution
    json_data = json.loads(request.body)

    try:
        return node_factory(json_data)
    except OSError as e:
        return JsonResponse({'message': e.strerror}, status=404)
    except NodeException as e:
        return JsonResponse({e.action: e.reason}, status=400)
