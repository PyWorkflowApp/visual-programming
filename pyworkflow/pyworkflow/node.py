class NodeInterface:
    def __init__(self, node_id, node_type, num_ports_in, num_ports_out):
        self.node_id = node_id
        self.node_type = node_type
        self.num_ports_in = num_ports_in
        self.num_ports_out = num_ports_out

    def execute(self):
        pass

    def validate(self):
        return True

    def __str__(self):
        return "Test"


class Node(NodeInterface):
    def __init__(self, node_id, node_type, num_ports_in, num_ports_out):
        super().__init__(node_id, node_type, num_ports_in, num_ports_out)

    def execute(self):
        pass

    def validate(self):
        return True
