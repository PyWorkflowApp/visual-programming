import unittest
from pyworkflow import Workflow, WorkflowException, Node, NodeException, node_factory
from pyworkflow.nodes import *
import networkx as nx

from pyworkflow.tests.sample_test_data import GOOD_NODES, BAD_NODES, DATA_FILES


class PyWorkflowTestCase(unittest.TestCase):
    def setUp(self):

        with open('/tmp/sample1.csv', 'w') as f:
            f.write(DATA_FILES["sample1"])

        with open('/tmp/sample2.csv', 'w') as f:
            f.write(DATA_FILES["sample2"])

        self.pyworkflow = Workflow("My Workflow", root_dir="/tmp")

        self.read_csv_node_1 = Node(GOOD_NODES["read_csv_node"])

        self.read_csv_node_2 = Node({
            "name": "Read CSV",
            "node_id": "2",
            "node_type": "io",
            "node_key": "ReadCsvNode",
            "is_global": False,
            "options": {
                "file": "/tmp/sample2.csv",
                "sep": ";",
            },
            "option_replace": {
                "sep": {
                    "node_id": "1",
                    "is_global": True,
                }
            }
        })

        self.join_node = Node(GOOD_NODES["join_node"])

        self.write_csv_node = Node({
            "name": "Write CSV",
            "node_id": "4",
            "node_type": "io",
            "node_key": "WriteCsvNode",
            "is_global": False,
            "options": {
                "file": "/tmp/sample_out.csv"
            }
        })

        self.string_flow_node = Node(GOOD_NODES["string_input"])
        self.string_global_flow_node = Node(GOOD_NODES["global_flow_var"])

        self.nodes = [
            self.read_csv_node_1,
            self.read_csv_node_2,
            self.join_node,
            self.write_csv_node,
            self.string_flow_node,
            self.string_global_flow_node,
        ]
        self.edges = [("1", "3"), ("2", "3"), ("3", "4"), ("7", "3")]

    def create_workflow(self):
        # When created in setUp(), duplicate Node/Edge errors would arise
        for node in self.nodes:
            self.pyworkflow.update_or_add_node(node)

        for edge in self.edges:
            source_node = self.pyworkflow.get_node(edge[0])
            target_node = self.pyworkflow.get_node(edge[1])
            self.pyworkflow.add_edge(source_node, target_node)

    def test_get_local_flow_nodes(self):
        node_with_flow = self.pyworkflow.get_node("3")
        flow_nodes = self.pyworkflow.load_flow_nodes(node_with_flow.option_replace)
        self.assertEqual(len(flow_nodes), 1)

    def test_get_global_flow_nodes(self):
        node_with_flow = self.pyworkflow.get_node("2")
        flow_nodes = self.pyworkflow.load_flow_nodes(node_with_flow.option_replace)
        self.assertEqual(len(flow_nodes), 1)

    def test_get_global_flow_node_exception(self):
        node_with_flow = self.pyworkflow.get_node("1")
        flow_nodes = self.pyworkflow.load_flow_nodes(node_with_flow.option_replace)
        self.assertEqual(len(flow_nodes), 0)

    def test_get_execution_order(self):
        self.create_workflow()
        order = self.pyworkflow.execution_order()
        self.assertEqual(order, ["7", "2", "1", "3", "4"])

    def test_xexecute_workflow(self):
        order = self.pyworkflow.execution_order()

        for node in order:
            executed_node = self.pyworkflow.execute(node)
            self.pyworkflow.update_or_add_node(executed_node)

    # def test_execute_workflow_load_data(self):
    #     print(self.pyworkflow.graph.nodes)
    #     data = self.pyworkflow.load_input_data("3")

    def test_fail_execute_node(self):
        with self.assertRaises(WorkflowException):
            self.pyworkflow.execute("100")

    def test_upload_file(self):
        with open('/tmp/sample1.csv', 'rb') as f:
            to_open = '/tmp/sample_upload.csv'
            saved_filed = self.pyworkflow.upload_file(f, to_open)

            self.assertEqual(to_open, saved_filed)
