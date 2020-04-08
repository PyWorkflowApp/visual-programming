import pandas as pd
from django.core.files.storage import FileSystemStorage
from django.conf import settings

fs = FileSystemStorage(location=settings.MEDIA_ROOT)


class Node:
    """Node object

    """
    def __init__(self, node_info, options=None):
        self.name = node_info.get('name')
        self.node_id = node_info.get('node_id')
        self.node_type = node_info.get('node_type')
        self.node_key = node_info.get('node_key')
        self.data = node_info.get('data')

        self.is_global = True if node_info.get('is_global') else False

        # Execution options are passed up from children
        self.options = options or dict()

        # User-override takes precedence
        if node_info.get("options"):
            self.options.update(node_info["options"])

    def execute(self, predecessor_data, flow_vars):
        pass

    def validate(self):
        return True

    def __str__(self):
        return "Test"


class FlowNode(Node):
    """FlowNode object
    """
    display_name = "Flow Control"
    DEFAULT_OPTIONS = {

    }

    def __init__(self, node_info, options=dict()):
        super().__init__(node_info, {**FlowNode.DEFAULT_OPTIONS, **options})


class StringNode(FlowNode):
    """StringNode object

    Allows for Strings to replace 'string' fields in Nodes
    """
    name = "String Input"
    num_in = 1
    num_out = 1
    color = 'purple'

    DEFAULT_OPTIONS = {
        'default_value': None,
        'var_name': 'my_var',
    }

    OPTION_TYPES = {
        'default_value': {
            "type": "string",
            "name": "Default Value",
            "desc": "Value this Node will pass as a flow variable"
        },
        'var_name': {
            "type": "string",
            "name": "Variable Name",
            "desc": "Name of the variable to use in another Node"
        }
    }

    def __init__(self, node_info):
        super().__init__(node_info)


class IONode(Node):
    """IONodes deal with file-handling in/out of the Workflow.

    Possible types:
        Read CSV
        Write CSV
    """
    color = 'black'
    display_name = "I/O"

    DEFAULT_OPTIONS = {
        # 'file': None,
    }

    def __init__(self, node_info, options=dict()):
        super().__init__(node_info, {**IONode.DEFAULT_OPTIONS, **options})

    def execute(self, predecessor_data, flow_vars):
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
            "desc": "CSV File"
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

    def execute(self, predecessor_data, flow_vars):
        try:
            # TODO: FileStorage implemented in Django to store in /tmp
            #       Better filename/path handling should be implemented.
            NodeUtils.replace_flow_vars(self.options, flow_vars)
            opts = self.options
            df = pd.read_csv(opts["filepath_or_buffer"], sep=opts["sep"],
                             header=opts["header"])
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

    def execute(self, predecessor_data, flow_vars):
        try:
            # Write CSV needs exactly 1 input DataFrame
            NodeUtils.validate_predecessor_data(len(predecessor_data), self.num_in, self.node_key)

            # Convert JSON data to DataFrame
            df = pd.DataFrame.from_dict(predecessor_data[0])

            # Write to CSV and save
            opts = self.options
            # TODO: Remove use of Django file storage from pyworkflow nodes
            fname = fs.path(opts["path_or_buf"])
            df.to_csv(fname, sep=opts["sep"], index=opts["index"])
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
    display_name = "Manipulation"

    DEFAULT_OPTIONS = {}

    def __init__(self, node_info, options=dict()):
        super().__init__(node_info, {**ManipulationNode.DEFAULT_OPTIONS, **options})

    def execute(self, predecessor_data, flow_vars):
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

    def execute(self, predecessor_data, flow_vars):
        try:
            NodeUtils.validate_predecessor_data(len(predecessor_data), self.num_in, self.node_key)
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

    def execute(self, predecessor_data, flow_vars):
        # Join cannot accept more than 2 input DataFrames
        # TODO: Add more error-checking if 1, or no, DataFrames passed through
        try:
            NodeUtils.validate_predecessor_data(len(predecessor_data), self.num_in, self.node_key)
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


class NodeUtils:

    @staticmethod
    def validate_predecessor_data(predecessor_data_len, num_in, node_key):
        validation_failed = False
        exception_txt = ""
        if node_key == 'WriteCsvNode' and predecessor_data_len != num_in:
                validation_failed = True
                exception_txt = '%s needs %d inputs. %d were provided'
        elif (node_key != 'WriteCsvNode' and predecessor_data_len > num_in):
                validation_failed = True
                exception_txt = '%s can take up to %d inputs. %d were provided'

        if validation_failed:
            raise NodeException(
                'execute',
                exception_txt % (node_key, num_in, predecessor_data_len)
            )

    @staticmethod
    def replace_flow_vars(node_options, flow_vars):
        for var in flow_vars:
            node_options[var['var_name']] = var['default_value']

        return
