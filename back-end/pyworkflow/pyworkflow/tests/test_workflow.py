import unittest
import os
from pyworkflow import Workflow, WorkflowException, Node, NodeException, node_factory
import networkx as nx

from pyworkflow.tests.sample_test_data import GOOD_NODES, BAD_NODES, DATA_FILES


class WorkflowTestCase(unittest.TestCase):
    def setUp(self):
        self.workflow = Workflow("Untitled", root_dir="/tmp", node_dir=os.path.join(os.getcwd(), 'nodes'))

        self.read_csv_node = GOOD_NODES["read_csv_node"]
        self.local_flow_node = GOOD_NODES["string_input"]
        self.write_csv_node = GOOD_NODES["write_csv_node"]
        self.join_node = GOOD_NODES["join_node"]
        self.global_flow_var = GOOD_NODES["global_flow_var"]

    def add_node(self, node_info, node_id):
        node_info["node_id"] = node_id
        node_to_add = Node(node_info)
        return self.workflow.update_or_add_node(node_to_add)

    def add_edge(self, source_node, target_node):
        response = self.workflow.add_edge(source_node, target_node)
        self.assertEqual(response, (source_node.node_id, target_node.node_id))

    ##########################
    # Workflow getters/setters
    ##########################
    def test_workflow_name(self):
        self.assertEqual(self.workflow.name, "Untitled")

    def test_workflow_dir_os_error(self):
        try:
            os.makedirs("foobar", 0000)
            test_workflow = Workflow(node_dir="foobar")
        except WorkflowException as e:
            self.assertEqual(e.action, "init workflow")

    def test_workflow_node_dir(self):
        self.assertEqual(self.workflow.node_dir, os.path.join(os.getcwd(), 'nodes'))

    def test_workflow_node_path(self):
        self.assertEqual(self.workflow.node_path('io', 'read_csv.py'), os.path.join(os.getcwd(), 'nodes/io/read_csv.py'))

    def test_set_workflow_name(self):
        self.workflow.name = "My Workflow"
        self.assertEqual(self.workflow.name, "My Workflow")

    def test_workflow_filename(self):
        self.assertEqual(self.workflow.filename, "Untitled.json")

    def test_workflow_from_json(self):
        new_workflow = Workflow("Untitled", root_dir="/tmp")
        workflow_copy = Workflow.from_json(self.workflow.to_json())

        self.assertEqual(new_workflow.name, workflow_copy.name)

    def test_workflow_from_json_key_error(self):
        with self.assertRaises(WorkflowException):
            new_workflow = Workflow.from_json(dict())

    def test_empty_workflow_to_session(self):
        new_workflow = Workflow("Untitled", root_dir="/tmp", node_dir=os.path.join(os.getcwd(), 'nodes'))
        saved_workflow = new_workflow.to_json()

        workflow_to_compare = {
            'name': 'Untitled',
            'root_dir': '/tmp',
            'node_dir': os.path.join(os.getcwd(), 'nodes'),
            'graph': Workflow.to_graph_json(new_workflow.graph),
            'flow_vars': Workflow.to_graph_json(new_workflow.flow_vars),
        }
        self.assertDictEqual(new_workflow.to_json(), workflow_to_compare)

    ##########################
    # Node lists
    ##########################
    def test_workflow_packaged_nodes(self):
        nodes = self.workflow.get_packaged_nodes()
        self.assertEqual(len(nodes), 5)

    def test_workflow_packaged_nodes_exception(self):
        result = self.workflow.get_packaged_nodes(root_path="foobar")
        self.assertIsNone(result)

    def test_get_flow_variables(self):
        flow_var_options = self.workflow.get_all_flow_var_options("1")

        self.assertEqual(len(flow_var_options), 1)

    def test_get_node_successors(self):
        successors = self.workflow.get_node_successors("1")

        self.assertEqual(successors, ["3", "2"])

    def test_fail_get_node_successors(self):
        try:
            successors = self.workflow.get_node_successors("100")
        except WorkflowException as e:
            self.assertEqual(str(e), "get node successors: The node 100 is not in the digraph.")

    def test_fail_get_node_predecessors(self):
        with self.assertRaises(WorkflowException):
            predecessors = self.workflow.get_node_predecessors("200")

    def test_get_node_predecessors(self):
        predecessors = self.workflow.get_node_predecessors("2")

        self.assertEqual(predecessors, ["1"])

    def test_fail_get_execution_order(self):
        copied_workflow = self.workflow
        with self.assertRaises(WorkflowException):
            copied_workflow._graph = nx.Graph()
            copied_workflow.execution_order()

    ##########################
    # Node operations
    ##########################
    def test_add_custom_node(self):
        with open(self.workflow.node_path('custom_nodes', 'good_custom_node.py'), 'w') as f:
            f.write((DATA_FILES['good_custom_node']))

        custom_node_info = {
            "name": "Custom Node",
            "node_id": "50",
            "node_type": "custom_node",
            "node_key": "MyGoodCustomNode",
            "is_global": False,
        }

        node_to_add = Node(custom_node_info)
        added_node = self.add_node(custom_node_info, "50")

        self.assertDictEqual(node_to_add.__dict__, added_node.__dict__)

    def test_add_read_csv_node(self):
        node_to_add = Node(self.read_csv_node)
        added_node = self.add_node(self.read_csv_node, "1")

        self.assertDictEqual(node_to_add.__dict__, added_node.__dict__)

    def test_add_write_csv_node(self):
        node_to_add = Node(self.write_csv_node)
        added_node = self.add_node(self.write_csv_node, "2")

        self.assertDictEqual(node_to_add.__dict__, added_node.__dict__)

    def test_get_node(self):
        retrieved_node = self.workflow.get_node("1")
        read_csv_node = Node(self.read_csv_node)

        self.assertDictEqual(retrieved_node.__dict__, read_csv_node.__dict__)

    def test_fail_get_node(self):
        retrieved_node = self.workflow.get_flow_var("100")

        self.assertIsNone(retrieved_node)

    def test_remove_node(self):
        node_to_remove = self.workflow.get_node("1")
        removed_node = self.workflow.remove_node(node_to_remove)

        self.assertDictEqual(node_to_remove.__dict__, removed_node.__dict__)

    def test_remove_node_error(self):
        node_to_remove = self.workflow.get_node("1")
        with self.assertRaises(WorkflowException):
            self.workflow.remove_node(node_to_remove)

    ##########################
    # Flow variable operations
    ##########################
    def test_add_string_node(self):
        node_to_add = Node(self.global_flow_var)
        added_node = self.add_node(self.global_flow_var, "1")

        self.assertDictEqual(node_to_add.__dict__, added_node.__dict__)

    def test_get_flow_var(self):
        retrieved_node = self.workflow.get_flow_var("1")
        global_flow_var = Node(self.global_flow_var)

        self.assertDictEqual(retrieved_node.__dict__, global_flow_var.__dict__)

    ##########################
    # Edge operations
    ##########################
    def test_add_node_edge_1_to_2(self):
        node_1 = self.workflow.get_node("1")
        node_2 = self.workflow.get_node("2")
        self.add_edge(node_1, node_2)
        return

    def test_add_node_edge_duplicated(self):
        node_1 = self.workflow.get_node("1")
        node_2 = self.workflow.get_node("2")

        with self.assertRaises(WorkflowException):
            self.workflow.add_edge(node_1, node_2)

    def test_remove_edge(self):
        node_1 = self.workflow.get_node("1")
        node_2 = self.workflow.get_node("2")
        response = self.workflow.remove_edge(node_1, node_2)

        self.assertEqual(response, ("1", "2"))

    def test_remove_edge_error(self):
        node_1 = self.workflow.get_node("1")
        node_2 = self.workflow.get_node("2")

        with self.assertRaises(WorkflowException):
            self.workflow.remove_edge(node_1, node_2)

    ##########################
    # Flow variable operations
    ##########################
    def test_execute_node(self):
        node_to_execute = self.workflow.get_node("1")

        response = self.workflow.execute("1")
        node_to_execute.data = 'Untitled-1'

        self.assertDictEqual(node_to_execute.__dict__, response.__dict__)

    def test_fail_execute_node(self):
        with self.assertRaises(WorkflowException):
            self.workflow.execute("100")

    ##########################
    # File I/O operations
    ##########################
    def test_download_file(self):
        file = self.workflow.download_file("1")

        self.assertEqual(file.name, "/tmp/sample1.csv")
        file.close()

    def test_download_file_error(self):
        self.assertIsNone(self.workflow.download_file("100"))

    def test_download_file_wrong_type(self):
        with self.assertRaises(WorkflowException):
            self.workflow.download_file("3")

