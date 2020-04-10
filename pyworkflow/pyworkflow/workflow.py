import networkx as nx
import json

from .node import Node
from .node_factory import node_factory

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location=settings.MEDIA_ROOT)


class Workflow:
    """ Workflow object

    Attributes:
        graph: A NetworkX Directed Graph
        file_path: Location of a workflow file
    """

    def __init__(self, graph=nx.DiGraph(), file_path=None, name='a-name', flow_vars=nx.Graph(), file_system=fs):
        #TODO: need to discuss a way to generating the workflow name. For now passing a default name.
        self._graph = graph
        self._file_path = file_path
        self._name = name
        self._flow_vars = flow_vars
        self._file_system = file_system

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
            raise WorkflowException('set_file_path', 'File ' + file_path + ' is not JSON.')

    @property
    def flow_vars(self):
        return self._flow_vars

    def get_node(self, node_id):
        """Retrieves Node from workflow, if exists

        Return:
            Node object, if one exists. Otherwise, None.
        """
        if self._graph.has_node(node_id) is not True:
            return None

        node_info = self.graph.nodes[node_id]
        return node_factory(node_info)

    def get_flow_var(self, node_id):
        """Retrieves a global flow variable from workflow, if exists

        Return:
            FlowNode object, if one exists. Otherwise, None.
        """
        if self._flow_vars.has_node(node_id) is not True:
            return None

        node_info = self.flow_vars.nodes[node_id]
        return node_factory(node_info)

    def update_or_add_node(self, node: Node):
        """ Update or add a Node object to the graph.

        Args:
            node - The Node object to update or add to the graph

        TODO:
            * validate() always returns True; this should perform actual validation
        """
        # Do not add/update if invalid
        if node.validate() is False:
            raise WorkflowException('update_or_add_node', 'Node is invalid')

        # Select the correct graph to modify
        graph = self.flow_vars if node.is_global else self.graph

        if graph.has_node(node.node_id) is False:
            graph.add_node(node.node_id)

        # NetworkX cannot store mutable data, so iterate through all Node
        # attributes to add to graph
        node_dict = node.__dict__
        for key in node_dict.keys():
            graph.nodes[node.node_id][key] = node_dict[key]

        return

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    def add_edge(self, node_from: Node, node_to: Node):
        """ Add a Node object to the graph.

        Args:
            node_from - The Node the edge originates from
              node_to - The Node the edge ends at

        Returns:
            Tuple representing the new Edge (from, to)

        TODO:
            * validate() always returns True; this should perform actual validation
        """
        # Prevent duplicate edges between the same two nodes
        # TODO: This may be incorrect usage for a `node_to` that has multi-in
        from_id = node_from.node_id
        to_id = node_to.node_id

        if self._graph.has_edge(from_id, to_id):
            raise WorkflowException('add_node', 'Edge between nodes already exists.')

        if node_from.validate() and node_to.validate():
            self._graph.add_edge(from_id, to_id)

        return (from_id, to_id)

    def remove_edge(self, node_from: Node, node_to: Node):
        """ Remove a node from the graph.

        Returns:
            Tuple representing the removed Edge (from, to)

        Raises:
            WorkflowException: on issue with removing node from graph
        """
        from_id = node_from.node_id
        to_id = node_to.node_id

        try:
            self._graph.remove_edge(from_id, to_id)
        except nx.NetworkXError:
            raise WorkflowException('remove_edge', 'Edge from %s to %s does not exist in graph.' % (from_id, to_id))

        return (from_id, to_id)

    def remove_node(self, node):
        """ Remove a node from the graph.

        Raises:
            WorkflowException: on issue with removing node from graph
        """
        try:
            # Select the correct graph to modify
            graph = self.flow_vars if node.is_global else self.graph

            graph.remove_node(node.node_id)
        except nx.NetworkXError:
            raise WorkflowException('remove_node', 'Node does not exist in graph.')

    def get_node_successors(self, node_id):
        try:
            return list(self._graph.successors(node_id))
        except nx.NetworkXError as e:
            raise WorkflowException('get node successors', str(e))

    def get_node_predecessors(self, node_id):
        try:
            return list(self._graph.predecessors(node_id))
        except nx.NetworkXError as e:
            raise WorkflowException('get node predecessors', str(e))

    def execute(self, node_id):
        """Execute a single Node in the graph.

        Reads any stored data from preceding Nodes and passes in to
        'node_to_execute` as a list(). After execution, the new/updated
        DataFrame is returned as a JSON object that is written to a new
        file, with the file name saved to the executed Node.

        Returns:
            Executed Node object

        """
        node_to_execute = self.get_node(node_id)

        if node_to_execute is None:
            raise WorkflowException('execute', 'The workflow does not contain node %s' % node_id)

        # Read in any data from predecessor/flow nodes
        # TODO: This should work for local FlowNodes, but global flow_vars still
        #       need a way to be assigned/replace Node options
        preceding_data = list()
        flow_vars = list()
        for predecessor in self.get_node_predecessors(node_id):
            try:
                node_to_retrieve = self.get_node(predecessor)

                if node_to_retrieve is None:
                    raise WorkflowException('retrieve node data', 'The workflow does not contain node %s' % node_id)

                if node_to_retrieve.node_type == 'FlowNode':
                    flow_vars.append(node_to_retrieve.options)
                else:
                    preceding_data.append(Workflow.retrieve_node_data(node_to_retrieve))

            except WorkflowException:
                # TODO: Should this append None, skip reading, or raise exception to view?
                preceding_data.append(None)

        # Pass in data to current Node to use in execution
        output = node_to_execute.execute(preceding_data, flow_vars)

        # Save new execution data to disk
        node_to_execute.data = Workflow.store_node_data(self, node_id, output)

        if node_to_execute.data is None:
            raise WorkflowException('execute', 'There was a problem saving node output.')

        return node_to_execute

    def execution_order(self):
        try:
            return list(nx.topological_sort(self._graph))
        except (nx.NetworkXError, nx.NetworkXUnfeasible) as e:
            raise WorkflowException('execution order', str(e))
        except RuntimeError as e:
            raise WorkflowException('execution order', 'The graph was changed while generating the execution order')

    @staticmethod
    def store_node_data(workflow, node_id, data):
        """Store Node data

        Writes the current DataFrame to disk in JSON format.

        Args:
            workflow: The Workflow that stores the graph.
            node_id: The Node which contains a DataFrame to save.
            data: A pandas DataFrame converted to JSON.

        Returns:

        """
        file_name = Workflow.generate_file_name(workflow.name, node_id)

        try:
            return fs.save(file_name, ContentFile(data))
        except Exception as e:
            return None

    @staticmethod
    def retrieve_node_data(node_to_retrieve):
        """Retrieve Node data

        Reads a saved DataFrame, referenced by the Node's 'data' attribute.

        Args:
            node_to_retrieve: The Node containing a DataFrame saved to disk.

        Returns:
            Contents of the file (a DataFrame) in a JSON object.

        Raises:
            WorkflowException: Node does not exist, file does not exist, or
                problem parsing the file.
        """
        try:
            with fs.open(node_to_retrieve.data) as f:
                return json.load(f)
        except OSError as e:
            raise WorkflowException('retrieve node data', str(e))
        except TypeError as e:
            raise WorkflowException('retrieve node data', str(e))
        except json.JSONDecodeError as e:
            raise WorkflowException('retrieve node data', str(e))

    @staticmethod
    def read_graph_json(file_like):
        """Deserialize JSON NetworkX graph

        Args:
            file_like: file-like object from which to read JSON-serialized graph

        Returns:
             NetworkX DiGraph object

        Raises:
            OSError: on file error
            NetworkXError: on issue with loading JSON graph data
        """
        json_data = json.load(file_like)
        return nx.readwrite.json_graph.node_link_graph(json_data)

    @staticmethod
    def generate_file_name(workflow_name, node_id):
        """Generates a file name for saving intermediate execution data.

        Current format is workflow_name - node_id

        Args:
            workflow_name: the name of the workflow
            node_id: the id of the workflow
        """
        #TODO: need to add validation
        if workflow_name is None:
            workflow_name = "a-name"

        return workflow_name + '-' + str(node_id)

    @classmethod
    def from_session(cls, data):
        """Create instance from graph (JSON) data and filename

        Typically takes Django session as argument, which contains
        `graph` and `file_path` keys.

        Args:
            data: dict-like with keys `file_path` and `graph`
        """
        file_path = data.get('file_path')
        graph_data = data.get('graph')
        name = data.get('name')
        flow_vars_data = data.get('flow_vars')
        if graph_data is None:
            graph = None
        else:
            graph = nx.readwrite.json_graph.node_link_graph(graph_data)

        if flow_vars_data is None:
            flow_vars = None
        else:
            flow_vars = nx.readwrite.json_graph.node_link_graph(flow_vars_data)

        return cls(graph, file_path, name, flow_vars)

    @classmethod
    def from_file(cls, file_like):
        """

        """
        graph = cls.read_graph_json(file_like)
        return cls(graph)

    @classmethod
    def from_request(cls, json_data):
        """

        """
        graph = nx.readwrite.json_graph.node_link_graph(json_data)
        return cls(graph)

    @staticmethod
    def to_graph_json(graph):
        return nx.readwrite.json_graph.node_link_data(graph)

    def to_session_dict(self):
        """Store Workflow information in the Django session.
        """
        out = dict()
        out['graph'] = Workflow.to_graph_json(self.graph)
        out['file_path'] = self.file_path
        out['name'] = self.name
        out['flow_vars'] = Workflow.to_graph_json(self.flow_vars)
        return out


class WorkflowException(Exception):
    def __init__(self, action: str, reason: str):
        self.action = action
        self.reason = reason

    def __str__(self):
        return self.action + ': ' + self.reason
