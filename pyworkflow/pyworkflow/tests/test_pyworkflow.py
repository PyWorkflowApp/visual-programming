import unittest
from pyworkflow import Workflow, WorkflowException, Node, NodeException, node_factory
from pyworkflow.nodes import *
import networkx as nx


class PyWorkflowTestCase(unittest.TestCase):
    def setUp(self):
        self.sample1 = (',key,A\n'
                        '0,K0,A0\n'
                        '1,K1,A1\n'
                        '2,K2,A2\n'
                        '3,K3,A3\n'
                        '4,K4,A4\n'
                        '5,K5,A5\n')

        self.sample2 = (',key,B\n'
                        '0,K0,B0\n'
                        '1,K1,B1\n'
                        '2,K2,B2\n')

        with open('/tmp/sample1.csv', 'w') as f:
            f.write(self.sample1)

        with open('/tmp/sample2.csv', 'w') as f:
            f.write(self.sample2)

        self.pyworkflow = Workflow("My Workflow", root_dir="/tmp")

        self.read_csv_node_1 = Node({
            "name": "Read CSV",
            "node_id": "1",
            "node_type": "io",
            "node_key": "ReadCsvNode",
            "is_global": False,
            "options": {
                "file": "/tmp/sample1.csv"
            }
        })

        self.read_csv_node_2 = Node({
            "name": "Read CSV",
            "node_id": "2",
            "node_type": "io",
            "node_key": "ReadCsvNode",
            "is_global": False,
            "options": {
                "file": "/tmp/sample2.csv"
            }
        })

        self.join_node = Node({
            "name": "Joiner",
            "node_id": "3",
            "node_type": "manipulation",
            "node_key": "JoinNode",
            "is_global": False,
            "options": {
                "on": "key"
            }
        })

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

        self.nodes = [self.read_csv_node_1, self.read_csv_node_2, self.join_node, self.write_csv_node]
        self.edges = [("1", "3"), ("2", "3"), ("3", "4")]

    def create_workflow(self):
        # When created in setUp(), duplicate Node/Edge errors would arise
        for node in self.nodes:
            self.pyworkflow.update_or_add_node(node)

        for edge in self.edges:
            source_node = self.pyworkflow.get_node(edge[0])
            target_node = self.pyworkflow.get_node(edge[1])
            self.pyworkflow.add_edge(source_node, target_node)

    def test_get_execution_order(self):
        self.create_workflow()
        order = self.pyworkflow.execution_order()
        self.assertEqual(order, ["2", "1", "3", "4"])

    def test_execute_workflow(self):
        order = self.pyworkflow.execution_order()

        for node in order:
            executed_node = self.pyworkflow.execute(node)
            self.pyworkflow.update_or_add_node(executed_node)

    def test_fail_execute_node(self):
        with self.assertRaises(WorkflowException):
            self.pyworkflow.execute("100")

    def test_upload_file(self):
        with open('/tmp/sample1.csv', 'rb') as f:
            to_open = '/tmp/sample_upload.csv'
            saved_filed = self.pyworkflow.upload_file(f, to_open)

            self.assertEqual(to_open, saved_filed)
