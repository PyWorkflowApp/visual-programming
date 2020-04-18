import unittest
from pyworkflow import Workflow, WorkflowException, Node, NodeException
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

        self.join_node = {
            "name": "Joiner",
            "node_id": "3",
            "node_type": "ManipulationNode",
            "node_key": "JoinNode",
            "is_global": False,
            "options": {
                "on": "key"
            }
        }

    def add_node(self, node_info, node_id):
        node_info["node_id"] = node_id
        node_to_add = Node(node_info)
        return self.workflow.update_or_add_node(node_to_add)

    def test_workflow_name(self):
        self.assertEqual(self.workflow.name, "Untitled")

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

    def test_add_xedge(self):
        # self.add_node(self.read_csv_node)
        # self.add_node(self.write_csv_node)

        node_1 = self.workflow.get_node("1")
        node_2 = self.workflow.get_node("2")
        response = self.workflow.add_edge(node_1, node_2)
        self.assertEqual(response, ("1", "2"))
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

    def test_get_node_successors(self):
        successors = self.workflow.get_node_successors("1")

        self.assertEqual(successors, ["2"])

    def test_get_node_predecessors(self):
        predecessors = self.workflow.get_node_predecessors("2")

        self.assertEqual(predecessors, ["1"])

    def test_get_execution_order(self):
        order = self.workflow.execution_order()
        self.assertEqual(order, ["1", "2"])

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

if __name__ == '__main__':
    unittest.main()
