""" node/models.py

"""


class NodeInterface:
    def __init__(self, node_id, node_type, num_ports_in, num_ports_out):
        id = node_id
        type = node_type
        num_ports_in = num_ports_in
        num_ports_out = num_ports_out

    def execute(self):
        pass

    def validate(self):
        pass

    def __str__(self):
        return "Test"


class Node(NodeInterface):
    def __init__(self, node_id, node_type, num_ports_in, num_ports_out):
        super().__init__(node_id, node_type, num_ports_in, num_ports_out)

    def execute(self):
        pass

    def validate(self):
        return True

    @property
    def id(self):
        return self._id
