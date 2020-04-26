import unittest
from pyworkflow import Workflow, WorkflowException, Node, NodeException, node_factory
import networkx as nx


class WorkflowTestCase(unittest.TestCase):
    def setUp(self):
        self.workflow = Workflow("Untitled", root_dir="/tmp")

        self.read_csv_node = {
            "name": "Read CSV",
            "node_id": "1",
            "node_type": "IONode",
            "node_key": "ReadCsvNode",
            "is_global": False,
            "options": {
                "file": "/tmp/sample.csv"
            }
        }

        self.write_csv_node = {
            "name": "Write CSV",
            "node_id": "2",
            "node_type": "IONode",
            "node_key": "WriteCsvNode",
            "is_global": False,
            "options": {
                "file": "/tmp/sample_out.csv"
            }
        }

        self.global_flow_var = {
            "name": "String Input",
            "node_id": "1",
            "node_type": "FlowNode",
            "node_key": "StringNode",
            "is_global": True,
            "options": {
                "default_value": "My value",
                "var_name": "my_var"
            }
        }

    def add_node(self, node_info, node_id):
        node_info["node_id"] = node_id
        node_to_add = Node(node_info)
        return self.workflow.update_or_add_node(node_to_add)

    def add_edge(self, source_node, target_node):
        response = self.workflow.add_edge(source_node, target_node)
        self.assertEqual(response, (source_node.node_id, target_node.node_id))

    def test_workflow_name(self):
        self.assertEqual(self.workflow.name, "Untitled")

    def test_set_workflow_name(self):
        self.workflow.name = "My Workflow"
        self.assertEqual(self.workflow.name, "My Workflow")

    def test_workflow_filename(self):
        self.assertEqual(self.workflow.filename, "Untitled.json")

    def test_add_read_csv_node(self):
        node_to_add = Node(self.read_csv_node)
        added_node = self.add_node(self.read_csv_node, "1")

        self.assertDictEqual(node_to_add.__dict__, added_node.__dict__)

    def test_add_write_csv_node(self):
        node_to_add = Node(self.write_csv_node)
        added_node = self.add_node(self.write_csv_node, "2")

        self.assertDictEqual(node_to_add.__dict__, added_node.__dict__)

    def test_add_string_node(self):
        node_to_add = Node(self.global_flow_var)
        added_node = self.add_node(self.global_flow_var, "1")

        self.assertDictEqual(node_to_add.__dict__, added_node.__dict__)

    def test_fail_get_node(self):
        retrieved_node = self.workflow.get_flow_var("100")

        self.assertIsNone(retrieved_node)

    def test_get_node(self):
        retrieved_node = self.workflow.get_node("1")
        read_csv_node = Node(self.read_csv_node)

        self.assertDictEqual(retrieved_node.__dict__, read_csv_node.__dict__)

    def test_get_flow_var(self):
        retrieved_node = self.workflow.get_flow_var("1")
        global_flow_var = Node(self.global_flow_var)

        self.assertDictEqual(retrieved_node.__dict__, global_flow_var.__dict__)

    def test_add_xedge_1_to_2(self):
        node_1 = self.workflow.get_node("1")
        node_2 = self.workflow.get_node("2")
        self.add_edge(node_1, node_2)
        return

    def test_add_xedge_duplicated(self):
        node_1 = self.workflow.get_node("1")
        node_2 = self.workflow.get_node("2")

        with self.assertRaises(WorkflowException):
            self.workflow.add_edge(node_1, node_2)

    def test_execute_node(self):
        node_to_execute = self.workflow.get_node("1")

        response = self.workflow.execute("1")
        node_to_execute.data = 'Untitled-1'

        self.assertDictEqual(node_to_execute.__dict__, response.__dict__)

    def test_fail_execute_node(self):
        with self.assertRaises(WorkflowException):
            self.workflow.execute("100")

    def test_get_flow_variables(self):
        flow_var_options = self.workflow.get_all_flow_var_options("1")

        self.assertEqual(len(flow_var_options), 1)

    def test_get_node_successors(self):
        successors = self.workflow.get_node_successors("1")

        self.assertEqual(successors, ["2"])

    def test_fail_get_node_successors(self):
        with self.assertRaises(WorkflowException):
            successors = self.workflow.get_node_successors("100")

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

    def test_remove_node(self):
        node_to_remove = self.workflow.get_node("1")
        removed_node = self.workflow.remove_node(node_to_remove)

        self.assertDictEqual(node_to_remove.__dict__, removed_node.__dict__)

    def test_remove_node_error(self):
        node_to_remove = self.workflow.get_node("1")
        with self.assertRaises(WorkflowException):
            self.workflow.remove_node(node_to_remove)
