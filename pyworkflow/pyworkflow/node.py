import pandas as pd


class Node:
    """Node object

    """
    def __init__(self, node_info, options=None):
        self.name = node_info.get('name')
        self.node_id = node_info.get('node_id')
        self.node_type = node_info.get('node_type')
        self.node_key = node_info.get('node_key')
        self.data = None

        # Execution options are passed up from children
        self.options = options or dict()

        # User-override takes precedence
        if node_info.get("options"):
            self.options.update(node_info["options"])

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
    color = 'black'

    DEFAULT_OPTIONS = {
        # 'file': None,
    }

    def __init__(self, node_info, options=dict()):
        super().__init__(node_info, {**IONode.DEFAULT_OPTIONS, **options})

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
    color = 'purple'

    DEFAULT_OPTIONS = {
        'filepath_or_buffer': None,
        'sep': ',',
        'header': 'infer',
    }
    OPTION_TYPES = {
        'filepath_or_buffer': {
            "type": "file",
            "name": "File",
            "desc": "File to read"
            },
        'sep': {"type": "string",
                "name": "Delimiter",
                "desc": "column delimiter, default ','"
            },
        'header': {"type": "string",
                   "name": "Column Name Row",
                   "desc": "Row number with column names (0-indexed) or 'infer'"
            }
    }

    def __init__(self, node_info, options=dict()):
        super().__init__(node_info, {**self.DEFAULT_OPTIONS, **options})

    def execute(self):
        try:
            # TODO: FileStorage implemented in Django to store in /tmp
            #       Better filename/path handling should be implemented.

            df = pd.read_csv(**self.options)
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
    DEFAULT_OPTIONS = {
        'path_or_buf': None,
        'sep': ',',
        'index': True,
    }

    def __init__(self, node_info, options=dict()):
        super().__init__(node_info, {**self.DEFAULT_OPTIONS, **options})

    def execute(self):
        try:
            # TODO: DataFrame would be stored from prior Node execution
            # Create empty DataFrame
            self.data = pd.DataFrame().to_json()

            # Read in empty DataFrame to export
            df = pd.read_json(self.data)
            df.to_csv(**self.options)
        except Exception as e:
            raise NodeException('write csv', str(e))


class ManipulationNode(Node):
    """ManipulationNodes deal with data manipulation.

    Possible types:
        Pivot
        Filter
        Multi-in
    """
    color = 'yellow'

    DEFAULT_OPTIONS = {}

    def __init__(self, node_info, options=dict()):
        super().__init__(node_info, {**ManipulationNode.DEFAULT_OPTIONS, **options})

    def execute(self):
        pass

    def validate(self):
        return True


class PivotNode(ManipulationNode):
    name = "Pivoting"
    num_in = 1
    num_out = 3

    DEFAULT_OPTIONS = {}

    def __init__(self, node_info, options=dict()):
        super().__init__(node_info, {**self.DEFAULT_OPTIONS, **options})


class JoinNode(ManipulationNode):
    name = "Joiner"
    num_in = 2
    num_out = 1

    DEFAULT_OPTIONS = {}

    def __init__(self, node_info, options=dict()):
        super().__init__(node_info, {**self.DEFAULT_OPTIONS, **options})


class NodeException(Exception):
    def __init__(self, action: str, reason: str):
        self.action = action
        self.reason = reason

    def __str__(self):
        return self.action + ': ' + self.reason
