from django.http import JsonResponse
import networkx as nx
import json
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def open_workflow(request):
    # Open filename specified
    file = request.GET.get('file')

    # File requested matches JSON extension
    if file is not None and file[-5:] == '.json':
        path = os.path.join(BASE_DIR, file)

        with open(path, 'r') as json_file:
            json_data = json.load(json_file)
            DG = nx.readwrite.json_graph.node_link_graph(json_data)

    # Create a test graph with 3 nodes
    else:
        DG = nx.DiGraph()
        DG.add_nodes_from([1, 2, 3])
        DG.add_edges_from([(1, 2), (2, 3)])

    # Construct response
    data = {
        'graph': nx.readwrite.node_link_data(DG),
        'nodes': DG.number_of_nodes(),
        'message': 'Saving graph to session.',
    }

    # Store in session
    # Not currently working; DiGraph is not JSON serializable
    request.session['graph'] = data['graph']

    return JsonResponse(data)


def save_workflow(request):
    # Send error message if no graph is in session
    if request.session.get('graph') is None:
        return JsonResponse({'message': 'No graph exists.'})

    graph = request.session.get('graph')

    with open('graph.json', 'w') as outfile:
        json.dump(graph, outfile)

    # # Create a test graph with 4 nodes
    # DG = nx.DiGraph()
    #
    # DG.add_nodes_from([1, 2, 3, 4])
    # DG.add_edges_from([(1, 2), (1, 4), (2, 3)])
    #
    # # Write to YAML file
    # nx.write_yaml(DG, 'test.yaml')

    return JsonResponse({
        'graph': graph,
        'message': 'Saved the graph to JSON file!'
    })
