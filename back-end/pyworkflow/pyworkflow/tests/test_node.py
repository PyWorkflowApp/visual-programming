import unittest
from pyworkflow import *
from pyworkflow.nodes import *
from pyworkflow.tests.sample_test_data import GOOD_NODES, BAD_NODES, DATA_FILES


class NodeTestCase(unittest.TestCase):
    def test_add_join_csv_node(self):
        node_to_add = node_factory(GOOD_NODES["join_node"])
        self.assertIsInstance(node_to_add, JoinNode)

    def test_add_filter_csv_node(self):
        node_to_add = node_factory(GOOD_NODES["filter_node"])
        self.assertIsInstance(node_to_add, FilterNode)

    def test_add_pivot_csv_node(self):
        node_to_add = node_factory(GOOD_NODES["pivot_node"])
        self.assertIsInstance(node_to_add, PivotNode)

    def test_add_string_node(self):
        node_to_add = node_factory(GOOD_NODES["string_input"])
        self.assertIsInstance(node_to_add, StringNode)

    def test_fail_add_node(self):
        bad_nodes = [
            node_factory(BAD_NODES["bad_node_type"]),
            node_factory(BAD_NODES["bad_flow_node"]),
            node_factory(BAD_NODES["bad_io_node"]),
            node_factory(BAD_NODES["bad_manipulation_node"])
        ]

        for bad_node in bad_nodes:
            self.assertIsNone(bad_node)

    def test_node_execute_not_implemented(self):
        test_node = Node(dict())
        test_io_node = IONode(dict())
        test_manipulation_node = ManipulationNode(dict())

        nodes = [test_node, test_io_node, test_manipulation_node]

        for node_to_execute in nodes:
            with self.assertRaises(NotImplementedError):
                node_to_execute.execute(None, None)

    def test_node_execute_exception(self):
        read_csv_node = node_factory(GOOD_NODES["read_csv_node"])
        write_csv_node = node_factory(GOOD_NODES["write_csv_node"])
        join_node = node_factory(GOOD_NODES["join_node"])

        nodes = [read_csv_node, write_csv_node, join_node]
        for node_to_execute in nodes:
            with self.assertRaises(NodeException):
                node_to_execute.execute(dict(), dict())
