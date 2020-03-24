import networkx as nx
import json
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from node.models import Node

fs = FileSystemStorage(location=settings.MEDIA_ROOT)


class WorkflowInterface:
    """ Interface for a Workflow object.

    Attributes:
        _file_path: Location of a workflow file
        _graph: A NetworkX Directed Graph
    """

    def __init__(self):
        self._file_path = None
        self._graph = None

    def add_node(self, node: Node):
        pass

    def read_json(self):
        pass

    def retrieve_from_session(self, request):
        pass

    def store_in_session(self, request):
        pass

    def write_json(self):
        pass

    def __str__(self):
        return "Test"


class Workflow(WorkflowInterface):
    """ A concrete Workflow object.

    """
    def __init__(self):
        super().__init__()

    def add_node(self, node: Node):
        """ Add a Node object to the graph.

        Args:
            node - The Node object to add to the graph

        TODO:
            * validate() always returns True; this should perform actual validation
        """
        if node.validate():
            # Only hashable Python objects can represent a node in a NetworkX graph.
            # For now, add Node from 'node_id' and iterate through keys to add
            # attributes. We may want to investigate alternatives.
            node_dict = node.__dict__
            self._graph.add_node(node.node_id)

            for key in node_dict.keys():
                # Graph node already includes 'id' for lookup
                if key == 'node_id':
                    continue

                # Add attribute to graph node
                self._graph.nodes[node.node_id][key] = node_dict[key]

        return

    def remove_node(self, node):
        """ Remove a node from the graph.

        Raises:
            WorkflowException: on issue with removing node from graph

        TODO:
            * 'node' passed in is a Dict, not custom Node class
            * Property accessor will need to be changed
        """
        try:
            self._graph.remove_node(node['node_id'])
        except nx.NetworkXError:
            raise WorkflowException('remove_node', 'Node does not exist in graph.')

        return

    def read_json(self):
        """ Read a Workflow file saved as JSON into a NetworkX graph

        Returns:
             NetworkX DiGraph object

        Raises:
            OSError: on file error
            NetworkXError: on issue with loading JSON graph data
        """
        print(fs.location)
        print(self.file_path)
        with fs.open(self.file_path, 'r') as file:
            json_data = json.load(file)
            return nx.readwrite.json_graph.node_link_graph(json_data)

    def retrieve_from_session(self, request):
        """Store Workflow information in the Django session.

        Args:
            request: The Django request object
        """
        self.file_path = request.session['file_path']

        data = request.session['graph']
        if data is None:
            self.graph = None
        else:
            self.graph = nx.readwrite.json_graph.node_link_graph(data)

        return

    def store_in_session(self, request):
        """Store Workflow information in the Django session.

        Args:
            request: The Django request object
        """
        request.session['graph'] = nx.readwrite.node_link_data(self.graph)
        request.session['file_path'] = self.file_path
        return

    def download_json(self):
        json_str = json.dumps(nx.readwrite.json_graph.node_link_data(self.graph))
        response = HttpResponse(json_str, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=%s' % self.file_path
        return response

    def write_json(self, file_name='example.json'):
        """ Read a Workflow file saved as JSON into a NetworkX graph

        Args:
            file_name: Optional argument for file name. Defaults to
                pre-existing name saved in the Workflow object.

        Returns:
             NetworkX DiGraph object

        Raises:
            WorkflowException: on file error or NetworkX parsing

        TODO:
            * Filename save logic isn't great. Need to figure out better way
              to default to session info, but allow/accept an alternate path.
        """
        if self.file_path is None:
            self.file_path = file_name

        try:
            with fs.open(file_name, 'w') as outfile:
                json.dump(nx.readwrite.json_graph.node_link_data(self.graph), outfile)
        except OSError as e:
            raise WorkflowException('write_json', e.strerror)
        except nx.NetworkXError as e:
            raise WorkflowException('write_json', str(e))

        return

    @property
    def graph(self):
        return self._graph

    @graph.setter
    def graph(self, graph):
        self._graph = graph

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path: str):
        if file_path is None or file_path[-5:] == '.json':
            self._file_path = file_path
        else:
            raise WorkflowException('load_file', 'File ' + file_path + ' is not JSON.')


class WorkflowException(Exception):
    def __init__(self, action: str, reason: str):
        self.action = action
        self.reason = reason

    def __str__(self):
        return self.action + ': ' + self.reason
