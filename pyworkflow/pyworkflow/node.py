import pandas as pd


class Node:
    """Node object

    """
    def __init__(self, node_info):
        self.name = node_info.get('name')
        self.node_id = node_info.get('node_id')
        self.node_type = node_info.get('node_type')
        self.node_key = node_info.get('node_key')
        self.data = None

    def execute(self):
        pass

    def validate(self):
        return True

    def __str__(self):
        return "Test"


class IONode(Node):
    """IONodes deal with file-handling in/out of the Workflow.

    Possible types:
        Read CSV
        Write CSV
    """
    def __init__(self, node_info):
        super().__init__(node_info)
        self.file = node_info.get('file')

    def execute(self):
        pass

    def validate(self):
        return True


class ReadCsvNode(IONode):
    """ReadCsvNode

    Reads a CSV file into a pandas DataFrame.

    Raises:
         NodeException: any error reading CSV file, converting
            to DataFrame.
    """
    name = "Read CSV"
    num_in = 0
    num_out = 1
    color = 'black'

    def __init__(self, node_info):
        super().__init__(node_info)

    def execute(self):
        try:
            # TODO: FileStorage implemented in Django to store in /tmp
            # Right now, /tmp/ is hardcoded, but should be changed as we
            # further consider file-handling/uploading
            with open('/tmp/' + self.file) as file_like:
                df = pd.read_csv(file_like)
                self.data = df.to_json()
        except Exception as e:
            raise NodeException('read csv', str(e))

    def __str__(self):
        return "ReadCsvNode"


class WriteCsvNode(IONode):
    """WriteCsvNode

    Writes the current DataFrame to a CSV file.

    Raises:
        NodeException: any error writing CSV file, converting
            from DataFrame.
    """
    name = "Write CSV"
    num_in = 1
    num_out = 0
    color = 'green'

    def __init__(self, node_info):
        super().__init__(node_info)

    def execute(self):
        try:
            self.data.to_csv('/tmp/' + self.file)
        except Exception as e:
            raise NodeException('write csv', str(e))


class ManipulationNode(Node):
    """ManipulationNodes deal with data manipulation.

    Possible types:
        Pivot
        Filter
        Multi-in
    """
    num_in = 1
    num_out = 1
    color = 'blue'

    def __init__(self, node_info):
        super().__init__(node_info)
        # self.num_in = 1
        # self.num_out = 1

    def execute(self):
        print("Executing ManipulationNode")
        pass

    def validate(self):
        return True


class NodeException(Exception):
    def __init__(self, action: str, reason: str):
        self.action = action
        self.reason = reason

    def __str__(self):
        return self.action + ': ' + self.reason
