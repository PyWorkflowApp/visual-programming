import unittest
from pyworkflow import *
from pyworkflow.nodes import *
import networkx as nx


class NodeTestCase(unittest.TestCase):
    def setUp(self):
        self.workflow = Workflow("Untitled", root_dir="/tmp")

        self.read_csv_node = {
            "name": "Read CSV",
            "node_id": "1",
            "node_type": "io",
            "node_key": "ReadCsvNode",
            "is_global": False,
            "options": {
                "file": "/tmp/sample.csv"
            }
        }

        self.write_csv_node = {
            "name": "Write CSV",
            "node_id": "2",
            "node_type": "io",
            "node_key": "WriteCsvNode",
            "is_global": False,
            "options": {
                "file": "/tmp/sample_out.csv"
            }
        }

        self.join_node = {
            "name": "Joiner",
            "node_id": "3",
            "node_type": "manipulation",
            "node_key": "JoinNode",
            "is_global": False,
            "options": {
                "on": "key"
            }
        }

        self.filter_node = {
            "name": "Filter",
            "node_id": "4",
            "node_type": "manipulation",
            "node_key": "FilterNode",
            "is_global": False,
            "options": {
                "on": "key"
            }
        }

        self.pivot_node = {
            "name": "Pivoting",
            "node_id": "5",
            "node_type": "manipulation",
            "node_key": "PivotNode",
            "is_global": False,
            "options": {
                "on": "key"
            }
        }

        self.string_input = {
            "name": "String Input",
            "node_id": "6",
            "node_type": "flow_control",
            "node_key": "StringNode",
            "is_global": False,
            "options": {
                "default_value": "My value",
                "var_name": "my_var"
            }
        }

        self.global_flow_var = {
            "name": "String Input",
            "node_id": "1",
            "node_type": "flow_control",
            "node_key": "StringNode",
            "is_global": True,
            "options": {
                "default_value": "My value",
                "var_name": "my_var"
            }
        }

        self.bad_flow_node = {
            "name": "Foobar",
            "node_id": "1",
            "node_type": "flow_control",
            "node_key": "foobar",
            "is_global": False,
        }

        self.bad_io_node = {
            "name": "Foobar",
            "node_id": "1",
            "node_type": "io",
            "node_key": "foobar",
            "is_global": False,
        }

        self.bad_manipulation_node = {
            "name": "Foobar",
            "node_id": "1",
            "node_type": "manipulation",
            "node_key": "foobar",
            "is_global": False,
        }

        self.bad_node_type = {
            "name": "Foobar",
            "node_id": "1",
            "node_type": "foobar",
            "node_key": "foobar",
            "is_global": False,
        }

    def add_node(self, node_info, node_id):
        node_info["node_id"] = node_id
        node_to_add = Node(node_info)
        return self.workflow.update_or_add_node(node_to_add)

    def test_add_join_csv_node(self):
        node_to_add = node_factory(self.join_node)
        self.assertIsInstance(node_to_add, JoinNode)

    def test_add_filter_csv_node(self):
        node_to_add = node_factory(self.filter_node)
        self.assertIsInstance(node_to_add, FilterNode)

    def test_add_pivot_csv_node(self):
        node_to_add = node_factory(self.pivot_node)
        self.assertIsInstance(node_to_add, PivotNode)

    def test_add_string_node(self):
        node_to_add = node_factory(self.string_input)
        self.assertIsInstance(node_to_add, StringNode)

    def test_fail_add_node(self):
        node_to_add = node_factory(self.bad_node_type)
        self.assertIsNone(node_to_add)

    def test_fail_add_flow_node(self):
        node_to_add = node_factory(self.bad_flow_node)
        self.assertIsNone(node_to_add)

    def test_fail_add_io_node(self):
        node_to_add = node_factory(self.bad_io_node)
        self.assertIsNone(node_to_add)

    def test_fail_add_manipulation_node(self):
        node_to_add = node_factory(self.bad_manipulation_node)
        self.assertIsNone(node_to_add)

    def test_node_execute_not_implemented(self):
        test_node = Node(dict())
        test_io_node = IONode(dict())
        test_manipulation_node = ManipulationNode(dict())

        nodes = [test_node, test_io_node, test_manipulation_node]

        for node_to_execute in nodes:
            with self.assertRaises(NotImplementedError):
                node_to_execute.execute(None, None)

    def test_add_global_flow_var(self):
        node_to_add = Node(self.global_flow_var)
        added_node = self.add_node(self.global_flow_var, "1")

        self.assertDictEqual(node_to_add.__dict__, added_node.__dict__)
