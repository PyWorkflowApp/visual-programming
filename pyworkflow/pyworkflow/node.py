import pandas as pd

# from .workflow import Workflow


class Node:
    """Node object

    """
    def __init__(self, node_info, options=None):
        self.name = node_info.get('name')
        self.node_id = node_info.get('node_id')
        self.node_type = node_info.get('node_type')
        self.node_key = node_info.get('node_key')
        self.data = node_info.get('data')

        # Execution options are passed up from children
        self.options = options or dict()

        # User-override takes precedence
        if node_info.get("options"):
            self.options.update(node_info["options"])

    def execute(self, predecessor_data):
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

    def execute(self, predecessor_data):
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
        'sep': {
            "type": "string",
            "name": "Delimiter",
            "desc": "column delimiter, default ','"
        },
        'header': {
            "type": "string",
            "name": "Column Name Row",
            "desc": "Row number with column names (0-indexed) or 'infer'"
        }
    }

    def __init__(self, node_info, options=dict()):
        super().__init__(node_info, {**self.DEFAULT_OPTIONS, **options})

    def execute(self, predecessor_data):
        try:
            # TODO: FileStorage implemented in Django to store in /tmp
            #       Better filename/path handling should be implemented.

            df = pd.read_csv(**self.options)
            return df.to_json()
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

    def execute(self, predecessor_data):
        try:
            # Write CSV needs exactly 1 input DataFrame
            if len(predecessor_data) != self.num_in:
                raise NodeException(
                    'execute',
                    'WriteCsv needs %d inputs. %d were provided' % (self.num_in, len(predecessor_data))
                )

            # Convert JSON data to DataFrame
            df = pd.DataFrame.from_dict(predecessor_data[0])

            # Write to CSV and save
            df.to_csv(**self.options)
            return df.to_json()
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

    def execute(self, predecessor_data):
        pass

    def validate(self):
        return True


class PivotNode(ManipulationNode):
    name = "Pivoting"
    num_in = 1
    num_out = 3

    DEFAULT_OPTIONS = {
        'index': None,
        'values': None,
        'columns': None,
        'aggfunc': 'mean',
        'fill_value': None,
        'margins': False,
        'dropna': True,
        'margins_name': 'All',
        'observed': False

    }

    def __init__(self, node_info, options=dict()):
        super().__init__(node_info, {**self.DEFAULT_OPTIONS, **options})

    def execute(self, predecessor_data):
        try:
            if len(predecessor_data) > self.num_in:
                raise NodeException(
                    'execute',
                    'PivotNode can take up to %d inputs. %d were provided' % (self.num_in, len(predecessor_data))
                )
            input_df = pd.DataFrame.from_dict(predecessor_data[0])
            output_df = pd.DataFrame.pivot_table(input_df, **self.options)
            return output_df.to_json()
        except Exception as e:
            raise NodeException('pivot', str(e))


class JoinNode(ManipulationNode):
    name = "Joiner"
    num_in = 2
    num_out = 1

    DEFAULT_OPTIONS = {}

    def __init__(self, node_info, options=dict()):
        super().__init__(node_info, {**self.DEFAULT_OPTIONS, **options})

    def execute(self, predecessor_data):
        # Join cannot accept more than 2 input DataFrames
        # TODO: Add more error-checking if 1, or no, DataFrames passed through
        try:
            if len(predecessor_data) > self.num_in:
                raise NodeException(
                    'execute',
                    'JoinNode can take up to %d inputs. %d were provided' % (self.num_in, len(predecessor_data))
                )

            first_df = pd.DataFrame.from_dict(predecessor_data[0])
            second_df = pd.DataFrame.from_dict(predecessor_data[1])

            combined_df = first_df.join(second_df, lsuffix='_caller', rsuffix='_other')

            return combined_df.to_json()
        except Exception as e:
            raise NodeException('join', str(e))


class NodeException(Exception):
    def __init__(self, action: str, reason: str):
        self.action = action
        self.reason = reason

    def __str__(self):
        return self.action + ': ' + self.reason
