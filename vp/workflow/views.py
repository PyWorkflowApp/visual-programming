from django.http import JsonResponse
import networkx as nx
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def open(request):

    # Open filename specified
    if request.GET.get('file'):
        path = os.path.join(BASE_DIR, request.GET.get('file'))
        DG = nx.read_yaml(path)

    # Create a test graph with 3 nodes
    else:
        DG = nx.DiGraph()

        DG.add_nodes_from([1, 2, 3])
        DG.add_edges_from([(1, 2), (2, 3)])

    # Construct response
    data = {
        # 'graph': DG,
        'nodes': DG.number_of_nodes(),
        'message': 'Saving graph to session.',
    }

    # Store in session
    # Not currently working; DiGraph is not JSON serializable
    request.session['graph'] = data

    return JsonResponse(data)

def save(request):

    # Send error message if no graph is in session
    if request.session.get('graph') is None:
        return JsonResponse({'message': 'No graph exists.'})


    # Create a test graph with 4 nodes
    DG = nx.DiGraph()

    DG.add_nodes_from([1, 2, 3, 4])
    DG.add_edges_from([(1, 2), (1, 4), (2, 3)])

    # Write to YAML file
    nx.write_yaml(DG, 'test.yaml')

    return JsonResponse({'message': 'Saved the graph to YAML file!'})