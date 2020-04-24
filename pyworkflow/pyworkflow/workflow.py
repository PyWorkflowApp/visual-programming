import inspect
import importlib
import json
import os
import networkx as nx
import sys

from collections import OrderedDict
from modulefinder import ModuleFinder

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

    def __init__(self, name="Untitled", root_dir=None, node_dir=None, graph=nx.DiGraph(), flow_vars=nx.Graph()):
        self._name = name
        self._root_dir = WorkflowUtils.set_root_dir(root_dir)
        self._node_dir = WorkflowUtils.set_custom_nodes_dir(node_dir)
        self._graph = graph
        self._flow_vars = flow_vars

    @property
    def node_dir(self):
        return self._node_dir

    @property
    def graph(self):
        return self._graph

    def path(self, file_name):
        return os.path.join(self.root_dir, file_name)

    def node_path(self, node_type, file_name):
        return os.path.join(self.node_dir, node_type, file_name)

    @property
    def root_dir(self):
        return self._root_dir

    @property
    def flow_vars(self):
        return self._flow_vars

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
        if self.flow_vars.has_node(node_id) is not True:
            return None

        node_info = self.flow_vars.nodes[node_id]
        return node_factory(node_info)

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

            if node.node_type == 'FlowNode':
                flow_variables.append(node.to_json())

        return flow_variables

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
            return list(self.graph.successors(node_id))
        except nx.NetworkXError as e:
            raise WorkflowException('get node successors', str(e))

    def get_node_predecessors(self, node_id):
        try:
            return list(self.graph.predecessors(node_id))
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

        # Load predecessor data and FlowNode values
        preceding_data = self.load_input_data(node_to_execute.node_id)
        flow_nodes = self.load_flow_nodes(node_to_execute.option_replace)

        try:
            # Validate input data, and replace flow variables
            node_to_execute.validate_input_data(len(preceding_data))
            execution_options = node_to_execute.get_execution_options(flow_nodes)

            # Pass in data to current Node to use in execution
            output = node_to_execute.execute(preceding_data, execution_options)

            # Save new execution data to disk
            node_to_execute.data = Workflow.store_node_data(self, node_id, output)
        except NodeException as e:
            raise e

        if node_to_execute.data is None:
            raise WorkflowException('execute', 'There was a problem saving node output.')

        return node_to_execute

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

                if flow_node is None or flow_node.node_type != 'FlowNode':
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

                if node_to_retrieve.node_type != 'FlowNode':
                    input_data.append(self.retrieve_node_data(node_to_retrieve))

            except WorkflowException:
                # TODO: Should this append None, skip reading, or raise exception to view?
                continue

        return input_data

    def execution_order(self):
        try:
            return list(nx.topological_sort(self.graph))
        except (nx.NetworkXError, nx.NetworkXUnfeasible) as e:
            raise WorkflowException('execution order', str(e))
        except RuntimeError as e:
            raise WorkflowException('execution order', 'The graph was changed while generating the execution order')

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

    @staticmethod
    def execute_workflow(workflow_location):
        """Execute entire workflow at a certain location.
           Current use case: CLI.
        """
        #load the file at workflow_location
        with open(workflow_location) as f:
            json_content = json.load(f)

        #convert it to a workflow
        workflow_instance = Workflow.from_json(json_content['pyworkflow'])

        #get the execution order
        execution_order = workflow_instance.execution_order()

        #execute each node in the order returned by execution order method
        #TODO exception handling: stop and provide details on which node failed to execute
        for node in execution_order:
            workflow_instance.execute(node)


class WorkflowUtils:
    @staticmethod
    def get_display_name(file):
        if file == 'io':
            return 'I/O'
        else:
            return file.replace('_', ' ').title()

    @staticmethod
    def set_custom_nodes_dir(custom_node_path):
        if custom_node_path is None:
            custom_node_path = os.path.join(os.getcwd(), '../pyworkflow/pyworkflow/nodes')

        if not os.path.exists(custom_node_path):
            os.makedirs(custom_node_path)

        return custom_node_path

    @staticmethod
    def set_root_dir(root_dir):
        if root_dir is None:
            root_dir = os.getcwd()

        if not os.path.exists(root_dir):
            os.makedirs(root_dir)

        return root_dir

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
                    'doc': klass.__doc__,
                    'options': {k: v.get_value() for k, v in klass.options.items()},
                    'option_types': klass.option_types,
                    'download_result': getattr(klass, "download_result", False)
                }

                if node_type == 'custom_nodes':
                    parsed_node['filename'] = node

                return parsed_node

        return None


class WorkflowException(Exception):
    def __init__(self, action: str, reason: str):
        self.action = action
        self.reason = reason

    def __str__(self):
        return self.action + ': ' + self.reason
