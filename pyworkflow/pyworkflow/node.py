import pandas as pd


class Node:
    """Node object

    """
    def __init__(self, node_info):
        self.node_id = node_info['node_id']
        self.num_in = node_info['num_in']
        self.num_out = node_info['num_out']
        self.node_type = node_info['node_type']
        self.node_key = node_info['node_key']
        self.data = None

    def execute(self):
        pass

    def validate(self):
        return True

    def __str__(self):
        return "Test"



    def execute(self):
        pass

    def validate(self):
        return True


class NodeException(Exception):
    def __init__(self, action: str, reason: str):
        self.action = action
        self.reason = reason

    def __str__(self):
        return self.action + ': ' + self.reason
