import networkx as nx
import json

from node.models import Node

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
        if node.validate():
            self._graph.add_node(node.node_id)

    def read_json(self):
        """ Read a Workflow file saved as JSON into a NetworkX graph

        Returns:
             NetworkX DiGraph object

        Raises:
            WorkflowException: on file error or NetworkX parsing
        """
        try:
            with open(self.file_path, 'r') as file:
                json_data = json.load(file)
                self.graph = nx.readwrite.json_graph.node_link_graph(json_data)

            return self.graph
        except OSError as e:
            raise WorkflowException('read_json', e.strerror)
        except nx.NetworkXError as e:
            raise WorkflowException('read_json', e)

    def retrieve_from_session(self, request):
        """Store Workflow information in the Django session.

        Args:
            request: The Django request object

        Return:
            Object containing the graph and file path from the session.
        """
        data = request.session['graph']

        self.graph = nx.readwrite.json_graph.node_link_graph(data)
        self.file_path = request.session['file_path']

        return {
            'graph': nx.readwrite.json_graph.node_link_graph(data),
            'file_path': request.session['file_path'],
        }

    def store_in_session(self, request):
        """Store Workflow information in the Django session.

        Args:
            request: The Django request object
        """
        request.session['graph'] = nx.readwrite.node_link_data(self.graph)
        request.session['file_path'] = self.file_path
        return

    def write_json(self, file_name='example.json'):
        """ Read a Workflow file saved as JSON into a NetworkX graph

        Args:
            file_name: Optional argument for file name. Defaults to
                pre-existing name saved in the Workflow object.

        Returns:
             NetworkX DiGraph object

        Raises:
            WorkflowException: on file error or NetworkX parsing
        """
        if self.file_path is None:
            self.file_path = file_name

        try:
            with open(self.file_path, 'w') as outfile:
                json.dump(nx.readwrite.json_graph.node_link_data(self.graph), outfile)
        except OSError as e:
            raise WorkflowException('write_json', e.strerror)
        except nx.NetworkXError as e:
            raise WorkflowException('read_json', e)

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
        if file_path[-5:] == '.json':
            self._file_path = file_path
        else:
            raise WorkflowException('load_file', 'File is not JSON.')


class WorkflowException(Exception):
    def __init__(self, action: str, reason: str):
        self.action = action
        self.reason = reason
