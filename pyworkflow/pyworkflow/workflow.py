import os
import networkx as nx
import json

from .node import Node
from .node_factory import node_factory


class Workflow:
    """ Workflow object

    Attributes:
        name: Name of the workflow
        root_dir: Used for reading/writing files to/from disk
        graph: A NetworkX Directed Graph
        flow_vars: Global flow variables associated with workflow
    """

    def __init__(self, name="Untitled", root_dir=None, graph=nx.DiGraph(), flow_vars=nx.Graph()):
        self._name = name
        self._root_dir = WorkflowUtils.set_root_dir(root_dir)
        self._graph = graph
        self._flow_vars = flow_vars

    @property
    def graph(self):
        return self._graph

    def path(self, file_name):
        return os.path.join(self.root_dir, file_name)

    @property
    def root_dir(self):
        return self._root_dir

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
            out_key = key
            if key == "option_values":
                out_key = "options"
            graph.nodes[node.node_id][out_key] = node_dict[key]

        return node

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def filename(self):
        return self.name + '.json'

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
            return node
        except (AttributeError, nx.NetworkXError):
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
                    preceding_data.append(self.retrieve_node_data(node_to_retrieve))

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

    def upload_file(self, uploaded_file, node_id):
        try:
            file_name = f"{node_id}-{uploaded_file.name}"
            to_open = self.path(file_name)

            # TODO: Change to a stream/other method for large files?
            with open(to_open, 'wb') as f:
                f.write(uploaded_file.read())

            uploaded_file.close()
            return to_open
        except OSError as e:
            raise WorkflowException('upload_file', str(e))

    def download_file(self, node_id):
        node = self.get_node(node_id)
        if node is None:
            return None

        try:
            # TODO: Change to generic "file" option to allow for more than WriteCsv
            to_open = self.path(node.options['file'].get_value())
            return open(to_open)
        except KeyError:
            raise WorkflowException('download_file', '%s does not have an associated file' % node_id)
        except OSError as e:
            raise WorkflowException('download_file', str(e))

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
        file_name = Workflow.generate_file_name(workflow, node_id)
        file_path = workflow.path(file_name)

        try:
            with open(file_path, 'w') as f:
                f.write(data)
            return file_name
        except Exception as e:
            return None

    def retrieve_node_data(self, node_to_retrieve):
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
            with open(self.path(node_to_retrieve.data)) as f:
                return json.load(f)
        except OSError as e:
            raise WorkflowException('retrieve node data', str(e))
        except TypeError:
            raise WorkflowException(
                'retrieve node data',
                'Node %s has not yet been executed. No data to retrieve.' % node_to_retrieve.node_id
            )
        except json.JSONDecodeError as e:
            raise WorkflowException('retrieve node data', str(e))

    @staticmethod
    def read_graph_json(json_data):
        """Deserialize JSON NetworkX graph

        Args:
            json_data: JSON data from which to read JSON-serialized graph

        Returns:
             NetworkX DiGraph object

        Raises:
            NetworkXError: on issue with loading JSON graph data
        """
        return nx.readwrite.json_graph.node_link_graph(json_data)

    @staticmethod
    def generate_file_name(workflow, node_id):
        """Generates a file name for saving intermediate execution data.

        Current format is 'workflow_name - node_id'

        Args:
            workflow: the workflow
            node_id: the id of the workflow
        """
        return f"{workflow.name}-{node_id}"

    @classmethod
    def from_json(cls, json_data):
        """Load Workflow from JSON data.

        Args:
            json_data: JSON-like data from session, or uploaded file

        Returns:
            New Workflow object

        Raises:
            WorkflowException: on missing data (KeyError) or on
                malformed NetworkX graph data (NetworkXError)
        """
        try:
            name = json_data['name']
            root_dir = json_data['root_dir']
            graph = Workflow.read_graph_json(json_data['graph'])
            flow_vars = Workflow.read_graph_json(json_data['flow_vars'])

            return cls(name=name, root_dir=root_dir, graph=graph, flow_vars=flow_vars)
        except KeyError as e:
            raise WorkflowException('from_json', str(e))
        except nx.NetworkXError as e:
            raise WorkflowException('from_json', str(e))

    @staticmethod
    def to_graph_json(graph):
        return nx.readwrite.json_graph.node_link_data(graph)

    def to_session_dict(self):
        """Store Workflow information in the Django session.
        """
        try:
            out = dict()
            out['name'] = self.name
            out['root_dir'] = self.root_dir
            out['graph'] = Workflow.to_graph_json(self.graph)
            out['flow_vars'] = Workflow.to_graph_json(self.flow_vars)
            return out
        except nx.NetworkXError as e:
            raise WorkflowException('to_session_dict', str(e))


class WorkflowUtils:
    @staticmethod
    def set_root_dir(root_dir):
        if root_dir is None:
            root_dir = os.getcwd()

        if not os.path.exists(root_dir):
            os.makedirs(root_dir)

        return root_dir


class WorkflowException(Exception):
    def __init__(self, action: str, reason: str):
        self.action = action
        self.reason = reason

    def __str__(self):
        return self.action + ': ' + self.reason
