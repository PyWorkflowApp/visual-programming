from django.http import JsonResponse

from pyworkflow import Workflow, WorkflowException, node_factory, NodeException


def node(request):
    """ Add new Node to graph

    Returns:
        200 - New Node was added to the graph
        400 - Node with 'id' already exists in the graph
        404 - Graph or Node does not exist
    """

    # Load workflow from session
    workflow = Workflow.from_session(request.session)
    # Check if a graph is present
    if workflow.graph is None:
        return JsonResponse({
            'message': 'A workflow has not been created yet.'
        }, status=404)

    # Extract request info for node creation
    # TODO: info is passed via GET, not POST, for easier testing
    new_node = create_node(request)

    if workflow.get_node(new_node.node_id) is not None:
        return JsonResponse({
            'message': 'A node with id %s already exists in the graph.' % new_node.node_id
        }, status=400)

    # Add Node to graph and re-save workflow to session
    workflow.add_node(new_node)
    request.session.update(workflow.to_session_dict())

    return JsonResponse({
        'message': 'Added new node to graph with id: %s' % (new_node.node_id)
    })


def edge(request, node_from_id, node_to_id):
    """ Add new edge to the graph

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

    # Add Edge between the Nodes to the graph and re-save workflow to session
    workflow.add_edge(node_from, node_to)
    request.session.update(workflow.to_session_dict())

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
    workflow = Workflow.from_session(request.session)
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


def create_node(request):
    """Pass all request info to Node Factory.

    Not all Nodes require a file path, but to keep storage/retrieval logic on
    the Django-side, it tests the file before sending to the Factory. This
    functionality may change, especially as we consider how we upload files to
    the server. Also, no test needed if a 'Write CSV' node as a file will be
    created, but occurs anyway.

    TODO: Currently a GET request for easier testing. Should be a POST request.
    """
    node_info = {
        'node_type': request.GET.get('type'),
        'node_key': request.GET.get('key'),
        'node_id': request.GET.get('id'),
        'num_in': request.GET.get('numPortsIn'),
        'num_out': request.GET.get('numPortsOut'),
        'file': request.GET.get('file')
    }

    try:
        return node_factory(node_info)
    except OSError as e:
        return JsonResponse({'message': e.strerror}, status=404)
