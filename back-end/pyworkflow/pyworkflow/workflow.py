import inspect
import importlib
import json
import os
import networkx as nx
import sys

from collections import OrderedDict
from modulefinder import ModuleFinder

from pyworkflow.nodes import ReadCsvNode, WriteCsvNode

from .node import Node, NodeException
from .node_factory import node_factory


class Workflow:
    """ Workflow object

    Attributes:
        name: Name of the workflow
        root_dir: Used for reading/writing files to/from disk
        node_dir: Location of custom nodes
        graph: A NetworkX Directed Graph
        flow_vars: Global flow variables associated with workflow
    """

    DEFAULT_ROOT_PATH = os.getcwd()
    DEFAULT_NODE_PATH = os.path.join(os.getcwd(), '../pyworkflow/pyworkflow/nodes')

    def __init__(self, name="Untitled", root_dir=DEFAULT_ROOT_PATH,
                 node_dir=DEFAULT_NODE_PATH, graph=nx.DiGraph(),
                 flow_vars=nx.Graph()):
        try:
            self._name = name
            self._root_dir = WorkflowUtils.set_dir(root_dir)
            self._node_dir = WorkflowUtils.set_dir(node_dir, custom_nodes=True)
            self._graph = graph
            self._flow_vars = flow_vars
        except OSError as e:
            raise WorkflowException('init workflow', str(e))

    ##################
    # GETTERS/SETTERS
    ##################
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def root_dir(self):
        return self._root_dir

    @property
    def node_dir(self):
        return self._node_dir

    @property
    def graph(self):
        return self._graph

    @property
    def flow_vars(self):
        return self._flow_vars

    @property
    def filename(self):
        return self.name + '.json'

    @staticmethod
    def generate_file_name(workflow, node_id):
        """Generates a file name for saving intermediate execution data.

        Current format is 'workflow_name - node_id'

        Args:
            workflow: the workflow
            node_id: the id of the workflow
        """
        return f"{workflow.name}-{node_id}"

    def path(self, file_name):
        return os.path.join(self.root_dir, file_name)

    def node_path(self, node_type, file_name):
        return os.path.join(self.node_dir, node_type, file_name)

    ##################
    # EDGE OPERATIONS
    ##################
    def add_edge(self, node_from: Node, node_to: Node):
        """ Add a Node object to the graph.

        Args:
            node_from - The Node the edge originates from
              node_to - The Node the edge ends at

        Returns:
            Tuple representing the new Edge (from, to)
        """
        # Prevent duplicate edges between the same two nodes
        # TODO: This may be incorrect usage for a `node_to` that has multi-in
        from_id = node_from.node_id
        to_id = node_to.node_id

        if self.graph.has_edge(from_id, to_id):
            raise WorkflowException('add_node', 'Edge between nodes already exists.')

        self.graph.add_edge(from_id, to_id)

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
            self.graph.remove_edge(from_id, to_id)
        except nx.NetworkXError:
            raise WorkflowException('remove_edge', 'Edge from %s to %s does not exist in graph.' % (from_id, to_id))

        return (from_id, to_id)

    ##################
    # NODE OPERATIONS
    ##################
    def get_all_flow_var_options(self, node_id):
        """Retrieve all FlowNode options for a specified Node.

        A Node can use all global FlowNodes, and any connected local FlowNodes
        for variable substitution.

        Args:
            node_id: The Node to GET

        Returns:
            list of all FlowNode objects, converted to JSON
        """
        # Add global FlowNodes
        graph_data = Workflow.to_graph_json(self.flow_vars)
        flow_variables = graph_data['nodes']

        # Append local FlowNodes
        for predecessor_id in self.get_node_predecessors(node_id):
            node = self.get_node(predecessor_id)

            if node.node_type == 'flow_control':
                flow_variables.append(node.to_json())

        return flow_variables

    def get_flow_var(self, node_id):
        """Retrieves a global flow variable from workflow, if exists

        Return:
            FlowNode object, if one exists. Otherwise, None.
        """
        if self.flow_vars.has_node(node_id) is not True:
            return None

        node_info = self.flow_vars.nodes[node_id]
        return node_factory(node_info)

    def get_node(self, node_id):
        """Retrieves Node from workflow, if exists

        Return:
            Node object, if one exists. Otherwise, None.
        """
        if self.graph.has_node(node_id) is not True:
            return None

        node_info = self.graph.nodes[node_id]
        return node_factory(node_info)

    def get_node_predecessors(self, node_id):
        try:
            return list(self.graph.predecessors(node_id))
        except nx.NetworkXError as e:
            raise WorkflowException('get node predecessors', str(e))

    def get_node_successors(self, node_id):
        try:
            return list(self.graph.successors(node_id))
        except nx.NetworkXError as e:
            raise WorkflowException('get node successors', str(e))

    def get_packaged_nodes(self, root_path=None, node_type=None):
        """Retrieve list of Nodes available to the Workflow.

        Recursively searches the `root_path` where Nodes are located. If none
        specified, the default is `self.node_path`.

        Each directory represents a given `node_type` (e.g. 'manipulation',
        'io', etc.). Individual Node classes are defined in files within these
        directories. Any custom nodes that the user has installed are included
        in this search, given they are located in the 'custom_nodes' directory.

        Args:
            root_path: Root location where Nodes are defined.
            node_type: The type of Node, defined by sub-directory name.

        Returns:
            OrderedDict() of Nodes, structured like the following

            {
                'I/O': [
                    {node1},
                    {node2},
                ],
                'Manipulation': [
                    ...
                ]
                ...
            }
        """
        if root_path is None:
            root_path = self.node_dir

        try:
            files = os.listdir(root_path)
        except OSError:
            return None

        nodes = list()
        data = OrderedDict()

        for file in files:
            file_path = os.path.join(root_path, file)

            if os.path.isdir(file_path):
                # Recurse if file is a directory
                display_name = WorkflowUtils.get_display_name(file)
                data[display_name] = self.get_packaged_nodes(file_path, file)
                continue

            # Otherwise, try parsing file for a Node class
            node, ext = os.path.splitext(file)

            # Skip init files or non-Python files
            if node == '__init__' or ext != '.py':
                continue

            nodes.append(WorkflowUtils.extract_node_info(node_type, node, file_path))

        if root_path == self.node_dir:
            # When traversal returns to `node_dir` return the entire OrderedDict()
            data.move_to_end('Custom Nodes')
            return data
        else:
            # Otherwise, return list containing all Nodes of a `node_type`
            return nodes

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

    def update_or_add_node(self, node: Node):
        """ Update or add a Node object to the graph.

        Args:
            node - The Node object to update or add to the graph
        """
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

    ####################
    # EXECUTION METHODS
    ####################
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

        # Load predecessor data and FlowNode values
        preceding_data = self.load_input_data(node_to_execute.node_id)
        flow_nodes = self.load_flow_nodes(node_to_execute.option_replace)

        try:
            # Validate input data, and replace flow variables
            node_to_execute.validate_input_data(len(preceding_data))
            execution_options = node_to_execute.get_execution_options(self, flow_nodes)

            # Pass in data to current Node to use in execution
            output = node_to_execute.execute(preceding_data, execution_options)

            # Save new execution data to disk
            node_to_execute.data = Workflow.store_node_data(self, node_id, output)
        except NodeException as e:
            raise e

        if node_to_execute.data is None and node_to_execute.node_type != "flow_control":
            raise WorkflowException('execute', 'There was a problem saving node output.')

        return node_to_execute

    def execution_order(self):
        try:
            return list(nx.topological_sort(self.graph))
        except (nx.NetworkXError, nx.NetworkXUnfeasible) as e:
            raise WorkflowException('execution order', str(e))
        except RuntimeError as e:
            raise WorkflowException('execution order', 'The graph was changed while generating the execution order')

    def load_flow_nodes(self, option_replace):
        """Construct dict of FlowNodes indexed by option name.

        During Node configuration, the user has the option to select FlowNodes
        to replace a given parameter value. A FlowNode selection is structured
        like the following JSON:

            "option_replace": {
                "sep": {
                    "node_id": id,
                    "is_global": true
                }
            }

        This method retrieves the specified FlowNode where the replacement value
        can then be retrieved.

        Args:
            option_replace: Flow variables user selected for a given Node.

        Returns:
            dict of FlowNode objects, indexed by the option name.
        """
        flow_nodes = dict()

        for key, option in option_replace.items():
            try:
                flow_node_id = option["node_id"]

                if option["is_global"]:
                    flow_node = self.get_flow_var(flow_node_id)
                else:
                    flow_node = self.get_node(flow_node_id)

                if flow_node is None or flow_node.node_type != 'flow_control':
                    raise WorkflowException('load flow vars', 'The workflow does not contain FlowNode %s' % flow_node_id)

                flow_nodes[key] = flow_node
            except WorkflowException:
                # TODO: Should this add a blank value, skip reading, or raise exception to view?
                continue

        return flow_nodes

    def load_input_data(self, node_id):
        """Construct list of predecessor DataFrames

        Retrieves the data file for all of a Node's predecessors. Ignores
        exceptions for missing Nodes/data as this is checked prior to execution.

        Args:
            node_id: The Node with predecessors

        Returns:
            list of dict-like DataFrames, used for Node execution
        """
        input_data = list()

        for predecessor_id in self.get_node_predecessors(node_id):
            try:
                node_to_retrieve = self.get_node(predecessor_id)

                if node_to_retrieve is None:
                    raise WorkflowException('retrieve node data', 'The workflow does not contain node %s' % predecessor_id)

                if node_to_retrieve.node_type != 'flow_control':
                    input_data.append(self.retrieve_node_data(node_to_retrieve))

            except WorkflowException:
                # TODO: Should this append None, skip reading, or raise exception to view?
                continue

        return input_data

    ##################
    # FILE I/O
    ##################
    def download_file(self, node_id):
        node = self.get_node(node_id)
        if node is None:
            return None

        try:
            # Check if file option is overridden by flow variable
            if 'file' in node.option_replace:
                flow_node = self.load_flow_nodes({'file': node.option_replace['file']})
                filename = flow_node['file'].get_replacement_value()
            else:
                filename = node.options['file'].get_value()

            # Construct path to file in Workflow dir
            to_open = self.path(filename)
            return open(to_open)
        except KeyError:
            raise WorkflowException('download_file', '%s does not have an associated file' % node_id)
        except OSError as e:
            raise WorkflowException('download_file', str(e))

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

    @staticmethod
    def upload_file(uploaded_file, to_open):
        try:
            # TODO: Change to a stream/other method for large files?
            with open(to_open, 'wb') as f:
                f.write(uploaded_file.read())

            uploaded_file.close()
            return to_open
        except OSError as e:
            raise WorkflowException('upload_file', str(e))

    ############################
    # WORKFLOW (DE)SERIALIZATION
    ############################
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
            return cls(
                name=json_data['name'],
                root_dir=json_data['root_dir'],
                node_dir=json_data['node_dir'],
                graph=Workflow.read_graph_json(json_data['graph']),
                flow_vars=Workflow.read_graph_json(json_data['flow_vars']),
            )
        except KeyError as e:
            raise WorkflowException('from_json', str(e))
        except nx.NetworkXError as e:
            raise WorkflowException('from_json', str(e))

    def to_json(self):
        """Save Workflow information in JSON format."""
        try:
            return {
                'name': self.name,
                'root_dir': self.root_dir,
                'node_dir': self.node_dir,
                'graph': Workflow.to_graph_json(self.graph),
                'flow_vars': Workflow.to_graph_json(self.flow_vars),
            }
        except nx.NetworkXError as e:
            raise WorkflowException('to_json', str(e))

    ####################
    # NetworkX GRAPH I/O
    ####################
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
    def to_graph_json(graph):
        """Serialize JSON NetworkX graph

        Args:
            graph: NetworkX graph to save to JSON

        Returns:
            JSON representation of NetworkX graph

        Raises:
            NetworkXError: on issue with saving graph to JSON
        """
        return nx.readwrite.json_graph.node_link_data(graph)


class WorkflowUtils:
    @staticmethod
    def get_display_name(file):
        if file == 'io':
            return 'I/O'
        else:
            return file.replace('_', ' ').title()

    @staticmethod
    def set_dir(dir_path, custom_nodes=False):
        """Makes directories to ensure path is valid.

        To prevent OSErrors for missing directories, especially in the case of
        non-default Workflow locations, this method ensures the `dir_path`
        specified exists.

        Args:
            dir_path: Fully-qualified directory to check/make
            custom_nodes: Creates a 'custom_nodes' sub directory when True

        Returns:
            The `dir_path` requested, with guarantee the path exists.
        """
        if custom_nodes:
            make_dir = os.path.join(dir_path, 'custom_nodes')
        else:
            make_dir = dir_path

        if not os.path.exists(make_dir):
            os.makedirs(make_dir)

        return dir_path

    @staticmethod
    def check_missing_packages(node_path):
        """Check Python file for uninstalled packages.

        When compiling the list of installed Nodes for a Workflow, if any
        module throws a `ModuleNotFoundError`, this method is called to
        compile a list of missing packages.

        Args:
            node_path: Location of the Node file.

        Returns:
            list of package names that are not installed
        """
        finder = ModuleFinder(node_path)
        finder.run_script(node_path)

        uninstalled = list()
        for missing_package in finder.badmodules.keys():
            if missing_package not in sys.modules:
                uninstalled.append(missing_package)

        return uninstalled

    @staticmethod
    def extract_node_info(node_type, node, file_path):
        """Extract information about a Node Class from a Python file.

        Takes an individual Python file, representing a Node subclass and
        extracts the attributes needed. If a module has packages that are not
        installed, the filename and missing package names are returned.

        Args:
            node_type: The type of Node.
            node: Name of the specific Node.
            file_path: Where the Node's file is located.

        Returns:
            dict-like with extracted Node information. On `ModuleNotFoundError`
            the filename and missing packages are returned.
        """
        # Check Node file for missing packages
        try:
            module = importlib.import_module('pyworkflow.nodes.' + node_type + '.' + node)
        except ModuleNotFoundError:
            return {
                "filename": node,
                "missing_packages": WorkflowUtils.check_missing_packages(file_path)
            }

        # Parse module for Node Class information
        for name, klass in inspect.getmembers(module):
            if inspect.isclass(klass) and klass.__module__.startswith('pyworkflow.nodes.' + node_type):
                try:
                    color = klass.color
                except AttributeError:
                    color = 'black'

                parsed_node = {
                    'name': klass.name,
                    'node_key': klass.__name__,
                    'node_type': node_type,
                    'num_in': klass.num_in,
                    'num_out': klass.num_out,
                    'color': color,
                    'filename': node,
                    'doc': klass.__doc__,
                    'options': {k: v.get_value() for k, v in klass.options.items()},
                    'option_types': klass.option_types,
                    'download_result': getattr(klass, "download_result", False)
                }

                # if node_type == 'custom_nodes':
                #     parsed_node['filename'] = node

                return parsed_node

        return None


class WorkflowException(Exception):
    def __init__(self, action: str, reason: str):
        self.action = action
        self.reason = reason

    def __str__(self):
        return self.action + ': ' + self.reason
